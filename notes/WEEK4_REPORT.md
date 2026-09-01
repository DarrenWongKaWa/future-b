# Week 4 report — tiny logistic gate versus classical θ=0.03

Worker S (Science). Extract `/Users/kawawong/Research/future-b`.
No new K4AI number. No merge to `main`. No edit of `holstein_ed.py`
or `l2_periodic_pole.py`. No widening of the net after the loss.

Preregister `notes/WEEK4_METRICS_PREREGISTER.md` was on disk **before**
`week4_learned_vs_classical.csv` and this report. Features, lr, L2,
steps, and the 0.5 threshold were not retuned after test.

## 1. Tests T1–T5

Source: `prototypes/future_b_neural_poc/week4_verdict.csv` and
`week4_learned_vs_classical.csv`. 13 train samples (sum of
`depth_oracle` over the six train cells).

| test | verdict | counts |
|------|---------|--------|
| T1 leakage | **PASS** | `raw_features` sees only \(g,\Omega,n,r_n,\lvert\Sigma\rvert\) |
| T2 train matching | **PASS** | 6/6 |
| T3 test matching | **FAIL** | 5/6; fail cell \((g/t,\Omega/t)=(0.75,0.8)\) |
| T4 cost | **PASS** (not a win) | mean test `n_cost_learned` \(99020.33\ldots<104520.66\ldots\) |
| T5 teacher/θ lock | **PASS** | `E0_SCBA_fixed` equals teacher; \(\theta=0.03\) |

T4 is cheaper only because the learned gate also **undercuts** the
matching grain on one test cell. The win rule requires T1–T4 together.
`beats_classical=false`. `paper1_go=false`.

`notes/WEEK4_STOP.md` was **not** written (no leakage). Thresholds
were not softened. The network was not widened.

## 2. What the learned gate did

Classical depths versus learned versus oracle:

| \(g/t\) | \(\Omega/t\) | split | classical | learned | oracle | match |
|---------|--------------|-------|-----------|---------|--------|-------|
| 0.15 | 0.5 | train | 1 | 1 | 1 | true |
| 0.15 | 0.8 | test | 1 | 1 | 1 | true |
| 0.15 | 2.0 | train | 1 | 1 | 1 | true |
| 0.45 | 0.5 | test | 2 | 2 | 2 | true |
| 0.45 | 0.8 | train | 2 | 2 | 2 | true |
| 0.45 | 2.0 | test | 1 | 2 | 1 | true |
| 0.75 | 0.5 | train | 4 | 3 | 3 | true |
| 0.75 | 0.8 | test | 3 | 2 | 3 | **false** |
| 0.75 | 2.0 | train | 2 | 2 | 2 | true |
| 1.05 | 0.5 | train | 5 | 4 | 4 | true |
| 1.05 | 0.8 | test | 4 | 3 | 3 | true |
| 1.05 | 2.0 | test | 2 | 2 | 2 | true |

On train the logistic copies the oracle (including the one-layer
leftover the classical gate left). On test it copies the leftover
cell \((1.05,0.8)\) but stops one layer too early at \((0.75,0.8)\),
where \(\lvert\Delta_{\mathrm{learned}}\rvert\) exceeds
\(\lvert\Delta_{\mathrm{fixed}}\rvert+10^{-4}t\).

It also **adds** a layer at test cell \((0.45,2.0)\) (depth 2 versus
classical 1). Matching still holds there; cost does not.

Weights: `prototypes/future_b_neural_poc/week4_gate_weights.csv`.

## 3. Claim ceiling

A tiny learned CPU gate trained on 13 deployable-feature samples does
**not** beat the classical residual rule \(\theta_{\mathrm{class}}=0.03\)
after cost and matched ED error on this frozen slice. Paper 1 is not
GO. Weeks 7–8 architecture ablations are not opened. This negative
result is preserved. It is not a license to add features, widen the
net, or claim Physics-for-AI.

## 4. What remains NOT_COMPUTED

- \(E0_{\mathrm{Born+VC}}\)
- \(L=4\) ED
- typed-block versus generic architecture (Experiment A lite)
- \(\Phi\), Keldysh, Anderson–Holstein, devices, DiagMC
- archive 11A as Future B evidence
