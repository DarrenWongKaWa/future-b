# Task 3: exact-preserving delayed-acceptance kernel

Experimental source-only continuation of Task 2 on
`diagram-compiler/task3-delayed-acceptance`. This is not a Future B
release, a Fortran backend, a P1 replacement, or a performance result.

## 1. Task-2 baseline

HEAD `a79bdf4213a768db74401e6525b4c6e6eb62d768`. Combined compiler
tests at Task-3 start: 333 passed (281 Task-1 + 52 Task-2). Exact
224/224 still match R1/`index_oracle` at max error
`2.7755575615628914e-17`. Exact modules and Task-2 `cheap_policy.py` /
`cheap_evaluator.py` / `CHEAP_POLICY.json` remain byte-identical
([baseline.json](../research/diagram_compiler/task3/baseline.json)).

## 2. Research question

Can the compiler pair the Task-1 exact evaluator and the Task-2 cheap
evaluator, plus a minimal reversible proposal contract, into an
executable delayed-acceptance kernel whose acceptance ratio preserves
a declared exact target?

## 3. Exact target semantics

```text
pi(x) = F(x)
```

only on the restricted set where Task-1 `F` is finite, real
(`|Im F| <= 1e-12`), and strictly positive. Policy:
`positive_real_F_v1`.

| Family | Legal as pi? |
|---|---|
| Scalar Holstein, `g != 0` | Yes (`F>0` algebraically) |
| Two-band n=1, `g != 0` | Yes (`F = (g/sqrt(L))^2 D tr(U) > 0`) |
| Two-band n>=2 | Admitted only when the sample `F>0`; otherwise fail-closed |
| `g = 0` / `F <= 0` / nonzero imag | REFUSE |

Refused transforms: `|F|`, `F^2`, complex modulus, public P1
`abs(Re M)`. Historical grouped `|F|` sampling is a different chain
and is not used.

## 4. Proposal abstraction

`ProposalSpec` only:

- `symmetric`: `log q(y,x)-log q(x,y)` must be `0`
- `provided_log_ratio`: caller supplies a finite real; reverse is negation

No topology generator, chain scheduler, or occupancy-swap IR. Reverse
of a rebinding is Binding swap.

## 5. Architecture alternatives

| Design | `ell_hat` | `ell_R` | Detailed balance |
|---|---|---|---|
| A | `log W_hat(y)-log W_hat(x)` | `log pi(y)-log pi(x)` | Only if `q` symmetric |
| **B (chosen)** | `log W_hat(y)-log W_hat(x)` | `log pi(y)-log pi(x)+log q(y,x)-log q(x,y)` | Yes, general reversible `q` |
| C | cheap + Hastings | same as B | Yes, but cheap becomes a transition score |

Design B keeps Task-2 `STATE_WEIGHT` independent of `q`. Hastings is
repaired in Stage 2. Design A is Design B with log-q identically 0.

## 6. Chosen DA architecture

Christen–Fox two-stage kernel, Design B, no clipping.

```text
alpha1 = min(1, exp(ell_hat))
alpha2 = min(1, exp(ell_R - ell_hat))
A = alpha1 * alpha2
```

Independent caller-supplied `u1`, `u2`. Log-space tests
`log max(u, 1e-300) < min(0, score)`. The tiny floor applies to RNG
only, never to `pi`, `W_hat`, or `q`.

## 7. Algebraic exactness proof

Let `r = exp(ell_hat)`, `R = exp(ell_R) = R_exact` under Design B, with
`r(y,x)=1/r` and `R(y,x)=1/R`. Then

```text
A_xy = min(1,r) min(1,R/r)
A_yx = min(1,1/r) min(1,r/R)
A_xy / A_yx = r * (R/r) = R = R_exact
```

Four-case split (`r >= 1` vs `<1`, `R/r >= 1` vs `<1`) yields the same
identity. The cheap weight need not equal `pi`.

## 8. Kernel compilation

```text
                    DiagramIR
                   /         \
             Exact DAG     Cheap DAG
                   \         /
                    \       /
                   DA Kernel
```

`compile_delayed_acceptance(ir)` snapshots the IR, reuses
`compile_exact` / `compile_cheap`, and returns an immutable kernel
whose `.spec` is JSON (`DelayedAcceptanceKernelSpec`). Closures are
not serialized. Reconstruction re-lowers from named identities.

```python
result = kernel.evaluate_transition(x, y, log_q_reverse_minus_forward, u1, u2)
```

Optional `exact_log_weight_x` plus `exact_x` Binding key skips
recomputing `exact(x)`. A mismatched key is refuse.

## 9. Lazy exact evaluation

Stage-1 reject evaluates `cheap(x)` and `cheap(y)` and does **not**
evaluate `exact(y)` or `exact(x)`. Stage-1 pass evaluates `exact(y)`
and `exact(x)` unless a correctly keyed cache supplies `exact(x)`.

Demo identity: `exact_candidate_evaluations == stage1_passes` (2 == 2).

## 10. Finite-state validation

Three-state `pi = (0.5, 0.3, 0.2)` with a different cheap weight, for
symmetric and asymmetric reversible `q`. Max detailed-balance residual
`1.39e-17`; stationarity residual `<= 2.78e-17`.
[finite_state_balance.csv](../research/diagram_compiler/task3/finite_state_balance.csv).

Mutations (drop Stage 2, drop `-ell_hat` in Stage 2, invert Hastings,
use cheap as exact) break balance.

## 11. Real diagram-family demonstration

Two-band n=1, `propagator_only_v1` cheap ≠ exact `F`, both `F>0`.

| Path | u1 | u2 | Stage 1 | exact(y) | Stage 2 | Accept |
|---|---|---|---|---|---|---|
| stage1_reject | 0.9 | 0.1 | reject | no | — | no |
| stage2_reject | 1e-16 | ~0.9976 | pass | yes | reject | no |
| accept | 1e-16 | 1e-16 | pass | yes | pass | yes |

[demo_transitions.json](../research/diagram_compiler/task3/demo_transitions.json).

## 12. P1 correspondence

| | Compiler DA | Public P1 |
|---|---|---|
| Structure | two-stage Christen–Fox | two-stage Christen–Fox |
| Cheap score | STATE_WEIGHT `log W_hat` | local `log P_kchange` TRANSITION_SCORE |
| Exact target | restricted positive `F` | native `P_accept = abs(Re M) * P_kchange` |
| Proposal | explicit log-q scalar | occupancy-swap inside `update_swap` |
| Clip | none | `±ln 10` |

Verdict: **NOT_IDENTICAL**. Common DA algebra, different objects.

## 13. Failure / numerical policy

Refuse: non-positive/complex/nonfinite `F` or `W_hat`; nonfinite log-q;
`u` outside `[0,1]`; stale exact(x) cache; unimplemented clip.
`g=0` cannot log. Do not floor exact weights.

## 14. Limitations

- Not a Markov-chain runner (no RNG owner, no burn-in, no observables).
- Scalar `propagator_only_v1` cheap equals exact, so Stage 2 is ~1 there.
- Two-band n>=2 positivity is fail-closed observation, not a theorem.
- No occupancy-swap generator; caller supplies `y` and log-q.
- No Fortran / native KernelIR.

## 15. Implications for Task 4

The spec records policy names, IR digest, Design B stage plan, and
numerical guards. Missing for native codegen: a Native Kernel IR for
the cheap/exact DAGs, a Fortran ABI for `Binding` and two uniforms,
explicit current-state exact cache layout, and a decision not to emit
Python closures. Do not generate Fortran in Task 3.
