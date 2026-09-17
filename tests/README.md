# Public tests

Layers (v1.1.0):

| file | layer |
|---|---|
| `test_da_balance.py`, `test_forward_reverse.py`, `test_audit_guards.py` | algebra / invalid-input behavior |
| `test_energy_zero.py`, `test_statistics.py`, `test_reject_state.py` | frozen-record / summary consistency |
| `test_p1_clean_source.py` | source-structure of shipped Fortran excerpts |
| `test_provenance_identities.py` | public vs timed vs frozen checksum identities |
| `test_packaging.py` | sdist/wheel boundaries; no private-path runtime |
| `test_fep_dmc_upstream.py` | public FEP-DMC pin + fail-closed verifier (no network) |
| `test_c0_adapter.py` | public C0 apply/verify contract (no network, no compiler) |
| `test_r1_oracles.py` | historical R1 *metadata* only |
| `test_c5_formation_q.py` | frozen C5 Q / HAC labels |

These do not compile `perturbo.x` and are not a native LiF pass.

```
pytest tests/test_da_balance.py tests/test_forward_reverse.py \
  tests/test_energy_zero.py tests/test_statistics.py tests/test_r1_oracles.py \
  tests/test_p1_clean_source.py tests/test_reject_state.py \
  tests/test_c5_formation_q.py tests/test_audit_guards.py -q
```
