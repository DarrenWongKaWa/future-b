# Week 1 report — finish C0 on L=2

Worker S (Science). Branch `prototype/future-b-neural-poc`.
HEAD at start: `d643a3678722c92c863c29066fc15f4c832eb0cc`.
Engineering checkpoint: `6aa77b7` L=2 ED green + cutoff table.
No new K4AI number. No merge to `main`. No commit from this worker.

## Preregistered labels (written before the table)

File: `notes/WEEK1_LABELS_PREREGISTER.md`.

That file was written to disk **before**
`prototypes/future_b_neural_poc/teacher_map_l2.csv` was generated and
before any twelve-cell `E0_ED` values were inspected. Labels use only

$$
\lambda = \frac{g^2}{2 t \Omega}
$$

with `t=1`, cuts `weak: λ<0.2`, `intermediate: 0.2 ≤ λ < 1`,
`strong: λ ≥ 1` (PROJECT_CONVENTION on this slice).

| g/t  | Ω/t | λ      | label        |
|------|-----|--------|--------------|
| 0.15 | 0.5 | 0.0225 | weak         |
| 0.15 | 0.8 | 0.0140625 | weak      |
| 0.15 | 2.0 | 0.005625 | weak       |
| 0.45 | 0.5 | 0.2025 | intermediate |
| 0.45 | 0.8 | 0.1265625 | weak      |
| 0.45 | 2.0 | 0.050625 | weak       |
| 0.75 | 0.5 | 0.5625 | intermediate |
| 0.75 | 0.8 | 0.3515625 | intermediate |
| 0.75 | 2.0 | 0.140625 | weak       |
| 1.05 | 0.5 | 1.1025 | strong       |
| 1.05 | 0.8 | 0.6890625 | intermediate |
| 1.05 | 2.0 | 0.275625 | intermediate |

Counts: 6 weak, 5 intermediate, 1 strong. Labels were not revised after
the table.

## Teacher CSV

Path: `prototypes/future_b_neural_poc/teacher_map_l2.csv`

Header (exact):
`g_over_t,omega_over_t,M_used,dim,E0_ED,DeltaE_cutoff,E0_Born,E0_SCBA,E0_Born_VC,note`

- `E0_ED`: **12/12 real** (not `WEEK1_INCOMPLETE`).
- Origin: `ξ_k=2t(1-cos k)`, `E0(g=0)=0`, periodic L=2,
  `src/keldysh4ai/future_b/teacher/holstein_ed.py`,
  `cutoff_kind=total_phonon_M`, `dim=(M+1)(M+2)`.
- Cutoff rule: smallest even `M` with `|E0(M)-E0(M-2)| < 1e-4 t`,
  scan even `M=0,2,…,20`. No cell needed `M>20`.
- `g=0` sanity (not a 13th row): `HolsteinL2ED(g=0)` gives `E0=0.0`.

| g/t  | Ω/t | M_used | dim | E0_ED | ΔE_cutoff | label |
|------|-----|--------|-----|-------|-----------|-------|
| 0.15 | 0.5 | 4 | 30 | -0.025011195833357803 | 2.499e-05 t | weak |
| 0.15 | 0.8 | 4 | 30 | -0.016411995814594443 | 2.783e-06 t | weak |
| 0.15 | 2.0 | 4 | 30 | -0.0075011729011287805 | 4.332e-08 t | weak |
| 0.45 | 0.5 | 8 | 90 | -0.22597056572509017 | 1.233e-06 t | intermediate |
| 0.45 | 0.8 | 6 | 56 | -0.14813779739257232 | 4.531e-06 t | weak |
| 0.45 | 2.0 | 4 | 30 | -0.06759567149368771 | 3.050e-05 t | weak |
| 0.75 | 0.5 | 10 | 132 | -0.6337558805587407 | 2.367e-05 t | intermediate |
| 0.75 | 0.8 | 8 | 90 | -0.4141522353421741 | 5.365e-06 t | intermediate |
| 0.75 | 2.0 | 6 | 56 | -0.18824875576961658 | 4.908e-07 t | weak |
| 1.05 | 0.5 | 14 | 240 | -1.2711554105515426 | 3.689e-05 t | strong |
| 1.05 | 0.8 | 10 | 132 | -0.821257338852671 | 1.029e-05 t | intermediate |
| 1.05 | 2.0 | 6 | 56 | -0.3704389369409427 | 1.324e-05 t | intermediate |

Strong corner `(g,Ω)=(1.05,0.5)`: recomputed; `E0_ED` **matches** the
accepted value `-1.2711554105515426` at `M=14`,
`ΔE0=3.689030338893673e-05 t`, `passes_1e-4=True`.

### Diagrammatic columns (honest tokens, not invented numbers)

| column | real cells | `NOT_COMPUTED` |
|---|---|---|
| `E0_Born` | 0 | 12 |
| `E0_SCBA` | 0 | 12 |
| `E0_Born_VC` | 0 | 12 |

Reasons (same for every cell; see CSV `note`):

- Library I (`crossing_block_poc.py`) is periodic with the signed
  `ξ_k`, but it returns $\Sigma(k,\omega)/G$, not a ground energy,
  and `PeriodicHolsteinModel` requires `n_k>=4` (not L=2).
- Library II (`chain_scba.py`) is an **open chain** with off-diagonal
  `-t`, not the signed periodic L=2 Hamiltonian
  `[[2t,-2t],[-2t,2t]]`. Open-chain `E0` is not an L=2 teacher number.
