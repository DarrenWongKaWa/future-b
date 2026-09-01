# Future B — 60-Day Scientific Line

Authority: **HUMAN LOCK 2026-08-31**.  If this plan and
`notes/REPO_AUDIT.md` disagree, this plan wins.

## Scientific order

The next two months test, in this order:

1. whether a real L=2 ED teacher map can be built;
2. whether Born and SCBA have structured, physically credible regions of use;
3. whether a classical adaptive stopping rule improves the error–cost tradeoff;
4. only conditionally, whether a tiny learned gate beats that classical rule;
5. only conditionally, whether typed physical blocks and routing beat a
   matched generic alternative.

A later week cannot rescue a failed earlier week.  Fixed diagram blocks and
the Dyson update remain physics; learning, if admitted at all, is restricted to
routing/stopping.

The signed conventions are binding:

- \(\xi_k=2t(1-\cos k)\), so \(E_0(g=0)=0\);
- the translator is \(E_{\rm lecture}=E_{\rm code}-2t\);
- tadpole/Hartree is OFF in the diagrammatic libraries;
- ED still contains \(g\,n(b+b^\dagger)\);
- Library I and Library II remain separate;
- no \(\Sigma_{\rm VC}\) may be added to SCBA without a written
  disjoint-diagram memo.

## Week 0 — completed engineering checkpoint

### Prerequisite and question

The problem, conventions, and two-library boundary were frozen before the
minimal ED check.  The question was only whether the periodic L=2
phonon-Fock implementation satisfied its signed limits.

### Recorded output

- Library I and Library II exist separately and differ at \(g/t=0.45\).
- `tests/test_ed_limits.py`: **13 passed** at commit `6aa77b7`.
- `prototypes/future_b_neural_poc/ed_cutoff_table.csv`: **11 data rows**,
  \(M=0,2,\ldots,20\).
- At \(g=1.05\), \(\Omega=0.5\), the first cutoff satisfying the signed
  energy check is \(M=14\), with
  \(E_0=-1.2711554105515426\) and
  \(\Delta E_0=3.689\times10^{-5}t\).
- `GENERIC_MODEL_SUFFICIENT` remains a Born-versus-Born+VC proxy-task result.
  It was not teacher-backed and neither establishes nor falsifies Future B.

### Stop rule and claim ceiling

Week 0 is complete.  Its strongest statement is: **the L=2 ED implementation
is engineering-green under the signed checks**.  Teacher coverage, controller
gain, and architecture evidence are all **NOT_COMPUTED**.

## Week 1 — finish C0 on L=2

### Prerequisite and question

Use the existing L=2 implementation without changing the signed conventions.
Ask whether a usable teacher comparison map exists on the frozen grid

\[
g/t\in\{0.15,0.45,0.75,1.05\},\qquad
\Omega/t\in\{0.5,0.8,2.0\}.
\]

### Required output

Create one teacher-map CSV with real values and these columns:

- `g_over_t`;
- `omega_over_t`;
- `E0_ED`;
- `E0_Born`;
- `E0_SCBA`;
- optional `E0_Born_VC`;
- `DeltaE_cutoff`;
- `note`.

If an optional quantity is not physically defined and computed under the same
convention, write `NOT_COMPUTED`; never substitute an inferred number.

Also produce:

- an atomic-limit audit of \(B_{\rm VC}\) against the continued-fraction
  coefficient sequences \(1,1,1,\ldots\) and \(1,2,3,\ldots\);
- a double-counting memo whose default is **NO adding VC onto SCBA**.

Weak/intermediate labels, any split, and all comparison conventions must be
declared before looking at the completed table.

### Stop rule and claim ceiling

Stop this scientific line if cutoff convergence fails on more than one
weak/intermediate cell, or if ED and momentum-space conventions cannot be
translated consistently.

After success, the strongest allowed statement is: **a real teacher comparison
map exists for the frozen L=2 slice**.  This is not coverage beyond the slice
and is not architecture evidence.

## Week 2 — C1 correctness against the teacher

### Prerequisite and question

Week 1 must have produced an admissible teacher map.  Carry forward the signed
checks \(g=0\) and one-shot Born \(\ne\) SCBA.  Then ask:

> Does SCBA improve on one-shot Born in weak coupling and lose that advantage
> in strong coupling when both are judged against ED?

This is a future test, not an observed result.

### Required output

Produce a teacher-backed Born/SCBA comparison table with the same observable,
sign convention, and spectral convention in every cell.  Record physical
signs and spectral behavior, including negative findings.

### Stop rule and claim ceiling

Stop if SCBA is not better than one-shot Born at weak coupling, or if signs or
spectra are unphysical.

After success, the strongest allowed statement is: **approximation utility has
a physically credible region dependence on the frozen L=2 slice**.  Solver
difference alone does not prove adaptivity or learning is useful.

## Week 3 — adaptive policy, still no architecture claim

### Prerequisite and question

Weeks 1–2 must show a structured teacher-backed decision.  Implement the
classical stopping rule

\[
\frac{\|\Delta\Sigma\|}{\|\Sigma\|}<\theta_{\rm class},
\]

with \(\theta_{\rm class}\) chosen only on a declared train split.

### Required output

Compare fixed-maximum SCBA with classically gated SCBA at matched target error
against ED, including the gate's compute cost.  No learned gate is allowed in
this week.

### Stop rule and claim ceiling

