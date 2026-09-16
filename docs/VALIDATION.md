# Validation

Bounded checks only. No general replay framework was built.

## Algebra (no native binary)

| test | claim |
|---|---|
| `tests/test_da_balance.py` | DA restores native \(\mathrm{abs}(\mathrm{Re}\,M)\) ratio; \(\lvert M\rvert_{\mathbb{C}}\) is a different target |
| `tests/test_forward_reverse.py` | occupancy reverse is antisymmetric; \(\Delta t\)+\(\Delta E\) double-flip is not |
| `tests/test_energy_zero.py` | \(Q=\) ratio \(-E_{\mathrm{bare}}\); unshifted \(\sim 9.105\,\mathrm{eV}\) is not \(Q\) |
| `tests/test_statistics.py` | frozen HAC threshold; relative precision; P1 classification |
| `tests/test_r1_oracles.py` | `BOUND_C` / `SHARED_X_GROUP` / `SUMMED_KERNEL`; \(\lvert\sum D\rvert\neq\sum\lvert D\rvert\) |
| `tests/test_p1_clean_source.py` | dump/reverse gated; stage-1 return before `cal_gkq`; counters independent of dump |

## Native fixture (historical, preserved)

`closure/2026-09-16-final/p1_fixture/` with `P1_FIXTURE=1`:

- 4372 stage-1 rejects: recorded live fingerprint match and
  \(\Delta g=\Delta\mathrm{env}=0\)
- 6350 accepted-Y P1 reverse checks passed
- `LINEAR_DA_COUNTS` stage-1 count 4372 independent of dump

`c2_live_fp` is a **partial** fingerprint. It is not a proof of complete
typed-state/cache non-pollution. The stronger a1 evidence is the
recorded g/environment increment.

## Clean confirmation (historical, not rerun)

Six + six \(N_{\mathrm{mc}}=200\) chains. See
[STATISTICS.md](STATISTICS.md). Not rerun in this wrap-up: the frozen
batch already classifies the \(\ge 5\%\) question as unresolved, and
rerunning would be optional stopping.

## C0 / C1 (preserved)

- C0 repair_v2: 4/4 OFF/shadow identity; independent frequency table
  check. Status `C0_ACCEPTED`.
- C1: 16 profile runs; swap exclusive / coarse MC \(\approx 0.212\).
  Full-detail observer \(+41\%\); sparse 1/16 fallback \(+3.2\%\).

## R1 oracles (preserved, not rerun as a search)

Scalar n1/n2 independent references; R1≡CSE at machine precision on the
same measure; M4 finite-domain partition/measure checks. See
`tests/test_m3_analytic.py` and related files in the full tree.
