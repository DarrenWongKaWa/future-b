# Motivation (this extract)

This is the scientific motive for Future B on this slice. It is a
**question**, not a result. It does not start Week 3, train a router,
implement DiagMC, or claim Physics-for-AI.

Scientific order and claim ceilings remain
`notes/SCIENCE_LINE_60DAY.md`. Signed conventions:
`notes/SIGNED_CONVENTION_SOURCES.md`.

## The physical bottleneck

A controlled electron–phonon problem (Holstein here; later, if earned,
realistic $g_{mn\nu}(\mathbf k,\mathbf q)$) is solved by dressing the
electron with phonon diagrams. The honest high-order route is to
**sum the electron–phonon Feynman series**, including vertex
corrections, not only the non-crossed rainbow.

That sum is hard and slow:

- the number of topologies grows rapidly with order;
- each graph carries internal momenta, frequencies, and (in materials)
  band and mode indices;
- crossed graphs are not optional decorations: on Holstein they can
  change the answer by a large factor relative to lowest-order
  self-consistent Born (Mishchenko, Nagaosa, Prokof’ev, PRL **113**,
  166402 (2014);
  `references/1406.4267-mishchenko-nagaosa-prokofev-prl-113-166402.pdf`);
- first-principles DiagMC can add those diagrams from a DFT/DFPT
  vertex on real materials (Luo, Park, Bernardi, Nat. Phys. **21**,
  1275 (2025);
  `references/s41567-025-02954-1-luo-park-bernardi-natphys-21-1275-nsfpar.pdf`),
  but the cost is the diagrammatic many-body stage itself, not only
  DFT.

Luo et al. split the pipeline as DFT/DFPT $\to$ coupling tensor $\to$
diagrammatic summation $\to$ polaron properties. Future B is about
the **third arrow**, on a frozen Holstein slice first. Storing Luo
does not authorize a DiagMC implementation or a materials teacher;
those remain outside the 60-day window.

One-shot Born is cheap and incomplete. SCBA resums the non-crossed
family and is still incomplete. Extra diagrams and extra SCBA
iterations cost compute. The live $L=2$ table asks whether that extra
work has **structure** in $(g,\Omega)$ versus ED, which is the
prerequisite for any adaptive policy.

## Two sides of the same motive

### 1. Accelerate the diagrammatic process

A neural module, if ever admitted, is for **compute policy**: which
allowed block to evaluate, and when to stop iterating, at matched
error versus a teacher. It is not a generic network that predicts
$E_0$ while discarding the diagrams.

On this slice the cheap and expensive objects already exist as
physics:

- Library I: additive Born / vertex blocks on bare $G_0$;
- Library II: SCBA on dressed $G$;
- teacher: periodic $L=2$ ED.

The intended speed-up is fewer wasted diagrams and fewer wasted
self-consistency steps, not a replacement solver.

### 2. Describe the network with the same physics

The internal computation should be readable as diagrammatic physics:

- typed propagators $G$, $D_0$;
- allowed diagram blocks $\mathcal B_c$ with fixed combinatorics;
- Dyson update $G^{-1}=G_0^{-1}-\Sigma$.

Those objects stay physics. They are not anonymous layers named after
Feynman graphs. If learning is admitted at all,
`notes/SCIENCE_LINE_60DAY.md` restricts it to **routing and
stopping**. Coefficients inside a known diagram, $\xi_k$, tadpole,
and $\Sigma_{\rm VC}$ on SCBA are not trainable knobs.

This is the Physics-for-AI half of the motive: the network is a
**gated diagrammatic calculation**, not a black box trained on
polaron numbers. Naming layers after diagrams does not establish
that claim. The 60-day line tests the claim in order, and a later
week cannot rescue a failed earlier week.

## What this does *not* say

- Luo 2025 and Mishchenko 2014 motivate why extra diagrams matter and
  why they are expensive. They are not this $L=2$ teacher and not a
  license to run DiagMC here.
- Week 2 (Born/SCBA vs ED on twelve cells) is not architecture
  evidence.
- A router, MLP, or GRU is **forbidden** until Week 3 exists and
  still leaves a problem.
- 11A inverse-problem numbers are unused.

## Current slice

Periodic $L=2$ Holstein, $\xi_k=2t(1-\cos k)$, tadpole off in the
libraries, two libraries separate. Live tables:
`prototypes/future_b_neural_poc/teacher_map_l2.csv` and
`week2_born_scba_vs_ed.csv`. Week 3 is not started.
