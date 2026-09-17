# v1.0.3 maintenance (packaging only)

No new LiF chains. No algorithm change. `P1_UNRESOLVED_WITHIN_BUDGET`
unchanged. v1.0.2 provenance records are immutable.

This release separates the GitHub research artifact from the PyPI sdist
and the installable wheel.

| id | action |
|---|---|
| D01 | `c2_oracle.py` moved to `historical/`; not in the wheel |
| D02 | `MANIFEST.in` ships only the canonical files tests open |
| D03 | sdist pytest runs from an extracted tarball |
| D04 | SPDX license, README, author, project URLs in METADATA |
| D05 | `docs/DISTRIBUTIONS.md` states GitHub ≠ sdist ≠ wheel |
