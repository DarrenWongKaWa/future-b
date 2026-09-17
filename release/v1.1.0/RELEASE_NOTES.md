# Future B v1.1.0 — first public C0 source adapter

- Not a scientific release. No LiF rerun. No P1 algorithm change.
- v1.0.2 (`05eab61108cae7e512a89f26530996c1591851b8`) remains immutable.
- v1.0.3 (`e2735a1603ad4351e3b84d1ec9109adb20d0d426`) is the packaging
  and public FEP-DMC identity baseline. Its `release/v1.0.3/` records
  are not rewritten.
- v1.1.0 adds `integration/c0`: fail-closed apply/verify of the C0
  `wq` refresh against pinned
  `05d08449cffdbd0dfbbbf5009add5cc887bc754b`.
- C0 is a source transform (LEVEL 0). It is not a `perturbo.x` build,
  not a LiF runtime validation, and not P1.
- Historical donor equivalence remains not established.
- The wheel still does not ship the adapter. GitHub and the sdist do.
