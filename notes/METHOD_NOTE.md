# Method note — periodic \(L=2\) Holstein teacher map and adaptive SCBA stopping

**切片结项，不是认证.** Slice: Future B live extract. Authority:
HUMAN LOCK 2026-08-31 and `notes/SCIENCE_LINE_60DAY.md`. This note is
the Weeks 5–6 closeout. It is not a journal paper, not CERTIFY, and
not a Physics-for-AI claim. Locked sentence:
`notes/SLICE_CLOSEOUT.md`.

## 1. Question

On a frozen one-electron Holstein ring, do one-shot Born and SCBA have
structured regions of use versus exact diagonalization, and does an
adaptive inner-loop stopping rule improve the error–cost tradeoff of
SCBA? If a classical residual gate already does that job, a learned
gate is admitted only when it beats the classical rule after cost, on
deployable features, with no teacher leakage.

The Hamiltonian and origin are signed:

\[
H=2tn-t\sum_{\mathrm{PBC}}(c^\dagger c+\mathrm{h.c.})
+\Omega b^\dagger b+g n(b+b^\dagger),\qquad
\xi_k=2t(1-\cos k),\qquad E_0(g=0)=0.
\]

Tadpole/Hartree is off in the diagrammatic libraries. Library I (bare
Born \(\pm\) VC on \(G_0\)) and Library II (SCBA on dressed \(G\)) stay
separate. Default: do not add \(\Sigma_{\mathrm{VC}}\) onto SCBA
(`notes/DOUBLE_COUNTING_MEMO.md`). \(E_0^{\mathrm{Born+VC}}\) is
`NOT_COMPUTED` in every cell.

## 2. Frozen slice and teacher

Grid, \(t=1\):

\[
g/t\in\{0.15,0.45,0.75,1.05\},\qquad
\Omega/t\in\{0.5,0.8,2.0\}
\]

(12 cells). Dimensionless coupling \(\lambda=g^2/(2t\Omega)\).

Teacher: periodic \(L=2\) ED, total-phonon cutoff, smallest even \(M\)
with \(|E_0(M)-E_0(M-2)|<10^{-4}t\)
(`src/keldysh4ai/future_b/teacher/holstein_ed.py`,
`prototypes/future_b_neural_poc/teacher_map_l2.csv`).

Diagrammatic \(E_0\): lowest interior \(\operatorname{Re} D(\omega)=0\)
of \(G(k=0)\), \(\eta=10^{-4}\), window \([-8.0,0.25]\), SCBA depth 64
(`l2_periodic_pole.py`). One-shot Born is depth 0 on \(G_0\).

Strong corner \((1.05,0.5)\): \(M=14\),
\(E_0^{\mathrm{ED}}=-1.2711554105515426\),
\(\Delta E_0=3.689\times10^{-5}t\).

## 3. Approximation regions (Week 2)

Artifact: `week2_born_scba_vs_ed.csv`, `notes/WEEK2_REPORT.md`.
Cuts (Week 2 only): weak \(\lambda<0.08\) (4 cells), strong
\(\lambda\ge0.80\) (1 cell).

T1–T4 passed. On every cell \(E_0^{\mathrm{ED}}<E_0^{\mathrm{SCBA}}<E_0^{\mathrm{Born}}<0\).
SCBA is closer to ED than one-shot Born in 12/12 cells. Relative SCBA
error versus ED increases with \(g\) at fixed \(\Omega\) and as
\(\Omega\) decreases at fixed \(g\) (17/17). At the strong cell,
\(\mathrm{rel}_{\mathrm{SCBA}}=0.37357\ge0.20\): SCBA underbinds versus
ED, not versus Born.

Allowed sentence: on this slice, Born and SCBA have structured,
physically credible regions of use versus ED. Not adaptivity, not
learning, not architecture.

## 4. Classical gate (Week 3)

Artifact: `week3_gated_vs_fixed.csv`, `week3_theta_selection.csv`,
`notes/WEEK3_REPORT.md`. Preregister:
`notes/WEEK3_METRICS_PREREGISTER.md`.

Inner iteration is rainbow depth \(n\). Deployable residual at
\(z_{\mathrm{diag}}=0+i\eta\):

\[
r_n=\frac{\lvert\Sigma^{(n)}-\Sigma^{(n-1)}\rvert}{\max(\lvert\Sigma^{(n)}\rvert,10^{-30})}.
\]

Stop at the smallest \(n\in\{1,\ldots,64\}\) with \(r_n<\theta\).
\(\theta_{\mathrm{class}}=0.03\) is the largest grid value that matches
fixed-maximum SCBA versus ED to \(10^{-4}t\) on all six **train**
cells. Test cells were not used to choose \(\theta\).

T1–T6 passed. Gated depths are 1–5 against fixed depth 64. Mean test
deployable Green count \(1.045\times10^5\) versus \(2.145\times10^6\).
Depth is monotone in \((g,\Omega)\) (17/17). An ED oracle is cheaper
by one layer on three cells (one held-out), so leftover_decision is
true.

Allowed sentence: a classical adaptive stopping rule improves this
slice’s SCBA error–cost behavior versus fixed-maximum depth 64. Not
neural. Not Physics-for-AI.

## 5. Learned gate (Week 4) — negative

Artifact: `week4_learned_vs_classical.csv`, `week4_verdict.csv`,
`notes/WEEK4_REPORT.md`. Preregister:
`notes/WEEK4_METRICS_PREREGISTER.md`.

One NumPy logistic regressor, 6 deployable features
\((g,\Omega,\lambda,n/64,\log_{10} r_n,\lvert\Sigma\rvert)\), 7
parameters, 4000 GD steps, lr \(0.1\), L2 \(10^{-2}\), trained on 13
\((cell,n)\) samples from the train oracle trajectory. Forbidden as
features: teacher energies, teacher errors, oracle depth, band strings.

T1 leakage pass. Train matching 6/6. Test matching **5/6**. Fail cell
\((0.75,0.8)\): learned depth 2 versus classical/oracle 3, grain
violated by \(\sim1.2\times10^{-4}t\). Mean test cost is lower only
because of that illegal early stop. `beats_classical=false`.
`paper1_go=false`. The net was not widened.

## 6. What this does not show

- Typed physical blocks plus routing beating a matched generic model
  (Weeks 7–8 were not opened).
- A generating functional, Keldysh contour, Anderson–Holstein, devices,
  or DiagMC.
- That SCBA is accurate at strong/adiabatic coupling (it is not, versus
  ED).
- That 11A or `GENERIC_MODEL_SUFFICIENT` is Future B evidence.

## 7. Limitations

Twelve cells, \(L=2\) only. The classical leftover versus oracle is at
most one rainbow layer. The learned gate had 13 training samples. Cost
counts a logistic evaluation as one Green evaluation (overcharge).
Pole \(E_0\) is a scalar readout of \(G(k=0)\), not a full spectrum.
VC remains `NOT_COMPUTED`.

## 8. Strongest defensible closeout

A real L=2 ED/Born/SCBA teacher map exists on the frozen twelve-cell
grid. SCBA improves on one-shot Born in weak coupling and loses
accuracy versus ED at large \(\lambda\) / small \(\Omega\). A classical
residual stop at \(\theta=0.03\) matches depth-64 SCBA versus ED to
the cutoff grain at a small fraction of the Green cost. A tiny learned
gate does not beat that classical rule after cost. Paper 1 is not GO.
Architecture ablations are not run.
