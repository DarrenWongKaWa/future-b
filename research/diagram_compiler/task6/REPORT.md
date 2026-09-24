# Task 6 — consolidated research report

Result: **LEVEL 2 established**. The Task-5 generated two-band n=1
kernel compiles with Ubuntu 22.04 gfortran 11.4 (public FEP-DMC
toolchain family) and matches `interpret_native_kernel`. Pinned FEP-DMC
`05d08449` remains `PUBLIC_PRISTINE`. Public P1 is not replaced.

Architecture A: separate validation executable. No `update_swap` patch.

## Baseline

Task-5 HEAD `9b4f3ed`. Generated Fortran and runtime hashes unchanged.
Regenerated source SHA256 matches Task 5.

## Native demo

Stage-1 reject / Stage-2 reject / accept match the interpreter with
floating abs err 0.0. Stage-1 reject exact-graph calls 0.

## Finite-state

Native score kernel: balance `6.94e-18`, stationarity `0.0`.

## Next

Task 7 — independent audit / experimental release gate. Not implemented.
Not a v1.2.0 release.
