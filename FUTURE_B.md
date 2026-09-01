# Future B — live working entry

This repository **is** the slim Future B extract.

- Daily root: `/Users/kawawong/Research/future-b`
- Parent worktree (provenance, archive):
  `/Users/kawawong/Research/Keldysh4ai-worktrees/future-b-neural-poc`
  branch `prototype/future-b-neural-poc`
- Do **not** work Future B from `/Users/kawawong/Research/Keldysh4ai` (`main`).
- Do **not** merge into Keldysh4ai `main`.
- 11A and old K4AI trees were **not copied** here. They remain in the parent.

Commit pins: `notes/SOURCE_PINS.md`.

## Read first

1. `notes/CONSTRAINTS_FUTURE_B.md` — how to work
2. `notes/SCIENCE_LINE_60DAY.md` — scientific order
3. `notes/LIVE_MANIFEST.md` — which files are live vs archive-in-tree

Process for this slice: tests + CSV + short `AGENT_LOG.md`. No new
K4AI ID, no extra worktree, no Freeze/CERTIFY, no 592/593 admission.

## Live science (current)

Frozen periodic \(L=2\) Holstein, \(\xi_k=2t(1-\cos k)\).

| Stage | Status | Where |
|---|---|---|
| Week 0 ED engineering green | done (`6aa77b7`) | `tests/test_ed_limits.py`, `ed_cutoff_table.csv` |
| Week 1 ED + Born/SCBA \(E_0\) columns | done (`e6a14f6`) | `teacher_map_l2.csv`, `l2_periodic_pole.py` |
| Week 2 Born/SCBA vs ED | T1–T4 pass (`a74fa6f`) | `week2_born_scba_vs_ed.csv`, `notes/WEEK2_REPORT.md` |
| Week 3 classical stopping | **not started** | human-gated |
| Router / MLP | **forbidden** until Week 3 exists and still leaves a problem | — |

## Do not treat as live Future B evidence

- `experiments/E10_gamma_theta/**` and 11A papers (inverse archive)
- `status/K4AI-592.md`, `status/K4AI-593.md`
- `experiments/FUTURE_B/*FREEZE.md` as admission
- `prototypes/future_b_neural_poc/architecture_audit_poc.py`,
  `physics_routing_poc.py`, `run_overnight.py` (`GENERIC_MODEL_SUFFICIENT`
  is proxy-only)
- `src/keldysh4ai/future_b/hopping/chain_scba.py` (open chain, not this \(L=2\) table)
- `crossing_block_poc.py` (\(n_k\ge 4\), not this \(L=2\) table)

Open those only as read-only archive. Do not copy their numbers into
the teacher map.
