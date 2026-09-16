# Clean P1 patch

`apply_p1_clean.py` copies an owned C2_fixture adapter tree and gates
dump / after-commit reverse behind `P1_FIXTURE` (default off). DA
counters live in the update, not in the dump subroutine.

Do not apply to historical C2/C5 evidence directories.
