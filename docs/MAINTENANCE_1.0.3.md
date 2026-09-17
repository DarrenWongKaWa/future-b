# v1.0.3 maintenance (packaging and public upstream pin)

No new LiF chains. No algorithm change. `P1_UNRESOLVED_WITHIN_BUDGET`
unchanged. v1.0.2 provenance records are immutable.

This release separates the GitHub research artifact from the PyPI sdist
and the installable wheel, and pins the public FEP-DMC source identity
used for later integration *development*. The pin is not a working
adapter and is not the proven timed donor.

| id | action |
|---|---|
| D01 | `c2_oracle.py` moved to `historical/`; not in the wheel |
| D02 | `MANIFEST.in` ships only the canonical files tests open |
| D03 | sdist pytest runs from an extracted tarball |
| D04 | SPDX license, README, author, project URLs in METADATA |
| D05 | `docs/DISTRIBUTIONS.md` states GitHub ≠ sdist ≠ wheel |
| D06 | Public FEP-DMC commit `05d08449cffdbd0dfbbbf5009add5cc887bc754b` pinned with per-file SHA256 |
