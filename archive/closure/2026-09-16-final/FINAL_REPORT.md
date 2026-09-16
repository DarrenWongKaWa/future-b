# Future B — final report

## 1. Question and Motivation

FACT: The material observable is LiF-electron polaron formation energy
\(Q=E_{\mathrm{polaron}}-E_{\mathrm{bare}}\) on a frozen Method0 discrete
Hamiltonian (20³, rank 20). The estimator is
\(Q=\mathrm{Re}(\sum N_b/\tau_{\max,b}/\sum D_b)-E_{\mathrm{bare}}\) with
\(E_{\mathrm{bare}}=9.35487318746596053\,\mathrm{eV}\).

INFERENCE: The scientific bet was that analytic delayed acceptance (P1)
and, if data allowed, tiny residual models (P4/P5) could cut exclusive
exact work on swap (~21% of coarse MC) without changing the exact target.

## 2. Approach and Model

FACT: Native Luo EZ Monte Carlo remains the consumer. P1 scores
\(\ell_{\mathrm{prop}}=\mathrm{clip}(\log P_{k\mathrm{change}},\pm\ln 10)\)
from cheap mid-band and phonon times, then applies exact stage-2
correction with \(\mathrm{abs}(\mathrm{Re} M)\).

FACT: Historical Group-v3 and fixed-order R1/CSE are different recipes
and were not reopened as search.

## 3. Key Mechanism

FACT: Stage-1 rejection returns before `cal_gkq` and environment
contraction. Fixture records g/env increment 0 on those returns.
Stage-2 uses the native exact ratio. Models were forbidden from replacing
that target.

## 4. Result and Evidence

FACT (energy zero): Unshifted ratios ~9.105 eV are **not** \(Q\). After
subtracting \(E_{\mathrm{bare}}\), C5_dev formation energies are
B0 −0.250253, B-best −0.247842, P1-fixture −0.249584 eV.

FACT (clean P1 confirmation, protocol frozen first):
`closure/2026-09-16-final/p1_confirm/result.json`.
Clean P1 \(Q=-0.246614\) eV (JK SE 3.35 meV), B-best \(Q=-0.251403\) eV
(SE 2.08 meV). Wall ratio \(T_{\mathrm{P1}}/T_{\mathrm{Bbest}}=0.956\)
with bootstrap 2.5–97.5% **0.940–0.972**. Independent a1 reject rate
**0.332**. HAC failed on some chains (`hac_ok=false`).

FACT: Classification **`P1_UNRESOLVED_WITHIN_BUDGET`**. The interval
crosses 0.95; HAC fails; \(K=T\mathrm{Var}\) point ratio 2.49 with a
uselessly wide bootstrap.

FACT: P4/P5 **`DATA_CONTRACT_NOT_CLOSED`**. R1 material
**`R1_MATERIAL_CONNECTION_NOT_CLOSED`**. Ground-state 1%
**`NOT_CERTIFIED`**. C6/C7 were not started.

## 5. Interpretation and Scope

INFERENCE: −0.25 eV matches the order of Luo et al. Fig. 2(b) at 20³.
It is not Table 1 (−0.408) or Fan–Migdal/DW (−0.538).

NEGATIVE RESULT (scoped): fixed-order R1 vs CSE ~0.9992; Group-v3 no
gain; historical fixture-P1 wall intervals included 1.

UNRESOLVED: whether a ≥5% wall saving exists for **clean** P1. The
point is a ~4.4% wall cut; the predeclared interval does not sit
entirely below 0.95.

NOT TESTED: P4/P5 learning gain; R1 as a material grouped consumer.

## 6. What Failed and Why

- Reporting \(Q\) as the unshifted ratio (fixed without rerunning chains).
- Calling C5 `status=OK` while 5/18 HAC tests failed.
- Treating `C2_DUMP=0` as a clean timed path (after-commit `p1_prop_ell`).
- P4/P5 never obtained 64-d packets or whole-chain labelled splits.
- Native grouped R1 measure cannot be closed from existing artifacts
  because `abs(sum D)`, `sum abs(D)`, and `abs(real D)` differ.

## 7. What Was Successfully Built

Native frequency repair; C1 exclusive timers; analytic P1 with
independent counters; event dumps; real-material 6+6+6 DEV; a **clean**
P1 binary (`P1_FIXTURE` default off); a frozen confirmation protocol
and batch.

## 8. What Was Not Demonstrated

Reliable ≥5% wall or equal-precision speedup; 1% ground-state
certification; learning-module value; R1 material sampling gain.

## 9. Why the Project Is Being Closed

The defined recipes have been taken as far as the frozen SINGLE_HOST
closure budget allows. Remaining uncertainty is recorded, not used to
open Future C.

## 10. Reproducibility / Evidence Map

See `FINAL_EVIDENCE.md` and `SHA256SUMS.txt`.
Historical night1 paths were not overwritten.

### OUT-OF-SCOPE FUTURE WORK — NOT PART OF THIS PROJECT

A longer HAC-stable confirmation of clean P1, a legal native grouped
measure, or a 64-d packet pipeline could be someone else's project.
They are **not** Future B continuation.
