# v1.0.1 maintenance (does not move tag v1.0.0)

Independent audit of `77835ca` / `FutureB_v1.0.0_77835ca.tar.gz`.
No new LiF chains. `P1_UNRESOLVED_WITHIN_BUDGET` unchanged.

| id | action |
|---|---|
| F01 | `hac_pass` no longer drops NaN/Inf/0/negative windows |
| F02 | `apply_p1_clean.py` fails closed; missing src does not delete dst |
| F03 | `C2_FORCE_A1` only if `p1_fixture_on()` |
| F04 | tests execute `stage2_exact_accept`; excerpt must contain `ellR - ell_hat` |
| F05 | R1 module labeled historical metadata |
| F06 | `recompute_q.py` labeled summary-consistency |
| F07 | `mean_jackknife_se` vs `ratio_of_sums_jackknife_se` |
| F08 | DA / classify / counters reject illegal input |
| F09 | patch marked historical-only |
| F10 | wheel vs source documented; Fortran package-data |
| F11 | wall / Var / K already in frozen JSON; README/tables show K as diagnostic |
| F12 | `docs/PUBLIC_MANIFEST.md` |
| F13 | `docs/SOURCE_ATTRIBUTION.md` (owner permission still required) |
| F14 | METHOD_P1 clip vs unclipped; two RNGs |
