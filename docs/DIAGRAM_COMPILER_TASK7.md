# Task 7: independent audit and reproducibility repair

Task 7 repairs the reproducibility blockers found while auditing the Task 6
worktree. It does not change the scientific scope of Tasks 1–6 and does not
touch Future B v1.2.0, C0, public P1, or the production FEP-DMC source.

## Repairs

- The R1 reference modules needed by the 224-case oracle are tracked under
  `src/keldysh4ai/scheme_d`.
- The historical fixed-order metadata and frozen R1 benchmark witness are
  tracked under `src/future_b/r1_fixed_order` and
  `benchmarks/r1_fixed_order`.
- The only source adjustment is relocation of the symbolic rebind fixture to
  the adjacent tracked `rebind_cases.csv`; its numerical content is unchanged.
- Absolute developer paths were removed from compiler evidence and provenance.
- `Dockerfile.u22` pins the public Ubuntu 22.04 image by digest and installs
  Ubuntu's gfortran 11.4 package.
- Task 6 now requires an explicit FEP-DMC path and uses no private default.
- GitHub Actions covers the compiler tests, the 224-case differential, the
  pinned FEP-DMC checkout, Docker rebuild, and Task 6 native validation.

## Fresh local evidence

After these repairs, a clean source checkout reproduces:

- `224/224` exact differential cases, maximum absolute error
  `2.7755575615628914e-17`;
- the compiler test suite with `483 passed, 1 skipped` when the external FEP
  path is not supplied;
- Task 6 with Ubuntu 22.04/gfortran 11.4, all fixture rows matching the
  NativeKernelIR interpreter, zero Stage-1 exact calls, balance residual
  `6.938893903907228e-18`, and stationarity residual `0.0`.

The one skipped test is the optional local FEP-DMC pin check when the caller
does not provide the external checkout. CI supplies the checkout explicitly.

## Claim ceiling

The resulting research preview can claim a bounded fixed-order DiagramIR,
exact and `propagator_only_v1` cheap evaluators, Design-B delayed acceptance
on `positive_real_F_v1`, typed NativeKernelIR lowering, deterministic Fortran
emission, and LEVEL 2 validation in the pinned public toolchain. It cannot
claim arbitrary-order or generic QFT compilation, production FEP-DMC
replacement, public P1 replacement, speedup, or broad material validation.
