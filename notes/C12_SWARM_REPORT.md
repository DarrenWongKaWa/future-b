# Candidate 1+2 joint closeout — Worker 3 (W3)

Live extract `/Users/kawawong/Research/future-b`. No new K4AI number.
No merge to `main`. No training. No Week-4 repair. No \(\Sigma_{\mathrm{VC}}\)
on SCBA. `paper1_go` stays false. This swarm does **not** open a tiny gate.

Neither Template A nor Template B applies: C1-T3 is PASS-SUFFICIENT
(no spectral leftover that survives \(\theta=0.03\); T1 even failed
monotone) **and** C2-T1 PASSES. The public sentence below is the mixed
weaker form. It is not an upgrade.

## Candidate 1

After the Week-3 \(\Sigma\)-residual at \(z=0+i\eta\) failed to mark a
one-layer \(E_0\) error, Candidate 1 asked whether discrete-\(L^2\)
\(A(\omega)\) versus ED Lehmann still shows structured error in
\(\lambda\), and whether classical \(\theta=0.03\) already suffices on
that observable. Source:
`prototypes/future_b_neural_poc/c1_spectral_vs_ed.csv` (12 rows;
SHA-256 `4632a573366e9724ff0c33983ac89ae84fb47f6e61420290e7a764253ea2049f`).
Rules: `notes/C1_METRICS_PREREGISTER.md`. Evaluation:
`notes/C1_REPORT.md`. Stop file: `notes/C1_STOP.md` (written because T1
failed). No spectral learned gate was trained.

| test | verdict | counts |
|------|---------|--------|
| C1-T1 Structure | **FAIL** | 15/17 monotone in `error_A(SCBA64)`; 2 exceptions, both involving \((1.05,0.5)\): fixed \(\Omega=0.5\), \(g=0.75\to 1.05\) (`1.2736098120802806 !< 0.9863172923173602`); fixed \(g=1.05\), \(\Omega=0.8\to 0.5\) (`1.4156798290239707 !< 0.9863172923173602`) |
| C1-T2 Residual \(\neq\) spectrum | no extra spectral leftover on this grid | 0/12 leftover cells; 12/12 `match_grain_ok=true`; no cell with `error_A(gate)−error_A(64)>0.05` |
| C1-T3 Classical sufficiency | **PASS-SUFFICIENT** | mean_test `error_A(SCBAgate)=0.5474091752020821` versus `error_A(SCBA64)=0.5469474366582046` (gap \(\approx 4.6\times 10^{-4}\le 0.05\)); worst test gap \(\approx 0.002176\le 0.10\) |

Stop Candidate 1: T1 fail **and** T3 PASS-SUFFICIENT. Thresholds were
not softened. The metric was not moved onto \(Z\) or \(M_1\). \(\theta\)
was not retuned. Next human action on Candidate 1: **none**.

## Candidate 2

Candidate 2 asked whether a fixed MA(0) block that is not deeper SCBA
can cut \(|E_0-E_0^{\mathrm{ED}}|\) on the strong cell enough that a
classical class-choice among \(\{\mathrm{Born},\mathrm{SCBA},\mathrm{MA0}\}\)
is not just an if-statement on \(\lambda\). Formula lock:
`notes/C2_MA0_FORMULA.md` (Berciu–Goodvin 2007 Eqs. 10–12; \(L=2\)
discrete \(\bar g_0\)). Rules: `notes/C2_METRICS_PREREGISTER.md`.
Source: `prototypes/future_b_neural_poc/c2_ma0_vs_ed.csv` (12 rows;
SHA-256 `2139c1616dfe9d84b702c8aefcffd5b2c60f421d8bdff5bd9485ab6438d9d260`).
Executable: `prototypes/future_b_neural_poc/ma0_l2.py`. Evaluation:
`notes/C2_REPORT.md`. `notes/C2_STOP.md` was **not** written (T1
passed). No router was trained. `MA0_ATOMIC=PASS` (12/12 \(t=0\) cells).

