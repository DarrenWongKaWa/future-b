# Agent log

## 2026-08-31 — Future B morning packet

- Authority: `HUMAN LOCK 2026-08-31`.
- Input engineering evidence: prototype commit `6aa77b7` and
  `prototypes/future_b_neural_poc/ed_cutoff_table.csv`.
- Interpretation retained: L=2 ED is engineering-green only; teacher coverage,
  adaptive-policy evidence, and architecture evidence remain `NOT_COMPUTED`.
- Wrote:
  - `notes/SCIENCE_LINE_60DAY.md`;
  - `notes/REPO_AUDIT.md`;
  - `notes/CONSTRAINTS_FUTURE_B.md`;
  - `notes/CLEANUP_PLAN.md`;
  - `notes/MORNING_REPORT.md`.
- During this packet-writing step, ran no ED, SCBA, Born, atomic-limit,
  architecture, router, training, or test command.
- Created no task number or worktree; performed no review gate, replay,
  cleanup, deletion, status transition, protocol rewrite, or merge to main.
- Did not modify K4AI-592/593, 11A, either diagram library, ED source, tests,
  or the cutoff CSV.
- Numeric rule: use only values already present in the human lock or cutoff
  CSV; every other absent result is `NOT_COMPUTED`.
- The next experiment is the frozen L=2 teacher map, but it was not run
  tonight.
- First command tomorrow:

  ```bash
  cd /Users/kawawong/Research/Keldysh4ai-worktrees/future-b-neural-poc && cat notes/SCIENCE_LINE_60DAY.md
  ```

## 2026-09-01 — Future B swarm takeover (Week 1 C0)

- Authority: `HUMAN LOCK 2026-08-31`. `notes/SCIENCE_LINE_60DAY.md`
  read end-to-end; scientific order not rewritten.
- Worktree: `/Users/kawawong/Research/Keldysh4ai-worktrees/future-b-neural-poc`
  on `prototype/future-b-neural-poc`. Start HEAD `d643a36`.
  No new worktree. No new K4AI number. No merge to `main`.
- Three workers: Science (lead), Audit, Constraints.
- Teacher map: `prototypes/future_b_neural_poc/teacher_map_l2.csv`
  has **12/12 real `E0_ED`**. Not `WEEK1_INCOMPLETE`.
- Born / SCBA / Born_VC: **0 real, 12 `NOT_COMPUTED` each**.
- Strong corner `(1.05, 0.5)` matches accepted
  `E0=-1.2711554105515426` at `M=14`.
- Atomic-limit verdict: **inconclusive**.
- Double-counting verdict: **default NO** (do not add \(\Sigma_{\rm VC}\)
  onto SCBA).
- STOP_APPLYING: new K4AI IDs, extra worktrees, pre-compute multi-round
  audits, replay-hash/JSON-schema/thread-variable compute blockers,
  mapping C0–C4 onto Freeze/CERTIFY, using 592/593 as live admission,
  K4AI-594 overbuild as template, certificate-before-CSV, root atomic
  contract as start condition.
- Root independent tests:
  `PYTHONPATH=src python -m pytest tests/test_ed_limits.py tests/test_teacher_map_l2.py tests/test_atomic_limit_audit.py -q`
  → **21 passed in 0.23s**.
- Refused: 11A, 592/593 edits, root-protocol rewrites, router training,
  Week 2 tables, invented numbers, Physics-for-AI claim.
- Next human action: same-origin periodic L=2 `E0_Born`/`E0_SCBA`
  extractors on this branch before Week 2. No router.

## 2026-09-01 — periodic L=2 Born/SCBA pole extractor

- Authority: `HUMAN LOCK 2026-08-31`. Pole definition frozen first in
  `notes/L2_POLE_DEFINITION.md` (η=1e-4, window [-8.0, 0.25],
  lowest interior Re D=0 of G(k=0), SCBA depth 64).
- Worktree remains `prototype/future-b-neural-poc`. No new worktree,
  no new K4AI number, no merge to `main`, no Week 2, no router.
- Extractor: `prototypes/future_b_neural_poc/l2_periodic_pole.py`.
  Does not import `chain_scba` or `crossing_block_poc`.
- `teacher_map_l2.csv`: 12/12 real `E0_ED` (unchanged), 12/12 real
  `E0_Born`, 12/12 real `E0_SCBA`, 12/12 `E0_Born_VC=NOT_COMPUTED`.
- g=0 poles: ED/Born/SCBA all 0. ξ_0=0, ξ_π=4t.
- Atomic-limit verdict unchanged: inconclusive. Double-counting
  default unchanged: NO Σ_VC on SCBA.
