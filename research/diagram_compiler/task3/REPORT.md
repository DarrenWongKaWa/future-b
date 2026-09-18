# Task 3 — consolidated research report

Result: **bounded delayed-acceptance kernel established** from Task-1
exact and Task-2 cheap evaluators, Design B, target
`positive_real_F_v1`. Not native codegen, not public P1, not a
speedup.

Process: tests were written before modules existed (collection red),
then implemented together. Not nine separate git milestones.

## 1. Task-2 baseline preservation

Worktree from `a79bdf4`. Combined tests at start: 333 passed. Exact
224/224 recheck required after delivery. Exact and Task-2 cheap
modules unchanged (see `baseline.json`). Original dirty Task-1
checkout not edited.

## 2. Exact target

`pi(x)=F(x)` iff `F` is finite, real, and `F>0`. Not `|F|`. Two-band
n=1 is positive for `g!=0`. `g=0` fail-closed.

## 3. Proposal

`ProposalSpec.symmetric` or `provided_log_ratio`. Reverse = negate
the log ratio. No topology IR.

## 4. Design

Chosen: **B**. A is B with log-q = 0. C would fold q into the cheap
score and is not used.

## 5. Spec / API

`DelayedAcceptanceKernelSpec` JSON. Executable:
`kernel.evaluate_transition(x, y, log_q, u1, u2)`.

## 6. Proof

Christen–Fox: `A_xy/A_yx = R` when `ell_hat` is reciprocal and
`ell_R = log R_exact`. See docs §7.

## 7. Pipeline

DiagramIR → exact DAG + cheap DAG → DA kernel.

## 8. Lazy exact

Stage-1 reject does not call `exact(y)`. Demo:
`exact_candidate_evaluations == stage1_passes == 2`.

## 9. Finite-state

Symmetric and asymmetric 3-state kernels: balance residual 1.39e-17.
Mutations break balance.

## 10. Demonstration

Two-band n=1: Stage-1 reject, Stage-2 reject, accept. Cheap ≠ exact.

## 11. Mutations

Drop Stage 2; drop `-ell_hat` in Stage 2; invert Hastings; cheap as
exact; stale cache; `g=0`; illegal uniforms; unimplemented q-term DROP
already in Task 2.

## 12. P1

Same two-stage algebra. Different cheap object, target, and proposal
representation. NOT_IDENTICAL.

## 13. Paths

| Path | Purpose |
|---|---|
| `target_policy.py` | `positive_real_F_v1` |
| `proposal.py` | `ProposalSpec` |
| `da_kernel.py` | Design B algebra + kernel |
| `tests/test_da_*.py` / `test_target_policy.py` / `test_proposal_spec.py` | Task-3 tests |
| `scripts/diagram_compiler_task3.py` | Evidence |
| `docs/DIAGRAM_COMPILER_TASK3.md` | Technical document |
| `research/diagram_compiler/task3/` | JSON/CSV + this report |

## 14. Verification

Closing run: Task-1 281, Task-2 52, Task-3 36, combined 369; exact
224/224 max error `2.7755575615628914e-17`; `git diff --check` at
commit.

## 15. Maturity

Delayed-acceptance generation: ESTABLISHED for Design B on the
restricted positive-`F` domain. Native codegen: NOT IMPLEMENTED.

## 16. Remaining gap

**A Native Kernel IR that lowers this DA spec plus the exact/cheap
DAGs into an explicit backend-ready plan (Fortran ABI, cache slot,
no Python closures).**

## 17. Next task

Task 4 — lower the generated delayed-acceptance kernel into an
explicit native KernelIR suitable for Fortran code generation. Not
implemented.
