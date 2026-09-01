# Atomic-limit audit (hop = 0): Born, Born+VC, SCBA vs CFE series

Week 1 C0 companion to `prototypes/future_b_neural_poc/teacher_map_l2.csv`.
This audit is **not** an L=2 finite-`t` teacher energy. It does not
authorize mixing Library I and Library II, adding $\Sigma_{\rm VC}$
onto SCBA, or training.

Script: `prototypes/future_b_neural_poc/atomic_limit_audit.py`
Numbers: `prototypes/future_b_neural_poc/atomic_limit_audit.json`

## Setup (hopping absent)

- Geometry: $N=1$ atomic; momenta collapse.
- Code origin: $G_0(z)=1/z$.
- Tadpole / Hartree: OFF.
- Do **not** call `crossing_block_poc.PeriodicHolsteinModel` (`t>0`, `n_k>=4`).
- Couplings: the same frozen $(g,\Omega)$ list as Week 1, now at hop $=0$.
- Grid: $z=i\nu$, $\nu=\mathrm{geomspace}(0.1,20,128)$.
- Library I: one-shot Born and Born+VC on $G_0$.
  $$
  \Sigma_{\rm Born}(z)=g^2 G_0(z-\Omega)=\frac{g^2}{z-\Omega},
  $$
  $$
  \Sigma_{\rm VC}(z)=g^4 G_0(z-\Omega)^2 G_0(z-2\Omega)
  $$
  (collapsed App01 kernel from `notes/CROSSING_BLOCK_SOURCE.md`).
- Library II: T=0 SCBA family via `scba_constant_cfe` (coefficients $1,1,1,\ldots$).
- Exact atomic reference: `exact_t0_linear_cfe` (coefficients $1,2,3,\ldots$).
- Depth: 64.

Declared metric (in the script, before residuals): relative $L^2$ of
$G(z)=1/(z-\Sigma)$ versus the exact linear CFE. Verdict rule: the
B_VC-moves token is used only if Born+VC is closer to exact than Born
on **every** frozen $(g,\Omega)$ cell; the opposite token only if it
is farther on every cell; otherwise `inconclusive`.

## $O(g^4)$ series (SOURCE_DERIVED from the two CFEs)

Write $\Sigma = g^2/(z-\Omega) + c\, g^4/((z-\Omega)^2(z-2\Omega)) + O(g^6)$.

| object | $c$ |
|---|---|
| one-shot Born | 0 |
| Born + VC on $G_0$ | 1 |
| SCBA / constant CFE $1,1,1,\ldots$ | 1 |
| exact linear CFE $1,2,3,\ldots$ | 2 |

At hop $=0$ the nested rainbow and the crossed App01 graph have the
same value, so a single bare $\mathcal B_{\rm VC}$ supplies the SCBA
$g^4$ piece, not the exact doubled coefficient. Relative to Born,
$c: 0\to 1$ is closer to $2$, but it lands on the SCBA series, not
on $1,2,3,\ldots$.

## Relative $L^2$ versus exact CFE (from the JSON)

| $g$ | $\Omega$ | Born vs exact | Born+VC vs exact | SCBA vs exact | B_VC closer than Born? |
|---|---|---|---|---|---|
| 0.15 | 0.5 | 2.6389e-02 | 1.4691e-02 | 1.4008e-02 | yes |
| 0.15 | 0.8 | 6.8190e-03 | 3.5761e-03 | 3.5012e-03 | yes |
| 0.15 | 2.0 | 4.5310e-04 | 2.2844e-04 | 2.2760e-04 | yes |
| 0.45 | 0.5 | 8.6439e-01 | 7.5436e-01 | 6.5197e-01 | yes |
| 0.45 | 0.8 | 3.5743e-01 | 2.3525e-01 | 2.0705e-01 | yes |
| 0.45 | 2.0 | 2.8370e-02 | 1.5100e-02 | 1.4644e-02 | yes |
| 0.75 | 0.5 | 5.5570e-01 | 6.2677e-01 | 6.5757e-01 | **no** |
| 0.75 | 0.8 | 1.0255e+00 | 9.3354e-01 | 8.4106e-01 | yes |
| 0.75 | 2.0 | 1.3064e-01 | 7.5194e-02 | 6.9802e-02 | yes |
| 1.05 | 0.5 | 6.1317e-01 | 6.9027e-01 | 5.4766e-01 | **no** |
| 1.05 | 0.8 | 9.7256e-01 | 7.9985e-01 | 4.0292e-01 | yes |
| 1.05 | 2.0 | 3.6394e-01 | 2.3114e-01 | 2.0503e-01 | yes |

Ten of twelve cells move closer to the exact CFE; the two largest
$\lambda=g^2/(2t\Omega)$ cells on this list ($g=0.75,\Omega=0.5$ and
$g=1.05,\Omega=0.5$) do not. One-shot Born+VC is not a resummation.

## Verdict

inconclusive

Default remains: do not add $\Sigma_{\rm VC}$ onto SCBA. The $O(g^4)$
coefficient that $\mathcal B_{\rm VC}$ adds on $G_0$ is already the
SCBA-family coefficient, not the exact linear coefficient. That is a
reason to keep the libraries separate, not a reason to stack them.

This audit does not produce L=2 teacher $E_0$ values and does not
reopen K4AI-565/568/570/592/593 or archive 11A.
