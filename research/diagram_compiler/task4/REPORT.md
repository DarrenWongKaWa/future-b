# Task 4 — consolidated research report

Result: **NativeKernelIR established** as a typed SSA + CFG lowering of
the Task-3 Design B kernel. Interpreter matches Task-3 on deterministic
transitions. No Fortran emitted.

Process: tests and implementation were written in one cycle after a
red collection would have failed on missing modules; not eleven
separate git milestones.

## 1. Baseline

Worktree from `3822036`. Start: 369 tests. Exact 224/224 unchanged.
`da_kernel.py` hash unchanged.

## 2. Chosen IR

Typed SSA + basic blocks. Not a nested AST. Not a Fortran AST.

## 3. Demonstration

Two-band n=1 kernel: 24 cheap ops, 33 exact ops, 8 blocks.
Stage-1 reject path contains no exact graph call.

## 4. Differential

`differential_results.csv`: four paths, all `accepted_match` and
`exact_y_match` true.

## 5. Finite-state

Balance residual 1.39e-17 via native score formulas.

## 6. Next

Task 5 — Fortran backend from NativeKernelIR. Not implemented.
