# 1% ground-state formation energy — documented, not pursued

**Status: `NOT_CERTIFIED` / `NOT_PURSUED`.**

Future B did **not** start C6/C7, did **not** launch 128 reference
chains, and did **not** invent a systematic remainder \(B=0\).

## Current fixed-setting numbers

Frozen Method0, \(20^3\), rank 20. Formation energy
\(Q=E_{\mathrm{polaron}}-E_{\mathrm{bare}}\) with
\(E_{\mathrm{bare}}=9.35487318746596053\,\mathrm{eV}\).

Historical C5 DEV (6 chains / arm):

| arm | \(Q\) (eV) | JK SE | rel. JK SE | point 95% HW | rel. 95% HW |
|---|---:|---:|---:|---:|---:|
| B0 | −0.250253260 | 2.368 meV | 0.946% | 6.088 meV | 2.433% |
| B-best | −0.247842001 | 3.712 meV | 1.498% | 9.541 meV | 3.850% |
| P1 | −0.249583768 | 2.343 meV | 0.939% | 6.023 meV | 2.413% |

Clean-P1 confirm (different batch, same setting): B-best
\(-0.251403\,\mathrm{eV}\) (rel. SE 0.826%, rel. HW 2.124%); P1
\(-0.246614\,\mathrm{eV}\) (rel. SE 1.358%, rel. HW 3.491%).

Wording that is allowed:

> For the frozen LiF \(20^3\)/rank20 configuration, the current
> statistical diagnostic uncertainty is at the few-percent level. We do
> not claim a 1% certified ground-state formation energy.

1% of \(\lvert Q\rvert\) is \(\approx 2.5\,\mathrm{meV}\). A 6 meV
half-width is about **2.4%**, not 1%. HAC failures mean even this
diagnostic is not a clean pass.

## What is statistical vs not certified

**Statistical (estimated, with caveats):** jackknife SE and HAC on
production blocks of a **fixed** discrete Hamiltonian. HAC 5/18 fail on
C5; confirm HAC also fail. Correlated-MC contract is therefore incomplete.

**Not certified:**

- projection-time remainder \(B_{\mathrm{projection}}\)
- perturbation-order / cap remainder \(B_{\mathrm{order}}\)
- numerical remainder \(B_{\mathrm{numerical}}\) (quadrature, SVD rank,
  interpolant)
- grid interpretation / finite \(20^3\)
- independent \(Q_{\mathrm{ref}}\) at the 1% contract

Literature (Luo et al. SI) has empirical LiF convergence plots. Those
are **not** this repository’s remainder budget \(B\). Do not set \(B=0\)
by citing the paper, and do not infer \(B\) from two nearby settings
alone.

## Two different scientific objects

1. **Fixed discrete Hamiltonian algorithm benchmark** (what we have):
   compare B0 / B-best / P1 at one frozen config.
2. **Thermodynamic / infinite-projection / fully converged material
   result** (what we do not have): the number you would put next to
   experiment or Table 1 of Luo et al. (\(-0.408\,\mathrm{eV}\)).

Our \(-0.25\,\mathrm{eV}\) is the right *order* for \(20^3\), not the
converged Table 1 value.

## If someone later wanted 1%

They would need, at least:

- projection-time convergence
- perturbation-order / cap control
- numerical remainder
- rank / grid interpretation where applicable
- independent \(Q_{\mathrm{ref}}\)
- correlated-MC statistics that actually pass a predeclared HAC/ESS rule
- an explicit systematic budget
  \(B=B_{\mathrm{projection}}+B_{\mathrm{order}}+B_{\mathrm{numerical}}\)

More Monte Carlo samples on the current setting **cannot** make a
systematic uncertainty disappear. Extra reference chains are not a
substitute for unresolved systematic control.

This list is documentation. It is **not** a Future B task.
