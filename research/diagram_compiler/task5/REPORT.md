# Task 5 — consolidated research report

Result: **Fortran backend established** for NativeKernelIR
(`fortran_v1` + `native_kernel_v1`). Compiled two-band n=1 kernel
matches `interpret_native_kernel` on discrete outputs exactly and on
floating outputs within predeclared `atol=1e-12`. No FEP-DMC
integration.

Process: runtime, emitter, compile harness, and tests were written in
one cycle after architecture/ABI research; not eleven separate git
milestones.

## 1. Baseline

Worktree from `0110f22`. Start: 383 tests. Exact 224/224 unchanged.
Task-4 `native_*.py` hashes unchanged
([baseline.json](baseline.json)).

## 2. Chosen architecture

Generated kernel + versioned primitive runtime. Not a monolithic
subroutine. Not per-kernel primitive bodies.

## 3. Demonstration

Two-band n=1: generated
[generated_twoband_n1.f90](generated_twoband_n1.f90), compiled with
gfortran 16.1.0 `-O0`. Stage-1 reject / Stage-2 reject / accept match
the interpreter. `ell_hat` and `ell_R` absolute error 0.0 on the
demo bindings.

## 4. Differential

[kernel_differential.csv](kernel_differential.csv) and
[primitive_differential.csv](primitive_differential.csv).

## 5. Finite-state

Compiled score kernel: balance residual `6.94e-18`, stationarity `0.0`
([finite_state_fortran.csv](finite_state_fortran.csv)).

## 6. Next

Task 6 — integrate the generated Fortran kernel into a pinned public
FEP-DMC validation path. Not implemented.
