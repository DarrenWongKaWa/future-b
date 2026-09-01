# Future B live file manifest

Extracted sibling: `/Users/kawawong/Research/future-b`.
Parent: this worktree at the commit recorded in `notes/SOURCE_PINS.md`.

Files below are the **live** Future B slice. Everything else in this
Keldysh4ai tree is archive or a foreign line. Archive is not deleted.

## Operational

- `FUTURE_B.md`
- `notes/CONSTRAINTS_FUTURE_B.md`
- `notes/SCIENCE_LINE_60DAY.md`
- `notes/MOTIVATION.md`
- `notes/LIVE_MANIFEST.md`
- `notes/SOURCE_PINS.md`
- `notes/MIGRATION.md`
- `notes/SIGNED_CONVENTION_SOURCES.md`
- `notes/CROSSING_BLOCK_SOURCE.md` (formula record only; no POC executable)
- `references/` (arXiv PDFs listed in `references/README.md`)
- `AGENT_LOG.md`

## Week notes (keep)

- `notes/WEEK1_LABELS_PREREGISTER.md`
- `notes/WEEK1_REPORT.md`
- `notes/WEEK2_METRICS_PREREGISTER.md`
- `notes/WEEK2_REPORT.md`
- `notes/WEEK3_METRICS_PREREGISTER.md`
- `notes/WEEK3_REPORT.md`
- `notes/WEEK4_METRICS_PREREGISTER.md`
- `notes/WEEK4_REPORT.md`
- `notes/METHOD_NOTE.md`
- `notes/SLICE_CLOSEOUT.md` (切片结项，不是认证)
- `notes/L2_POLE_DEFINITION.md`
- `notes/L2_POLE_EXTRACTOR.md`
- `notes/ATOMIC_LIMIT_AUDIT.md`
- `notes/DOUBLE_COUNTING_MEMO.md`
- `notes/REPO_AUDIT.md` (classification only; not a deletion list)
- `notes/CLEANUP_PLAN.md` (PLAN ONLY)

## Code and tables

- `src/keldysh4ai/future_b/teacher/holstein_ed.py`
- `src/keldysh4ai/future_b/teacher/__init__.py`
- `src/keldysh4ai/future_b_atomic.py` (atomic-limit CFE only)
- `prototypes/future_b_neural_poc/l2_periodic_pole.py`
- `prototypes/future_b_neural_poc/build_teacher_map_l2.py`
- `prototypes/future_b_neural_poc/build_week2_table.py`
- `prototypes/future_b_neural_poc/week3_classical_gate.py`
- `prototypes/future_b_neural_poc/week4_learned_gate.py`
- `prototypes/future_b_neural_poc/atomic_limit_audit.py`
- `prototypes/future_b_neural_poc/teacher_map_l2.csv`
- `prototypes/future_b_neural_poc/week2_born_scba_vs_ed.csv`
- `prototypes/future_b_neural_poc/week3_depth_scan.csv`
- `prototypes/future_b_neural_poc/week3_gated_vs_fixed.csv`
- `prototypes/future_b_neural_poc/week3_theta_selection.csv`
- `prototypes/future_b_neural_poc/week4_learned_vs_classical.csv`
- `prototypes/future_b_neural_poc/week4_gate_weights.csv`
- `prototypes/future_b_neural_poc/week4_verdict.csv`
- `prototypes/future_b_neural_poc/ed_cutoff_table.csv`
- `prototypes/future_b_neural_poc/atomic_limit_audit.json`
- `prototypes/future_b_neural_poc/l2_pole_diagnostics.json`

## Tests

- `tests/test_ed_limits.py`
- `tests/test_teacher_map_l2.py`
- `tests/test_l2_periodic_pole.py`
- `tests/test_week2_table.py`
- `tests/test_week3_gate.py`
- `tests/test_week4_gate.py`
- `tests/test_slice_closeout.py`
- `tests/test_atomic_limit_audit.py`

## Explicitly not live (stay in parent tree only)

- `AGENTS.md` full inverse-line contract (preamble points here instead)
- `experiments/E10_gamma_theta/**`, 11A papers
- `status/K4AI-*`, `task_specs/`, `queue/`, `evidence/K4AI-*`
- `experiments/FUTURE_B/*FREEZE.md` as admission
- `crossing_block_poc.py`, `architecture_audit_poc.py`,
  `physics_routing_poc.py`, `typed_poc.py`, `real_physics_poc.py`
- `src/keldysh4ai/future_b/hopping/chain_scba.py`
- `src/keldysh4ai/negf/**`
