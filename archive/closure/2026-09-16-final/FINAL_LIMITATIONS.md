# Limitations

- Formation energies are **fixed 20³ / rank20 / finite τ, order**. Not
  thermodynamic-limit or 1% ground-state certified.
- HAC lag 2/4/8 failed on some chains in both C5_dev and clean-P1
  confirmation. Statistical-efficiency claims are unresolved.
- Clean P1 still contains C1 observer no-op calls (`C1_PROFILE` off).
  Fixture work is gated by `P1_FIXTURE`.
- `c2_live_fp` is a partial fingerprint; fixture g/env deltas are the
  stronger a1 evidence.
- Complete `Re(M)` reverse from Y was not added to the production path.
- P4/P5 and R1 material consumer were not tested as performance claims.
- Docker wall time includes container start; both arms used the same
  definition (protocol).