Stop neural escalation if useful extra work is unstructured in
\((g,\Omega)\), or if the classical gate already matches the fixed-maximum
method at the required accuracy–cost point.

After success, the strongest allowed statement is: **a classical adaptive
stopping rule improves the slice's error–cost behavior**.  This is not neural
or Physics-for-AI architecture evidence.

## Week 4 — tiny learned gate, or skip

### Prerequisite and question

Proceed only if Week 3 leaves a real decision that the classical gate does not
already solve.  Train one tiny CPU gate on deployable inference features only.
Teacher values, teacher errors, and teacher admission labels are forbidden
features.

### Required output

Compare the tiny gate with the classical gate under the same target-error and
cost accounting, including inference cost.  Optional L=4 ED is permitted only
if the L=2 map is clean and memory is acceptable; otherwise it remains
`NOT_COMPUTED`.

### Stop rule and claim ceiling

Stop immediately on teacher-feature leakage.  If the learned gate does not
beat the classical gate after cost, preserve that negative result, skip Paper
1, and continue only to the method note.

The strongest possible positive statement is: **a tiny learned gate improves
on the classical stopping rule for this frozen slice**.  Diagram-derived
architecture gain remains untested.

## Weeks 5–6 — write the method note

### Prerequisite and question

Use whatever survived Weeks 1–4; do not require a positive neural result.
Ask only what the evidence actually supports.

### Required output

Write a 2–4 page method note containing the question, frozen slice, teacher
table, gate table, cost accounting, negative results, and limitations.

Paper 1 becomes `GO` only if Week 4 shows a real learned advantage after cost.
Otherwise close with the strongest supported weaker result: teacher map,
approximation regions, classical gate, or learned-gate negative result.

### Stop rule and claim ceiling

Implementation completeness never upgrades claim strength.  If Paper 1 is not
`GO`, stop the architecture branch after the method note.

## Weeks 7–8 — only if Paper 1 is GO

### Prerequisite and question

Week 4 must have shown a real learned advantage after cost.  Then ask whether
typed physical blocks and routing contribute beyond one matched generic
alternative.

### Required output

Run Experiment A lite only:

- one matched generic baseline;
- one ablation replacing/removing typed physical blocks;
- one ablation removing routing.

### Stop rule and claim ceiling

If no advantage remains after matching information and cost, reject the
Physics-for-AI claim for this slice and stop the line.

The strongest possible positive statement is limited to this controlled
slice: **typed physical blocks and routing contribute beyond one matched
generic alternative**.  It does not establish a general many-body
Physics-for-AI architecture.

## Claim strength follows evidence

| Evidence available | Strongest defensible statement |
|---|---|
| L=2 limits and cutoff table | L=2 ED is engineering-green. |
| Frozen-grid ED teacher table | A teacher comparison map exists for this L=2 slice. |
| Teacher-backed Born/SCBA comparison | Approximation utility varies credibly across this slice. |
| Classical and, conditionally, learned gate with cost | Adaptive stopping helps; neural gain exists only if it beats the classical rule. |
| Matched generic baseline plus typed/routing ablations | Limited architecture evidence exists for this slice only. |

## What stops the whole Future B line

Stop and write the strongest defensible closeout if any of the following
occurs:

1. the Week 1 teacher map cannot be established under the signed cutoff and
   convention rules;
2. ED and momentum-space conventions cannot be translated consistently;
3. Week 2 produces unphysical signs/spectra or fails the weak-coupling sanity
   check;
4. useful extra computation is unstructured in \((g,\Omega)\);
5. the classical gate is sufficient, leaving no justified neural question;
6. the learned gate fails to beat the classical gate after cost;
7. the matched architecture test shows no gain attributable to typed blocks or
   routing;
8. evidence is contaminated by teacher leakage, a convention change,
   cross-library mixing, or use of 11A as architecture evidence.

A stop produces a negative or limited method note.  It does not authorize a
replacement sweep, relaxed threshold, larger network, or new physical model.

## Explicitly outside the next two months

- \(\Phi\)-learning or a \(\Phi\)-derivable network;
- Keldysh/nonequilibrium implementation;
- Anderson–Holstein;
- GAAFET or any other device application;
- NQS;
- DiagMC implementation;
- transport or realistic-material extensions;
- adding \(\Sigma_{\rm VC}\) to SCBA;
- widening a network to repair a negative result;
- router training before the teacher map and classical gate exist;
- a new mPFDNN, NQS-tutorial, or LLM–Hartree–Fock reading program;
- new K4AI task numbers, new worktrees, or certification scaffolding for the
  prototype slice;
- mapping C0–C4 onto the old Freeze/CERTIFY machinery.

The optional L=4 check remains conditional on Week 4 and is not a second model
line.

## 11A archive boundary

11A stays frozen and unused by this scientific line:

- do not rerun, rewrite, or delete its numbers;
- do not use them as labels, training data, baselines, priors, or architecture
  evidence;
- do not transfer its inverse-problem claim, gate status, or certification to
  Future B;
- do not use K4AI-592 or K4AI-593 as live admission gates for this periodic
  prototype, and do not change their recorded states;
- historical references to 11A must say explicitly that it is unused as Future
  B architecture evidence.

## Planning references only

The Future B chapter, Berciu–Goodvin, Mitrić et al.,
Mishchenko–Nagaosa–Prokof'ev, and the cited atomic-limit continued fractions
may guide interpretation.  They are not new implementation tickets and do not
start a new reading program.
