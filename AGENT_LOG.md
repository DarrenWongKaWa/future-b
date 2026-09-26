# Agent log

## 2026-09-26 — Future B v1.3.1: toolkit bug attribution corrected

- v1.3.0 presented `FUTUREB_WQFIX` as a new finding. It is the C0 defect
  (recorded in v1.0, adapter in v1.1.0, same line of `add_external_ph`).
  Docs, docstrings and the native report now say so; the two
  `remove_external_ph` bugs remain new.
- Checked composition on a pin clone: C0 then `prepare --profile fixes`
  succeeds (redundant guarded call); `prepare` then C0 is refused.
- Documentation only; `release/v1.3.0/SHA256SUMS.txt` frozen by hash.

## 2026-09-26 — Future B v1.3.0: FEP-DMC toolkit in the package

- Moved the native FEP-DMC toolkit from `research/r1_grouped/native_rb` into
  `future_b.fepdmc` (patches, patched Fortran data, Docker driver, pooled
  estimator, exactness validator, analysis modules) with the
  `future-b-fepdmc` command; moved the finite R1 grouped toy into
  `future_b.r1_grouped`. `research/r1_grouped` keeps reports and evidence.
- `future-b-fepdmc prepare --profile research` on a clean pin reproduces the
  sources of the verified research build byte for byte.
- Froze `release/v1.2.0/SHA256SUMS.txt` by hash; current record is
  `release/v1.3.0/`. C0/P1 adapters and frozen science unchanged.
- Source tree: `546 passed, 1 skipped`. Unpacked 1.3.0 sdist: `131 passed`.
  Wheel ships `fepdmc/data/*` and the console script.

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
