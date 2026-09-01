# Candidate 1 report — A(ω), Z, M1 versus ED Lehmann

Worker 1 (Science). Extract `/Users/kawawong/Research/future-b`.
No new K4AI number. No merge to `main`. No edit of `holstein_ed.py`
or `l2_periodic_pole.py`. No router, logistic, MLP, or learned gate.
θ_class remains 0.03. Depths are Week-3 `depth_gated`. `paper1_go`
stays false.

Preregister `notes/C1_METRICS_PREREGISTER.md` was on disk **before**
any A(ω) or M1 numbers, before
`prototypes/future_b_neural_poc/c1_spectral_vs_ed.csv`, and before
this report. Tests T1–T3 are evaluated here from that CSV only.

Question: after the Week-3 Σ-residual at z=0+iη failed to mark a
one-layer E0 error, do A(ω), Z, or the first moment versus ED Lehmann
still show structured error in λ? Does classical θ=0.03 already
suffice on that observable?

## 1. Tests T1–T3

Source: `prototypes/future_b_neural_poc/c1_spectral_vs_ed.csv`
(12 rows). A(ω)=−(1/π) Im G^R(k=0, ω+iη_A) for ED, Born, SCBA64, and
SCBAgate. η_A=0.05 t. ω=`np.linspace(-8.0, 4.0, 1601)`. ED Lehmann
uses teacher `M_used`. SCBAgate uses Week-3 `depth_gated` at
θ=0.03. E0 windows from `teacher_map_l2.csv` / Week-3 `E0_gated`.

| test | verdict | counts |
|------|---------|--------|
| T1 Structure | **FAIL** | 15/17 comparisons; 2 exceptions (at most one allowed) |
| T2 Residual ≠ spectrum | no extra spectral leftover on this grid | 0/12 leftover cells; 12/12 `match_grain_ok=true`; no cell with error_A(gate)−error_A(64)>0.05 |
| T3 Classical sufficiency | **PASS-SUFFICIENT** | mean_test error_A(gate)=0.5474091752020821 ≤ mean_test error_A(64)+0.05; 6/6 test cells have error_A(gate)−error_A(64)≤0.10 (worst 0.0021761106230745453) |

`notes/C1_STOP.md` **was written** because T1 failed. Thresholds were
not softened. T3 is independently PASS-SUFFICIENT, so a spectral gate
is not opened either. No network.

### T1 exceptions (error_A of SCBA64)

Grid of `error_A_SCBA64`:

| g/t | Ω/t=0.5 | 0.8 | 2.0 |
|------|---------|-----|-----|
| 0.15 | 0.01541895 | 0.00393799 | 0.00027529 |
| 0.45 | 0.58869613 | 0.21049125 | 0.02028843 |
| 0.75 | 1.27360981 | 0.87952359 | 0.12161429 |
| 1.05 | 0.98631729 | 1.41567983 | 0.37355865 |

Fifteen consecutive comparisons increase. Two fail, both at
(1.05, 0.5):

- fixed Ω=0.5, g=0.75→1.05: 1.2736098120802806 !< 0.9863172923173602
- fixed g=1.05, Ω=0.8→0.5: 1.4156798290239707 !< 0.9863172923173602

Week-2 `rel_SCBA` on E0 was 17/17 monotone. Discrete-L2 A(ω) is not.
That is a T1 fail, not a license to retune the observable onto Z or
M1.

### T2

Every Week-3 cell has `match_grain_ok=true`. On this A(ω) grid,
error_A(SCBAgate)−error_A(SCBA64) is at most a few 10^{-3} (test worst
0.0021761106230745453 at (0.45, 0.5); strong-cell train gap
0.002830556741512821). None exceed 0.05. No cell has a failed E0
match with a close spectrum. Record: **no extra spectral leftover on
this grid**.

### T3

TEST cells only:

- mean_test error_A(SCBAgate) = 0.5474091752020821
- mean_test error_A(SCBA64) = 0.5469474366582046
- mean gap = 0.00046173854387754343 ≤ 0.05
- 6/6 test cells have gap ≤ 0.10

PASS-SUFFICIENT: classical θ=0.03 already matches depth-64 SCBA on
A(ω) to the preregistered tolerances. Stop opening a spectral gate.
Do not train.

## 2. Companion observables (not stop criteria)

Z is finite on all 12×4 entries (none `NOT_COMPUTED`). Z_ED falls as
λ rises / Ω falls (0.973 at (0.15, 2.0) to 0.100 at (1.05, 0.5)).
SCBA64 overestimates that weight at the strong cell (Z_SCBA64=0.423
versus Z_ED=0.100). error_M1(SCBA64) is smaller than error_A and
increases toward the strong/adiabatic corner on this grid. Those
patterns are recorded; they do not replace T1.

On every cell, error_A(Born) > error_A(SCBA64). That 12/12 count is
descriptive, not a T1–T3 criterion.

## 3. Claim ceiling

On this frozen periodic L=2 grid, discrete-L2 A(ω) error of depth-64
SCBA versus ED Lehmann is not monotone in λ (15/17; two exceptions at
(1.05, 0.5)). Classical θ=0.03 already matches depth-64 on A
(PASS-SUFFICIENT; mean test gap 4.62×10^{-4}). No extra spectral
leftover versus the Week-3 E0 grain. Candidate 1 stops. This is not a
learned gate and not Physics-for-AI.

## 4. What remains NOT_COMPUTED / closed

- any learned spectral gate, router, logistic, MLP, or GRU
- retuning θ or the A-grid after T1
- E0_Born_VC (still `NOT_COMPUTED` in every cell)
- L≠2, open-chain spectra, Σ_VC on SCBA
- Weeks 7–8, Paper 1 GO, Physics-for-AI
- archive 11A, K4AI-592, K4AI-593 as live Future B proof
