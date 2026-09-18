# Task 6: FEP-DMC toolchain validation of generated Fortran

Experimental Diagram Compiler integration. This is not a production
replacement of FEP-DMC Monte Carlo acceptance and is not public P1.

## 1. Task-5 baseline

HEAD `9b4f3ed5d5c29a288b8e4524d983bd55d33a008b`. Generated two-band n=1
Fortran SHA256 `ff4aa2de2338cb9c6894487ac805b4bbd971549dfbdb0e1480888c5af588c32e`.
Runtime SHA256 `64ec0f3071380023e9287197adc815d05cd51a6c5c79889b0d35cb162b7f85b2`.
Backend `fortran_v1`, primitive set `native_kernel_v1`. Combined tests
480 at Task-5 close. Exact 224/224. See
[baseline.json](../research/diagram_compiler/task6/baseline.json).

## 2. Integration question

Can the Task-5 generated kernel be compiled and executed in the public
FEP-DMC scientific toolchain while matching the NativeKernelIR
interpreter?

## 3. Semantic boundary vs public P1

| | Compiler kernel | Public P1 / native JJ |
|---|---|---|
| Target | `positive_real_F_v1` | `abs(Re M)*P_kchange` |
| Cheap | `propagator_only_v1` STATE_WEIGHT | local `P_kchange` TRANSITION_SCORE |
| DA | Design B | P1 Architecture C on `update_swap` |
| State | Holstein Binding | Feynman diagram / Wannier |

They are not identical. Task 6 does not replace P1.

## 4. Integration architecture alternatives

| | A separate validation exe | B files added to FEP-DMC | C shadow `update_swap` |
|---|---|---|---|
| LEVEL 2 | yes | yes | needs LEVEL 3 map |
| Production invasion | none | new files | production JJ |
| P1 confusion | none | low | high |

## 5. Chosen validation path

**A.** Separate `futureb_dc_validate.x` compiled with Ubuntu 22.04
gfortran 11.4. Pinned FEP-DMC tree remains `PUBLIC_PRISTINE`. Nothing
is copied into `pert-src`. LEVEL 3/4 not attempted.

## 6. Public build environment

- OS authority: `public.ecr.aws/docker/library/ubuntu:22.04`
- Compiler: GNU Fortran 11.4.0 (`11.4.0-1ubuntu1~22.04.3`)
- Container used: `futureb-u22-env:local` (local Ubuntu 22.04.5 + distro
  gfortran cache of that public OS)
- Flags: `-O0 -std=f2008 -ffree-line-length-none -fcheck=bounds -J.`
- QE / HDF5 / MPI: not linked
- Private image `r5p0-env:ubuntu2004`: not used

## 7. Source adapter/state if any

No FEP-DMC source transform. `integration/diagram_compiler/verify_pin.py`
classifies `PUBLIC_PRISTINE` vs `UNKNOWN` and refuses compiler-kernel
needles in the upstream tree. Production files:

- `diagMC_JJ_updates.f90` `6c97c694…`
- `diagMC.f90` `599868f4…`
- `pert_param.f90` `b36eefce…`
- `makefile` `e8b16763…`

HEAD `05d08449cffdbd0dfbbbf5009add5cc887bc754b`.

## 8. Fixture/oracle bridge

Canonical JSON
[fixture_manifest.json](../research/diagram_compiler/task6/fixture_manifest.json)
plus deterministic text files under `fixtures/`. Values come from
`interpret_native_kernel`. The native driver is `emit_driver` output, not
a handwritten DA formula.

## 9. Native differential validation

[native_differential.csv](../research/diagram_compiler/task6/native_differential.csv):
Stage-1 reject, Stage-2 reject, accept, asymmetric `log q`, cached and
uncached exact(x), `g=0` cheap failure (status 2), nonfinite `log q`
(status 3), invalid `u1`/`u2` (status 4). Discrete fields match exactly.
Floating abs err 0.0 where defined.

## 10. Native exact-laziness

[native_call_counts.csv](../research/diagram_compiler/task6/native_call_counts.csv):
Stage-1 reject has `n_exact_graph=0` and zero twoband/vertex/matmul/trace.
Stage-1 pass cases have `n_exact_graph>0`. Cached exact(x) has
`n_exact_graph=1`.

## 11. Finite-state revalidation

Compiled score kernel on the same Ubuntu gfortran: balance residual
`6.938893903907228e-18`, stationarity `0.0`.

## 12. Provenance chain

DiagramIR → NativeKernelIR digest `4932e8b0…` → generated Fortran
`ff4aa2de…` → runtime `64ec0f30…` → FEP-DMC pin `05d08449…` (unmodified)
→ Ubuntu 22.04 gfortran 11.4 → ELF `futureb_dc_validate.x` SHA256
`1f2dfd60668ef8a5aa11fa0fe147293546208d76dc9d137577bcde14cf69d59e`
→ fixtures → native differential. Binary hash is this compiler only.

## 13. What LEVEL was reached

LEVEL 0: PASS (Task 5). LEVEL 1: PASS. LEVEL 2: PASS. LEVEL 3: NOT
ATTEMPTED. LEVEL 4: NOT ATTEMPTED.

## 14. What was NOT established

Production FEP-DMC does not call the generated kernel. Public P1 is
unchanged. No speedup. No Binding map from `type(fynman)`. Variable-order
compilation is absent. One gfortran family (11.4 on Ubuntu 22.04 aarch64);
not a multi-compiler portability claim.

## 15. Release-readiness assessment

READY_FOR_INDEPENDENT_AUDIT of the experimental Diagram Compiler line
through LEVEL 2. Not a Future B v1.2.0 release, not a P1 release, and
not production FEP-DMC.
