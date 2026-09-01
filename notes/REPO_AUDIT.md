# Future B repository audit

Authority: **HUMAN LOCK 2026-08-31**.  Operational entry point:
`notes/CONSTRAINTS_FUTURE_B.md`.  Scientific order and stop rules:
`notes/SCIENCE_LINE_60DAY.md`.  If this audit disagrees with the 60-day
plan, **the 60-day plan wins**.  Science owns the live teacher map
(`prototypes/future_b_neural_poc/teacher_map_l2.csv`); this audit does
not inspect, rewrite, or gate that CSV.

Audit identity (2026-09-01, Worker A, documentation only):

- worktree: `/Users/kawawong/Research/Keldysh4ai-worktrees/future-b-neural-poc`
- branch: `prototype/future-b-neural-poc`
- HEAD at audit start: `d643a3678722c92c863c29066fc15f4c832eb0cc`
- classification: READY for this prototype-slice audit; no new K4AI ID,
  worktree, compute, or `main` merge.

This file classifies gates.  It does not authorize cleanup, deletion,
router training, convention change, or a Physics-for-AI claim.

### KEEP_BIND_FUTURE_B

Live scientific constraints that still bind this prototype.

- **HUMAN LOCK 2026-08-31 and the 60-day scientific order.**  Week 1 is
  the frozen L=2 teacher map; later weeks are conditional and cannot
  rescue a failed earlier week.  Source:
  `notes/SCIENCE_LINE_60DAY.md`, `notes/CONSTRAINTS_FUTURE_B.md`.
- **Signed dispersion and energy origin remain frozen.**
  $\xi_k=2t(1-\cos k)$, so $E_0(g=0)=0$; translator
  $E_{\rm lecture}=E_{\rm code}-2t$.  Do not change $\xi_k$.
  Executable pin: first line of
  `src/keldysh4ai/future_b/teacher/holstein_ed.py`; limit checks:
  `tests/test_ed_limits.py`.
- **Tadpole/Hartree is OFF in the diagrammatic libraries; ED retains
  $g\,n(b+b^\dagger)$.**  These are two statements, not one.  Do not
  turn tadpole ON in Library I/II, and do not strip the ED interaction
  to “match” the libraries.
- **Two-library firewall.**  Library I is bare Born plus bare VC
  (`prototypes/future_b_neural_poc/crossing_block_poc.py`, provenance
  `prototypes/future_b_neural_poc/CROSSING_BLOCK_SOURCE.md`).  Library II
  is SCBA with dressed $G$
  (`src/keldysh4ai/future_b/hopping/chain_scba.py`).  Kind split and
  double-counting FAIL conditions remain in
  `experiments/FUTURE_B/FUTURE_B_C1_BLOCK_LIBRARY_FREEZE.md`.  No block
  crosses libraries.  No $\Sigma_{\rm VC}$ is added to SCBA without a
  written disjoint-diagram memo; current default is NO.
  In this extract the formula record is `notes/CROSSING_BLOCK_SOURCE.md`
  and the paper map is `notes/SIGNED_CONVENTION_SOURCES.md`; parent
  freeze paths stay archive-only.
- **Evidence hierarchy.**  ED engineering-green $\ne$ teacher coverage
  $\ne$ architecture evidence.  Week 0 record: `tests/test_ed_limits.py`
  (13 passed at commit `6aa77b7`),
  `prototypes/future_b_neural_poc/ed_cutoff_table.csv` (11 data rows).
  Strongest allowed Week-0 statement: L=2 ED is engineering-green under
  the signed checks.  Teacher coverage, controller gain, and architecture
  evidence remain `NOT_COMPUTED` until later weeks actually produce them.
