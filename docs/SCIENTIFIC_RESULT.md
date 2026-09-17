# Scientific result (Future B, closed)

**Project status: CLOSED.** This document is the scientific record, not a
proposal for another cycle.

FACT / INFERENCE / UNRESOLVED / NEGATIVE RESULT / NOT TESTED are marked
explicitly.

## 1. Question and Motivation

FACT: The primary material observable is the LiF-electron polaron
formation energy on a frozen discrete Hamiltonian (Luo EZ / Method0,
\(20^3\) phonon grid, rank 20):

\[
Q = E_{\mathrm{polaron}} - E_{\mathrm{bare}}
= \mathrm{Re}\!\left[
  \frac{\sum_b N_b/\tau_{\max,b}}{\sum_b D_b}
\right]
- E_{\mathrm{bare}}
\]

with \(E_{\mathrm{bare}} = 9.35487318746596053\,\mathrm{eV}\).

FACT: The unshifted ratio \(\sim +9.105\,\mathrm{eV}\) is **not** \(Q\).
A previous postprocessing error omitted \(E_{\mathrm{bare}}\). Corrected
values are \(\approx -0.25\,\mathrm{eV}\).

INFERENCE: Native FEP-DMC spend is concentrated in electron–phonon
vertices, environments, and a subset of Monte Carlo updates. The
scientific bet was that a *legally corrected* cheap filter on the swap
update could skip some exclusive exact work without changing the target.

## 2. Approach and Model

FACT: The consumer remains native Luo EZ diagrammatic Monte Carlo
(Perturbo FEP-DMC). Future B did not replace the Hamiltonian, the
material, or the exact weight.

FACT: Analytic P1 delayed acceptance scores a cheap log-ratio
\(\ell_{\mathrm{prop}}=\mathrm{clip}(\log P_{k\mathrm{change}},\pm\ln 10)\)
from mid-band energies and phonon times, then applies an exact stage-2
correction using \(\mathrm{abs}(\mathrm{Re}\,M)\), not
\(\lvert M\rvert_{\mathbb{C}}\).

FACT: Historical Group-v3 and frozen P4/P5 recipes are different
objects. P4/P5 were **not** trained in this wrap-up. Fixed-order R1 is
an evaluator of `SHARED_X_GROUP`, not a native grouped sampler.

## 3. Key Mechanism

FACT: On an eligible swap, stage-1 rejection returns *before*
`cal_gkq` and environment contraction. The bounded fixture recorded
4372 such rejections with g/environment increment 0.

FACT: Stage-2 uses the native exact ratio. No learned model was allowed
to replace that target.

FACT: Reverse P1 scores use occupancy reverse (swap phonon assignment at
fixed time order). Flipping both \(\Delta t\) and \(\Delta E\) is
algebraically wrong and was repaired.

## 4. Result and Evidence

### 4.1 Fixed-setting formation energy (historical C5 DEV, preserved)

Six independent real-material chains per arm, \(N_{\mathrm{mc}}=200\times 10^4\)
attempts, same Method0 setting. Jackknife SE and Student-\(t_5\) 95%
point half-width:

| arm | \(Q\) (eV) | JK SE (meV) | rel. JK SE | 95% HW (meV) | rel. 95% HW |
|---|---:|---:|---:|---:|---:|
| B0 | −0.250253260 | 2.368 | 0.946% | 6.088 | 2.433% |
| B-best | −0.247842001 | 3.712 | 1.498% | 9.541 | 3.850% |
| P1 (fixture binary) | −0.249583768 | 2.343 | 0.939% | 6.023 | 2.413% |

Evidence: `benchmarks/c5_dev/frozen_results.json`,
`research/mainline/CLOSURE/2026-09-14/runs/night1/C5_dev/recomputed/`.

FACT: HAC Bartlett lags 2/4/8 failed on 5/18 chains
(B0_r3, Bbest_r1, Bbest_r2, Bbest_r4, P1_r1). This batch is **not** a
full statistical acceptance pass.

FACT: These numbers are a **fixed discrete Hamiltonian algorithm
benchmark**. They are **not** a 1% certified ground-state result.
1% of \(\lvert Q\rvert\) is \(\approx 2.5\,\mathrm{meV}\), not
\(\sim 91\,\mathrm{meV}\).

### 4.2 Clean P1 vs B-best (protocol frozen first)

