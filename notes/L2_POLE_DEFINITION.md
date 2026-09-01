# Periodic L=2 pole extractor — definition frozen before the 12-cell fill

Authority: HUMAN LOCK 2026-08-31. This file is the pole convention for
`E0_Born` and `E0_SCBA` on the frozen L=2 teacher map. It was written
**before** those twelve diagrammatic energies were computed. It does
not start Week 2, train a router, mix libraries, or reopen 11A.

Executable pin: `prototypes/future_b_neural_poc/l2_periodic_pole.py`.

## Geometry and origin (not reopened)

- Periodic $L=2$ only. Momenta $\{k=0,k=\pi\}$. No other $n_k$.
- $\xi_k=2t(1-\cos k)$, so $\xi_0=0$, $\xi_\pi=4t$.
- $t=1$. Code origin $E_0(g=0)=0$.
- Tadpole / Hartree OFF. No static shift is added by hand.
- $G(k,z)=1/(z-\xi_k-\Sigma(z))$. $\Sigma$ is local, hence
  $k$-independent, for this Holstein rainbow.

## Frozen numerical locks (written before compute)

| lock | value | status |
|---|---|---|
| $\eta$ | $10^{-4}t = 10^{-4}$ | PROJECT_CONVENTION, frozen |
| search window | $\omega\in[-8.0, 0.25]$ | PROJECT_CONVENTION, frozen |
| coarse grid | `np.linspace(-8.0, 0.25, 16501)` | PROJECT_CONVENTION |
| SCBA shift depth $N$ | 64 | PROJECT_CONVENTION, frozen |
| Born | one-shot on $G_0$ ($N=0$ tail) | kind lock |
| $E_0^{\mathrm{Born+VC}}$ | not defined here | stays `NOT_COMPUTED` |

Do not retune $\eta$, the window, or $N$ after seeing the table.

## What $E_0$ is

Let $z(\omega)=\omega+i\eta$ with the frozen $\eta$. Let $\Sigma(z)$
be Born or SCBA as below. For $k=0$,

$$
D(\omega)=z(\omega)-\Sigma\bigl(z(\omega)\bigr)
= \omega+i\eta-\Sigma(\omega+i\eta).
$$

$G(k=0,z)=1/D$. A **real-frequency pole** is a root of
$\operatorname{Re} D(\omega)=0$ in the **open** interval
$(-8.0,0.25)$. $E_0$ is the **lowest** such root.

This is the vanishing of the real part of the retarded denominator. It
is not an unlabeled argmax of the spectral function. If no interior
root exists, write `NOT_COMPUTED`. Do not substitute a peak location,
an open-chain energy, or a continuum $n_k\ge 4$ number.

Bisection refine on $\operatorname{Re} D$ to $10^{-14}$ after a
coarse sign change is part of the same definition, not a second
convention.

## Born (one-shot, $G_0$)

$$
\Sigma_{\mathrm{Born}}(z)=\frac{g^2}{2}\sum_{k\in\{0,\pi\}}
G_0(k,z-\Omega),\qquad
G_0(k,z)=\frac{1}{z-\xi_k}.
$$

No dressed $G$. No vertex block.

## SCBA (rainbow, dressed $G$)

$$
\Sigma_{\mathrm{SCBA}}(z)=\frac{g^2}{2}\sum_{k\in\{0,\pi\}}
G(k,z-\Omega),\qquad
G(k,z)=\frac{1}{z-\xi_k-\Sigma_{\mathrm{SCBA}}(z)}.
$$

Truncation: $\Sigma(z-(N+1)\Omega)=0$ with frozen $N=64$, then
the rainbow recurrence upward to $\Sigma(z)$. This is the definition
of SCBA for this extractor, not a license to import
`chain_scba.py`.

## Hard bans

- Do not call `src/keldysh4ai/future_b/hopping/chain_scba.py` (open chain).
- Do not call `crossing_block_poc.py` ($n_k\ge 4$).
- Do not add $\Sigma_{\mathrm{VC}}$ onto SCBA.
- Do not fill $E_0^{\mathrm{Born+VC}}$ from this extractor.
- Do not start Week 2, train a gate, merge to `main`, or create a K4AI id.

## Claim ceiling after a successful fill

Allowed: the frozen twelve cells have real `E0_Born` and `E0_SCBA`
under this same-origin L=2 definition, or a named cell is
`NOT_COMPUTED`.

Not allowed: “C0 is complete,” “Week 2 is open,” “SCBA wins at weak
coupling,” “$B_{\mathrm{VC}}$ passed the atomic limit,”
Physics-for-AI.
