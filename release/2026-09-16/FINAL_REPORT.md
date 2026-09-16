# Future B — final report (release wrap-up, 2026-09-16)

Canonical scientific text: `docs/SCIENTIFIC_RESULT.md`.
This file is the release-bundle copy with the required ten sections.

**project_status = CLOSED**

## 1. Question and Motivation

FACT: The material observable is LiF-electron polaron formation energy
\(Q=E_{\mathrm{polaron}}-E_{\mathrm{bare}}\) on frozen Method0
(\(20^3\), rank 20):

\[
Q=\mathrm{Re}\Big(\sum_b N_b/\tau_{\max,b}\Big/\sum_b D_b\Big)-E_{\mathrm{bare}}
\]

with \(E_{\mathrm{bare}}=9.35487318746596053\,\mathrm{eV}\).

FACT: The unshifted \(\sim+9.105\,\mathrm{eV}\) ratio is not \(Q\).

INFERENCE: The methods question was whether exact-corrected analytic
delayed acceptance (P1), and possibly tiny residual models or grouped
R1 evaluation, could reduce exclusive exact work without changing \(Q\).

## 2. Approach and Model

FACT: Native Luo EZ / Perturbo FEP-DMC remains the consumer. P1 scores
clipped \(\log P_{k\mathrm{change}}\) then restores the native ratio
with \(\mathrm{abs}(\mathrm{Re}\,M)\).

FACT: P4/P5 were not trained. R1 material grouped sampling was not
implemented. C6/C7 were not started.

## 3. Key Mechanism

FACT: Stage-1 rejection returns before `cal_gkq` and environment
contraction. Fixture: 4372 such events with recorded g/env increment 0.
Stage-2 is exact. Occupancy reverse is antisymmetric; \(\Delta t\) +
\(\Delta E\) double-flip is not.

## 4. Result and Evidence

FACT (C5 DEV, preserved):

| arm | \(Q\) (eV) | JK SE | rel. SE | 95% HW | rel. HW |
|---|---:|---:|---:|---:|---:|
| B0 | −0.250253260 | 2.368 meV | 0.946% | 6.088 meV | 2.433% |
| B-best | −0.247842001 | 3.712 meV | 1.498% | 9.541 meV | 3.850% |
| P1 fixture | −0.249583768 | 2.343 meV | 0.939% | 6.023 meV | 2.413% |

HAC 5/18 fail. Not a statistical pass. Not 1% ground state.

FACT (clean P1 confirm, protocol frozen first): wall ratio 0.956,
bootstrap [0.940, 0.972], crosses 0.95, `hac_ok=false`, a1 rate 0.332
on 1 395 968 eligible swaps. Classification
**`P1_UNRESOLVED_WITHIN_BUDGET`**. Not rerun in this wrap-up.

FACT: C0 \(\omega_q\) repair POSITIVE. C1 swap \(\approx 21.2\%\) FACT.
R1/CSE overall 0.9992 scoped NEGATIVE (evaluator). Group-v3
`NO_DEMONSTRATED_GAIN_FIXED_RECIPE`.

## 5. Interpretation and Scope

INFERENCE: \(-0.25\,\mathrm{eV}\) is the right order for Luo et al.
Fig. 2(b) at \(20^3\), not Table 1 (\(-0.408\,\mathrm{eV}\)).

The fixed-setting statistical diagnostic is at the few-percent level.
A 1% ground-state certification was not attempted.

P1 demonstrated real early rejection and a small observed wall-time
reduction. The predeclared \(\ge 5\%\) practical-gain criterion was
**not established**.

## 6. What Failed and Why

- Reporting \(Q\) as the unshifted ratio (fixed in postprocessing; chains
  not rerun for that shift).
- Calling C5 `status=OK` while 5/18 HAC tests failed.
- Treating `C2_DUMP=0` as a clean timed path (after-commit `p1_prop_ell`).
- P4/P5 never obtained 64-D packets (stopped as future work, not
  “ML is impossible”).
- Native grouped R1 measure cannot be closed from existing artifacts
  because \(\lvert\sum D\rvert\), \(\sum\lvert D\rvert\), and
  \(\mathrm{abs}(\mathrm{Re}\,D)\) differ.

## 7. What Was Successfully Built

Native frequency repair; C1 exclusive timers; analytic P1 with
independent counters; event dumps; real-material 6+6+6 DEV; a clean
P1 binary; a frozen confirmation protocol and batch; a public
documentation and unit-test package.

## 8. What Was Not Demonstrated

Reliable \(\ge 5\%\) wall or equal-precision speedup; 1% ground-state
certification; P4/P5 value; R1 as a material grouped consumer; neural
acceleration of FEP-DMC.

## 9. Why the Project Is Being Closed

The defined recipes were taken as far as the frozen SINGLE_HOST
closure budget allows. Remaining uncertainty is recorded. It is not
used to open Future C or another Future B swarm.

## 10. Reproducibility / Evidence Map

- `docs/` — scientific surface
- `benchmarks/` — frozen numbers
- `tests/test_*` listed in the README — public unit tests
- `closure/2026-09-16-final/` — native confirm (private tree; HDF5)
- `research/mainline/CLOSURE/2026-09-14/runs/night1/` — C0–C5
  (private tree; do not overwrite)

### OUT-OF-SCOPE FUTURE WORK — NOT PART OF THIS PROJECT

See `docs/future_work/`. Independent later research only.