- Tests: `PYTHONPATH=src python -m pytest tests/test_ed_limits.py tests/test_teacher_map_l2.py tests/test_l2_periodic_pole.py tests/test_atomic_limit_audit.py -q`
  → 28 passed.
- Refused: Week 2 ranking, router training, mixing libraries, filling
  VC, claiming C0-complete or Physics-for-AI.
- Allowed sentence: frozen L=2 cells now have real ED, Born, and SCBA
  ground energies under the signed origin. That is not a Week 2 verdict.

## 2026-09-01 — Week 2 docs / constraints hygiene

- Week 2 is analysis of e6a14f6 `teacher_map_l2.csv`; no new ED run.
- No new worktree, no K4AI id, no merge to `main`, no router.
- Science owns `notes/WEEK2_METRICS_PREREGISTER.md` / week2 CSV / `notes/WEEK2_REPORT.md` (tests are Science’s; this slice invents no T1–T4 verdict).
- Constraints process remains tests + csv + short log; CERTIFY/worktree not live admission.

## 2026-09-01 — Week 2 Science closeout (root)

- T1 PASS 4/4 weak; T2 PASS rel_SCBA=0.37357≥0.20 at (1.05,0.5); T3 PASS 17/17; T4 PASS 12/12. No WEEK2_STOP.md.
- Independent pytest: 35 passed in 0.43s (week2 + teacher-map + pole + ED + atomic). Teacher map / ED / pole code unchanged.
- Claim ceiling copied in notes/WEEK2_REPORT.md. Week 3 not started. No router. No merge to main.

## 2026-09-01 — Future B working-copy migration

- Working entry: `FUTURE_B.md`. `AGENTS.md` preamble: inverse/11A rules
  do not apply to `prototypes/future_b_*` or this prototype slice.
- Slim sibling: `/Users/kawawong/Research/future-b` from live manifest
  only. Parent archive not deleted. No merge to `main`. No Week 3.
- Pins: `notes/SOURCE_PINS.md` (`6aa77b7`, `e6a14f6`, `a74fa6f`).
- Slim-repo pytest after extract: 35 passed in 0.39s. No 11A, no POC
  routers, no Week 3, no merge to Keldysh4ai `main`.

## 2026-09-01 — signed-convention papers into this extract

- Local map: `notes/SIGNED_CONVENTION_SOURCES.md`.
- Formula record: `notes/CROSSING_BLOCK_SOURCE.md` (no `crossing_block_poc.py`).
- arXiv PDFs in `references/` (Goodvin 2006, Ciuchi 1997, Barišić 2006,
  Mishchenko 2014, Mitrić 2022). SHA-256 in `references/README.md`.
- Did not copy 11A, Jauho, parent Freeze, or the Future B chapter TeX.
- No Week 3, no router, no teacher-map edit, no merge to `main`.

## 2026-09-01 — Luo 2025 PDF as planning-only

- Why it was missing: not a source for the six signed bullets;
  `SCIENCE_LINE_60DAY.md` keeps DiagMC / realistic materials outside
  the 60-day window. Parent chapter lists it as applied high-fid.
- Now stored: NSF PAR accepted manuscript
  `references/s41567-025-02954-1-luo-park-bernardi-natphys-21-1275-nsfpar.pdf`
  (DOI `10.1038/s41567-025-02954-1`). Not the Nature typeset PDF.
- Still not an $L=2$ oracle. No DiagMC run. No teacher-map edit.

## 2026-09-01 — motivation note

- Wrote `notes/MOTIVATION.md`: e–ph Feynman sums (DiagMC) are accurate
  and slow; a network would accelerate policy; the same diagrammatic
  objects would describe the network. Question, not a result.
- Pointed from `SCIENCE_LINE_60DAY.md`, `FUTURE_B.md`, `README.md`.
- No Week 3, no router, no DiagMC implementation, no Physics-for-AI claim.

## 2026-09-01 — 60-day line through method note

- Human opened the 60-day line. Week 3 preregister on disk before CSVs.
- Classical gate: \(\theta_{\mathrm{class}}=0.03\). T1–T6 pass.
  Depths 1–5 vs 64. leftover_decision=true (one extra layer vs oracle
  on three cells). Artifacts: `week3_*.csv`, `notes/WEEK3_REPORT.md`.
- Week 4: 6-feature NumPy logistic, 13 train samples, deployable
  features only. T3 FAIL 5/6 at (0.75, 0.8). `beats_classical=false`.
  `paper1_go=false`. No widen, no retune. `notes/WEEK4_REPORT.md`.
