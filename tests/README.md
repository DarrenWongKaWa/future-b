# Public tests

These do not need LiF HDF5 or Docker:

```
pytest tests/test_da_balance.py tests/test_forward_reverse.py \
  tests/test_energy_zero.py tests/test_statistics.py tests/test_r1_oracles.py \
  tests/test_p1_clean_source.py tests/test_reject_state.py \
  tests/test_c5_formation_q.py -q
```
