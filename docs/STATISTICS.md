# Statistics

Protocol frozen in `closure/2026-09-16-final/FINAL_PROTOCOL.md` **before**
the clean-P1 confirmation batch. This wrap-up does not retune it.

## Estimator

\[
\hat Q = \mathrm{Re}\Big(\sum_b N_b/\tau_{\max,b}\Big/\sum_b D_b\Big) - E_{\mathrm{bare}}
\]

The additive shift does not change method-to-method variance or timing
ratios. It **does** change the scientific meaning of the number and the
1% scale (\(1\%\times\lvert Q\rvert\approx 2.5\,\mathrm{meV}\)).

## Per-chain HAC

Bartlett HAC on production blocks, lags 2, 4, 8. Fail the
statistical-efficiency claim if any chain has \(\max\mathrm{SE}/\min\mathrm{SE}>1.25\).
Do not drop failing chains. Do not change lags after seeing data.

Historical C5: **5/18** fail. Clean confirm: HAC fail on some chains in
both arms (`hac_ok=false`).

## Across-chain jackknife

Six independent replicates. Delete-one jackknife SE on \(\hat Q\).
Point diagnostic 95% half-width uses Student \(t_{5,0.975}=2.57058\).

Relative figures use \(\lvert Q\rvert\) as denominator. They are
**statistical diagnostics**, not a total uncertainty including
projection, order, and numerical remainder.

## Timing

\(T\) is host `elapsed_s` of the same Docker run that produced the
blocks (same workload as \(Q\)). Development diagnostic
\(K=T\cdot\mathrm{Var}_{\mathrm{JK}}(\hat Q)\) is reported but was not
used as a pass rule: its bootstrap on six chains is extremely wide.

## Bootstrap

2000 replicate-index resamples, seed `9143610`, joint across arms.

Practical-gain threshold: cost ratio 0.95 (\(\ge 5\%\) wall improvement).

| rule | classification |
|---|---|
| boot 97.5% \(< 0.95\) **and** HAC pass | `P1_GAIN_ESTABLISHED` |
| boot 2.5% \(> 0.95\) | `P1_NO_PRACTICAL_GAIN` |
| interval crosses 0.95, or HAC fail, after frozen budget | `P1_UNRESOLVED_WITHIN_BUDGET` |

Observed clean P1 / B-best wall ratio: **0.956 [0.940, 0.972]**.
Classification: **`P1_UNRESOLVED_WITHIN_BUDGET`**.

An interval containing 1 is **not** a proof of exact equality.
Crossing 0.95 is **not** permission to keep sampling.