- No eta-stable same-origin L=2 pole extractor was admitted. Prefer
  `NOT_COMPUTED` over a wrong geometry or a noisy peak.

## Atomic-limit one-sentence verdict

**inconclusive:** on hop=0, bare Born+VC moves closer to the exact
linear CFE (`1,2,3,…`) than one-shot Born in 10/12 frozen couplings
and farther in 2/12, while its $O(g^4)$ coefficient equals the SCBA
series (`1,1,1,…`), not the exact series.

Details: `notes/ATOMIC_LIMIT_AUDIT.md`.

## Double-counting one-sentence verdict

**Default NO:** do not add $\Sigma_{\rm VC}$ onto SCBA; SCBA already
resums non-crossing rainbow / nested Born diagrams and does not sum
crossed phonon lines, and the libraries stay unmerged.

Details: `notes/DOUBLE_COUNTING_MEMO.md`.

## Claim ceiling

Twelve real `E0_ED` values exist on the frozen slice, so the strongest
allowed statement is:

**a real teacher comparison map exists for the frozen L=2 slice.**

This is not coverage beyond the slice. This is not architecture
evidence. This is not Physics-for-AI. `GENERIC_MODEL_SUFFICIENT`
remains a Born-versus-Born+VC proxy result and does not justify a
bigger network. L=2 ED green ≠ teacher coverage ≠ architecture
evidence; Week 1 supplies the ED column of a comparison map only.
Born/SCBA/Born_VC columns are `NOT_COMPUTED`, so Week 2 C1 utility
questions are **not** answered.

## Tests run

Interpreter: `/Users/kawawong/Research/Keldysh4ai/.venv/bin/python`
(Python 3.12.13). `python` is not on the default PATH in this shell.

```
cd /Users/kawawong/Research/Keldysh4ai-worktrees/future-b-neural-poc
PYTHONPATH=src python -m pytest tests/test_ed_limits.py -q
```

Observed: `13 passed in 0.15s`.

```
PYTHONPATH=src python -m pytest tests/test_teacher_map_l2.py tests/test_atomic_limit_audit.py -q
```

Observed: `8 passed in 0.10s` (teacher-map builder + hop=0 audit).

Builder/audit runs:

```
PYTHONPATH=src python prototypes/future_b_neural_poc/build_teacher_map_l2.py
PYTHONPATH=src python prototypes/future_b_neural_poc/atomic_limit_audit.py
```

`g0_sanity_E0=0.0`; strong-corner `matched_accepted_E0=True`; atomic
JSON verdict `inconclusive`.

## Files written

- `notes/WEEK1_LABELS_PREREGISTER.md`
- `notes/ATOMIC_LIMIT_AUDIT.md`
- `notes/DOUBLE_COUNTING_MEMO.md`
- `notes/WEEK1_REPORT.md`
- `prototypes/future_b_neural_poc/teacher_map_l2.csv`
- `prototypes/future_b_neural_poc/build_teacher_map_l2.py`
- `prototypes/future_b_neural_poc/atomic_limit_audit.py`
- `prototypes/future_b_neural_poc/atomic_limit_audit.json`
- `tests/test_teacher_map_l2.py`
- `tests/test_atomic_limit_audit.py`

## Files refused

- `notes/REPO_AUDIT.md`, `notes/CLEANUP_PLAN.md`,
  `notes/CONSTRAINTS_FUTURE_B.md`, `notes/SWARM_REPORT.md`,
  `AGENT_LOG.md` (other workers / root)
- rewrite of `notes/SCIENCE_LINE_60DAY.md`
- archive 11A rerun/rewrite/use as Future B proof
- any change to K4AI-592 / K4AI-593
- router / MLP training
- Week 2 Born/SCBA comparison tables
- adding $\Sigma_{\rm VC}$ onto SCBA
- changing $\xi_k$ back to $-2t\cos k$
- tadpole ON in libraries
- $\Phi$, Keldysh contour, Anderson–Holstein, GAAFET, NQS, DiagMC
- invented diagrammatic `E0` numbers
- new git worktree, new K4AI number, merge to `main`, git commit

STATUS: PASS
CLAIM: A real L=2 ED teacher comparison map exists for the frozen twelve-cell slice (12/12 E0_ED); Born/SCBA/Born_VC remain NOT_COMPUTED, which is not architecture evidence.
ARTIFACTS:
notes/WEEK1_LABELS_PREREGISTER.md
notes/ATOMIC_LIMIT_AUDIT.md
notes/DOUBLE_COUNTING_MEMO.md
notes/WEEK1_REPORT.md
prototypes/future_b_neural_poc/teacher_map_l2.csv
prototypes/future_b_neural_poc/build_teacher_map_l2.py
prototypes/future_b_neural_poc/atomic_limit_audit.py
prototypes/future_b_neural_poc/atomic_limit_audit.json
tests/test_teacher_map_l2.py
tests/test_atomic_limit_audit.py
TESTS: PYTHONPATH=src python -m pytest tests/test_ed_limits.py -q -> 13 passed in 0.15s; PYTHONPATH=src python -m pytest tests/test_teacher_map_l2.py tests/test_atomic_limit_audit.py -q -> 8 passed in 0.10s; g=0 ED E0=0.0; (1.05,0.5) E0_ED matches -1.2711554105515426
NEXT_DEPENDENCIES: Week 2 C1 teacher-backed Born-vs-SCBA comparison may start only after same-origin periodic L=2 E0_Born and E0_SCBA exist (currently 12/12 NOT_COMPUTED); no router, no library mix, no Sigma_VC on SCBA
