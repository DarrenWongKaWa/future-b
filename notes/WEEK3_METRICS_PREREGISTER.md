# Week 3 metrics — preregistered before any gated SCBA table

Authority: HUMAN LOCK 2026-08-31 plus the human open of the 60-day
line (Week 3 classical stopping). Binding constraints:
`notes/CONSTRAINTS_FUTURE_B.md`. Sequence and claim-ceiling language
in `notes/SCIENCE_LINE_60DAY.md` remain in force.

This file is written **before**
`prototypes/future_b_neural_poc/week3_depth_scan.csv`,
`prototypes/future_b_neural_poc/week3_gated_vs_fixed.csv`,
`prototypes/future_b_neural_poc/week3_theta_selection.csv`, and
**before** `notes/WEEK3_REPORT.md`. Split, residual, \(\theta\) grid,
matching grain, cost units, leftover rule, and tests T1–T6 depend only
on \((g,\Omega,t)\), on the signed rainbow depth, and on the formulas
below. They are not fitted to \(|\Delta|\) values, depths, or residuals.
Cuts, the split, and the \(\theta\) grid will not be moved after seeing
errors.

Week 3 implements the classical stopping rule

$$
\frac{\|\Delta\Sigma\|}{\|\Sigma\|}<\theta_{\mathrm{class}}
$$

on the frozen periodic \(L=2\) SCBA rainbow. It does not rerun L=2 ED,
does not edit `holstein_ed.py` or `l2_periodic_pole.py`, does not
change \(\eta\), \(L\), \(\xi_k\), tadpole, or `SCBA_DEPTH=64`, does
not call `chain_scba.py`, does not invent \(E_0^{\mathrm{Born+VC}}\),
and does not train a router, MLP, or GRU.

## Frozen slice and signed conventions (not reopened)

- \(t = 1\)
- \(g/t \in \{0.15, 0.45, 0.75, 1.05\}\)
- \(\Omega/t \in \{0.5, 0.8, 2.0\}\)
- twelve cells
- \(\xi_k = 2t(1-\cos k)\), so \(E_0(g=0)=0\)
- translator \(E_{\mathrm{lecture}}=E_{\mathrm{code}}-2t\)
- tadpole / Hartree OFF
- Library I and Library II remain separate
- default **NO** \(\Sigma_{\mathrm{VC}}\) on SCBA
- 11A unused
- \(E_0^{\mathrm{Born+VC}}\) stays `NOT_COMPUTED`
- pole definition unchanged: \(\eta=10^{-4}\), window \([-8.0,0.25]\),
  coarse grid `np.linspace(-8.0, 0.25, 16501)`, \(E_0\) = lowest
  interior \(\operatorname{Re} D=0\) of \(G(k=0)\)

Immutable input: `prototypes/future_b_neural_poc/teacher_map_l2.csv`
at teacher-map commit `e6a14f6`. Those \(E_0\) values are not
recomputed here. Fixed-maximum SCBA is the already-recorded
`E0_SCBA` column (rainbow depth \(N=64\)).

## What is being gated

The live extractor’s SCBA is the nested T=0 rainbow of depth \(n\),
with tail \(\Sigma(z-(n+1)\Omega)=0\). Depth \(n=0\) is one-shot Born.
Depth \(n=64\) is frozen fixed-maximum SCBA. Successive integer depths
are the inner iterations of this approximation. Week 3 does **not**
switch diagram class (no Born-versus-SCBA routing, no VC).

## Residual (deployable; no teacher)

Diagnostic frequency, PROJECT_CONVENTION:

$$
z_{\mathrm{diag}}=0+i\eta.
$$

This is the code-origin band bottom. It does not use \(E_0^{\mathrm{ED}}\),
teacher errors, or admission labels. It lies on the frozen coarse grid.

Let \(\Sigma^{(n)}(z)\) be `rainbow_sigma(..., depth=n)`. For
\(n\in\{1,\ldots,64\}\):

```
r_n = |Σ^{(n)}(z_diag) − Σ^{(n−1)}(z_diag)| / max(|Σ^{(n)}(z_diag)|, ε_norm)
```