Clean production binary SHA256
`f9518a21fc2b8750fb3b7ed6f6e065db398cb2f425969cd718d1dcdef2b2c25c`.
`P1_FIXTURE` gating was compiled **before** this binary and before the
timing batch; confirmation ran `P1_FIXTURE=0` (no `c2_swap.tsv`).
Released Fortran excerpts are a byte copy of that tree
([PROVENANCE.md](PROVENANCE.md)). Fixture dump/reverse run only if
`P1_FIXTURE=1`. The 0.956 ratio was **not** rerun after the GitHub
packaging.

| arm | \(Q\) (eV) | JK SE (meV) | rel. SE | wall \(T\) (s) | \(K=T\cdot\mathrm{Var}_{\mathrm{JK}}\) |
|---|---:|---:|---:|---:|---:|
| B-best | −0.251403 | 2.077 | 0.826% | 32.721 | \(1.412\times 10^{-4}\) |
| clean P1 | −0.246614 | 3.350 | 1.358% | 31.293 | \(3.511\times 10^{-4}\) |

Same six-chain workload for \(T\) and \(\mathrm{Var}(\hat Q)\).

- Wall ratio \(T_{\mathrm{P1}}/T_{\mathrm{Bbest}} = 0.956\);
  bootstrap 2000, seed 9143610: **[0.940, 0.972]**. Crosses 0.95.
- Cost–variance point ratio \(K_{\mathrm{P1}}/K_{\mathrm{Bbest}} = 2.486\);
  bootstrap **[0.164, 21.5]** (unusable). HAC not clean
  (`hac_ok=false`; B-best chains 0,3; P1 chains 0,2,3).
- Independent counters (6 P1 chains pooled): 1 395 968 eligible;
  463 424 stage-1 rejects (rate 0.332); 932 544 exact-stage;
  30 600 stage-2 rejects; 901 944 accepts.
  Identity \(n_{a1}+n_{a2}+n_{\mathrm{acc}}=n_{\mathrm{eligible}}\) holds.

FACT: the wall point estimate is a \(\sim 4.4\%\) reduction. The JK
variance **point** estimate is larger for P1
(\(\mathrm{SE}\) 3.350 vs 2.077 meV). That is **not** a certified
statement that P1 is \(2.49\times\) worse at equal precision: HAC
failed and the \(K\) interval is too wide.

INFERENCE: the unproven implication is
“fewer expensive calls \(\Rightarrow\) lower equal-precision total
cost”, not merely “0.956 versus a 0.95 wall threshold”.

Classification (frozen wall-ratio rule): **`P1_UNRESOLVED_WITHIN_BUDGET`**.
Do not upgrade \(K\) to `P1_NO_PRACTICAL_GAIN` or to a slowdown claim.

Evidence: `benchmarks/p1_vs_bbest/frozen_results.json`,
`closure/2026-09-16-final/FINAL_PROTOCOL.md`.

### 4.3 Engineering positives (preserved)

- C0: `add_external_ph` now refreshes \(\omega_q\) via `cal_wq_int`.
  OFF/shadow identity and table check passed (`C0_ACCEPTED`, repair_v2).
- C1: swap is \(\approx 21.2\%\) of coarse exclusive MC
  (`f_swap=0.21198`). Environment/propagator/EPC remain large.
- Logger NEWUNIT bug (negative unit reopened `status=replace`) repaired.
- Reverse double-flip repaired.

### 4.4 Scoped evaluator result (R1)

NEGATIVE RESULT (scoped): in the tested fixed-order compile-once domain,
R1 vs optimized CSE total-time ratio is \(\approx 0.9992\) (tier range
0.9863–1.0034). Correctness/reuse was validated; no additional evaluator
speedup was established.

NOT TESTED: a legal native material grouped consumer
(`SHARED_X_GROUP` as the Monte Carlo object).

## 5. Interpretation and Scope

INFERENCE: \(-0.25\,\mathrm{eV}\) matches the order of Luo et al.
Fig. 2(b) at \(20^3\). It is not their Table 1 value (\(-0.408\,\mathrm{eV}\))
and not Fan–Migdal/DW (\(-0.538\,\mathrm{eV}\)).

