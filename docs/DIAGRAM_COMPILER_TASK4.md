# Task 4: NativeKernelIR

Experimental source-only continuation of Task 3 on
`diagram-compiler/task4-native-kernel-ir`. This is not Fortran
emission, a native binary, a P1 replacement, or a performance result.

## 1. Task-3 baseline

HEAD `3822036e419384c1dc93d28735455511554a8844`. Combined compiler
tests at start: 369 passed. Exact 224/224 max error
`2.7755575615628914e-17`. Task-3 `da_kernel.py` and Task-1/2 exact
modules remain byte-identical
([baseline.json](../research/diagram_compiler/task4/baseline.json)).

## 2. Research question

Can the validated Exact DAG, Cheap DAG, and Design B DA kernel be
lowered into an explicit typed control/data-flow IR that a future
backend can consume without Python closures or DiagramIR?

## 3. Python semantics that had to be eliminated

Closures (`compile_evaluator` inner function), `Binding` as the IR
value, dict-keyed DAG caches, Python exceptions as the only refuse
channel, `Factor` reconstruction, `evaluate_transition` as the
executable. Those remain at the Python interpreter edge only.

## 4. IR architecture alternatives

| Strategy | Verdict |
|---|---|
| Nested AST | Laziness not a graph query |
| **Typed SSA + CFG (chosen)** | Matches existing DAGs; Stage-1 laziness is reachability |
| Fortran-shaped AST | Emission target, not a neutral IR |

## 5. Chosen NativeKernelIR

`ir_kind=NativeKernelIR`, schema 1, kind `diagram` or `score`.
Contains `source` identities, `BindingLayout`, reusable `graphs`
(cheap/exact SSA), `blocks` with SSA ops and terminators
`br` / `br_cond` / `return`.

## 6. Type system

`bool`, `i64`, `f64`, `c128`, `c128_m2` (fixed 2×2). No generic tensors.

## 7. Binding layout

Two-band n=1: `k`, `q[1]`, `tau[2]`, `t`, `omega`, `g`, `L`, `delta`,
`gap`. See [binding_layout.json](../research/diagram_compiler/task4/binding_layout.json).

## 8. Primitive set

Version `native_kernel_v1`. Cheap: `prim.electron_scalar`,
`prim.phonon`, `prim.prefactor`, `add_c128`, `mul_c128`. Exact adds
`prim.electron_twoband`, `prim.vertex_sigmaz`, `matmul`, `trace`,
`scale_m2`. Control: `log_positive_real`, `log_uniform`, `min_f64`,
`lt_f64`, `check_log_q`, `call_graph`, `phi`.

## 9. CFG

```text
entry --stage1--> exact_candidate --cache?--> use_cache / compute_exact_x
                       |                              \
                       |                               v
                  reject_stage1                    after_exact_x (exact y)
                                                       |
                                              accept / reject_stage2
```

## 10. Exact-laziness invariant

`exact_candidate_ops_on_reject_path` is empty. Stage-1 reject blocks
are `{entry, reject_stage1}`. Interpreter: Stage-1 reject has
`exact_y_evaluated=false`.

## 11. Error/status model

Integer codes: `OK=0`, `INVALID_EXACT_TARGET`, `INVALID_CHEAP_WEIGHT`,
`INVALID_PROPOSAL_RATIO`, `INVALID_RANDOM_UNIFORM`,
`CACHE_KEY_MISMATCH`, `INVALID_IR`. Not Python exception class names.

## 12. Interpreter

`interpret_native_kernel` executes graphs and CFG. It does not call
`DelayedAcceptanceKernel.evaluate_transition`. Primitive formulas are
local copies of frozen ξ, Gel, D, two-band eigh+U, σ_z vertex.

## 13. Differential validation

Four two-band n=1 transitions (Stage-1 reject, Stage-2 reject, accept,
asymmetric q) match Task-3 accept bits, `exact_y`, and scores.
Scalar n=1..4 three-path tests also match.

## 14. Finite-state validation

Design B scores executed via `native_acceptance_probability` (same
`ell_hat`/`ell_R`/`min`/`exp` as the CFG). Asymmetric 3-state:
balance residual `1.39e-17`, stationarity `2.78e-17`.

## 15. Serialization

[NATIVE_KERNEL_IR.json](../research/diagram_compiler/task4/NATIVE_KERNEL_IR.json)
round-trips: serialize → deserialize → validate → interpret.

## 16. Proposed Fortran ABI

Specification only; **not implemented**.

```text
subroutine evaluate_da_kernel( &
    x_k, x_q, x_tau, x_t, x_omega, x_g, x_L, x_delta, x_gap, &
    y_k, y_q, y_tau, y_t, y_omega, y_g, y_L, y_delta, y_gap, &
    log_q_reverse_minus_forward, u1, u2, &
    exact_x_valid, exact_log_weight_x, &
    accepted, reject_stage, ell_hat, ell_R_valid, ell_R, &
    exact_y_evaluated, status)
```

`intent(in)` physics arrays and uniforms; `intent(out)` decision and
status. `q(n)`, `tau(2n)` with n frozen in the kernel. Host sets
`exact_x_valid` only when the cached log-weight belongs to x.

## 17. Limitations

Interpreter still uses Python `Binding` at the edge to fill loads.
`validate_binding` torus checks are not SSA ops (host/ABI duty).
Cache identity is a host flag, not a Binding equality instruction.
Primitive formulas live in the interpreter until a Fortran backend
maps `prim.*` names. Score-kind IR is used for abstract finite-state
weights (not diagram Bindings).

## 18. Task-5 requirements

Map NativeKernelIR types to Fortran declarations; map arithmetic and
`prim.*` to subroutines; emit blocks/branches; emit the ABI above.
The backend should not need DiagramIR, CheapPolicy, or DA algebra
beyond what is already explicit in the IR.
