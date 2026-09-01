# Future B cleanup plan

Status: **PLAN ONLY — no cleanup, move, deletion, worktree removal, or main
merge occurred in this swarm.**  Archive before delete, and inspect before
archive.  Prefer `archive/` over delete.  Do not mass-delete.  Do not touch
11A numbers.  Do not declare any worktree safe to delete.

## Target repository shape

- `notes/CONSTRAINTS_FUTURE_B.md` remains the sole live operational entry
  point for `prototypes/future_b_*`.
- `notes/SCIENCE_LINE_60DAY.md` controls the scientific order and stop
  rules.  If an audit or this plan disagrees with that file, the 60-day
  plan wins.
- `notes/REPO_AUDIT.md` classifies KEEP_BIND / KEEP_AS_ARCHIVE_ONLY /
  STOP_APPLYING.  It is not a deletion list.
- Old task, freeze, evidence, and inverse-line protocols remain available
  as historical records but do not intercept the Future B prototype path.
- The existing `prototype/future-b-neural-poc` branch remains outside
  `main` until a human requests a later review/merge decision.  This swarm
  does not merge to `main`.

## Proposed `archive/11a/` treatment — deferred

Do not move anything in this swarm.  A later human-reviewed cleanup may
create an `archive/11a/` index or relocate/mark these families as
archive-only:

- `experiments/E10_gamma_theta/validation/OPHIS11A_*`;
- `experiments/E10_gamma_theta/validation/frozen_protocol_ophis11a.yaml`;
- `experiments/E10_gamma_theta/validation/ophis11a_engine.py` and
  `run_ophis11a.py`;
- `experiments/E10_gamma_theta/validation/results_ophis11a/**`;
- `papers/P1_keldysh_method/OPHIS11A_*`, its 11A data, and 11A figures;
- corresponding K4AI-557/558/559/560/562 task, status, queue, and evidence
  records.

The archive operation must preserve paths or provide a checked index so
old citations remain resolvable.  It must state that 11A is an
inverse-problem record and is unused as Future B architecture evidence.
No 11A numerical artifact is rewritten or deleted by this plan.

## Existing worktrees

Base directory: `/Users/kawawong/Research/Keldysh4ai-worktrees/`.
Inventory confirmed 2026-09-01 from `git worktree list` on this checkout
(HEAD `d643a3678722c92c863c29066fc15f4c832eb0cc`).  Labels below are
documentation labels, **not deletion authorization**.  No listed worktree
is declared safe to delete by this plan.

| Worktree or group | Label now | Planned handling |
|---|---|---|
| `future-b-neural-poc` | `ACTIVE_WEEK1_PROTOTYPE` | This is the **ACTIVE Week-1 prototype worktree**. Science is running the L=2 teacher map here. Keep. No merge to `main`. Audit worker does not touch science CSVs. |
| `K4AI-594-holstein-l2-ed` | `STOPPED_SUPERSEDED_DIRTY_DO_NOT_REMOVE` | Ignore. It is unmerged and contains dirty process-overbuild files; do not remove, merge, reset, or use it as authority. |
| `K4AI-565-future-b-atomic-core` | `DIRTY_LEGACY_DO_NOT_REMOVE` | Preserve pending separate inspection; do not treat its untracked files as cleanup candidates. |
| `K4AI-566-future-b-plan-archive`, `K4AI-567-future-b-fb00-recon` | `ARCHIVE_UNMERGED_PLAN_OR_POC` | Ignore in the live line; preserve branches/commits; do not merge opportunistically. |
| K4AI-568 through K4AI-575R2 worktrees that still exist | `ARCHIVE_RECORD_ONLY` | Ignore as live gates. Eventual worktree removal may be considered only after confirming branches/commits/evidence are preserved, and only with a later human decision. Not authorized now. |
| `K4AI-583-future-b-task-ladder`, `K4AI-584-future-b-engineering-rebaseline`, `K4AI-585-future-b-controller-prototype` | `ARCHIVE_UNMERGED_PLAN_OR_POC` | Ignore; do not merge into the 60-day line. |
| K4AI-586 through K4AI-593 worktrees that still exist | `ARCHIVE_RECORD_ONLY` | Preserve their negative/closeout records; stop using them as live periodic-prototype gates. Do not change 592/593 recorded states. |
| `E10-gamma-theta`, `E10-validation` | `ARCHIVE_11A_READ_ONLY` | Keep read-only; no rerun and no Future B evidence transfer. Do not touch 11A numbers. |
| Inverse-line numbered worktrees still present (K4AI-103 family, 401–562, and other non-Future-B checkouts) | `FOREIGN_LINE_DO_NOT_TOUCH` | Out of Future B cleanup scope. Preserve. Do not prune from this plan. |
| `/Users/kawawong/Research/Keldysh4ai` | `MAIN_UNTOUCHED` | Do not merge the prototype in this swarm. Shared main remains INTEGRATION-ONLY. |

