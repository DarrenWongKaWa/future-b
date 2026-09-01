# Candidate 1 metrics — preregistered before any A(ω) or M1 numbers

Authority: HUMAN LOCK 2026-08-31 plus a **new spectral question** on
the closed L=2 slice. Binding constraints:
`notes/CONSTRAINTS_FUTURE_B.md`. Sequence and claim-ceiling language
in `notes/SCIENCE_LINE_60DAY.md` remain in force. This is not a repair
of Week 4, not a learned gate, and not Weeks 7–8.

This file is written **before** any new spectral errors are computed,
**before** `prototypes/future_b_neural_poc/c1_spectral_vs_ed.csv`, and
**before** `notes/C1_REPORT.md`. Grid, bands, split, spectral
definition, η_A, ω-grid, Z window, M1 window, error formulas, SCBAgate
depth source, and tests T1–T3 are frozen here as **rules only**. They
are not fitted to A(ω), Z, or M1 values. Cuts, θ, and depths will not
be moved after seeing spectral errors.

Candidate 1 asks: after the Week-3 Σ-residual at z=0+iη failed to mark
a one-layer E0 error, do A(ω), Z, or the first moment versus ED Lehmann
still show structured error in λ? Does classical θ=0.03 already suffice
on that observable?

Candidate 1 does **not** train a router, logistic, MLP, or any learned
gate. It does not edit `holstein_ed.py` or `l2_periodic_pole.py`
(import only). It does not retune θ, does not add features, does not
set `paper1_go` true, and does not add Σ_VC onto SCBA.

## Frozen slice and signed conventions (not reopened)

- t = 1
- g/t ∈ {0.15, 0.45, 0.75, 1.05}
- Ω/t ∈ {0.5, 0.8, 2.0}
- twelve cells
- ξ_k = 2t(1−cos k), so E_0(g=0)=0 and ξ_0=0
- translator E_lecture = E_code − 2t
- tadpole / Hartree OFF in diagrammatic libraries
- Library I and Library II remain separate
- default **NO** Σ_VC on SCBA
- 11A unused
- E_0^{Born+VC} stays `NOT_COMPUTED`
- pole definition unchanged: η_pole = 10^{-4}t, window [−8.0, 0.25],
  E_0 = lowest interior Re D=0 of G(k=0)

Immutable inputs (do not edit):

- `prototypes/future_b_neural_poc/teacher_map_l2.csv`
- `prototypes/future_b_neural_poc/week3_gated_vs_fixed.csv`

Do not recompute E0_ED, E0_Born, or E0_SCBA. Do not recompute the
Week-3 gate. Do not edit week2 / week3 / week4 CSVs.

## Dimensionless coupling and Week-2 bands (frozen)

```
λ = g² / (2 t Ω)
```

With t=1 this is λ = g²/(2Ω). No spectral quantity enters the formula.

Week-2 bands (not Week-1 labels):

| band         | criterion                |
|--------------|--------------------------|
| weak         | λ < 0.08                 |
| intermediate | 0.08 ≤ λ < 0.80          |
| strong       | λ ≥ 0.80                 |

Preregistered λ and band (formula only; no |Δ| or A numbers):

| g/t  | Ω/t | λ = g²/(2 t Ω) | band         |
|------|-----|-----------------|--------------|
| 0.15 | 0.5 | 0.022500        | weak         |
| 0.15 | 0.8 | 0.0140625       | weak         |
| 0.15 | 2.0 | 0.005625        | weak         |
| 0.45 | 0.5 | 0.202500        | intermediate |
| 0.45 | 0.8 | 0.1265625       | intermediate |
| 0.45 | 2.0 | 0.050625        | weak         |
| 0.75 | 0.5 | 0.562500        | intermediate |
| 0.75 | 0.8 | 0.3515625       | intermediate |
| 0.75 | 2.0 | 0.140625        | intermediate |
| 1.05 | 0.5 | 1.102500        | strong       |
| 1.05 | 0.8 | 0.6890625       | intermediate |
| 1.05 | 2.0 | 0.275625        | intermediate |

