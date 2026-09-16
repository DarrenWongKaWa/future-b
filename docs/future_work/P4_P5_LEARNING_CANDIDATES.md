# P4 / P5 — future-work candidates (not implemented)

**Status in Future B: `FUTURE_WORK_CANDIDATE`.**

This project **stopped** P4/P5. It did **not** collect new training
data, fit P4, train P5, or deploy either model.

That stop is a **scope/budget closure**, not a proof that machine
learning cannot accelerate FEP-DMC.

Historical Group-v3 (`NO_DEMONSTRATED_GAIN_FIXED_RECIPE`) is a
*different* completed recipe and remains a scoped negative. Do not
conflate it with P4/P5.

## 1. Scientific motivation

Stage-1 delayed acceptance needs a cheap score for the expensive residual

\[
b = \ell_R - \ell_{\mathrm{prop}}
\]

where \(\ell_R\) is the exact native log-ratio
(\(\mathrm{abs}(\mathrm{Re}\,M)\) plus legal propagator pieces) and
\(\ell_{\mathrm{prop}}\) is the analytic P1 score. A model may predict
\(\hat b\) from **cheap** state packets. Approximate DA uses

\[
\hat\ell = \mathrm{clip}(\ell_{\mathrm{prop}}+\hat b, -\ln 10, +\ln 10).
\]

The exact native stage-2 correction **must remain**. No model may
replace the exact target.

## 2. Frozen candidate definitions (do not retune)

### P4

\[
\hat b = a\cdot (p_Y^{\mathrm{norm}} - p_X^{\mathrm{norm}})
\]

- 64 parameters, no intercept
- weighted ridge, \(\lambda=10^{-3}\)
- solve the linear system directly
- no feature search, no \(\lambda\) search

### P5

\[
\hat b = \frac{1}{2}\Big[ f(p_Y^{\mathrm{norm}},p_X^{\mathrm{norm}})
- f(p_X^{\mathrm{norm}},p_Y^{\mathrm{norm}}) \Big]
\]

- MLP \(128\to 32\to 1\), \(\tanh\)
- fixed output bias \(=0\)
- 4160 trainable parameters
- FP64, Huber \(\delta=1\), Adam \(10^{-3}\), batch 512, 200 epochs
- seed **11** is the deployment seed; 22/33 are reproducibility
  diagnostics only. Do not pick a better seed.

## 3. What was not completed

- complete proposal-level data contract (64-D cheap packets \(p(X),p(Y)\))
- exact finite \(\ell_R\), \(\ell_{\mathrm{prop}}\), residual \(b\)
- cost metadata, chain/event IDs, reservoir inclusion probabilities
- TRAIN / DEV / HOLDOUT split **by whole independent chain**
- final P4 fit, final P5 fit
- native deployment
- real-material ON comparison against **both** B-best and clean P1

Existing C2 dumps have finite \(\ell_R\) on short chains. They do **not**
contain the frozen 64-D packets. That is why the earlier closure said
`DATA_CONTRACT_NOT_CLOSED`. This wrap-up **does not** build that
pipeline.

## 4. Features that must not be used

- exact future environment
- full \(g\) if that defeats the claimed saved work
- saved \(\ell_R\) as an input
- accept/reject as an input
- \(Q_{\mathrm{ref}}\)
- timing labels as inference features

## 5. What a future researcher would do

1. Passive B-best (or clean P1-off) event collection on the frozen LiF
   setting.
2. Write 64-D cheap-state packets for \(X\) and \(Y\) (existing
   definition; **no new features**).
3. Record exact \(\ell_R\), \(\ell_{\mathrm{prop}}\), \(b\), costs, IDs.
4. Split by whole chain into TRAIN / DEV / HOLDOUT.
5. Fit P4 (direct ridge) and P5 (frozen NN recipe, seed 11).
6. Batch-1 native inference cost: feature construction + prediction +
   exact correction on stage-1 pass. Compare to skippable exclusive
   exact work. If there is no positive cost headroom, **stop** before
   expensive ON chains.
7. If headroom exists, deploy in native DA and compare to **B-best and
   clean P1** under a protocol frozen in advance.

A candidate that beats B-best but not clean P1 does **not** show added
value from learning.

## 6. Difficulty and compute

This is a **moderate software/data-engineering** project, not a
large-model/GPU problem. The frozen models are tiny.

Recommended: a normal x86_64 CPU workstation or server. GPU is optional
and not required. Do not redesign P4/P5 into a transformer, GNN, or RL
agent as part of “the same candidate”.

## 7. Allowed conclusion later

Recipe-specific:

`GAIN_ESTABLISHED` / `NO_PRACTICAL_GAIN` /
`UNRESOLVED_WITHIN_BUDGET` / `DATA_CONTRACT_NOT_CLOSED` /
`DEPLOYMENT_NOT_CLOSED`.

Not allowed: “machine learning cannot accelerate FEP-DMC”.