K4AI-594 remains `STOPPED_SUPERSEDED_DIRTY_DO_NOT_REMOVE`.

## Protocol handling

- Do not rewrite `AGENTS.md` or mass-edit root protocols in this swarm.
- Keep `AGENT_TASK_PROTOCOL.md`, `GIT_PROTOCOL.md`,
  `SESSION_BOOTSTRAP.md`, `REPRODUCIBILITY.md`, `EVIDENCE_PROTOCOL.md`,
  `SCIENTIFIC_CERTIFICATION.md`, and related schemas for the lines they
  govern.
- For Future B, stop applying their task-ID / extra-worktree /
  pre-compute multi-round audit / replay-hash / JSON-schema /
  thread-variable requirements as permission to create a small prototype
  table.  Classification is in `notes/REPO_AUDIT.md` section
  STOP_APPLYING_TO_FUTURE_B.
- If interception continues later, the only permitted root-protocol
  change is a short, human-reviewed preamble stating that archive/11A and
  the inverse line keep those rules while `prototypes/future_b_*` follows
  `notes/CONSTRAINTS_FUTURE_B.md`.  Do not empty or reinterpret the
  protocols.

## Delete versus archive

Prefer `archive/` or an archive index.  Never delete:

- 11A numerical records, JSON, tables, or figures;
- `prototypes/future_b_neural_poc/ed_cutoff_table.csv`;
- `prototypes/future_b_neural_poc/teacher_map_l2.csv` (Science-owned;
  this plan does not touch it);
- Science-owned Week-1 notes if present:
  `notes/WEEK1_LABELS_PREREGISTER.md`,
  `notes/ATOMIC_LIMIT_AUDIT.md`,
  `notes/DOUBLE_COUNTING_MEMO.md`,
  `notes/WEEK1_REPORT.md`;
- live authorities `notes/SCIENCE_LINE_60DAY.md` and
  `notes/CONSTRAINTS_FUTURE_B.md`;
- failed runs or negative scientific results;
- signed convention records;
- K4AI-592/593 statuses/evidence;
- branches or dirty worktrees before separate inspection.

Only generated, unregistered scratch may be considered for later
deletion, and only after a dry review confirms that it is neither cited
nor the sole copy of a result.  No such deletion decision was made in
this swarm.

## Cleanup sequence when a human later authorizes it

1. Read `notes/SCIENCE_LINE_60DAY.md` and
   `notes/CONSTRAINTS_FUTURE_B.md`.
2. Produce a dry inventory of 11A records, Future B historical records,
   branches, worktrees, and generated scratch.
3. Add archive indices/labels before moving any tracked file.  Prefer
   `archive/` over delete.
4. Verify every preserved result remains addressable.
5. Consider worktree removal separately from branch/evidence deletion.
   No worktree is pre-cleared as safe to delete.
6. Ask for a specific human approval before any deletion or main merge.

This swarm executed none of those steps.
