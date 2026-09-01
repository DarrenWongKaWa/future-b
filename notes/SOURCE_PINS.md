# Source pins — Future B live slice

Parent repository: `/Users/kawawong/Research/Keldysh4ai`
Live worktree: `/Users/kawawong/Research/Keldysh4ai-worktrees/future-b-neural-poc`
Branch: `prototype/future-b-neural-poc`

These commits are immutable references for the numbers in the live
CSVs. Regenerating a CSV is a new step; it does not rewrite these pins.

| pin | commit | what it freezes |
|---|---|---|
| ED engineering green + cutoff table | `6aa77b7` | `tests/test_ed_limits.py` 13 passed; `ed_cutoff_table.csv`; strong corner \(M=14\), \(E_0=-1.2711554105515426\) |
| 60-day packet | `d643a36` | `notes/SCIENCE_LINE_60DAY.md`, first constraints/audit |
| Week 1 ED column (12/12) | `6be8a2e` | `teacher_map_l2.csv` ED column; atomic audit inconclusive |
| Same-origin Born/SCBA poles | `e6a14f6` | `l2_periodic_pole.py`; 12/12 `E0_Born` and `E0_SCBA`; `E0_Born_VC=NOT_COMPUTED` |
| Week 2 T1–T4 | `a74fa6f` | `week2_born_scba_vs_ed.csv`; `notes/WEEK2_REPORT.md` |

Full hashes (parent worktree):

```
6aa77b7d163d78aa149e29f832a959a6f13005c9
d643a3678722c92c863c29066fc15f4c832eb0cc
6be8a2e3ccbc8e60f1c6def6b54f5bdcc0bf915b
e6a14f652467f28bf67976b9334d5db822111449
a74fa6ff69bbec31ed00345b623d923839cd1e56
```

`main` at extract time: `d35044d` (K4AI-593 record). Not a Future B
authority. Do not merge the prototype into `main` as part of this
extract.
