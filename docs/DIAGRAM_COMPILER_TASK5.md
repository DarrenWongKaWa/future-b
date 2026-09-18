# Task 5: Fortran backend for NativeKernelIR

Experimental source continuation of Task 4 on
`diagram-compiler/task5-fortran-backend`. This is a standalone
compiled Fortran kernel. It is not FEP-DMC integration, a public P1
replacement, or a performance result.

## 1. Task-4 baseline

HEAD `0110f22abc9831b20f69d7a5228af8d4773fa3d5`. Combined compiler
tests at start: 383 passed. Exact 224/224 max error
`2.7755575615628914e-17`. NativeKernelIR modules remain byte-identical
([baseline.json](../research/diagram_compiler/task5/baseline.json)).

## 2. Backend research question

Can a validated NativeKernelIR be translated into compilable Fortran
such that the compiled kernel matches `interpret_native_kernel` on
declared semantic outputs?

## 3. Backend architecture comparison

| Strategy | Verdict |
|---|---|
| A. One monolithic generated subroutine | Duplicates primitive bodies; harder to mutation-test primitives |
| **B. Generated kernel + versioned runtime (chosen)** | Primitive names already versioned as `native_kernel_v1` |
| C. Fully generated primitive bodies per kernel | Same math copied into every order/model kernel |

Evidence favored B: primitive differential tests compile one runtime;
kernels only emit SSA/CFG.

## 4. Chosen runtime/codegen split

- `fortran_codegen.py` emits kernel-specific Fortran from NativeKernelIR only.
- `fortran/native_kernel_runtime_v1.f90` implements `native_kernel_v1`.
- Backend identity: `fortran_v1`. Runtime identity: `native_kernel_v1`.

The emitter imports `native_ir` only. It does not import DiagramIR,
CheapPolicy, target derivation, proposal derivation, R1, or P1.

## 5. Type mapping

| NativeKernelIR | Fortran |
|---|---|
| `f64` | `real(real64)` |
| `c128` | `complex(real64)` |
| `i64` | `integer(int64)` |
| `bool` | `logical` |
| `c128_m2` | `complex(real64) :: a(2,2)` |

Kinds come from `iso_fortran_env`. Layout field `L` is `integer(int64)`
on the ABI and converted with `real(L, real64)` at `load`.

## 6. ABI implementation

Two-band n=1 dummy list (Fortran-only, no `bind(C)`):

```text
subroutine evaluate_da_kernel( &
    x_k, x_q(1), x_tau(2), x_t, x_omega, x_g, x_L, x_delta, x_gap, &
    y_k, y_q(1), y_tau(2), y_t, y_omega, y_g, y_L, y_delta, y_gap, &
    log_q_reverse_minus_forward, u1, u2, &
    exact_x_valid, exact_log_weight_x, &
    accepted, reject_stage, ell_hat, ell_R_valid, ell_R, &
    exact_y_evaluated, status)
```

Cache contract A: the caller sets `exact_x_valid=.true.` only when
`exact_log_weight_x` belongs to this `x`. The kernel does not compare
Bindings. `CACHE_KEY_MISMATCH` remains reserved and unused.
Score-kind IR uses `log_wx, log_wy, log_px, log_py` instead of Bindings.

Driver I/O uses integer 0/1 for logicals. `u1` and `u2` are caller
inputs; the backend does not generate RNG.

## 7. Primitive runtime semantics

Copied from Task-4 `native_interpret.py`:

- `nk_xi`: `2 t (1-cos k)`
- `nk_electron_scalar`: `exp(-xi dtau)`
- `nk_electron_twoband`: `exp(-dtau H)` for real-symmetric
  `H=[[xi,delta],[delta,xi+gap]]` via `H=m I+K`, `K^2=r^2 I`,
  `cosh`/`sinh` (no LAPACK, no eigenvectors)
