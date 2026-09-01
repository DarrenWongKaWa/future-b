# Future B working-copy migration

Date: 2026-09-01. This is an entry and extract step. It is not Week 3.
It does not merge to `main`. It does not delete archive files.

## What moved

1. **Working entry** for this mixed Keldysh4ai tree is now
   `FUTURE_B.md`. Daily Future B work should not start from
   `/Users/kawawong/Research/Keldysh4ai` on `main`.
2. **This directory**
   `/Users/kawawong/Research/future-b`
   is that slim sibling. It contains only the live manifest in
   `notes/LIVE_MANIFEST.md`. Inverse/11A/K4AI task machinery and
   overnight POC files were not copied.

## What did not move

- 11A numerical records
- K4AI-592 / 593 statuses
- other worktrees
- `chain_scba.py` and `crossing_block_poc.py` as live \(L=2\) solvers
- router / Week 3 code (none started)

The parent git tree still holds the archive. Prefer archive over
delete. A later human may index `archive/11a/`; that is not this step.

## How to work after this

Preferred editor root: `/Users/kawawong/Research/future-b`.

Need a number from 11A or an old freeze: open the parent worktree
read-only. Do not paste those numbers into `teacher_map_l2.csv`.

Physical conventions are unchanged. Process for the slice remains
tests + CSV + short log.
