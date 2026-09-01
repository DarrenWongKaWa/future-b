# Candidate 2 report — MA(0) vs ED on the frozen L=2 map

Worker 2 (W2). Live extract `/Users/kawawong/Research/future-b`.
No new K4AI number. No merge to `main`. No learned gate, logistic,
MLP, or router. No Weeks 7–8. No \(\Sigma_{\mathrm{VC}}\) on SCBA.
`holstein_ed.py` and `l2_periodic_pole.py` were not edited.
Week-2/3/4 CSVs were not edited. `AGENT_LOG.md` was not edited.

Preregister `notes/C2_METRICS_PREREGISTER.md` and formula lock
`notes/C2_MA0_FORMULA.md` were written to disk **before**
`prototypes/future_b_neural_poc/c2_ma0_vs_ed.csv` and before this
report. The frozen \(\lambda\)-only chooser was not moved after
seeing \(E_0^{\mathrm{MA0}}\).

Question (now answered on this slice): can a fixed MA(0) block that
is not deeper SCBA cut \(|E_0-E_0^{\mathrm{ED}}|\) on the strong cell
enough that a classical class-choice among
\(\{\mathrm{Born},\mathrm{SCBA},\mathrm{MA0}\}\) is not just an
if-statement on \(\lambda\)?

## 0. Atomic \(t=0\) check

`MA0_ATOMIC = PASS` (12/12 frozen \((g,\Omega)\) cells at hop \(t=0\)).
\(G_{\mathrm{MA0}}(t=0)\) matches `exact_t0_linear_cfe` (coefficients
\(1,2,3,\ldots\)) to \(\sim 10^{-16}\) relative \(L^2\) on
\(z=i\nu\), \(\nu=\mathrm{geomspace}(0.1,20,128)\), depth 64.
SCBA / `scba_constant_cfe` (\(1,1,1,\ldots\)) remains farther from
the exact linear series. The linear CFE was **not** used as the
finite-\(t\) teacher block.

## 1. Tests C2-T1–T3

Source: `prototypes/future_b_neural_poc/c2_ma0_vs_ed.csv`
(12 rows; \(E_0^{\mathrm{ED}}\), \(E_0^{\mathrm{Born}}\),
\(E_0^{\mathrm{SCBA}}\) copied from
`prototypes/future_b_neural_poc/teacher_map_l2.csv`).
\(E_0^{\mathrm{MA0}}\) from
`prototypes/future_b_neural_poc/ma0_l2.py` (Berciu–Goodvin 2007
Eqs. (10)–(12); \(L=2\) discrete \(\bar g_0\); same pole window,
\(\eta\), and coarse grid as `l2_periodic_pole.py`).

| test | verdict | counts |
|------|---------|--------|
| C2-T1 strong-cell gain | **PASS** | \((1.05,0.5)\): \(\mathrm{rel}_{\mathrm{MA0}}=0.1285436067168423\le\mathrm{rel}_{\mathrm{SCBA}}-0.10=0.2735727642372323\); `MA0_ATOMIC=PASS` |
| C2-T2 not just the \(\lambda\) if-statement | **PASS** | count \(=3>0\) |
| C2-T3 physical signs | **PASS** | 12/12 cells have \(E_0^{\mathrm{MA0}}<0\); \(g=0\) pole is \(E_0^{\mathrm{MA0}}=0\) |

`notes/C2_STOP.md` was **not** written: T1 passed, so Candidate 2
does not stop on the strong-cell rule. No router was trained.

Strong cell \((g/t,\Omega/t)=(1.05,0.5)\), \(\lambda=1.1025\):

- \(E_0^{\mathrm{ED}}=-1.2711554105515426\)
- \(E_0^{\mathrm{Born}}=-0.6062574864800551\), \(\mathrm{rel}=0.523065801830631\)
- \(E_0^{\mathrm{SCBA}}=-0.7962863700566889\), \(\mathrm{rel}=0.37357276423723235\)
- \(E_0^{\mathrm{MA0}}=-1.1077565093816188\), \(\mathrm{rel}=0.1285436067168423\)

T1 gain versus SCBA: \(\mathrm{rel}_{\mathrm{SCBA}}-\mathrm{rel}_{\mathrm{MA0}}=0.24502915752039005\ge 0.10\).
MA0 still underbinds versus ED, but by much less than SCBA.

T2 cells (`best_block=ma0`, `lambda_if_block=scba`, gap
\(>0.05|E_0^{\mathrm{ED}}|\)):

| \(g/t\) | \(\Omega/t\) | \(\lambda\) | gap \(|E_0^{\mathrm{MA0}}-E_0^{\mathrm{SCBA}}|\) | gap \(/|E_0^{\mathrm{ED}}|\) |
|---------|--------------|-------------|--------------------------------------------------|------------------------------|
| 0.75    | 0.5          | 0.5625      | 0.07160768989514343                              | 0.11298938927716405          |
| 0.75    | 0.8          | 0.3515625   | 0.02882710003867406                              | 0.06960508136544767          |
| 1.05    | 0.8          | 0.6890625   | 0.10704309435583792                              | 0.13034050265581962          |

On this grid `best_block` is `ma0` in 12/12 cells. That 12/12 count
is **not** a T1–T3 success criterion except as it feeds T2. The
frozen \(\lambda\) chooser still returns `scba` on the eleven
non-strong cells; only three of those disagreements exceed the
preregistered \(0.05|E_0^{\mathrm{ED}}|\) gap. Weak-coupling MA0
versus SCBA gaps are smaller than that cut, so they do not count
as a T2 remainder.

T3: every \(g>0\) cell has \(E_0^{\mathrm{MA0}}<0\). Independent
\(g=0\) pole (`e0_ma0(g=0,\Omega=0.8)`) sits at \(0\).

## 2. Claim ceiling

classical class-choice has a non-\(\lambda\) remainder; human may open a later tiny gate.

This worker does **not** open that gate. No class router is trained.
This is not Weeks 7–8, not Physics-for-AI, and not a license to add
\(\Sigma_{\mathrm{VC}}\) onto SCBA.

## 3. What remains NOT_COMPUTED / closed

- \(E_0^{\mathrm{Born+VC}}\): still `NOT_COMPUTED` in all 12 teacher-map
  cells; not a C2 column.
- MA(1) / MA(2) (Berciu–Goodvin 2007 Eqs. (16) and (18)–(24)).
- Any learned gate, logistic, MLP, or router.
- Weeks 7–8 architecture bake-off.
- \(\Phi\), Keldysh, devices, 11A, DiagMC.
- \(\Sigma_{\mathrm{VC}}\) on SCBA (forbidden; default **NO**).
- `paper1_go` remains false; this file does not set it true.

SHA-256:

```
2139c1616dfe9d84b702c8aefcffd5b2c60f421d8bdff5bd9485ab6438d9d260  c2_ma0_vs_ed.csv
```
