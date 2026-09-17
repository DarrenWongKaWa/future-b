# Future B v1.0.3 — packaging maintenance (not a scientific release)

- Packaging and distribution-boundary maintenance only.
- No scientific result changed.
- No benchmark was rerun.
- No P1 algorithm change.
- v1.0.2 provenance remains historical and immutable
  (`05eab61108cae7e512a89f26530996c1591851b8`).
- The sdist is now self-testing from an unpacked tarball.
- Runtime Python no longer installs `c2_oracle.py`; that helper lives
  under `historical/`.
- GitHub research artifact, PyPI sdist, and wheel are documented as
  three different objects.
- Public FEP-DMC source identity is pinned
  (`05d08449cffdbd0dfbbbf5009add5cc887bc754b`) as a prospective
  integration baseline. Historical donor equivalence is not established.
  The pin is not a working adapter.
