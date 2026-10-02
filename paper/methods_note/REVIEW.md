# Independent review of the methods note (2026-10-02)

The draft in this folder was reviewed by a panel of independent referees. For
each of ten candidate contributions there was one referee and two skeptics: a
prior-art skeptic who searched the literature, and an evidence auditor who
re-derived the numbers from `research/r1_grouped/`. A completeness critic then
looked across the repository. **The note is withdrawn pending revision.** Do
not cite it or reuse its numbers without checking this file.

## Overall judgement

Future B has a small, genuine scientific contribution, and it is a
code-correctness contribution rather than a physics or methods result:

- **New:** two previously unreported defects in public FEP-DMC's
  `remove_external_ph`, verified at source level and reported upstream
  ([yaoluo/FEP-DMC#1](https://github.com/yaoluo/FEP-DMC/issues/1)):
  - (b) a reference trace at the wrong momentum, which matters only for
    multiband systems;
  - (c) a removal outside the addition's support, which breaks detailed balance.
- **Already known but re-measured:** the stale-frequency defect (a), already
  disclosed as C0 in v1.0. Its effect on energies has now been measured, and
  it is null within errors.
- **Diagnosis:** in the low-sign multiband regime, FEP-DMC's outermost-only
  external moves equilibrate the number of external pairs slowly. The remedy
  is the any-position end-pair update of Mishchenko et al. (2000).
- **Known methods, applied competently:** the validation ladder, the pooled
  ratio estimator, the sign-variance diagnostic, delayed acceptance and the
  diagram compiler. Their efficiency outcomes are null or unresolved.

None of this has been shown to change a published FEP-DMC number. In size it
is an upstream issue (or PR) plus at most a short technical note. It becomes
a paper only if the defects or the equilibration bias are shown to change a
published result beyond its quoted error, or are shown conclusively not to.

| candidate | novelty | significance |
|---|---|---|
| three external-phonon defects | likely new: (b), (c); (a) disclosed earlier | low |
| ordering invariant of native external pairs | incremental; anticipated by Mishchenko et al. 2000 (crossing end pairs) | low |
| external-pair equilibration bias and ordered move | incremental; the move restores Mishchenko et al. 2000 App. A | low |
| validation ladder | known (MCMC testing literature) | low |
| pooled ratio estimator, batch variability | known (textbook ratio estimators) | low |
| sign-variance decomposition | incremental (reweighting autocorrelation literature) | low |
| exact moves without net gain | incremental; baselines not equilibrated | low |
| R1 grouped measure on a toy | incremental (partial-summation methods) | low |
| P1 delayed acceptance (v1.0) | incremental (Christen–Fox delayed acceptance) | low |
| Diagram Compiler | engineering integration of known techniques | low |

## Corrected in v1.3.5

- **maxOrder-7 shift.** It is ΔE = −0.00319 ± 0.00081, about 4σ, against a
  4-chain baseline whose error is ±0.00074. Earlier versions said 11σ
  (v1.3.0–v1.3.3, one error bar) and 6σ (v1.3.4, a mistyped ±0.00040).
  Against the pristine code, all three fixes give −0.00237 ± 0.00051.
- **E, not Q.** The maxOrder-7 values (Table I, NATIVE_REPORT (j)) are total
  energies E. With E_bare = −0.7417 eV, the shift is 2.4% of Q, not 0.36%.
- **Labels.** The "unfixed" baseline already includes fix (a).
- **LiF hole is a published case and is not reproduced.** The published
  20³ value is 2.10 ± 0.01 eV; our runs at τ_max = 23.2 eV⁻¹ give
  |Q| ≈ 1.6–1.8 eV with unmatched settings. This is unreconciled.
- **Sign ratio.** It estimates the sign's share of the variance at fixed chain
  dynamics. It is not a bound on methods that change the chain.
- **No-gain claims.** These are now "no resolved gain against
  non-equilibrated native baselines".
- **LiF-electron sign sample.** It comes from about 70 independent chains
  (102 values, some re-runs of the same chain).

## Still to fix before any submission

- **LiF hole.** Reconcile it with the published value. Run the authors'
  exact settings (τ_max, maxOrder, NSV, band window, run length) with
  pristine, fixed, and fixed + ordered-move kernels.
- **Other published multiband cases.** Test anatase with NSV = 60; the
  one-chain NSV = 20 result is −0.087 eV against the published −0.146 eV. Also
  test STO at the published τ_max.
- **Missing evidence files.** Re-run the maxOrder-7 baselines with 8–24
  chains, and ship as evidence JSON every number that now exists only in
  NATIVE_REPORT prose: τ_int 1788/1328/1163, the pristine −0.87393, the round
  trip 0.44 → 3.6e-15, the 10⁷-step runs, and the burn-in pair counts.
- **Lead with the strongest evidence for each defect.** For (b) that is the
  8-vs-8 comparison (−0.00453 ± 0.00039, about 11σ). Defect (c) alone gives
  about 2.6σ.
- **Equilibration claim.** Present it as start-dependence of a 2×10⁶-update
  protocol (the upstream default is 10⁷). The bias is 0.16 ± 0.05 eV against
  one native batch, about 2.2σ after heavy-tail inflation. The sign ratio is
  1.8 ± 0.3. τ_int ≈ 1800 was measured before fixes (b) and (c).
- **Ordering section.** Native drops terms that vanish only as τ_max → ∞, so
  the invariant is not "part of the estimator's definition". Cite Mishchenko
  et al. 2000 Sec. III.D and Fig. 3(c).
- **Efficiency.** Either drop all efficiency claims, or re-time on native
  x86 hardware against equilibrated baselines. The CPU ratios came from
  linux/amd64 containers on Apple Silicon. Against the single equilibrated
  native batch, the ordered move's apparent net is about 4.9, unreplicated.
- **RNG shim.** The xorshift64 MKL replacement was never tested for quality.
- **Toy checks.** There are 117, not 118.
- **Prior art to cite**, as found by the reviewers (check each before use):
  - Mishchenko, Prokof'ev, Sakamoto, Svistunov, PRB 62, 6317 (2000), App. A
    and Fig. 3(c);
  - Greitemann & Pollet (2018) and Bighin et al. (2018), on remove/insert
    supports;
  - Geweke (2004) and Grosse & Duvenaud (2014), on MCMC testing;
  - Liu, Christ & Jung (2012) and Wolff (2004), on reweighting and
    derived-quantity errors;
  - Kieu & Griffin (1994) and Chen & Haule (2019), on partial summation;
  - Christen & Fox (2005) and Banterle et al., on delayed acceptance;
  - FeynmanDiagram.jl, CoS and CDet, on diagram compilation.
