# Future B v1.3.1 — documentation correction for the FEP-DMC toolkit

- Documentation-only release. No code path, patch anchor, patched Fortran or
  number changes. The v1.3.0 release record is immutable.
- Corrects the v1.3.0 bug attribution. Of the three opt-in native fixes,
  `FUTUREB_WQFIX` (stale phonon frequency in `add_external_ph`) is not a new
  finding: it is the defect Future B recorded in v1.0 and ships as the C0
  source adapter since v1.1.0, on the same line. v1.3.0 re-found it
  independently and is the first to measure its effect on EZ energies
  (paper cases within 1–3 meV). The two `remove_external_ph` bugs
  (`FUTUREB_EXTRMFIX`, `FUTUREB_EXTFIX`), the native ordering constraint and
  the external-pair under-equilibration are new in v1.3.0.
- Documents how the toolkit and C0 compose: `future-b-fepdmc prepare` works
  on a C0 tree (then `--wqfix` is redundant); C0 refuses a tree `prepare` has
  already patched.
- Updated: `docs/FEP_DMC_TOOLKIT.md`, `docs/CONTRIBUTIONS.md`,
  `docs/CAPABILITIES.md`, `README.md`, the `future_b.fepdmc` and `wqfix`
  docstrings, and `research/r1_grouped/native_rb/NATIVE_REPORT.md`.
- Frozen `P1_UNRESOLVED_WITHIN_BUDGET` unchanged. No speedup claim.
