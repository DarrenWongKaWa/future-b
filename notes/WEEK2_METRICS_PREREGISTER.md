# Week 2 metrics — preregistered before the Born/SCBA vs ED delta table

Authority: HUMAN LOCK 2026-08-31 plus the Week 2 Science prompt
(Worker S). Binding constraints:
`notes/CONSTRAINTS_FUTURE_B.md`. Sequence and claim-ceiling language
in `notes/SCIENCE_LINE_60DAY.md` remain in force except that the Week 2
**question** is the corrected pair below, not the older sentence in
that file.

This file is written **before**
`prototypes/future_b_neural_poc/week2_born_scba_vs_ed.csv` and **before**
`notes/WEEK2_REPORT.md`. Metrics, bands, and tests T1–T4 depend only
on the formulas of $(g,\Omega,t)$ and on the signed definitions of
$\Delta_X$ and $\mathrm{rel}_X$. They are not fitted to
$|\Delta|$ values. Cuts will not be moved after seeing errors.

Week 2 is **analysis of the existing 12-cell map**. It does not rerun
L=2 ED, train a gate, change $\eta$, $L$, dispersion, or tadpole,
call `chain_scba.py`, edit `holstein_ed.py` or `l2_periodic_pole.py`,
or invent $E_0^{\mathrm{Born+VC}}$. It does not start Week 3.

## Corrected Week 2 questions (binding)

1. At weak $\lambda$, is SCBA closer to ED than one-shot Born?
2. At strong / adiabatic $\lambda$, does SCBA lose accuracy versus
   ED (not versus Born)?

Do **not** force the sentence “SCBA becomes worse than Born at strong
coupling.” Ranking SCBA against Born at large $\lambda$ is not a
success criterion. T1–T4 below remain the tests.

## Frozen slice and signed conventions (not reopened)

- $t = 1$
- $g/t \in \{0.15, 0.45, 0.75, 1.05\}$
- $\Omega/t \in \{0.5, 0.8, 2.0\}$
- twelve cells
- $\xi_k = 2t(1-\cos k)$, so $E_0(g=0)=0$
- translator $E_{\mathrm{lecture}}=E_{\mathrm{code}}-2t$
- tadpole / Hartree OFF in diagrammatic libraries
- Library I and Library II remain separate
- default **NO** $\Sigma_{\mathrm{VC}}$ on SCBA
- 11A unused
- ED green $\neq$ architecture
- $E_0^{\mathrm{Born+VC}}$ stays `NOT_COMPUTED`

Immutable input: `prototypes/future_b_neural_poc/teacher_map_l2.csv`
at teacher-map commit `e6a14f6`. Those $E_0$ values are not
recomputed here.

## Dimensionless coupling (formula of $(g,\Omega,t)$ only)

```
λ = g² / (2 t Ω)
```

With $t=1$ this is $\lambda = g^2/(2\Omega)$. No energy, residual,
or pole-search quantity enters the formula.

## Bands (frozen now; Week 2 only)

These cuts **replace** the Week-1 label cuts for Week 2 only. They do
not edit `notes/WEEK1_LABELS_PREREGISTER.md`.

| band         | criterion        |
|--------------|------------------|
| weak         | $\lambda < 0.08$ |
| intermediate | $0.08 \le \lambda < 0.80$ |
| strong       | $\lambda \ge 0.80$ |

This puts $(g/t,\Omega/t)=(1.05,0.5)$, $\lambda=1.1025$, in
**strong**. Cuts are a PROJECT_CONVENTION on this twelve-cell slice.
They are not a Holstein phase-diagram claim and not architecture
evidence.

## Preregistered $\lambda$ and band for all twelve cells

Computed from the formula above (no $|\Delta|$ numbers):

