# Future B v1.3.2 — sdist self-test and optional scipy

- Packaging fix. No patch anchor, patched Fortran, algorithm or number
  changes. The v1.3.0 and v1.3.1 release records are immutable.
- v1.3.1 failed its own tests where scipy is not installed, and in the
  unpacked sdist:
  - `future_b.fepdmc.analysis.analyze_mode_rb` and `compare_between`
    imported scipy at module level. scipy is now imported inside `main()`,
    and it is an optional extra: `pip install 'future-b[analysis]'`.
  - `release/v1.3.1/SHA256SUMS.txt` lists `docs/CONTRIBUTIONS.md`, which the
    sdist did not ship. `MANIFEST.in` now includes it.
- New test: every analysis module imports with scipy absent, so a local
  environment that has scipy can no longer hide this.
- Checked like CI: clean Python 3.12 venv without scipy, source tree and
  unpacked sdist.
- Frozen `P1_UNRESOLVED_WITHIN_BUDGET` unchanged. No speedup claim.
