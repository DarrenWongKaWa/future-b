# Source closure for `B_VC`: fourth-order Holstein crossing block

Copied into this extract as the formula record for Barišić App01 and
for $\xi_k=2t(1-\cos k)$. PDF:
`references/cond-mat-0607731-barisic-epjb-54-1.pdf`.
Map to the six signed bullets:
`notes/SIGNED_CONVENTION_SOURCES.md`.

This extract does **not** contain `crossing_block_poc.py`. Live
`E0_Born_VC` remains `NOT_COMPUTED`. This file does not amend teacher
numbers, mix libraries, or authorize $\Sigma_{\rm VC}$ on SCBA.

## Primary source

O. S. Barišić and S. Barišić, *Quantum adiabatic polarons by translationally
invariant perturbation theory*, **Eur. Phys. J. B 54**, 1 (2006),
DOI `10.1140/epjb/e2006-00413-5`, arXiv `cond-mat/0607731v1`.

- TeX source URL: `https://export.arxiv.org/e-print/cond-mat/0607731`
- Parent-retrieved TeX SHA-256:
  `7693b0198b810cecbee489c90fc1d834ba7c41ddb2c67887b9afa08b0e48c639`
- Formula: Appendix Eq. (App01) plus its vertex convolution; main-text
  Eqs. (14)--(15).

## Domain reconciliation

The source is a 1D periodic Holstein lattice at zero electron density, for an
intermittently added electron.  This matches the prototype's single-polaron,
zero-density, retarded Green-function scope.  The source writes a `-g`
Holstein vertex whereas this slice freezes Goodvin plus-$g$; the
second-order and fourth-order blocks used here are even in $g$, so their
values are invariant under that sign change.

The parent one-site/open-chain POC cannot directly host a momentum-dependent
crossing diagram.  The parent `crossing_block_poc.py` therefore used a
separate periodic-1D backend. That executable is **not** in this extract.

## Fixed diagrammatic block

The source's free retarded propagator is

$$
G_0(k,\omega)=\frac{1}{\omega-\xi_k+i\eta},
\qquad \xi_k=2t(1-\cos k).
$$

Appendix App01 gives

$$
\Sigma_k^C(\omega)=\frac{g^2}{N}\sum_q
G_0(k-q,\omega-\Omega)\,\Gamma_q(\omega),
$$

$$
\Gamma_q(\omega)=\frac{g^2}{N}\sum_{q'}
G_0(q'-q,\omega-2\Omega)G_0(q',\omega-\Omega).
$$

Substitution gives the crossing block (Library I, on bare $G_0$):

$$
\mathcal B_{\rm VC}[G_0](k,\omega)=
\frac{g^4}{N^2}\sum_{q,q'}
G_0(k-q,\omega-\Omega)
G_0(q'-q,\omega-2\Omega)
G_0(q',\omega-\Omega).
$$

Its topology is the first crossing of two phonon lines / leading vertex
correction: three free electron propagators, two internal momenta, one external
momentum, fixed combinatorial factor one, and order $g^4$.  All coefficients
and sums are fixed, never neural parameters.

## Disjointness from `B_BORN`

`B_BORN` is order $g^2$, has one free propagator and one momentum sum.
`B_VC` is order $g^4$, has three propagators and two momentum sums, and is
momentum dependent.  That is disjointness **inside Library I**. It does
not authorize adding $\mathcal B_{\rm VC}$ onto SCBA (Library II). See
`notes/DOUBLE_COUNTING_MEMO.md`.

## POC boundary

The formula is source-backed inside the periodic-1D zero-density domain.
Controller labels, activation thresholds, and parent POC performance
remain `POC_ONLY` and are not live Future B evidence.