| test | verdict | counts |
|------|---------|--------|
| C2-T1 Strong-cell gain | **PASS** | \((1.05,0.5)\): `rel_MA0=0.1285436067168423` \(\le\) `rel_SCBA−0.10=0.2735727642372323`. \(E_0^{\mathrm{MA0}}=-1.1077565093816188\) vs \(E_0^{\mathrm{SCBA}}=-0.7962863700566889\) vs \(E_0^{\mathrm{ED}}=-1.2711554105515426\) |
| C2-T2 Not just the \(\lambda\) if-statement | **PASS** | 3 remainder cells (`best_block=ma0`, `lambda_if_block=scba`, gap \(>0.05|E_0^{\mathrm{ED}}|\)): \((0.75,0.5)\), \((0.75,0.8)\), \((1.05,0.8)\) |
| C2-T3 Physical signs | **PASS** | 12/12 cells have \(E_0^{\mathrm{MA0}}<0\); \(g=0\) pole is \(0\) |

The frozen \(\lambda\)-only chooser still returns `scba` on eleven
non-strong cells. Weak-coupling MA0-versus-SCBA gaps below the
preregistered cut do not count as T2 remainder. This swarm does not
train a class router.

## What remains NOT_COMPUTED / closed

- \(E_0^{\mathrm{Born+VC}}\): still `NOT_COMPUTED` in all 12 teacher-map
  cells; not a C1 or C2 column.
- \(L=4\) (and any \(L\neq 2\)).
- Learned gates, logistic, MLP, GRU, or router (none trained here).
- \(\Phi\), Keldysh, devices, DiagMC, 11A.
- Weeks 7–8 architecture bake-off (not opened).
- MA(1) / MA(2).
- \(\Sigma_{\mathrm{VC}}\) on SCBA (forbidden; default **NO**).
- `paper1_go` remains false (`week4_verdict.csv`; SHA-256
  `ed47daaea831e80959870663b91c7e296afbe4809f1dd6395b221d36b778ed8f`).

Pinned first-slice CSVs (unchanged by this closeout):

```
a65dcde29457de0d3935b01f48693d8febb6042749c40fa65e315679d65f836a  teacher_map_l2.csv
73d7ccc625323c6372ea7aba95a850d589c72aaa48f899005cec02d8435303f4  week2_born_scba_vs_ed.csv
19d66c8a0f0c9c931ea02b67cb274f7cbe3cd1b8a78e7d1e996f05164e7d8d20  week3_gated_vs_fixed.csv
```

## Allowed public sentence

On this L=2 slice, classical θ=0.03 already matches depth-64 SCBA on A(ω) (no spectral leftover; Candidate 1 stops). MA(0) cuts the strong-cell E0 error versus SCBA by the declared margin and a λ-only chooser misses three remainder cells. No learned gate was trained. paper1_go stays false.

Do not upgrade this to Template A (C2-T1 did not fail) or Template B
(C1 leftover does not exist). Do not say architecture verified.

## Files changed / files refused

Changed in this W3 closeout:

- `notes/C12_SWARM_REPORT.md` (this file)
- `AGENT_LOG.md` (short append)
- `notes/LIVE_MANIFEST.md` (list C1/C2 artifacts)
- `tests/test_c12_swarm.py` (existence + `paper1_go` still false)

Refused:

- week2 / week3 / week4 CSVs (not edited)
- `holstein_ed.py`, `l2_periodic_pole.py`
- `notes/SCIENCE_LINE_60DAY.md` week plan
- setting `paper1_go` true
- training a router or spectral / class gate
- repairing Week 4
- adding \(\Sigma_{\mathrm{VC}}\) onto SCBA
- writing `notes/C2_STOP.md` (T1 passed; stop file would be a false stop)
- parent worktree, merge to Keldysh4ai `main`, new K4AI IDs, Weeks 7–8
- filling \(E_0^{\mathrm{Born+VC}}\), \(L=4\), \(\Phi\), Keldysh,
  devices, DiagMC

C1/C2 compute artifacts already on disk (not rewritten here):
`notes/C1_METRICS_PREREGISTER.md`, `notes/C1_REPORT.md`,
`notes/C1_STOP.md`, `prototypes/future_b_neural_poc/c1_spectral.py`,
`prototypes/future_b_neural_poc/c1_spectral_vs_ed.csv`,
`tests/test_c1_spectral.py`, `notes/C2_METRICS_PREREGISTER.md`,
`notes/C2_MA0_FORMULA.md`, `notes/C2_REPORT.md`,
`prototypes/future_b_neural_poc/ma0_l2.py`,
`prototypes/future_b_neural_poc/c2_ma0_vs_ed.csv`,
`tests/test_c2_ma0.py`.

## Next human action

None on Candidate 1.

On Candidate 2: classical class-choice has a non-\(\lambda\) remainder;
human may open a later tiny gate. The swarm does **not** open it.
A later question needs a new preregister in this repo.