Counts: 4 weak, 7 intermediate, 1 strong.

## Frozen spectral conventions (all four methods)

For every method X ∈ {ED, Born, SCBA64, SCBAgate},

```
A_X(ω) = −(1/π) Im G^R_X(k=0, ω + i η_A)
```

Do **not** mix ED's code array `spectral = −2 Im G` without converting.
Conversion, if that array is touched: A = spectral / (2π). All four A
share the retarded definition above.

Locks (PROJECT_CONVENTION; do not retune per cell):

- η_A = 0.05 t = 0.05 (broader than pole η=1e-4)
- ω grid = `np.linspace(-8.0, 4.0, 1601)`
- k = 0 only
- ξ_0 = 0

Diagrammatic Green (Born, SCBA64, SCBAgate):

```
G_X(k=0, z) = 1 / (z − ξ_0 − Σ_X(z)) = 1 / (z − Σ_X(z))
Σ_X(z) = rainbow_sigma(z, g, Ω, depth=d)   # l2_periodic_pole.py
```

Depths:

- Born: d = 0
- SCBA64: d = 64
- SCBAgate: d = `depth_gated` already recorded in
  `week3_gated_vs_fixed.csv` (classical residual r_n at z=0+iη_pole,
  θ_class=0.03). Do **not** retune θ. Do **not** use spectral error to
  choose depth. Do **not** recompute the residual scan to pick a new n.

ED Lehmann: `HolsteinL2ED` at `M_used` from `teacher_map_l2.csv`. Same
η_A and same ω grid. Same A definition.

E0 sources (windows only; not recomputed here):

- E0_ED, E0_Born, E0_SCBA64 from `teacher_map_l2.csv`
  (`E0_SCBA` is SCBA64)
- E0_SCBAgate from `week3_gated_vs_fixed.csv` column `E0_gated`

## Error metrics (definitions only; no numerical evaluation here)

Discrete L2 on the frozen 1601-point grid (numpy `linalg.norm`, no dω):

```
error_A(X) = ||A_X − A_ED||_2 / ||A_ED||_2
```

First moment on the frozen window [−8, 4], same grid, trapezoid:

```
M1_X = ∫ ω A_X(ω) dω / ∫ A_X(ω) dω
error_M1(X) = |M1_X − M1_ED| / Ω
```

If a denominator is non-finite or zero, fail closed (do not invent a
number; do not write NaN into error_A or error_M1).

Quasiparticle weight on this tiny grid, trapezoid, method-own pole:

```
QP window for Z_X = [E0_X − Ω, E0_X + 0.5 Ω]
Z_X = ∫_{ω ∈ QP window ∩ [−8,4]} A_X(ω) dω
```

Use frozen-grid points that fall in the closed window. No edge
interpolation. If fewer than two grid points lie in the window, or if
Z_X is negative, >2, or not finite (NaN/inf), write `NOT_COMPUTED` for
that cell/method and keep error_A and error_M1. Do not substitute a
Lehmann residue, a Σ-derivative residue, or an argmax.

Z is recorded. T1–T3 below use **error_A** only. Z and error_M1 are
companion observables, not stop criteria.

## Train / test split (Week-3 split; frozen)

TRAIN (not used to choose θ or depth in Candidate 1):

```
(0.15, 0.5), (0.15, 2.0), (0.45, 0.8),
(0.75, 0.5), (0.75, 2.0), (1.05, 0.5)
```

TEST (C1-T3 mean_test uses these six cells only):

```
(0.15, 0.8), (0.45, 0.5), (0.45, 2.0),
(0.75, 0.8), (1.05, 0.8), (1.05, 2.0)
```

The split is not revised after seeing spectral errors. θ_class remains
0.03 from Week 3. Spectral error is not an input to the gate.

## Tests T1–T3 (rules only; not evaluated in this file)

Pass/fail is reported later in `notes/C1_REPORT.md` from the analysis
CSV. This file does not evaluate T1–T3 and does not record a verdict.

