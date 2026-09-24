# Agent log

## 2026-09-24 — Diagram Compiler source integration

- Base: public GitHub `main` at `cbc951c`; source preview:
  `diagram-compiler-v0.1.0` / `2fc153f`.
- The two histories have no common Git ancestor. This branch transplants the
  bounded compiler paths onto public `main`; it does not merge unrelated
  histories or change the `v1.2.0` tag.
- Added the compiler source, independent R1 oracle, tests, Task 1--7 evidence,
  native validation bridge and dedicated CI workflow.
- Preserved all files locked by `release/v1.2.0/SHA256SUMS.txt`, including
  public P1, README, packaging metadata and distribution manifest.
- Source-tree tests with pinned FEP-DMC/Docker: `526 passed`.
- In a Docker-equipped environment without the configured local image and
  without a pinned checkout: `524 passed, 2 skipped`; the optional native
  tests now check the configured image before collection.
- Frozen sdist check: `110 passed`; it omits compiler evidence by the frozen
  v1.2.0 manifest and skips only evidence-dependent compiler tests.
- Task 6 integration check: `4 passed` with pinned FEP-DMC
  `05d08449`; compiled finite-state balance `6.938893903907228e-18`,
  stationarity `0.0`.
- Independent `future-b-diagram-compiler` 0.2.0 wheel/sdist built from a
  staged source manifest. A clean wheel ran the scalar n=1 quickstart and
  included the Fortran runtime. A clean sdist completed the Task-1 224-case
  script (max error `2.7755575615628914e-17`) and its suite
  (`413 passed, 2 skipped`; external FEP-DMC pin and local image not supplied
  there).
- Four editable draw.io pages record the compiler, delayed-acceptance,
  native-validation, and future material-provider flows.
- No production `update_swap` change, public P1 replacement, physics claim,
  speedup claim or Future B version/tag change.
