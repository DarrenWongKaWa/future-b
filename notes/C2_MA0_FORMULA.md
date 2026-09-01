# MA(0) formula lock — written before any twelve-cell \(E_0^{\mathrm{MA0}}\)

Authority: Future B Candidate 2. This file quotes the Momentum Average
MA(0) self-energy that will be implemented in
`prototypes/future_b_neural_poc/ma0_l2.py`. It is written **before**
those twelve \(E_0^{\mathrm{MA0}}\) values are computed.
Luo 2025 is related work only, not a formula source.

Executable: `prototypes/future_b_neural_poc/ma0_l2.py`.
Must not import `chain_scba` or `crossing_block`.
Must not add \(\Sigma_{\mathrm{VC}}\) onto SCBA.

## Papers

1. G. L. Goodvin, M. Berciu, and G. A. Sawatzky, *The Green’s
   function of the Holstein polaron*, Phys. Rev. B **74**, 245104
   (2006), arXiv:cond-mat/0609597.
   PDF: `references/cond-mat-0609597-goodvin-berciu-sawatzky-prb-74-245104.pdf`.
   Original MA continued fraction, here identified as MA(0).

2. M. Berciu and G. L. Goodvin, *Systematic improvement of the
   Momentum Average approximation for the Green’s function of a
   Holstein polaron*, Phys. Rev. B **76**, 165109 (2007),
   arXiv:0705.4154.
   PDF: `references/0705.4154-berciu-goodvin-prb-76-165109.pdf`
   (SHA-256 `123ba942f731a3754821c2b40a3cd1d7346d0803f84f0d4895588de13bf1948b`).
   Names the original MA as MA(0) and writes the continued fraction
   used below.

## Quoted MA(0) (Berciu–Goodvin 2007)

Berciu and Goodvin, Phys. Rev. B **76**, 165109 (2007), Sec. II,
Eqs. (10)–(12). The original MA is MA(0). Every free propagator
inside every self-energy diagram is replaced by its Brillouin-zone
momentum average

\[
\bar g_0(\omega)=\frac{1}{N}\sum_{\mathbf k}G_0(\mathbf k,\omega)
\qquad\text{(their Eq. (10))}.
\]

The MA(0) self-energy is momentum-independent:

\[
\Sigma_{\mathrm{MA}^{(0)}}(\omega)=g^2 A_1(\omega)
\qquad\text{(their Eq. (11))},
\]

with the continued fractions (their Eq. (12))

\[
A_n(\omega)
=\frac{n\,\bar g_0(\omega-n\Omega)}{1-g^2\bar g_0(\omega-n\Omega)\,A_{n+1}(\omega)}
=\cfrac{n\,\bar g_0(\omega-n\Omega)}{1-\cfrac{(n+1)g^2\bar g_0(\omega-n\Omega)\,\bar g_0(\omega-(n+1)\Omega)}{1-\cdots}}.
\]

The same object is Goodvin, Berciu, and Sawatzky, Phys. Rev. B
**74**, 245104 (2006), Eqs. (17)–(19):

\[
G(k,\omega)=\frac{1}{\omega-\varepsilon_k-\Sigma_{\mathrm{MA}}(\omega)+i\eta}
\qquad\text{(their Eq. (18))},
\]

\[
\Sigma_{\mathrm{MA}}(\omega)
=\cfrac{g^2\bar g_0(\omega-\Omega)}{1-\cfrac{2g^2\bar g_0(\omega-\Omega)\bar g_0(\omega-2\Omega)}{1-\cfrac{3g^2\bar g_0(\omega-2\Omega)\bar g_0(\omega-3\Omega)}{1-\cdots}}}
\qquad\text{(their Eq. (19))}.
\]

Eq. (19) of 2006 is identical to \(g^2 A_1(\omega)\) of 2007 Eq. (11).
This Candidate 2 block is **MA(0)**, not MA(1), not MA(2), and not a
deeper SCBA rainbow.

## Code-origin \(L=2\) specialization (PROJECT_CONVENTION)