- Weeks 5–6: `notes/METHOD_NOTE.md`. Weeks 7–8 not opened.
- No new K4AI id, no merge to `main`, no \(\Sigma_{\mathrm{VC}}\) on
  SCBA, no invented PASS, no Physics-for-AI claim.
- Next: none on this line unless a human reopens a new question.

## 2026-09-01 — slice closeout (not CERTIFY)

- Record: `notes/SLICE_CLOSEOUT.md`. Status: **切片结项，不是认证**.
- Three claim CSVs pinned by SHA-256: teacher map, Week 2, Week 3 gate.
- Four signed conventions unchanged. Week 4 verdict stays
  `paper1_go=false`. No gate repair. No merge to Keldysh4ai `main`.
- 11A remains archive. Later work, if any, is a new question with a
  new preregister.

## 2026-09-01 — live copy is this extract only

- Do not maintain `prototype/future-b-neural-poc` as a second live
  closeout. Pins, CSVs, and `notes/SLICE_CLOSEOUT.md` live here.

## 2026-09-01 — Candidate 1+2 joint closeout (W3)

- Record: `notes/C12_SWARM_REPORT.md`. Mixed weaker sentence (not
  Template A or B): C1-T3 PASS-SUFFICIENT and C2-T1 PASS.
- C1: T1 FAIL 15/17 (exceptions at (1.05,0.5)); T2 no leftover 0/12;
  T3 PASS-SUFFICIENT (mean test gap \(\approx 4.6\times 10^{-4}\)).
  Stop. `notes/C1_STOP.md` already on disk. No spectral gate.
- C2: T1 PASS on (1.05,0.5); T2 PASS (3 remainder cells);
  T3 PASS; `MA0_ATOMIC=PASS`. No `C2_STOP.md`. No router.
- `paper1_go` stays false. Week 2/3/4 CSVs not edited. Weeks 7–8 not
  opened. Swarm does not open a tiny gate.
- Next: none on Candidate 1. On Candidate 2 a human may later open a
  tiny gate; this swarm does not.

## 2026-09-18 — Diagram Compiler Task 2 cheap evaluator

- Isolated worktree from Task-1 HEAD `1185d81`, branch
  `diagram-compiler/task2-cheap-evaluator`. Original dirty
  `diagram-compiler/task1` checkout was not edited.
- Policy: `propagator_only_v1`. Semantics: `STATE_WEIGHT`.
  `ell_hat(x,y)=log W_hat(y)-log W_hat(x)`. Reciprocity by
  construction. No delayed acceptance. No Fortran. No P1 rewrite.
- Tests: Task-1 281 passed; Task-2 52 passed; exact 224/224 recheck
  max error `2.7755575615628914e-17`. Two-band cheap expensive
  primitives 0 vs exact 7/28/110 at n=1/2/3. Scalar cheap equals
  exact (not a scalar speedup).
- Evidence: `research/diagram_compiler/task2/`,
  `docs/DIAGRAM_COMPILER_TASK2.md`.
- Next: Task 3 delayed-acceptance kernel (not implemented).

## 2026-09-18 — Diagram Compiler Task 3 delayed acceptance

- Isolated worktree from Task-2 HEAD `a79bdf4`, branch
  `diagram-compiler/task3-delayed-acceptance`. Dirty Task-1 and
  Task-2 checkouts were not edited.
- Target: `positive_real_F_v1` (`pi=F` iff real, finite, `F>0`). Not
  `|F|`. Design B: Hastings only in Stage 2. Cheap score remains
  Task-2 STATE_WEIGHT.
- Demo two-band n=1: Stage-1 reject (no exact(y)), Stage-2 reject,
  accept. Finite-state balance residual 1.39e-17. No Fortran. No
  P1 rewrite. No speedup claim.
- Evidence: `research/diagram_compiler/task3/`,
  `docs/DIAGRAM_COMPILER_TASK3.md`.
- Next: Task 4 native KernelIR (not implemented).

## 2026-09-18 — Diagram Compiler Task 4 NativeKernelIR

- Isolated worktree from Task-3 HEAD `3822036`, branch
  `diagram-compiler/task4-native-kernel-ir`. Earlier worktrees were
  not edited.
- Typed SSA + CFG NativeKernelIR. Interpreter matches Task-3 on
  two-band n=1 Stage-1 reject / Stage-2 reject / accept. Exact ops
  unreachable on Stage-1 reject. No Fortran emitted. No speedup claim.
- Evidence: `research/diagram_compiler/task4/`,
  `docs/DIAGRAM_COMPILER_TASK4.md`.
- Next: Task 5 Fortran backend (not implemented).
