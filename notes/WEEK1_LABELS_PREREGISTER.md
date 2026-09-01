# Week 1 labels — preregistered before the L=2 teacher table

Authority: HUMAN LOCK 2026-08-31 (notes/SCIENCE_LINE_60DAY.md Week 1:
"Weak/intermediate labels, any split, and all comparison conventions
must be declared before looking at the completed table.").

This file is written **before** any inspection or generation of
`prototypes/future_b_neural_poc/teacher_map_l2.csv` and **before** any
`E0_ED` values for the twelve frozen cells are read from a teacher
table. Labels depend only on `(g, Ω, t)`. They are not fitted to
energies, cutoffs, or diagrammatic residuals.

## Frozen slice (not enlarged)

- `t = 1`
- `g/t ∈ {0.15, 0.45, 0.75, 1.05}`
- `Ω/t ∈ {0.5, 0.8, 2.0}`
- twelve cells

Energy origin (already frozen; restated, not reopened):

- `ξ_k = 2t(1 − cos k)` so `E0(g=0) = 0`
- translator: `E_lecture = E_code − 2t`

## Dimensionless coupling (formula of `(g, Ω, t)` only)

The 1D Holstein dimensionless coupling on a chain of bandwidth
`W = 4t` is

```
λ = 2 g² / (W Ω) = g² / (2 t Ω)
```

With `t = 1` this is `λ = g² / (2 Ω)`. No other parameter (including
`E0`) enters the formula.

## Label thresholds (declared before the table)

On this slice only:

| label        | criterion        |
|--------------|------------------|
| weak         | `λ < 0.2`        |
| intermediate | `0.2 ≤ λ < 1.0`  |
| strong       | `λ ≥ 1.0`        |

These cuts are a **PROJECT_CONVENTION** for Week 1 reporting on the
frozen twelve-cell grid. They are not a scientific claim about the
Holstein phase diagram and are not architecture evidence.

## Preregistered labels for all twelve cells

Computed from the formula above (no energies):

| g/t  | Ω/t | λ = g²/(2 t Ω) | label        |
|------|-----|----------------|--------------|
| 0.15 | 0.5 | 0.022500       | weak         |
| 0.15 | 0.8 | 0.0140625      | weak         |
| 0.15 | 2.0 | 0.005625       | weak         |
| 0.45 | 0.5 | 0.202500       | intermediate |
| 0.45 | 0.8 | 0.1265625      | weak         |
| 0.45 | 2.0 | 0.050625       | weak         |
| 0.75 | 0.5 | 0.562500       | intermediate |
| 0.75 | 0.8 | 0.3515625      | intermediate |
| 0.75 | 2.0 | 0.140625       | weak         |
| 1.05 | 0.5 | 1.102500       | strong       |
| 1.05 | 0.8 | 0.6890625      | intermediate |
| 1.05 | 2.0 | 0.275625       | intermediate |

Counts: 6 weak, 5 intermediate, 1 strong.

## Comparison conventions (also declared before the table)

1. `E0_ED` comes from `src/keldysh4ai/future_b/teacher/holstein_ed.py`
   (periodic L=2, signed Hamiltonian, total-phonon cutoff).
2. For each cell the cutoff `M_used` is the smallest even
   `M ∈ {0, 2, …, 20}` (higher only if a cell fails at `M = 20`) with
   `|E0(M) − E0(M−2)| < 1e-4 t`. `dim = (M+1)(M+2)`.
3. `E0_Born`, `E0_SCBA`, and `E0_Born_VC` are reported only if they
   can be evaluated on the **same** energy origin and the **same**
   periodic L=2 geometry. Otherwise the literal token `NOT_COMPUTED`
   is written. Open-chain SCBA energies are not L=2 teacher numbers.
4. Library I (bare Born + bare VC on `G0`) and Library II (SCBA on
   dressed `G`) stay in separate folders. Default: **do not** add
   `Σ_VC` onto SCBA.
5. Tadpole/Hartree remains OFF in the diagrammatic libraries; the ED
   Hamiltonian still contains `g n (b + b†)`.
6. Labels above will not be revised after the teacher table is
   generated.

## What this preregister does not authorize

- training a router or MLP
- mixing Library I and Library II
- using archive 11A, K4AI-592, or K4AI-593 as Future B proof
- treating `GENERIC_MODEL_SUFFICIENT` as a teacher-backed result
- enlarging the twelve-cell grid
