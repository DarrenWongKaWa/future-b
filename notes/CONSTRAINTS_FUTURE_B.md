# Future B live constraints

Authority: **HUMAN LOCK 2026-08-31**.
Applies to branch `prototype/future-b-neural-poc` and `prototypes/future_b_*`.
`notes/SCIENCE_LINE_60DAY.md` wins conflicts.

1. **This L=2 slice is closed (结项，不是认证).**
   Teacher map exists. Week 3 classical gate exists (\(\theta=0.03\)).
   Week 4 tiny logistic did not beat it (test matching 5/6;
   `paper1_go=false`). Do not widen the net, add features, or retune
   \(\theta\) to repair that negative. Paper 1 is not GO. Weeks 7–8
   stay closed. Do not train another router on this slice. A later
   question needs a new preregister; it is not a larger gate.
   Record: `notes/SLICE_CLOSEOUT.md`.

2. **Libraries stay separate.** Library I = bare Born + bare VC, uses
   $G_0$. Library II = SCBA, uses dressed $G$. Do not add
   $\Sigma_{\rm VC}$ onto SCBA. Default double-counting: **NO**.
   L=2 diagrammatic $E_0$ comes only from
   `l2_periodic_pole.py` ($k=0,\pi$). Not `chain_scba.py`, not
   $n_k\ge 4$.

3. **Do not change signed dispersion or tadpole.**
   $\xi_k=2t(1-\cos k)$, $E_0(g=0)=0$,
   $E_{\rm lecture}=E_{\rm code}-2t$.
   Tadpole/Hartree **OFF** in diagrammatic libraries. ED still contains
   $g\,n(b+b^\dagger)$.
   Papers: `notes/SIGNED_CONVENTION_SOURCES.md`, PDFs in `references/`.

4. **ED green ≠ teacher coverage ≠ paper / architecture evidence.**
   Engineering-green L=2 limits do not admit a router, a method paper,
   or Physics-for-AI.

5. **No 11A reopen.** No $\Phi$ / Keldysh / Anderson–Holstein /
   devices / NQS / DiagMC.

6. **Required process: tests + CSV + short `AGENT_LOG.md`. Nothing else.**
   1. No new K4AI IDs.
   2. No extra worktrees.
   3. No replay-hash / JSON-schema / thread-variable gates as compute blockers.
   4. No mapping C0–C4 onto Freeze/CERTIFY.
   5. No using K4AI-592/593 as live admission.
   6. Do not PASS 592/593.

7. **No invented numbers.** Missing quantities are `NOT_COMPUTED`.

8. **`GENERIC_MODEL_SUFFICIENT` is Born-vs-Born+VC proxy only.**
   Do not “fix” it by widening a network.

9. **Science line wins.** Human lock 2026-08-31.
   `notes/SCIENCE_LINE_60DAY.md` controls sequence, stop rules, and
   claim ceilings.

Hard stops: no merge to `main`; no training; no $\Sigma_{\rm VC}$ on
SCBA; no $\xi_k$ change; no tadpole ON; no Physics-for-AI claim;
no teacher-feature leakage; no invented numbers; no 11A.
