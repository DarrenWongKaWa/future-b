# Candidate 2 metrics — preregistered before any twelve-cell \(E_0^{\mathrm{MA0}}\)

Authority: Future B Candidate 2 (Worker 2). Binding:
`notes/SCIENCE_LINE_60DAY.md`, `notes/CONSTRAINTS_FUTURE_B.md`,
`notes/L2_POLE_DEFINITION.md`. Formula lock:
`notes/C2_MA0_FORMULA.md`.

This file is written **before** any twelve-cell \(E_0^{\mathrm{MA0}}\)
is computed, **before**
`prototypes/future_b_neural_poc/c2_ma0_vs_ed.csv`, and **before**
`notes/C2_REPORT.md`. Tests C2-T1–T3 are **rules only**. This file
does not evaluate them and does not contain PASS/FAIL numbers for
those tests.

Question (not a result): can a fixed MA(0) block that is **not**
deeper SCBA cut \(|E_0-E_0^{\mathrm{ED}}|\) on the strong cell enough
that a classical class-choice among \(\{\mathrm{Born},\mathrm{SCBA},\mathrm{MA0}\}\)
is not just an if-statement on \(\lambda\)?

## Frozen slice (not enlarged)

- \(t=1\)
- \(g/t\in\{0.15,0.45,0.75,1.05\}\)
- \(\Omega/t\in\{0.5,0.8,2.0\}\)
- twelve cells
- periodic \(L=2\), momenta \(\{k=0,k=\pi\}\)
- \(\xi_k=2t(1-\cos k)\), so \(\xi_0=0\), \(\xi_\pi=4t\), \(E_0(g=0)=0\)
- tadpole / Hartree **OFF**
- Library I and Library II remain separate
- default **NO** \(\Sigma_{\mathrm{VC}}\) on SCBA
- no \(\Sigma_{\mathrm{Born}}+\Sigma_{\mathrm{VC}}\), no
  \(\Sigma_{\mathrm{SCBA}}+\Sigma_{\mathrm{VC}}\), no neural \(\Sigma\)
- MA(0) is its **own** module, not mixed into SCBA or Library I
- 11A unused; Weeks 7–8 not opened; no learned gate, logistic, MLP,
  or router

Immutable teacher input (not recomputed):
`prototypes/future_b_neural_poc/teacher_map_l2.csv`.
\(E_0^{\mathrm{ED}}\), \(E_0^{\mathrm{Born}}\), and
\(E_0^{\mathrm{SCBA}}\) are **copied**. \(E_0^{\mathrm{Born+VC}}\)
stays `NOT_COMPUTED`.

Pole convention for \(E_0^{\mathrm{MA0}}\) is the same as
`notes/L2_POLE_DEFINITION.md`: lowest interior
\(\operatorname{Re} D(\omega)=0\) of \(G(k=0)\), \(\eta=10^{-4}\),
window \([-8.0,0.25]\), coarse grid `np.linspace(-8.0, 0.25, 16501)`.
Do not retune \(\eta\), the window, or the grid after seeing
\(E_0^{\mathrm{MA0}}\). Import those locks from
`l2_periodic_pole.py`.

## Dimensionless coupling (formula of \((g,\Omega,t)\) only)

```
λ = g² / (2 t Ω)
```

With \(t=1\) this is \(\lambda=g^2/(2\Omega)\). No energy, residual,
or pole-search quantity enters the formula.

## Bands (Week-2 cuts, restated, not refit)

| band         | criterion                    |
|--------------|------------------------------|
| weak         | \(\lambda < 0.08\)           |
| intermediate | \(0.08 \le \lambda < 0.80\)  |
| strong       | \(\lambda \ge 0.80\)         |

Strong cell is the unique \((g/t,\Omega/t)=(1.05,0.5)\),
\(\lambda=1.1025\).

Preregistered \(\lambda\) and band (no \(|\Delta|\) numbers):

| \(g/t\) | \(\Omega/t\) | \(\lambda=g^2/(2t\Omega)\) | band         |
|---------|--------------|----------------------------|--------------|
| 0.15    | 0.5          | 0.022500                   | weak         |
| 0.15    | 0.8          | 0.0140625                  | weak         |
| 0.15    | 2.0          | 0.005625                   | weak         |
| 0.45    | 0.5          | 0.202500                   | intermediate |
| 0.45    | 0.8          | 0.1265625                  | intermediate |
| 0.45    | 2.0          | 0.050625                   | weak         |
| 0.75    | 0.5          | 0.562500                   | intermediate |
| 0.75    | 0.8          | 0.3515625                  | intermediate |
| 0.75    | 2.0          | 0.140625                   | intermediate |
| 1.05    | 0.5          | 1.102500                   | strong       |
| 1.05    | 0.8          | 0.6890625                  | intermediate |
| 1.05    | 2.0          | 0.275625                   | intermediate |

Counts: 4 weak, 7 intermediate, 1 strong.

## Frozen \(\lambda\)-only classical chooser (the if-statement on \(\lambda\))

Written here **before** any \(E_0^{\mathrm{MA0}}\). The chooser does
not see Born/SCBA/MA0 residuals.

```
if λ < 0.08:            SCBA
if 0.08 ≤ λ < 0.80:     SCBA
if λ ≥ 0.80:            MA0
```

