# Future B v1.3.4 — draft methods note and a significance correction

- Documentation and release metadata only. No code, patch anchor, patched
  Fortran, algorithm or measured number changes. The v1.3.0–v1.3.3 release
  records are immutable.
- Adds `paper/methods_note/`: a draft preprint-style note on the v1.3.x
  FEP-DMC findings (validation ladder, three external-phonon defects,
  ordering constraint, external-pair equilibration bias, pooled estimator,
  sign-variance ceiling), as LaTeX source with a table tracing every
  number to `research/r1_grouped/`. The PDF is attached to the GitHub
  release (the repository ignores `*.pdf`).
- Correction: earlier releases quoted the LiF-hole maxOrder-7 shift from the
  native fixes as "11σ". That figure divided the shift by one error bar. With
  both errors combined it is −0.00319 ± 0.00052, about 6σ. Corrected in
  `docs/FEP_DMC_TOOLKIT.md` and `NATIVE_REPORT.md`; the v1.3.0 release notes
  keep the old figure as an immutable record.
- The defects are reported upstream: https://github.com/yaoluo/FEP-DMC/issues/1
- Frozen `P1_UNRESOLVED_WITHIN_BUDGET` unchanged. No speedup claim.