| g/t  | Ω/t | $\lambda = g^2/(2 t \Omega)$ | band         |
|------|-----|-------------------------------|--------------|
| 0.15 | 0.5 | 0.022500                      | weak         |
| 0.15 | 0.8 | 0.0140625                     | weak         |
| 0.15 | 2.0 | 0.005625                      | weak         |
| 0.45 | 0.5 | 0.202500                      | intermediate |
| 0.45 | 0.8 | 0.1265625                     | intermediate |
| 0.45 | 2.0 | 0.050625                      | weak         |
| 0.75 | 0.5 | 0.562500                      | intermediate |
| 0.75 | 0.8 | 0.3515625                     | intermediate |
| 0.75 | 2.0 | 0.140625                      | intermediate |
| 1.05 | 0.5 | 1.102500                      | strong       |
| 1.05 | 0.8 | 0.6890625                     | intermediate |
| 1.05 | 2.0 | 0.275625                      | intermediate |

Counts: 4 weak, 7 intermediate, 1 strong.

Weak cells ($\lambda<0.08$): $(0.15,0.5)$, $(0.15,0.8)$,
$(0.15,2.0)$, $(0.45,2.0)$.

Strong cell: $(1.05,0.5)$ only.

## Metrics (definitions only; no numerical evaluation here)

For $X\in\{\mathrm{Born},\mathrm{SCBA}\}$:

```
Δ_X   = E0_X − E0_ED          (positive = underbinding)
rel_X = |Δ_X| / |E0_ED|
scba_beats_born = true  iff  |Δ_SCBA| < |Δ_Born|
```

`scba_beats_born` is recorded as lowercase `true`/`false`. It is a
descriptive column, not a Week-2 success criterion except as used by
T1 on the weak cells.

No new observables. No spectra unless T4 fails.

## Tests T1–T4 (rules only; not evaluated in this file)

Copied from the Week 2 Science prompt. Pass/fail is reported later in
`notes/WEEK2_REPORT.md` from the analysis CSV. This file does not
evaluate T1–T4.

T1 Weak-coupling sanity: on every cell with λ<0.08, |Δ_SCBA| < |Δ_Born|. Fail Week 2 if any weak cell violates.
T2 Strong-coupling accuracy collapse versus ED: on the strong cell (1.05, 0.5), rel_SCBA ≥ 0.20. This is “SCBA loses at strong coupling” versus ED, NOT “SCBA worse than Born”.
T3 Monotone structure: rel_SCBA should increase when λ increases at fixed Ω, and when Ω decreases at fixed g, with at most one minor exception recorded as a note, not a rescue sweep.
T4 Physical signs: for g>0, E0_ED < E0_SCBA < E0_Born < 0. Fail if any cell violates unless a documented pole-search miss.

If T1 or T4 fails: write `notes/WEEK2_STOP.md` and do not soften
thresholds. Do not write the claim-ceiling sentence.

T2 fail does not by itself require `WEEK2_STOP.md` unless T1 or T4
also fails. T3 may have at most one minor exception as a note.

## Analysis CSV (declared schema; not written yet)

Path: `prototypes/future_b_neural_poc/week2_born_scba_vs_ed.csv`

Columns exactly:

```
g_over_t,omega_over_t,lambda,band,E0_ED,E0_Born,E0_SCBA,
delta_Born,delta_SCBA,rel_Born,rel_SCBA,scba_beats_born,note
```

`band` $\in \{\mathrm{weak},\mathrm{intermediate},\mathrm{strong}\}$
from the Week-2 cuts above, **not** from Week-1 labels. `E0_*` columns
must equal the teacher-map values. `E0_Born_VC` is not a column and is
not invented.

## What this preregister does not authorize

- training a router, MLP, or GRU
- starting Week 3 classical gating
- mixing Library I and Library II
- adding $\Sigma_{\mathrm{VC}}$ onto SCBA
- filling $E_0^{\mathrm{Born+VC}}$
- changing $\eta$, $L$, $\xi_k$, tadpole, or the pole extractor
- calling `chain_scba.py`
- using archive 11A, K4AI-592, or K4AI-593 as Future B proof
- treating `GENERIC_MODEL_SUFFICIENT` as a teacher-backed result
- claiming architecture, conservation, or Physics-for-AI
- enlarging the twelve-cell grid
- moving the $\lambda$ cuts after seeing errors
