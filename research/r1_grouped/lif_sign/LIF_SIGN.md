# LiF native average sign

**Question.** The F1–F3 report ([REPORT.md](../REPORT.md)) left one open
question: what is the average sign ⟨s⟩ of native LiF sampling under
`|Re D|`? It bounds how much any sign-based grouped measure could help.

**Source.** No new run was needed. In `diagmc-EZ` mode, FEP-DMC records
the sign through `measure_EZ_wfn` (`diagMC_gt.f90`). At every measurement
it accumulates `gtrue = Re D_num / |Re D_samp|`, and it writes the average
to `sign.dat-*` and to stdout as `<g/Z>`. In general the numerator uses
`gkq_full` and the sampling weight uses `gkq`. Under `DMC_Method = 0`,
however, `cal_gkq_vtex_int` also calls `solve_gkq_full_fast`, so
`gkq ≡ gkq_full` and `gtrue` is a pure ±1 sign. [fepdmc/analysis/collect_sign.py](../../../src/future_b/fepdmc/analysis/collect_sign.py) reads those files read-only from
the local run tree into [native_sign_runs.csv](native_sign_runs.csv) (177
runs). [fepdmc/analysis/summarize_sign.py](../../../src/future_b/fepdmc/analysis/summarize_sign.py) then pools the production
campaigns into [lif_sign_summary.json](lif_sign_summary.json).

Rules for the pooled number:
- Only production campaigns count: `Nmcmc(1e4) ≥ 100`.
- Fixtures and duplicate copies are excluded.
- Standard errors come from the spread between independent chains.

All runs share the same setup: `lif-sp3`, `calc_mode = 'diagmc-EZ'`,
`DMC_Method = 0` (Luo EZ), and `band_min = band_max = 1`. The last point
means **a single band**: D is a complex scalar, and its sign comes
entirely from the Wannier-gauge phases of `g(k,q)`. That is the same
mechanism as the toy's k-dependent vertex.

## Result

| campaign | chains | ⟨s⟩ |
|---|---|---|
| FEP-DMC dataset `LiF-electron/E-nk/reference` (upstream authors' output) | 3 | 0.9426 ± 0.0016 |
| Future B QREF (Nmcmc 2000) | 30 | 0.9438 ± 0.0024 |
| Future B night-1 C1/C5_dev/C6/C7 | 44 | 0.9423 ± 0.0048 |
| Future B luo_energy_1pct review | 12 | 0.9482 ± 0.0030 |
| Future B clean-P1 confirm (B-best + P1) | 12 | 0.9484 ± 0.0044 |
| scheme_d F25 | 1 | 0.9509 |
| **pooled** | **102** | **0.944 ± 0.002** |

Runs with `Nmcmc ≤ 10` report ⟨s⟩ ≈ 0.98–1.0. Those chains are too short
to reach the higher orders where the signs appear, so they are excluded.
The upstream authors' reference output agrees with the Future B
campaigns, so the number does not depend on a Future B binary.

## Consequence for the grouped consumer

The ratio-estimator variance scales as `1/⟨s⟩²`.

- **Ceiling.** Suppose a grouped measure removed *every* cancellation,
  so that ⟨s⟩_B = 1. The variance would still fall only by a factor of
  1/0.944² = **1.12**, a 12% saving in samples. No grouping of any size
  or shape can beat this.
- **Realistic transfer.** In the signed toy, 4-vertex tiled groups
  recovered 9–16% of the sign deficit `1 − ⟨s⟩`. Applying the best of
  those to LiF gives ⟨s⟩_B ≈ 0.953 and a variance gain of **1.019**,
  about 2%.
- **Toy costs on top.** The toy also showed a larger `τ_int` for
  group-invariant observables (3–25% worse) and extra cost for group
  evaluation. Both are expected to outweigh a ~2% sign gain.

**Verdict: no-go** for a *sign*-motivated grouped consumer on LiF-electron
single band. R1 grouping could still pay off only through:
1. Rao–Blackwellization of the `Q` estimator. This needs `Q`'s
   per-diagram estimator to vary within a group. The EZ energy estimator
   (`measure_gt`: order and phonon-energy terms from vertex times) does
   vary under re-pairing, so this is not excluded, but the toy gain was
   7–24% on such observables;
2. materials or settings with a much worse sign. The dataset also has
   LiF-hole, TiO₂ and SrTiO₃, whose ⟨s⟩ has not been measured here.

## Limits

- **EZ mode only.** EZ fixes the external time at `τ = 1/kT = 232 eV⁻¹`
  (T = 50 K). So ⟨s⟩ = 0.944 is already the sign at a very long time. The
  paper's `dataset/Figure-1` shows a different estimator: the G(τ)
  "matrix product" mode, whose S(τ) falls to 0.33 at τ = 11.5 eV⁻¹ and to
  0.24 at τ = 14. In G(τ) mode the sign problem is severe, and grouping
  might matter there. That case is not assessed here.
- The measured weight is the trace with normalized `gkq`. A positive
  rescaling does not change the sign.
- Each chain's own error is not used. Chains within a campaign are
  treated as independent replicas.