with \(\varepsilon_{\mathrm{norm}}=10^{-30}\). The gate uses this
scalar residual (Holstein \(\Sigma\) is local). A secondary coarse-grid
\(L^2\) residual is **recorded** and is **not** used to choose
\(\theta_{\mathrm{class}}\):

```
R_n = ||Σ^{(n)} − Σ^{(n−1)}||_2 / max(||Σ^{(n)}||_2, ε_norm)
```

over the frozen 16501-point coarse grid.

Stop at the smallest \(n\in\{1,\ldots,64\}\) with \(r_n<\theta\).
If none, use \(n=64\). Then \(E_0\) is the signed lowest interior
\(\operatorname{Re} D=0\) root at that depth. Depth \(n=0\) is never
a gated SCBA stop (the rule needs two successive \(\Sigma\)).

## Declared train / test split (from \((g,\Omega)\) only)

Six / six. Each \(\Omega\) appears on both sides. The unique Week-2
strong cell is in **train** so \(\theta\) is not chosen blind to that
corner. Held-out cells still include \(g/t=1.05\) at the other two
\(\Omega\).

**Train** (choose \(\theta_{\mathrm{class}}\) only here):

```
(0.15, 0.5), (0.15, 2.0), (0.45, 0.8),
(0.75, 0.5), (0.75, 2.0), (1.05, 0.5)
```

**Test** (frozen \(\theta\), no retune):

```
(0.15, 0.8), (0.45, 0.5), (0.45, 2.0),
(0.75, 0.8), (1.05, 0.8), (1.05, 2.0)
```

The split is not revised after seeing depths or errors.

## \(\theta\) grid and selection (train only)

Candidate grid, PROJECT_CONVENTION, not fitted:

```
θ ∈ {1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4,
     3e-5, 1e-5, 3e-6, 1e-6, 1e-7, 1e-8}
```

Matching grain: \(10^{-4}t\), the same absolute grain as the ED cutoff.

For a cell and a candidate \(\theta\), let \(n(\theta)\) be the gated
depth and \(E_0(\theta)\) the pole at that depth. Let
\(E_0^{(64)}\) be teacher-map `E0_SCBA`. Let

```
Δ_X = E0_X − E0_ED
```

**Match** on a cell iff \(E_0(\theta)\) is finite and

```
|Δ_gated| ≤ |Δ_fixed| + 1e-4 t
```

That is the declared “matched target error against ED”: gated SCBA is
allowed to be no worse than fixed-maximum SCBA by more than the ED
cutoff grain.

**Selection:** the **largest** \(\theta\) on the grid such that **every**
train cell matches. Largest \(\theta\) is the cheapest admissible
classical gate. If no grid value matches all six train cells, write
`theta_class=NOT_ADMISSIBLE` and do not claim an error–cost
improvement.

After selection, freeze \(\theta_{\mathrm{class}}\) and apply it to
test cells with no retune.

## Cost units (deployable algorithm)

The deployable gated algorithm is: scan \(r_n\) at \(z_{\mathrm{diag}}\)
only, then one pole search at the stopped depth.

```
n_layer              = depth_used + 1
n_green_pole         = 2 * n_layer * 16501
n_green_discover     = (depth_used + 1) * (depth_used + 2)
n_green_gated_total  = n_green_pole + n_green_discover
n_green_fixed        = 2 * 65 * 16501
```

Fixed-maximum SCBA does not pay discovery. `n_green_discover` at one
frequency is negligible next to the pole grid; it is still counted.
This experiment may compute a full depth scan in order to fill the
CSV; that offline scan is **not** the deployable cost.

## Oracle depth (analysis only; not a gate)

For leftover-decision accounting only:

```
n_oracle = smallest n ∈ {1,…,64} with |E0(n) − E0_ED| ≤ |E0_64 − E0_ED| + 1e-4 t
```

If none, `n_oracle=64`. This uses teacher energies. It is **not** a
deployable feature and **not** \(\theta_{\mathrm{class}}\).

## Leftover decision (whether Week 4 may start)

A leftover decision exists **only if all** of the following hold:

1. `theta_class` is admissible;
2. matching holds on all six test cells;
3. mean `n_green_gated_total` on test is strictly less than
   `n_green_fixed`;
