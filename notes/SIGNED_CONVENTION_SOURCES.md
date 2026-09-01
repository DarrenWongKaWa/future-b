# Signed-convention sources (this extract)

Authority: **HUMAN LOCK 2026-08-31**. This file maps the six binding
bullets in `notes/SCIENCE_LINE_60DAY.md` onto papers that now live in
`references/`. It does not reopen conventions, mix libraries, copy 11A numbers,
or reopen the closed L=2 gate. Slice closeout:
`notes/SLICE_CLOSEOUT.md` (结项，不是认证).

PDF copies and SHA-256: `references/README.md`.
Crossing-block formula record: `notes/CROSSING_BLOCK_SOURCE.md`.
Live double-counting default: `notes/DOUBLE_COUNTING_MEMO.md` (**NO**
$\Sigma_{\rm VC}$ on SCBA).

Parent freeze / K4AI evidence files stay in the parent worktree. They
are not live admission here.

## Binding bullets → sources

| Bullet in `SCIENCE_LINE_60DAY.md` | Class | Source in this tree |
|---|---|---|
| $\xi_k=2t(1-\cos k)$, so $E_0(g=0)=0$ | SOURCE_DERIVED band (Barišić) plus PROJECT_CONVENTION origin | Barišić & Barišić (2006) free $G_0$; executable pin `src/keldysh4ai/future_b/teacher/holstein_ed.py` |
| $E_{\rm lecture}=E_{\rm code}-2t$ | PROJECT_CONVENTION translator | Relates Barišić/code origin to Goodvin $\varepsilon_{\mathbf k}=-2t\cos k$ |
| tadpole/Hartree OFF in the diagrammatic libraries | SOURCE_DERIVED restriction | Goodvin SCBA (non-crossed only); Ciuchi “no bubble diagrams” |
| ED still contains $g\,n(b+b^\dagger)$ | SOURCE_DERIVED (Goodvin plus-$g$) | Goodvin after Eq. (1); ED Hamiltonian in `holstein_ed.py` |
| Library I and Library II remain separate | SOURCE_DERIVED kind split | Goodvin: SCBA = non-crossed rainbow; Barišić App01 = first crossed graph on $G_0$ |
| no $\Sigma_{\rm VC}$ on SCBA without a disjoint-diagram memo | live default **NO** | Ciuchi Sec. III.3; this extract’s memo is `notes/DOUBLE_COUNTING_MEMO.md` |

## Papers stored here

### 1. Goodvin, Berciu, Sawatzky (2006)

G. L. Goodvin, M. Berciu, and G. A. Sawatzky, *The Green’s function of
the Holstein polaron*, Phys. Rev. B **74**, 245104 (2006).
DOI `10.1103/PhysRevB.74.245104`. arXiv `cond-mat/0609597`.
PDF: `references/cond-mat-0609597-goodvin-berciu-sawatzky-prb-74-245104.pdf`.

Used for:

- plus-$g$ local Holstein vertex, after Eq. (1):
  $g\sum_i n_i(b_i+b_i^\dagger)$;
- 1D nearest-neighbor band Eq. (2):
  $\varepsilon_{\mathbf k}=-2t\cos k$ (lecture origin; **not** the
  code $\xi_k$);
- $T=0$ vacuum-addition retarded $G$;
- SCBA sums **only** non-crossed diagrams (text after Table 1);
- atomic-limit continued fraction Eq. (13) (coefficients $1,1,1,\ldots$
  are the SCBA/constant-CFE family, not the exact linear series).

Ciuchi and Bonča write a **minus** in front of the coupling. This slice
freezes Goodvin’s plus-$g$ writing. Do not mix the two signs.

### 2. Ciuchi, de Pasquale, Fratini, Feinberg (1997)

S. Ciuchi, F. de Pasquale, S. Fratini, and D. Feinberg, *Dynamical
mean-field theory of the small polaron*, Phys. Rev. B **56**, 4494
(1997). DOI `10.1103/PhysRevB.56.4494`. arXiv `cond-mat/9703118`.
PDF: `references/cond-mat-9703118-ciuchi-prb-56-4494.pdf`.

Used for:

- T=0 emission-only Born/SCBA kernel
  $\Sigma\sim g^2 G(z-\Omega)$ (Sec. III-B);
- “no bubble diagrams, no phonon renormalization” (Sec. II) — tadpole /
  Hartree stays **OFF** in the diagrammatic libraries;
- impurity / atomic continued fractions Eqs. (35)–(38);
- Sec. III.3: at zero density the $O(g^4)$ non-crossing piece and the
  vertex correction take the **same value**, so a self-consistent
  non-crossing / Migdal scheme is not an exact theorem. That is why
  adding $\Sigma_{\rm VC}[G_0]$ onto SCBA is forbidden by default.

### 3. Barišić and Barišić (2006)

O. S. Barišić and S. Barišić, *Quantum adiabatic polarons by
translationally invariant perturbation theory*, Eur. Phys. J. B **54**,
1 (2006). DOI `10.1140/epjb/e2006-00413-5`. arXiv `cond-mat/0607731`.
PDF: `references/cond-mat-0607731-barisic-epjb-54-1.pdf`.
Formula record: `notes/CROSSING_BLOCK_SOURCE.md`.

