# Limitations

- **Fixed setting.** All LiF \(Q\) numbers use Method0, \(20^3\), rank 20,
  finite projection time and order cap. They are not thermodynamic-limit
  or infinite-order values.
- **HAC.** Several chains fail the predeclared lag-2/4/8 stability rule.
  Statistical-efficiency claims are unresolved.
- **Systematic remainder \(B\).** Projection, order, and numerical
  remainder were not closed. Literature SI plots are not this project's
  contract \(B\).
- **P1 timing.** Clean P1 still contains C1 observer no-op `c1_mark_*`
  and `c1_tic` ncall increments. `C1_PROFILE=off` skips clock work and
  CSV write. Remaining overhead was not subtracted from \(T\).
- **g/environment totals.** Production confirm did not print independent
  g/env ncall (write gated by profile). Skip evidence is the fixture.
- **Partial fingerprint.** `c2_live_fp` is not a full cache proof.
- **Complete Re(\(M\)) reverse from committed Y** was not added to the
  production path (fixture reverse is the P1 score, not a full matrix
  recomputation).
- **Docker wall** includes container start; both arms used the same
  definition.
- **P4/P5** were not trained. **R1 material consumer** was not
  implemented. **C6/C7** were not started.
- **Upstream.** Luo–Bernardi compression and band-product sums are not
  Future B novelty.
