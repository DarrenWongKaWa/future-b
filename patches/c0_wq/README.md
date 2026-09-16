# C0 \(\omega_q\) refresh

`apply_wq_refresh.py` inserts `call cal_wq_int` after `sample_q` in
`add_external_ph`. Authorized only for owned
`night1/C0/repair_v2/trees/{baseline,candidate}` in the original
workflow. Do not patch historical evidence in place.