INFERENCE: P1 is a real implementation: it runs on LiF and rejects
\(\approx 1/3\) of eligible swaps before g/environment. The clean
confirm showed a \(\approx 4.4\%\) wall-time **point** reduction and a
**larger** JK-variance point estimate. Neither a \(\ge 5\%\) wall gain
nor an equal-precision cost reduction was established. The frozen
classification is unresolved on the predeclared **wall** rule; \(K\) is
a diagnostic, not a second pass/fail after seeing the data.

The fixed-setting statistical diagnostic is at the **few-percent**
level. A 1% ground-state certification was **not attempted**.

## 6. Negative / Unresolved Results

| claim | disposition |
|---|---|
| clean P1 \(\ge 5\%\) wall gain vs B-best | `P1_UNRESOLVED_WITHIN_BUDGET` |
| historical fixture-P1 wall bootstrap | intervals include 1 (timing contaminated) |
| Group-v3 fixed recipe | `NO_DEMONSTRATED_GAIN_FIXED_RECIPE` |
| R1 vs CSE (fixed-order evaluator) | `NO_ADDITIONAL_CSE_GAIN_ESTABLISHED` |
| P4 / P5 | `FUTURE_WORK_CANDIDATE` (not trained) |
| R1 material grouped consumer | `FUTURE_WORK` (not implemented) |
| 1% ground-state \(Q\) | `NOT_CERTIFIED` / `NOT_PURSUED` |

Do **not** upgrade unresolved or not-tested items into “ML cannot
accelerate FEP-DMC” or “all grouping is impossible”.

## 7. Engineering Contributions

- Native scientific-software audit and \(\omega_q\) repair.
- Exclusive nested timers.
- Exact-corrected analytic delayed acceptance in the swap update.
- Event-level fixture: stage-1 g/env skip, occupancy reverse,
  `abs(Re M)` target.
- Independent production counters (`LINEAR_DA_COUNTS`).
- Energy-zero correction in postprocessing.
- Frozen confirmation protocol written *before* the clean-P1 batch.

Upstream Luo/Park/Bernardi FEP-DMC, Perturbo, electron–phonon
compression, and matrix-product band summation are **not** Future B
inventions.

## 8. Reproducibility

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) and
[DATA_AND_LICENSE.md](DATA_AND_LICENSE.md).

Minimal path (no 56 GB workspace, no LiF HDF5):

```bash
python3 -m venv .venv && .venv/bin/python -m pip install --upgrade pip && .venv/bin/pip install -e ".[dev]"
.venv/bin/pytest tests/test_da_balance.py tests/test_forward_reverse.py \
  tests/test_energy_zero.py tests/test_statistics.py tests/test_r1_oracles.py \
  tests/test_p1_clean_source.py tests/test_reject_state.py -q
python examples/lif_small_fixture/recompute_q.py
```

Full LiF native chains require QE 6.5, Perturbo, the authors' epwan
HDF5, and Docker `r5p0-env:ubuntu2004` (not redistributed here).

## 9. Future Work

Documented **outside** this closed project:

- [P4/P5 learning candidates](future_work/P4_P5_LEARNING_CANDIDATES.md)
- [R1 real-material grouped consumer](future_work/R1_REAL_MATERIAL_GROUPED_CONSUMER.md)
- [1% ground-state certification](future_work/GROUND_STATE_1PCT.md)

They are not Future B continuation tasks.

## Status table

| item | status |
|---|---|
| C0 \(\omega_q\) repair | POSITIVE / PRESERVED |
| C1 hotspot profile | FACT / PRESERVED |
| corrected LiF fixed-setting \(Q\) | RESULT / PRESERVED |
| clean P1 correctness | COMPLETE (source + fixture) |
| clean P1 \(\ge 5\%\) practical gain | `UNRESOLVED_WITHIN_BUDGET` |
| historical Group-v3 | `NO_DEMONSTRATED_GAIN_FIXED_RECIPE` |
| P4 | `FUTURE_WORK_CANDIDATE` |
| P5 | `FUTURE_WORK_CANDIDATE` |
| R1 fixed-order evaluator | `VALIDATED_IN_SCOPE` + `NO_ADDITIONAL_CSE_GAIN_ESTABLISHED` |
| R1 real-material grouped consumer | `FUTURE_WORK` |
| 1% ground-state \(Q\) | `NOT_CERTIFIED` / `NOT_PURSUED` |
| GitHub package | `v1.0.3` packaging maintenance (science frozen at `v1.0.0`) |