- **Teacher-feature firewall.**  Teacher values, teacher errors, and
  teacher admission labels may be evaluation targets only; they are
  forbidden inference features (`notes/CONSTRAINTS_FUTURE_B.md` hard
  stops).  Existing allowlists include
  `src/keldysh4ai/future_b/hopping/heuristics.py`
  (`FORBIDDEN_FEATURE_SUBSTRINGS`).  POC routing/audit code in
  `prototypes/future_b_neural_poc/physics_routing_poc.py` and
  `architecture_audit_poc.py` does not authorize a router run.  No
  router, MLP, GRU, or learned gate before a real teacher map **and**
  the Week-3 classical gate.
- **Week-1 labels are preregistered by Science, not by this audit.**
  `notes/SCIENCE_LINE_60DAY.md` requires weak/intermediate labels, any
  split, and comparison conventions **before** looking at the completed
  table.  Science owns `notes/WEEK1_LABELS_PREREGISTER.md`.  This audit
  does not rewrite that file or the teacher-map CSV.
- **`GENERIC_MODEL_SUFFICIENT` is proxy-only.**  The Born-versus-Born+VC
  POC verdict in
  `prototypes/future_b_neural_poc/ARCHITECTURE_NECESSITY_AUDIT.md` (also
  referenced from `PHYSICS_ROUTING_RESULT.md`) neither establishes nor
  falsifies Future B.  Do not “fix” it by widening a network.
- **11A is frozen and unused by this scientific line.**  Do not rerun,
  rewrite, delete, or use 11A numbers as labels, training data,
  baselines, priors, or architecture evidence.  Historical 11A
  references must say it is unused as Future B architecture evidence.
  A missing Future B quantity is `NOT_COMPUTED`.
- **Claim ceiling and stop rules of the 60-day plan remain binding.**
  Implementation completeness never upgrades claim strength.  No
  $\Phi$-learning, Keldysh/nonequilibrium, Anderson–Holstein,
  GAAFET/devices, NQS, DiagMC, transport, realistic materials, new
  mPFDNN/NQS/LLM-HF reading line, or invented numbers.  Do not claim
  Physics-for-AI from this prototype slice.
- **Prototype process is proportional.**  For this exploratory slice the
  live working record is focused tests, a real CSV, and a short
  `AGENT_LOG.md` (`notes/CONSTRAINTS_FUTURE_B.md` item 6).  Heavier
  reproducibility and review are added only after evidence exists and a
  scientific claim is ready to advance.

### KEEP_AS_ARCHIVE_ONLY

Records to preserve, not live admission/compute gates for this prototype.
Prefer `archive/` over delete; do not mass-delete; do not touch 11A
numbers; do not change recorded 592/593 states.

- **K4AI-592 / K4AI-593 historical teacher-line closeout.**  Preserve
  exactly as recorded:
  `status/K4AI-592.md` (independently reviewed FAIL,
  `THRESHOLD_CHANGE_REQUIRED`, coverage/neural eligibility false);
  `status/K4AI-593.md` (documentation MERGED; embedded scientific
  verdict `TEACHER_COVERAGE_NOT_ESTABLISHED`);
  `status/HUMAN_DECISION_REQUIRED_K4AI-592.md`;
  `queue/failed/K4AI-592.yaml`;
  `queue/failed/HUMAN_DECISION_REQUIRED_K4AI-592.yaml`;
  `queue/passed/K4AI-593.yaml`;
  `task_specs/K4AI-593-threshold-change-closeout.md`;
  `evidence/K4AI-592/**`;
  `evidence/K4AI-593/**`;
  `evidence/J-FUTURE_B-OPTED-FEASIBILITY-592-0001/**`;
  `experiments/FUTURE_B/teacher_expansion/POST_K4AI-592_CLOSEOUT.md`.
  These close an earlier finite-open / exact-reference teacher line.
  They are not live admission for the periodic L=2 prototype.
- **11A inverse-problem archive (read-only).**  Preserve:
  `experiments/E10_gamma_theta/validation/OPHIS11A_*`,
  `frozen_protocol_ophis11a.yaml`, `ophis11a_engine.py`,
  `run_ophis11a.py`, `results_ophis11a/**`;
  `papers/P1_keldysh_method/OPHIS11A_*`,
  `papers/P1_keldysh_method/data/ophis11a_presentation_cells.csv`,
  `papers/P1_keldysh_method/figures/ophis11a_*`;
  corresponding K4AI-557/558/559/560/562 task, status, queue, and
  evidence records.  Inverse-line record only.