Goodvin’s lecture band is \(\varepsilon_k=-2t\cos k\). This extract
uses the signed code origin \(\xi_k=2t(1-\cos k)\), \(\xi_0=0\),
\(\xi_\pi=4t\), \(E_0(g=0)=0\). Translator:
\(E_{\mathrm{lecture}}=E_{\mathrm{code}}-2t\). Do not switch
\(\xi_k\) back to \(-2t\cos k\).

On periodic \(L=2\), \(N=2\) and \(k\in\{0,\pi\}\). The momentum
average is the **discrete two-point average**, not the infinite-chain
1D formula \(\bar g_0(\omega)=\mathrm{sgn}(\omega)/\sqrt{(\omega+i\eta)^2-4t^2}\)
listed after Goodvin 2006 Eq. (19) for \(N\to\infty\):

\[
\bar g_0(z)=\frac12\sum_{k\in\{0,\pi\}}G_0(k,z)
=\frac12\left(\frac{1}{z-\xi_0}+\frac{1}{z-\xi_\pi}\right)
=\frac12\left(\frac{1}{z}+\frac{1}{z-4t}\right).
\]

Tadpole / Hartree is **OFF**: no static Hartree shift is added to
\(\Sigma_{\mathrm{MA0}}\).

Dyson on \(k=0\):

\[
G(k=0,z)=\frac{1}{z-\xi_0-\Sigma_{\mathrm{MA0}}(z)}
=\frac{1}{z-\Sigma_{\mathrm{MA0}}(z)},
\]

\[
\Sigma_{\mathrm{MA0}}(z)=g^2 A_1(z),
\]

with \(A_n\) as in 2007 Eq. (12) using this \(\bar g_0\).

Pole readout (same locks as `l2_periodic_pole.py`; do not retune):

- \(z(\omega)=\omega+i\eta\), \(\eta=10^{-4}\)
- \(D(\omega)=z(\omega)-\Sigma_{\mathrm{MA0}}(z(\omega))\)
- \(E_0^{\mathrm{MA0}}\) = lowest interior root of
  \(\operatorname{Re} D(\omega)=0\) in the open interval \((-8.0,0.25)\)
- coarse grid `np.linspace(-8.0, 0.25, 16501)`, then bisection on
  \(\operatorname{Re} D\)
- if no interior root: `NOT_COMPUTED`

## Truncation (PROJECT_CONVENTION, frozen before compute)

Continued-fraction depth \(N=64\), the same integer as
`SCBA_DEPTH` in `l2_periodic_pole.py`. Tail:

\[
A_{N+1}(z)=(N+1)\,\bar g_0\bigl(z-(N+1)\Omega\bigr),
\]

i.e. an undressed momentum-averaged propagator at the last phonon.
This is the same tail kind as \(\Sigma(z-(N+1)\Omega)=0\) for the
L=2 rainbow and as `exact_t0_linear_cfe` in
`src/keldysh4ai/future_b_atomic.py`. Recur \(n=N,\ldots,1\).
Do not retune \(N\) after seeing \(E_0^{\mathrm{MA0}}\).
At \(g=0\), \(\Sigma_{\mathrm{MA0}}=0\) and \(E_0^{\mathrm{MA0}}=0\).

## Atomic \(t=0\) reduction (check only; not the finite-\(t\) block)

At hop \(t=0\), \(\xi_k=0\) and \(\bar g_0(z)=1/z\). Then 2006
Eq. (19) / 2007 Eqs. (11)–(12) collapse to the exact atomic
continued fraction with coefficients \(1,2,3,\ldots\)
(Goodvin 2006, Eqs. (12) and the paragraph after; Ciuchi linear
series). SCBA / constant CFE remains \(1,1,1,\ldots\).

The finite-\(t\) teacher comparison uses MA(0) with the \(L=2\)
\(\bar g_0\) above. The linear CFE is **not** substituted for MA(0)
at finite \(t\).

## Hard bans

- not MA(1) or MA(2) (2007 Eqs. (16) and (18)–(24))
- not a deeper SCBA rainbow
- not \(\Sigma_{\mathrm{SCBA}}+\Sigma_{\mathrm{VC}}\)
- not `chain_scba.py`, not `crossing_block`
- not a learned gate