Used for:

- free retarded propagator
  $G_0(k,\omega)=1/(\omega-\xi_k+i\eta)$ with
  $\xi_k=2t(1-\cos k)$ (this is the **code** origin:
  $\xi_0=0$, $\xi_\pi=4t$, $E_0(g=0)=0$);
- Appendix App01 crossed / vertex block $\mathcal B_{\rm VC}$ on
  **bare** $G_0$ (Library I). The live teacher map still has
  `E0_Born_VC=NOT_COMPUTED`. The POC executable
  `crossing_block_poc.py` was **not** copied into this extract.

The source writes a $-g$ vertex. Second- and fourth-order kernels used
here are even in $g$, so the numerical value is invariant. ED still
uses Goodvin plus-$g$.

## Translator (PROJECT_CONVENTION, not a paper equation)

Goodvin’s 1D band is $\varepsilon_k=-2t\cos k$, so
$\varepsilon_0=-2t$. Barišić / this code use
$\xi_k=2t(1-\cos k)=\varepsilon_k+2t$, so $\xi_0=0$. Energies reported
in this repository are on the code origin. The lecture translation is

$$
E_{\rm lecture}=E_{\rm code}-2t.
$$

Do not change $\xi_k$ back to $-2t\cos k$. Executable checks:
`tests/test_ed_limits.py` (`code_dispersion([0,π])==(0,4t)`,
`HolsteinL2ED(g=0)` has $E_0=0$).

## Two libraries (kind split, not a license to stack)

- **Library I:** additive blocks on bare $G_0$ (one-shot Born, and
  Barišić App01 VC). Lives in the parent POC; this extract does not
  execute VC.
- **Library II:** SCBA resummation on dressed $G$, tadpole off. Live
  $L=2$ extractor: `prototypes/future_b_neural_poc/l2_periodic_pole.py`.

Goodvin: SCBA is a complete non-crossed rainbow, not an additive
$O(g^2)$ piece beside another complete $\Sigma$. Ciuchi Sec. III.3:
topological disjointness of the crossed graph from SCBA does **not**
authorize $\Sigma_{\rm SCBA}+\Sigma_{\rm VC}[G_0]$. The written memo
required by the sixth bullet is `notes/DOUBLE_COUNTING_MEMO.md`, and
its default is **NO**.

## Planning-only PDFs (not formula sources for the six bullets)

These are the papers named at the end of `notes/SCIENCE_LINE_60DAY.md`.
They may guide interpretation. They are not implementation tickets.

- A. S. Mishchenko, N. Nagaosa, and N. Prokof’ev, *Diagrammatic Monte
  Carlo method for many-polaron problems*, Phys. Rev. Lett. **113**,
  166402 (2014). DOI `10.1103/PhysRevLett.113.166402`. arXiv
  `1406.4267`.
  PDF: `references/1406.4267-mishchenko-nagaosa-prokofev-prl-113-166402.pdf`.
  Square-lattice finite-density Holstein; vertex corrections beyond
  lowest-order SCBA. An adaptation motive, not this $L=2$ table.
- P. Mitrić, V. Janković, N. Vukmirović, and D. Tanasković, *Spectral
  functions of the Holstein polaron: Exact and approximate solutions*,
  Phys. Rev. Lett. **129**, 096401 (2022). DOI
  `10.1103/PhysRevLett.129.096401`. arXiv `2112.15542`.
  PDF: `references/2112.15542-mitric-prl-129-096401.pdf`.
  `SCIENCE_LINE_60DAY.md` names “Mitrić et al.” without a DOI; this is
  the matching Holstein exact-vs-approximate spectral paper stored
  here. Not a live-slice formula source. Not DMFT/HEOM code in this
  tree.
- Y. Luo, J. Park, and M. Bernardi, *First-principles diagrammatic
  Monte Carlo for electron–phonon interactions and polaron*, Nat.
  Phys. **21**, 1275–1282 (2025). DOI `10.1038/s41567-025-02954-1`.
  PDF (NSF PAR accepted manuscript, not the Nature typeset PDF):
  `references/s41567-025-02954-1-luo-park-bernardi-natphys-21-1275-nsfpar.pdf`.
  Parent chapter class: **applied / later high-fidelity reference**.
  First-principles DiagMC on LiF, SrTiO$_3$, TiO$_2$. Used in
  `notes/MOTIVATION.md` as the slow, high-order diagram-sum example.
  Not a formula source for $\xi_k$, tadpole, plus-$g$, or the two-library split.
  Not this $L=2$ teacher. `SCIENCE_LINE_60DAY.md` still lists DiagMC
  implementation and realistic-material extensions as **outside** the
  next two months. Storing the PDF does not authorize a DiagMC run.

The Future B chapter fragment remains in the parent:
`papers/P3_physics_for_ai/keldysh4ai_v1_future_b.tex`. It is planning
text, not a published paper, and was not copied.

## Explicitly not stored here

- 11A / OPHIS inverse-problem papers;
- Jauho Keldysh lecture notes;
- parent `experiments/FUTURE_B/*FREEZE.md` as admission.