T1 Structure: error_A(SCBA64) increases with λ (equivalently with g)
at each fixed Ω, and increases when Ω decreases at fixed g, at most
one recorded exception. Compare consecutive g in {0.15, 0.45, 0.75,
1.05} at each Ω, and consecutive Ω in decreasing {2.0, 0.8, 0.5} at
each g. Strict increase (`>`). Expected comparisons: 9 (g-up at fixed
Ω) + 8 (Ω-down at fixed g) = 17. Fail T1 if more than one comparison
violates. If T1 fails, write `notes/C1_STOP.md` and stop Candidate 1
(no network).

T2 Residual ≠ spectrum: there exists at least one cell where Week-3
`match_grain_ok` is true (gated E0 matches depth-64 versus ED to
1e-4 t) BUT error_A(SCBAgate) − error_A(SCBA64) exceeds 0.05, OR the
opposite (`match_grain_ok` false but
|error_A(SCBAgate) − error_A(SCBA64)| ≤ 0.05). If no such cell, write
“no extra spectral leftover on this grid”. T2 is a diagnostic. It is
not a license to train.

T3 Classical sufficiency: **PASS-SUFFICIENT** if
mean_test error_A(SCBAgate) ≤ mean_test error_A(SCBA64) + 0.05
AND no test cell is worse than SCBA64 by more than 0.10
(error_A_gate − error_A_64 ≤ 0.10 on every TEST cell).
**FAIL-SUFFICIENT** otherwise. FAIL-SUFFICIENT is NOT a license to
train; it only means “spectral leftover exists”. Then stop Candidate 1
with that sentence.

Stop Candidate 1 if T1 fails, OR if T3 is PASS-SUFFICIENT. Either way,
no network. If T3 is PASS-SUFFICIENT, say so in the report (stop
opening a spectral gate); do not train. Do not write a learned-gate
ticket.

## Analysis CSV (declared schema; not written yet)

Path: `prototypes/future_b_neural_poc/c1_spectral_vs_ed.csv`

Columns exactly:

```
g_over_t,omega_over_t,lambda,band,split,M_used,depth_gate,
error_A_Born,error_A_SCBA64,error_A_SCBAgate,
error_M1_Born,error_M1_SCBA64,error_M1_SCBAgate,
Z_ED,Z_Born,Z_SCBA64,Z_SCBAgate,note
```

Twelve data rows. `band` follows Week-2 cuts. `split` is `train` or
`test`. `depth_gate` is Week-3 `depth_gated`. `M_used` is the teacher
cutoff. Unstable Z is `NOT_COMPUTED`. error_A and error_M1 are finite
floats (no NaN). `E0_Born_VC` is not a column and is not invented.

## What this preregister does not authorize

- training a router, logistic, MLP, GRU, or any learned gate
- widening Week 4 features or changing θ to flip (0.75, 0.8)
- opening Weeks 7–8 architecture
- mixing Library I and Library II
- adding Σ_VC onto SCBA
- filling E_0^{Born+VC}
- changing η_pole, η_A, L, ξ_k, tadpole, SCBA_DEPTH, or the ω grid
  after seeing errors
- calling `chain_scba.py`
- using archive 11A, K4AI-592, or K4AI-593 as Future B proof
- treating `GENERIC_MODEL_SUFFICIENT` as a teacher-backed result
- claiming architecture, conservation, or Physics-for-AI
- enlarging the twelve-cell grid
- moving the split, λ cuts, or T3 tolerances after seeing errors
- using spectral error to choose rainbow depth
- setting `paper1_go` true
- editing `AGENT_LOG.md`, `holstein_ed.py`, or `l2_periodic_pole.py`

## Claim ceiling after a successful fill

Allowed, if the CSV and T1–T3 support it: on this frozen L=2 grid,
A(ω) versus ED Lehmann does or does not show structured error in λ,
and classical θ=0.03 does or does not already suffice on that
observable.

Not allowed: Physics-for-AI; a learned spectral gate; “Future B
succeeded”; Paper 1 GO.