- **Inverse-line certification stack.**  Keep files; stop using them as
  permission to compute this prototype:
  `docs/protocols/SCIENTIFIC_CERTIFICATION.md`,
  `docs/protocols/SCIENTIFIC_GATEKEEPER.md`,
  `docs/research_basis/KELDYSH_*`,
  `status/SCIENTIFIC_AUTHORITY.yaml`,
  `status/SCIENTIFIC_GATES.yaml`,
  `evidence/scientific_competency/KELDYSH_GATE_V1/**`,
  `evidence/EVIDENCE_SCHEMA.yaml`,
  `evidence/CLAIM_EVIDENCE_MAP.yaml`.
- **Old Future B Freeze / CERTIFY / C1H ladder (historical).**  Preserve
  `experiments/FUTURE_B/FUTURE_B_*_FREEZE.md`,
  `C0_EXECUTION_PRECONDITIONS.md`, `C1_EXECUTION_PRECONDITIONS.md`,
  `C1H_EXECUTION_PRECONDITIONS*.md`,
  `frozen_protocol_future_b_*.yaml`,
  `FUTURE_B_ATOMIC_C1_ARCCLOSE.md`,
  `experiments/FUTURE_B/README.md` (already: C0–C4 in the chapter are
  pedagogical labels, not repository task IDs), and evidence under
  `evidence/K4AI-565/` through `evidence/K4AI-591R1/` plus
  `evidence/J-FUTURE_B-*`.  Scientific cautions (kind split,
  double-counting FAIL, no 11A $\theta$ in C0) may be cited.  The
  Freeze/CERTIFY lifecycle is not the live meaning of the 60-day
  Weeks 1–8 / C0–C4 planning labels.
- **Stopped K4AI-594 overbuild.**  Worktree
  `/Users/kawawong/Research/Keldysh4ai-worktrees/K4AI-594-holstein-l2-ed`
  (branch `task/K4AI-594-holstein-l2-ed`) remains
  `STOPPED_SUPERSEDED_DIRTY_DO_NOT_REMOVE`.  Preserve for later
  inspection.  Do not merge, reset, delete, or treat as authority.
- **Root protocols as records for the lines they still govern.**
  `AGENTS.md`, `docs/protocols/AGENT_TASK_PROTOCOL.md`,
  `SESSION_BOOTSTRAP.md`, `GIT_PROTOCOL.md`, `EVIDENCE_PROTOCOL.md`,
  `REPRODUCIBILITY.md`, `EXECUTION_QUEUE.md`, `COMPUTE_POLICY.md`,
  `FAILURE_RECOVERY.md`, `TASK_MODES.md`.  Do not rewrite them in this
  swarm.  `TASK_MODES.md` already states EXPLORE as default with
  proportional evidence and no independent review by default; that
  guidance is context, not a new Future B task ladder.
- **Prototype POC and Week-0 engineering artifacts as history/inputs,
  not architecture proof.**  `ed_cutoff_table.csv`, overnight/routing/
  architecture POC JSON and figures, and
  `FIRST_LAYER_REVIEW_PACKET.md` remain.  Do not use 11A or the proxy
  audit as Future B labels.

### STOP_APPLYING_TO_FUTURE_B

Gates that must stop intercepting `prototypes/future_b_*` and this
worktree.  Keep the files; stop routing this scientific slice through
them as admission or compute blockers.

- **New K4AI IDs.**  Stop creating or requiring a new `K4AI-###` for
  this prototype slice.  Machinery:
  `AGENTS.md` task numbering,
  `docs/protocols/AGENT_TASK_PROTOCOL.md` (13-field atomic contract,
  `task_specs/` / `status/` / `queue/` lock).  The 60-day plan lists
  “new K4AI task numbers … for the prototype slice” as outside the next
  two months.
