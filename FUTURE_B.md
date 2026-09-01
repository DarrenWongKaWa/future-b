# Future B — live working entry

This repository **is** the live Future B extract. Work only here.

- Daily root: `/Users/kawawong/Research/future-b`
- Do **not** keep a second live copy on the parent prototype branch.
- Do **not** work Future B from `/Users/kawawong/Research/Keldysh4ai` (`main`).
- Do **not** merge into Keldysh4ai `main`.
- 11A and old K4AI trees were **not copied** here. Leave them in the
  parent archive; do not maintain that archive from this slice.

Commit pins: `notes/SOURCE_PINS.md`.

## Read first

1. `notes/CONSTRAINTS_FUTURE_B.md` — how to work
2. `notes/SCIENCE_LINE_60DAY.md` — scientific order
3. `notes/MOTIVATION.md` — why diagrammatic cost, and why a network would still be physics
4. `notes/SIGNED_CONVENTION_SOURCES.md` — papers for the signed conventions
5. `notes/LIVE_MANIFEST.md` — which files are live vs archive-in-tree

Process for this slice: tests + CSV + short `AGENT_LOG.md`. No new
K4AI ID, no extra worktree, no Freeze/CERTIFY, no 592/593 admission.

## Slice status

**切片结项，不是认证.** Closed 2026-09-01. Paper 1 is not GO.
Allowed sentence and forbidden claims: `notes/SLICE_CLOSEOUT.md`.
Method note: `notes/METHOD_NOTE.md`. 11A stays archived. Do **not**
merge this as “Future B succeeded” into Keldysh4ai `main`.

## Live science (closed L=2 slice)

Frozen periodic \(L=2\) Holstein, \(\xi_k=2t(1-\cos k)\).

| Stage | Status | Where |
|---|---|---|
| Week 0 ED engineering green | done (`6aa77b7`) | `tests/test_ed_limits.py`, `ed_cutoff_table.csv` |
| Week 1 ED + Born/SCBA \(E_0\) columns | done (`e6a14f6`) | `teacher_map_l2.csv`, `l2_periodic_pole.py` |
| Week 2 Born/SCBA vs ED | T1–T4 pass (`a74fa6f`) | `week2_born_scba_vs_ed.csv`, `notes/WEEK2_REPORT.md` |
| Week 3 classical stopping | T1–T6 pass; \(\theta=0.03\) | `week3_gated_vs_fixed.csv`, `notes/WEEK3_REPORT.md` |
| Week 4 tiny learned gate | negative (test matching 5/6) | `week4_verdict.csv`, `notes/WEEK4_REPORT.md` |
| Weeks 5–6 method note | written; Paper 1 not GO | `notes/METHOD_NOTE.md` |
| Weeks 7–8 architecture | **not opened** | Paper 1 is not GO |
| Router / MLP | **closed**: learned gate did not beat \(\theta=0.03\) | do not widen |
| Candidate 1 spectra | **stopped** (T1 fail; T3 PASS-SUFFICIENT) | `c1_spectral_vs_ed.csv`, `notes/C1_REPORT.md` |
| Candidate 2 MA(0) | T1–T3 pass; no router trained | `c2_ma0_vs_ed.csv`, `notes/C2_REPORT.md` |
| C1+C2 joint | mixed closeout; `paper1_go` still false | `notes/C12_SWARM_REPORT.md` |

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
