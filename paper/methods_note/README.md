# Methods note (draft)

*Exactness checks and estimator pitfalls in first-principles diagrammatic
Monte Carlo of polarons.* A short preprint-style write-up of the v1.3.x
FEP-DMC findings: the validation ladder, three external-phonon defects, the
ordering constraint, the external-pair equilibration bias, the pooled
estimator, and the sign-variance ceiling.

**Status: withdrawn pending revision.** An independent review found errors
and overclaims; read [REVIEW.md](REVIEW.md) before using anything here.
v1.3.5 corrects the verified numbers; the remaining issues are listed there.

Build (TeX Live with revtex4-2; TikZ for the figure):

```bash
pdflatex main.tex && pdflatex main.tex
```

The repository ignores `*.pdf`, so the PDF is not committed. Build it
locally, or download it from the v1.3.4 GitHub release.

## Where every number comes from

Paths are relative to `research/r1_grouped/`.

| Claim in the note | Source |
|---|---|
| Ladder L1 (5,937 states, balance ≤ 2e-17, oracle 5e-15) | `REPORT.md`, `evidence/` |
| Round trip 0.44 → 3.6e-15 (stale ω) | `native_rb/NATIVE_REPORT.md` (g) |
| Stale-ω effect on energies | `native_rb/NATIVE_REPORT.md` (g) table |
| Table I (maxOrder 7 kernels, total energies E) | `native_rb/evidence/external_pair_validation.json`, set `maxorder7` (the native row has 4 chains) |
| ΔE = −0.00319 ± 0.00081 (≈ 4σ; 2.4% of Q) | Table I rows 1 and 4, errors combined in quadrature; E_bare = −0.7417 eV |
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
| LiF electron ⟨s⟩ ≈ 0.944 (about 70 independent chains) | `lif_sign/lif_sign_summary.json`; duplicates noted in REVIEW.md |
| Table IV (net efficiencies) | `native_rb/NATIVE_REPORT.md` (e)–(k); external move: `native_rb/evidence/lif_hole500_ext_allfix_pooled.json` |
| τ_int(order) ≈ 150–200, τ_int(n_ext) → 56 | `lif_hole500_ext_allfix_pooled.json` traces; `lif_hole500_ext_pscan.json` |

## Corrections

See [REVIEW.md](REVIEW.md) for the corrections made in v1.3.5 (the
maxOrder-7 shift is about 4σ and 2.4% of Q; earlier versions said 11σ and
6σ) and for what still has to be fixed.
