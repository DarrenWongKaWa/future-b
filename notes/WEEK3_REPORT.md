# Week 3 report — classical SCBA stopping on the frozen L=2 map

Worker S (Science). Extract `/Users/kawawong/Research/future-b`.
No new K4AI number. No merge to `main`. No edit of `holstein_ed.py`
or `l2_periodic_pole.py`. No router training in this week.

Preregister `notes/WEEK3_METRICS_PREREGISTER.md` was on disk **before**
`week3_depth_scan.csv`, `week3_gated_vs_fixed.csv`,
`week3_theta_selection.csv`, and this report. \(\theta_{\mathrm{class}}\)
was chosen only on the declared train split.

## 1. Tests T1–T6

Source: `prototypes/future_b_neural_poc/week3_gated_vs_fixed.csv`
and `week3_theta_selection.csv`. Depth-64 poles equal teacher-map
`E0_SCBA` (T1).

| test | verdict | counts |
|------|---------|--------|
| T1 same-origin lock | **PASS** | 12/12 depth-64 \(E_0\) equal teacher `E0_SCBA` |
| T2 train matching | **PASS** | 6/6 train cells; \(\theta_{\mathrm{class}}=0.03\) |
| T3 test matching | **PASS** | 6/6 test cells; \(\theta\) not retuned |
| T4 cost | **PASS** | mean test depth \(2.166\ldots<64\); mean `n_green_gated_total` \(104520.66\ldots<2145130\) |
| T5 structure | **PASS** | 17/17 comparisons; 0 exceptions |
| T6 physical signs | **PASS** | 12/12 have \(E_0^{\mathrm{ED}}<E_0^{\mathrm{gated}}<0\) |

`notes/WEEK3_STOP.md` was **not** written. Thresholds were not softened.

## 2. Selected gate and cost

Train-only rule: largest grid \(\theta\) such that every train cell
satisfies \(|\Delta_{\mathrm{gated}}|\le|\Delta_{\mathrm{fixed}}|+10^{-4}t\).

- \(\theta_{\mathrm{class}}=0.03\)
- admissible: true
- deployable residual: \(r_n=|\Sigma^{(n)}-\Sigma^{(n-1)}|/|\Sigma^{(n)}|\)
  at \(z_{\mathrm{diag}}=0+i\eta\)

| split | mean `depth_gated` | mean `depth_oracle` | mean `n_green_gated_total` | `n_green_fixed` |
|-------|--------------------|---------------------|----------------------------|-----------------|
| train | 2.5 | — | — | 2145130 |
| test | 2.1666… | 2.0 | 104520.66… | 2145130 |

Per-cell gated depths (train/test as preregistered):

| \(g/t\) | \(\Omega/t\) | split | `depth_gated` | `depth_oracle` |
|---------|--------------|-------|---------------|----------------|
| 0.15 | 0.5 | train | 1 | 1 |
| 0.15 | 0.8 | test | 1 | 1 |
| 0.15 | 2.0 | train | 1 | 1 |
| 0.45 | 0.5 | test | 2 | 2 |
| 0.45 | 0.8 | train | 2 | 2 |
| 0.45 | 2.0 | test | 1 | 1 |
| 0.75 | 0.5 | train | 4 | 3 |
| 0.75 | 0.8 | test | 3 | 3 |
| 0.75 | 2.0 | train | 2 | 2 |
| 1.05 | 0.5 | train | 5 | 4 |
| 1.05 | 0.8 | test | 4 | 3 |
| 1.05 | 2.0 | test | 2 | 2 |

Fixed-maximum SCBA is depth 64. The classical gate stops at depth 1–5
and keeps ED error within the declared grain of the depth-64 rainbow.
Extra inner work is structured in \((g,\Omega)\): depth rises with \(g\)
at fixed \(\Omega\) and falls as \(\Omega\) rises at fixed \(g\).

The leftover versus the ED oracle is one extra rainbow layer on three
cells, of which one is held-out: \((1.05,0.8)\). Mean test oracle depth
\(2.0<2.166\ldots\), so `leftover_decision=true` under the preregistered
rule. That gap is small. It is still a leftover decision.

## 3. Claim ceiling

On the frozen periodic L=2 slice, a classical adaptive stopping rule
improves the error–cost behavior of SCBA versus ED relative to
fixed-maximum depth 64. This is not neural, not a learned gate, and
not Physics-for-AI.

## 4. What remains NOT_COMPUTED

- \(E0_{\mathrm{Born+VC}}\): still `NOT_COMPUTED` in all 12 cells
- any learned gate, router, MLP, or GRU (Week 4 may start only because
  leftover_decision is true)
- \(L\neq 2\), open-chain energies, \(\Sigma_{\mathrm{VC}}\) on SCBA
- architecture, conservation, or Physics-for-AI evidence
- archive 11A, K4AI-592, and K4AI-593 as live Future B proof

## 5. Week 4 is opened, narrowly

Week 4 is allowed because the preregistered leftover rule fired, not
because the residual gate failed. The classical gate already captures
almost all of the depth-64 cost. A learned gate has to beat
\(\theta=0.03\) after cost, on deployable features only, with no
teacher-feature leakage. If it does not, preserve the negative result
and skip Paper 1.