- **Extra worktrees.**  Stop requiring a new isolated
  `Keldysh4ai-worktrees/K4AI-###-*` checkout to write a two-site table.
  Machinery: `AGENTS.md` worktree identity,
  `docs/protocols/SESSION_BOOTSTRAP.md`,
  `docs/protocols/GIT_PROTOCOL.md` section 2.  Live work stays on
  existing `prototype/future-b-neural-poc` /
  `/Users/kawawong/Research/Keldysh4ai-worktrees/future-b-neural-poc`.
  Do not add a worktree in this swarm.
- **Pre-compute multi-round audits.**  Stop requiring independent
  review, certification, or multi-round audit *before* small exploratory
  compute.  Machinery: `AGENT_TASK_PROTOCOL.md` REVIEW stage,
  `GIT_PROTOCOL.md` review-gate merge, `EVIDENCE_PROTOCOL.md` E4/E5,
  `SCIENTIFIC_CERTIFICATION.md` / `KELDYSH_GATE_V1`.  Review belongs
  after evidence exists and a scientific claim is being advanced.
- **Replay-hash / JSON-schema / thread-variable gates as compute
  blockers.**  Stop treating an 18-field run record
  (`docs/protocols/REPRODUCIBILITY.md` section 2), input/output sha256
  and clean-room `replay_of` hashes, `evidence/EVIDENCE_SCHEMA.yaml`
  JSON/YAML schema validity, exact `PYTHONPATH` pins (historical
  Future B job pattern in `scripts/run_future_b_c1h_job.py` and
  `task_specs/K4AI-575R2-numerical-repair.md`), or one-thread variables
  (`OMP_NUM_THREADS` / `VECLIB_MAXIMUM_THREADS` / related
  `cpu_threads` admission in `COMPUTE_POLICY.md` and
  `EXECUTION_QUEUE.md`) as permission to run this prototype.  Those
  controls remain valid for CERTIFY / inverse-line jobs.  They do not
  precede a two-site teacher CSV.
- **Mapping C0–C4 onto Freeze/CERTIFY.**  Stop equating the 60-day
  Weeks 1–8 / C0–C4 planning labels with
  `experiments/FUTURE_B/*FREEZE.md`, `frozen_protocol_future_b_*.yaml`,
  C0/C1/C1H execution-precondition checklists, or CERTIFY/KELDYSH_GATE
  machinery.  `experiments/FUTURE_B/README.md` already distinguishes
  chapter C0–C4 as pedagogical labels.  The 60-day plan forbids mapping
  C0–C4 onto the old Freeze/CERTIFY ladder.
- **Using 592/593 as live admission for this prototype.**  Stop reading
  `status/K4AI-592.md`, `status/K4AI-593.md`,
  `HUMAN_DECISION_REQUIRED_K4AI-592`, or
  `TEACHER_COVERAGE_NOT_ESTABLISHED` as a blocker or PASS gate for
  periodic L=2 Week 1.  Preserve their recorded states; do not change
  them to PASS; do not reopen a 592R1 threshold rewrite from this
  swarm.
- **The stopped K4AI-594 process overbuild as a live template.**  Stop
  importing its unmerged task contract, strict JSON/replay runner,
  input hashes, clean-tree enforcement, or environment gates onto this
  branch.
- **Any rule that blocks writing a real CSV until its certificate is
  perfect.**  Stop applying to Future B.  Live process for this slice:
  signed physics, a focused test, a real CSV, a short log.  Absent
  quantities stay `NOT_COMPUTED`.
- **Root-protocol atomic contract as a start condition for this
  worktree.**  This checkout is the HUMAN LOCK prototype, not
  `task/K4AI-###`.  Do not FAIL-CLOSED for missing a new task spec.
  Inverse-line and ordinary numbered tasks keep their own contracts.
