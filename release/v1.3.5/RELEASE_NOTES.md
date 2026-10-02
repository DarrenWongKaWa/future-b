# Future B v1.3.5 — corrections after an independent review

- Documentation and release metadata only. No code, patch anchor, patched
  Fortran or measured number changes. The v1.3.0–v1.3.4 release records are
  immutable.
- An independent review (referees, prior-art skeptics, evidence auditors and
  a completeness critic) re-derived the v1.3.x claims from the evidence. Its
  findings are in `paper/methods_note/REVIEW.md`. The methods note is
  withdrawn pending revision, and no PDF is attached to this release.
- Corrected:
  - The LiF-hole maxOrder-7 shift from the two new fixes is
    ΔE = −0.00319 ± 0.00081 (about 4σ; 4-chain baseline). v1.3.4 said 6σ,
    from a mistyped ±0.00040; v1.3.0–v1.3.3 said 11σ.
  - Those values are total energies E. The shift is 2.4% of Q, not 0.36%.
  - The "unfixed" baseline already includes the stale-frequency fix (a).
  - The LiF hole is a published case (published 20³ value 2.10 ± 0.01 eV).
    Our runs (|Q| ≈ 1.6–1.8 eV, unmatched settings) do not reproduce it.
  - The sign-variance ratio is an estimate at fixed chain dynamics, not a
    bound.
  - "No gain" claims are now "no resolved gain against non-equilibrated
    native baselines".
  - The toy has 117 exact checks, not 118.
- Scientific scope, per the review: two new FEP-DMC code defects (reported
  upstream, yaoluo/FEP-DMC#1), a re-measured known defect, and a diagnosis of
  slow external-pair mixing. Everything else applies known methods. No
  published FEP-DMC number has been shown to change.
- Frozen `P1_UNRESOLVED_WITHIN_BUDGET` unchanged. No speedup claim.