- `nk_phonon`: `exp(-omega dtau)`
- `nk_prefactor`: `(g/sqrt(L))**(2n)`
- `nk_vertex_sigmaz`: `(g/sqrt(L)) diag(1,-1)`
- `nk_matmul` / `nk_scale_m2` / `nk_add_m2` / `nk_trace`

Matrix contract: mathematical `(i,j)` is Fortran `a(i,j)` (column-major
storage). No new clipping. `log_positive_real` uses IEEE finite checks
and `imag_atol` from the IR (default `1e-12`). Uniform floor `1e-300`.

## 8. SSA emission

One explicit definition per SSA id. Unknown opcode raises
`INVALID_IR`. Temporaries are declared with explicit kinds.
`phi` is copied on predecessor `goto` edges.

## 9. CFG emission

Labeled `continue` + `goto` (and structured `if` for `br_cond`).
Stage-1 reject is labels 100 then 200; exact graph calls start at
320/330. Exact work is not hoisted above Stage 1.

## 10. Error/status lowering

Integer codes match Task 4: `OK=0`, `INVALID_EXACT_TARGET=1`,
`INVALID_CHEAP_WEIGHT=2`, `INVALID_PROPOSAL_RATIO=3`,
`INVALID_RANDOM_UNIFORM=4`, `CACHE_KEY_MISMATCH=5`, `INVALID_IR=6`.
Generated kernels assign `status` and return. They do not `error stop`.

## 11. Numerical policy

Unchanged Design B: `ell_hat=log W_hat(y)-log W_hat(x)`,
`ell_R=log pi(y)-log pi(x)+log q(y,x)-log q(x,y)`, Stage 1
`log max(u1,1e-300) < min(0, ell_hat)`, Stage 2
`log max(u2,1e-300) < min(0, ell_R-ell_hat)`. Predeclared
`atol=1e-12`, `rtol=1e-10`. Discrete fields match exactly.

## 12. Primitive differential validation

[primitive_differential.csv](../research/diagram_compiler/task5/primitive_differential.csv):
all eight primitives within tolerance vs the interpreter oracles.
Nonsymmetric complex matmul is not equal to the transpose product.

## 13. Full kernel differential validation

[kernel_differential.csv](../research/diagram_compiler/task5/kernel_differential.csv):
two-band n=1 Stage-1 reject, Stage-2 reject, accept, and asymmetric
`log q` match the interpreter. Scalar n=1..4 and two-band n=2 also
compile and match. Invalid `u`/`q`/`g=0` statuses match.

## 14. Native exact-laziness evidence

[call_counts.csv](../research/diagram_compiler/task5/call_counts.csv):
Stage-1 reject has `n_exact_graph=0` and zero
`electron_twoband`/`vertex`/`matmul`/`trace`. Stage-1 pass has
`n_exact_graph>0`.

## 15. Source determinism/provenance

Same NativeKernelIR yields the same generated `.f90` SHA256
`ff4aa2de2338cb9c6894487ac805b4bbd971549dfbdb0e1480888c5af588c32e`.
No timestamps. Binary hashes are recorded for this compiler only and
are not a cross-compiler guarantee
([source_provenance.json](../research/diagram_compiler/task5/source_provenance.json)).

## 16. Limitations

One public compiler (`gfortran` 16.1.0 Homebrew). Not portable Fortran
from one compiler. Cache identity remains a host flag. Score-kind
finite-state uses log-weights, not Bindings. No topology sampler, no
RNG, no GPU, no LLVM, no variable-order compiler. Tiny-`delta`
eigenvector formulas were rejected after Agent-3 stress; the runtime
uses the `cosh`/`sinh` form instead. This is not FEP-DMC integration.

## 17. Task-6 integration requirements

Wire a generated `evaluate_da_kernel` into a pinned public FEP-DMC
validation path and compare generated-kernel behavior to the compiler
oracle. Do not silently replace public P1. Keep u1/u2 owned by the
host RNG. Keep cache identity explicit.