4. mean `n_oracle` on test is strictly less than mean `depth_used`
   of the classical gate on test (the residual rule leaves savings
   an ED-using oracle could take).

If (1)–(3) hold and (4) fails, the classical residual gate already
matches the oracle at this grain: **no neural question**. If matching
fails, or extra depth is unstructured, or the gate does not beat
fixed-maximum cost, stop neural escalation. Do not train a router
to rescue a failed or empty Week 3.

## Tests T1–T6 (rules only; not evaluated in this file)

T1 Same-origin lock: for every cell, the scan’s \(E_0\) at depth 64
equals teacher-map `E0_SCBA` at float equality. Fail Week 3 if any
cell differs. Do not replace a mismatch with an invented number.

T2 Train matching: selected \(\theta_{\mathrm{class}}\) is a grid
value (not `NOT_ADMISSIBLE`) and all six train cells match. If this
fails, write `notes/WEEK3_STOP.md` and do not claim improvement.

T3 Test matching: frozen \(\theta_{\mathrm{class}}\) matches all six
test cells. Fail the improvement claim if any test cell violates; do
not retune \(\theta\).

T4 Cost: on test, mean `n_green_gated_total` < `n_green_fixed` and
mean `depth_used` < 64. If matching holds but T4 fails, the classical
gate is equivalent to fixed-maximum at the required accuracy–cost
point.

T5 Structure: `depth_used` is non-decreasing in \(g\) at each fixed
\(\Omega\), and non-increasing in \(\Omega\) at each fixed \(g\), with
at most one minor exception recorded as a note, not a rescue sweep.
Unstructured extra work stops neural escalation.

T6 Physical signs: for \(g>0\), every finite gated \(E_0\) satisfies
\(E_0^{\mathrm{ED}} < E_0^{\mathrm{gated}} < 0\). Fail if any cell
violates unless the pole search is a documented `NOT_COMPUTED`.

T1 fail or T6 fail: write `notes/WEEK3_STOP.md`. Do not soften
thresholds.

## Analysis CSVs (declared schema; not written yet)

Path: `prototypes/future_b_neural_poc/week3_depth_scan.csv`

```
g_over_t,omega_over_t,depth,E0,abs_D,n_crossings,
sigma_diag_re,sigma_diag_im,rel_sigma_diag,rel_sigma_l2,note
```

780 data rows (12 cells × depths \(0,\ldots,64\)). `rel_sigma_*` at
depth 0 is empty. `E0` may be `NOT_COMPUTED`.

Path: `prototypes/future_b_neural_poc/week3_gated_vs_fixed.csv`

```
g_over_t,omega_over_t,lambda,band,split,theta_class,
E0_ED,E0_SCBA_fixed,E0_gated,depth_gated,depth_oracle,
rel_sigma_at_stop,delta_fixed,delta_gated,rel_fixed,rel_gated,
match_grain_ok,n_green_fixed,n_green_gated_total,note
```

`band` follows Week-2 cuts (\(\lambda<0.08\) weak, \(\lambda\ge 0.80\)
strong). `split` is `train` or `test`. `E0_Born_VC` is not a column.

Path: `prototypes/future_b_neural_poc/week3_theta_selection.csv`

```
theta_class,admissible,n_train_match,n_test_match,
mean_depth_gated_train,mean_depth_gated_test,mean_depth_oracle_test,
leftover_decision,note
```

One data row. `leftover_decision` is lowercase `true`/`false`.

## What this preregister does not authorize

- training a router, MLP, or GRU
- mixing Library I and Library II
- adding \(\Sigma_{\mathrm{VC}}\) onto SCBA
- filling \(E_0^{\mathrm{Born+VC}}\)
- changing \(\eta\), \(L\), \(\xi_k\), tadpole, or `SCBA_DEPTH`
- calling `chain_scba.py`
- using archive 11A, K4AI-592, or K4AI-593 as Future B proof
- treating `GENERIC_MODEL_SUFFICIENT` as a teacher-backed result
- claiming architecture, conservation, or Physics-for-AI
- enlarging the twelve-cell grid
- moving the split, \(\theta\) grid, or matching grain after seeing errors
- using \(E_0^{\mathrm{ED}}\), teacher errors, or admission labels as
  deployable gate features