CSV token `lambda_if_block` is lowercase `scba` or `ma0`.
On this grid that is `scba` on eleven cells and `ma0` only on the
strong cell \((1.05,0.5)\). Born is never selected by this \(\lambda\)
rule. The chooser is not trained and is not a router.

## Metrics (definitions only; no numerical evaluation here)

For \(X\in\{\mathrm{Born},\mathrm{SCBA},\mathrm{MA0}\}\):

```
rel_X = |E0_X − E0_ED| / |E0_ED|
```

`best_block` = \(\mathrm{argmin}_X |E0_X-E0_{ED}|\) among
\(\{\mathrm{Born},\mathrm{SCBA},\mathrm{MA0}\}\), written lowercase
`born` / `scba` / `ma0`. If two absolute errors are numerically equal,
the earlier name in that ordered triple wins. If `E0_MA0` is
`NOT_COMPUTED`, drop MA0 from the argmin; `best_block` cannot be
`ma0`.

`lambda_if_block` is the frozen \(\lambda\) rule above.

No new observables. No spectra. No learned class gate.

## Atomic \(t=0\) check (not a teacher \(E_0\))

At hop \(t=0\), MA(0) must move toward the exact atomic continued-
fraction coefficients \(1,2,3,\ldots\); SCBA moves toward
\(1,1,1,\ldots\). Executable reference:
`src/keldysh4ai/future_b_atomic.py` (`exact_t0_linear_cfe`,
`scba_constant_cfe`). Grid: \(z=i\nu\),
\(\nu=\mathrm{geomspace}(0.1,20,128)\), depth 64, frozen
\((g,\Omega)\) list.

```
MA0_ATOMIC = PASS
  iff on every frozen (g, Ω) cell at t=0,
      relL2(G_MA0, G_exact_linear) < relL2(G_SCBA, G_exact_linear).
Otherwise MA0_ATOMIC = FAIL.
```

This check may be run before the twelve-cell table. It is not a
twelve-cell \(E_0^{\mathrm{MA0}}\). If `MA0_ATOMIC = FAIL`, do not
treat MA0 as a teacher-side winner: still report `E0_MA0` if poles
exist, but C2-T1 cannot pass as a physical win.

## Tests C2-T1–T3 (rules only; not evaluated in this file)

Pass/fail is reported later in `notes/C2_REPORT.md` from
`c2_ma0_vs_ed.csv` plus the atomic check. This file does not
evaluate T1–T3 and must not be edited after seeing \(E_0^{\mathrm{MA0}}\)
to record a pass/fail verdict.

C2-T1 Strong-cell gain: on \((1.05,0.5)\),
`rel_MA0 ≤ rel_SCBA − 0.10`. Requires a real `E0_MA0` (not
`NOT_COMPUTED`) and `MA0_ATOMIC = PASS`. If this fails: Candidate 2
STOPS. Write `notes/C2_STOP.md`. No routing.

C2-T2 Not just the if-statement: count cells where
`best_block ≠ lambda_if_block` **and** the absolute-energy gap
between those two blocks exceeds \(0.05|E0_{ED}|\), i.e.
\(|E0_{\mathrm{best}}-E0_{\lambda\text{-if}}| > 0.05|E0_{ED}|\).
If `E0_MA0` is missing on a cell, that cell cannot count as a MA0
remainder. If the count is 0: class-choice is a \(\lambda\)
if-statement. STOP. Do not learn a router. If T1 already failed,
still report the T2 count, but Candidate 2 is already stopped.

C2-T3 Physical signs: `E0_MA0 < 0` for every \(g>0\) cell with a
real pole, and \(g=0\) gives `E0_MA0=0`. Fail = implementation
error, STOP Candidate 2.

Do **not** train a class router even if T1 and T2 pass. If both
pass, the allowed later sentence is only: “classical class-choice has
a non-\(\lambda\) remainder; human may open a later tiny gate.”
This worker does not open it.

## Analysis CSV (declared schema; not written yet)

Path: `prototypes/future_b_neural_poc/c2_ma0_vs_ed.csv`

Columns exactly:

```
g_over_t,omega_over_t,lambda,band,E0_ED,E0_Born,E0_SCBA,E0_MA0,rel_Born,rel_SCBA,rel_MA0,best_block,lambda_if_block,note
```

`band` from the Week-2 cuts above. `E0_ED`, `E0_Born`, `E0_SCBA`
must equal the teacher-map values. If `E0_MA0` is missing, write
`NOT_COMPUTED` in `E0_MA0` and `rel_MA0`. `E0_Born_VC` is not a
column and is not invented.

## What this preregister does not authorize

- a learned gate, logistic, MLP, or router
- Weeks 7–8 architecture bake-off
- \(\Phi\), Keldysh, devices, 11A, DiagMC
- adding \(\Sigma_{\mathrm{VC}}\) onto SCBA
- \(\Sigma_{\mathrm{Born}}+\Sigma_{\mathrm{VC}}\) or neural \(\Sigma\)
- Physics-for-AI
- inventing numbers; missing values are `NOT_COMPUTED`
- editing week2 / week3 / week4 CSVs
- setting `paper1_go` true
- editing `holstein_ed.py` or `l2_periodic_pole.py`
- mixing MA(0) into SCBA or Library I
- using the atomic \(1,2,3,\ldots\) CFE as the finite-\(t\) block
  (it is the \(t\to 0\) check only)
- moving \(\lambda\) cuts or the \(\lambda\) chooser after seeing
  \(E_0^{\mathrm{MA0}}\)
