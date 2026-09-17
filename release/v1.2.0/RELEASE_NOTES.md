# Future B v1.2.0 — first public P1 source adapter

- Not a scientific release. No LiF rerun. Frozen classification
  `P1_UNRESOLVED_WITHIN_BUDGET` unchanged.
- v1.0.2, v1.0.3, and v1.1.0 release records are immutable.
- Adds `integration/p1`: fail-closed apply/verify of delayed-acceptance
  P1 against pinned FEP-DMC `05d08449cffdbd0dfbbbf5009add5cc887bc754b`.
- Exact stage-2 ratio is native `log(P_accept)`. Operating domain is
  Method0, one DMC band, `zeroTMC=.true.`, `sample_gt=.false.`, score
  `prop`. Finite T, multiband, and other methods `error stop`.
- C0 and P1 compose in either order to the same postimage.
- LEVEL 0 source validation. Not a `perturbo.x` build, not a LiF
  runtime, not the historical 0.956 binary, no speedup claim.
- Wheel does not ship the adapter. GitHub and the sdist do.
