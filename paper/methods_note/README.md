# Methods note (draft)

*Exactness checks and estimator pitfalls in first-principles diagrammatic
Monte Carlo of polarons.* A short preprint-style write-up of the v1.3.x
FEP-DMC findings: the validation ladder, three external-phonon defects, the
ordering constraint, the external-pair equilibration bias, the pooled
estimator, and the sign-variance ceiling.

**Status: draft.** Before submission, it still needs the affiliation, the
author's review, and a decision on the venue.

Build (TeX Live with revtex4-2; TikZ for the figure):

```bash
pdflatex main.tex && pdflatex main.tex
```

`main.pdf` is the build of the committed `main.tex`.

## Where every number comes from

Paths are relative to `research/r1_grouped/`.

| Claim in the note | Source |
|---|---|
| Ladder L1 (5,937 states, balance ≤ 2e-17, oracle 5e-15) | `REPORT.md`, `evidence/` |
| Round trip 0.44 → 3.6e-15 (stale ω) | `native_rb/NATIVE_REPORT.md` (g) |
| Stale-ω effect on energies | `native_rb/NATIVE_REPORT.md` (g) table |
| Table I (maxOrder 7 kernels) | `native_rb/evidence/external_pair_validation.json`, set `maxorder7`; the native row is `NATIVE_REPORT.md` (j) |
| ΔQ = −0.00319 ± 0.00052 (≈ 6σ) | Table I rows 1 and 4, errors combined in quadrature |
| Agreement at maxOrder 21 and 51 (≤ 0.8σ) | `external_pair_validation.json`, sets `maxorder21`, `maxorder51` |
| Full order −1.722 → −1.627, ⟨s⟩ 0.090 → 0.111 | `native_rb/evidence/lif_hole500_allfix_vs_wqfix.json` |
| Paper cases +1.0 ± 3.2 meV, +0.25 ± 1.0 meV | `external_pair_validation.json`, `paper_cases_beta232`; `NATIVE_REPORT.md` (j) |
| Ordering: −0.8749 vs −0.8763…−0.8767 | `external_pair_validation.json`, `maxorder7` |
| Table II and Fig. 1 | `native_rb/evidence/lif_hole500_ext_pscan.json` |
| τ_int 1788 / 1328 / 1163, conditional sign | `native_rb/NATIVE_REPORT.md` (i) |
| Burn-in then native: 10.9–11.6 pairs, −1.771 ± 0.103 | `native_rb/evidence/lif_hole500_burnext_vs_allfix.json`; `NATIVE_REPORT.md` (k) |
| Mean-of-ratios example (−1.89 / −1.72 vs −1.72 / −1.66) | `native_rb/NATIVE_REPORT.md` (g) |
| Batch variability (×5; 2.35 → 2.62 → 1.08) | `native_rb/NATIVE_REPORT.md` (h) |
| Table III (sign ceiling) | `native_rb/evidence/{lif_elec,sto,lif_hole500}_variance_decomposition.json` |
| LiF electron ⟨s⟩ = 0.944 ± 0.002 (102 chains) | `lif_sign/lif_sign_summary.json` |
| Table IV (net efficiencies) | `native_rb/NATIVE_REPORT.md` (e)–(k); external move: `native_rb/evidence/lif_hole500_ext_allfix_pooled.json` |
| τ_int(order) ≈ 150–200, τ_int(n_ext) → 56 | `lif_hole500_ext_allfix_pooled.json` traces; `lif_hole500_ext_pscan.json` |

## Correction carried here

Earlier documents (v1.3.0–v1.3.3, and the first version of the upstream
issue) quoted the maxOrder-7 shift as "11σ". That figure divided the shift
by a single error bar. With both errors combined it is
−0.00319 ± 0.00052, about 6σ. The note and v1.3.4 use the corrected value.
