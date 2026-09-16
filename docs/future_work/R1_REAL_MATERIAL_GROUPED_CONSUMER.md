# R1 real-material grouped consumer — future-work roadmap

**Status in Future B: `FUTURE_WORK`.** Implementation is **stopped**.
This document is the restart packet for later independent research
(for example at Zhejiang University). It is **not** a Future B task.

Preserved scoped result (do not rerun as a fishing expedition):

> The validated fixed-order R1 evaluator demonstrated structural reuse
> and correctness, but did not establish an additional evaluator-speed
> advantage over the optimized CSE baseline in the tested domain
> (overall R1/CSE \(\approx 0.9992\)).

That statement is about **evaluators of the same object**. It is not
“R1 is useless” and not “grouped sampling of LiF is impossible”.

---

## 8.1 Scientific objective

Native Luo EZ DiagMC samples **one diagram / local ratio at a time**.
The Monte Carlo object is

\[
\texttt{BOUND\_C}:\qquad
\pi(C) \propto \mathrm{abs}(\mathrm{Re}\, D(C))
\]

with open phonon legs and electron-band matrices carried on that
specific configuration \(C\).

R1, as implemented in this repository, compiles a **shared-variable
weighted sum**

\[
\texttt{SHARED\_X\_GROUP}:\qquad
F_n(x)=\sum_{C\in G(x)} W_n(C;x)
\]

and evaluates it by recursive/shared execution (hash-consed DAG,
rebind-many). A third object is

\[
\texttt{SUMMED\_KERNEL}:\qquad
\text{some internal variables already integrated.}
\]

These three objects must stay distinct. Evaluating \(F_n(x)\) correctly
does **not** automatically give a legal sampler of native \(\pi(C)\),
and a legal sampler of a group measure does **not** automatically reduce
wall-clock \(T\) at equal precision on \(Q\).

The desired future transition is:

> outer native **variable-order** sampling
> + bounded **local exact grouping** with **full open-boundary context**,
> in which R1 actually performs cross-diagram reuse inside a
> real-material FEP-DMC calculation of the **same** \(Q\).

Do **not** assume the entire high-order topology space can be globally
precompiled. Do **not** invent a new global grouped algorithm as a
substitute for the missing measure.

Existing Route B (M5, scalar toy): a four-vertex local group with
complete boundaries, sitting *inside* an outer variable-order chain
that still uses explicit weights. That toy legality does **not**
transport onto LiF EZ without a new derivation.

---

## 8.2 Core mathematical difficulty

### What is still missing

A legal grouped Monte Carlo object needs **all** of the following,
written as formulae and independently checked. Future B closed the
project before this list was a native material sampler.

1. **Group definition.** For a configuration \(C\), what is \(G(C)\)?
   Vertices, pairings, time order, phonon modes, crystal momenta, band
   indices? Is \(G\) a function of a local window only?
2. **Partition vs cover.** Do groups partition diagram space, or do they
   overlap? Overlap requires multiplicity \(m(C)\) in the target.
3. **Anchor / group-selection probability.** Who proposes the group?
   If an outer native move proposes an anchor diagram \(C_0\) and then
   the group is \(G(C_0)\), the selection probability of the group is
   \(\sum_{C\in G} q(C)\) only if that is how the code actually
   proposes. Native swap/add/remove densities are **not** uniform on
   \(G\).
4. **Multiplicity.** If \(C\) belongs to several windows, the estimator
   must divide by \(m(C)\) or sample windows with a documented
   inclusion probability.
5. **Proposal density \(q(G\to G')\)** including Jacobian of any
   continuous time/momentum map.
6. **Reverse proposal \(q(G'\to G)\)**. Occupancy reverse vs
   time-reversal vs band-index reverse are different maps. The P1
   occupancy reverse is a **BOUND_C** map, not a group map.
7. **Target density \(\pi(G)\).** Candidate (illegal if used blindly):

   \[
   \pi_{\mathrm{signed}}(G)\propto \mathrm{abs}\Big(\sum_{C\in G} D(C)\Big)
   \qquad\text{vs}\qquad
   \pi_{\mathrm{abs}}(G)\propto \sum_{C\in G}\mathrm{abs}(D(C)).
   \]

   Native Luo uses a **third** target,
   \(\mathrm{abs}(\mathrm{Re}\,D(C))\) on a single \(C\).
8. **Normalization** of \(\pi\) over the union of groups, including
   the empty/high-order tails of variable-order space.
9. **Jacobians / variable mapping.** Time-ordered simplices, crystal
   momentum conservation, umklapp, SVD interpolant coordinates.
10. **Sign / complex phase.** Multiband \(D(C)\) is complex. Grouping
    can increase cancellations.
11. **External / open phonon legs.** A local vertex group that ignores
    open legs changes the physical object. Route B required **complete
    boundary**.
12. **Electron-band ordering.** Matrix products do not commute.
    `SHARED_X_GROUP` must preserve multiplication order; CSE of scalars
    is not a substitute.
13. **Numerator estimator** for \(\sum_b N_b/\tau_{\max,b}\).
14. **Denominator estimator** for \(\sum_b D_b\).
15. **Variable perturbation order.** Native order-changing moves must
    either (a) stay outside the group or (b) have a documented group
    birth/death kernel.
16. **Double counting.** Pairings that can be drawn as two local
    windows.

### Why \(\mathrm{abs}(\sum D)\neq \sum\mathrm{abs}(D)\)

On any finite set with a relative minus sign,

\[
\Big\lvert\sum_{C\in G} D_C\Big\rvert
\;\ne\;
\sum_{C\in G}\lvert D_C\rvert
\;\ne\;
\sum_{C\in G}\mathrm{abs}(\mathrm{Re}\, D_C)
\]

in general. This is not hypothetical: M4 crossing-minus controls
(`x19.csv` class) are a finite-domain witness.

If the **physics** you want is the signed sum \(F=\sum D_C\), the
Monte Carlo **weight** still has to say which measure you sample.
Options:

- Sample groups with \(\pi(G)\propto\lvert F(G)\rvert\) and estimate
  \(\mathrm{sign}(F)\) (phase problem can explode).
- Sample diagrams with \(\pi(C)\propto\mathrm{abs}(\mathrm{Re}\,D(C))\)
  and use R1 only as an **evaluator** of a conditional expectation
  (this is BOUND_C + a better function evaluation; it is not grouped
  sampling).
- Heat-bath inside a group on a **positive** toy measure (M4 scalar
  \(W_n>0\)). That identity does **not** hold for native
  \(\mathrm{abs}(\mathrm{Re}\,D)\) with open legs.

### Why a correct grouped signed sum is not a sampler

A unit test that

```
R1(G) == CSE(G) == sum_explicit(G)
```

proves **evaluation**. A legal MH/heat-bath kernel additionally needs
\(q,\pi,m,\) reverse, and that the invariant measure is the one whose
expectation is \(Q\). You can have a perfect \(F(G)\) and still:

- double-count diagrams
- miss native add/remove moves that leave the local window
- estimate \(\sum D\) while the native denominator is
  \(\sum \mathrm{abs}(\mathrm{Re}\,D)\)
- change the sign/phase distribution so that \(\mathrm{Var}(\hat Q)\)
  grows faster than the evaluator cheapens

**Hardware does not repair an invalid measure.**

---

## 8.3 Recommended research route

Frozen candidate (do not replace with a global compiler of all
diagrams):

```
outer variable-order native sampling
  + bounded local grouping
  + exact grouped evaluation with full open-boundary context
```

### Stage R1-F1 — derive a finite enumerable grouped model

Write \(\pi,q,m,\) Jacobian, numerator, denominator on a **finite**
set of diagrams (fixed max order, no material files). Prove
\(\mathbb{E}[Y]=\sum W\) or explicitly record the bias term.
Independent check: enumeration.

**Stop** if this derivation cannot be closed. Do not start Fortran.

### Stage R1-F2 — independent small-system oracle

A second implementation (dense enumerate or a different DAG) of the
same formulae. No shared code with R1.

### Stage R1-F3 — stationary distribution / normalization

Run the kernel; compare histogram to \(\pi\) on the finite set;
check \(\sum p=1\) and reverse-kernel identities.

### Stage R1-F4 — material matrix provider and open-boundary operator

Connect Luo \(\varepsilon_{nk}\), \(\omega_{q\nu}\), \(g_{mn\nu}(k,q)\)
(rank-20 SVD / H-table as already used in M6 n1). Preserve open phonon
legs. Do not drop band order.

### Stage R1-F5 — native variable-order proposal machinery

Hook the local group into add/remove/swap **without** changing illegal
support. Every native move that can enter/leave the window needs a
reverse.

### Stage R1-F6 — full observable \(Q\)

Same \(Q=E_{\mathrm{polaron}}-E_{\mathrm{bare}}\) with the documented
\(E_{\mathrm{bare}}\). Numerator and denominator both from the new
measure, or an unbiased combination that is written down.

### Stage R1-F7 — evaluator benchmark (not yet “faster physics”)

Compare, on the **same object**:

- native individual-diagram evaluation
- optimized CSE
- grouped R1

This repeats the honest M3/M4 lesson: R1 and CSE can tie.

### Stage R1-F8 — equal-precision material efficiency

Only after F6 correctness: \(T\) and \(\mathrm{Var}(\hat Q)\) on the
same workload, protocol frozen first, vs the appropriate baseline
(native BOUND_C and CSE, not a slow Python explicit sum).

---

## 8.4 Workload estimate

Planning estimates, not promises. Repository evidence (M3–M6 took
multiple documented days each for **toy** legality; native P1 swap
alone needed C0–C5 plus a clean-binary wrap-up) argues this is **not**
a one-day patch.

| work | range | why |
|---|---|---|
| Mathematical derivation (F1) | several focused days – ~2 weeks | three distinct measures; open legs; variable order |
| Prototype + finite-domain oracle (F2–F3) | ~1–3 weeks | M4-scale: partition, sampling identities, negative controls |
| Material / native integration (F4–F6) | potentially several weeks | M6 still had n2/full-order consumer `NOT_COMPUTED`; native Fortran state is large |
| Statistical confirmation (F8) | additional compute + analysis | independent chains, HAC, frozen protocol; LiF \(N_{\mathrm{mc}}=200\) already ~30 s/chain on 1 core but HAC was dirty |
| Evaluator microbenchmark (F7) | days, after correctness | already known to be easy to over-claim |

Single-host 6 GiB was enough to **discover** that the measure was not
closed. It is the wrong environment to pretend F5–F8 will finish in a
weekend.

---

## 8.5 Recommended future machine

Planning estimate only. **Revise after Stage R1-F2/F3 profiling.**
CPU count does not fix an invalid grouped measure.

Preferred development / confirmation node:

- Linux x86_64
- 32–64 physical CPU cores
- 128 GB RAM minimum
- 256 GB RAM preferred if grouped-state width / high-order intermediate
  storage becomes large
- fast local NVMe scratch
- \(\ge 1\,\mathrm{TB}\) local scratch for traces, checkpoints, material
  data

GPU:

- **not required** for the current R1 formulation
- optional only if a later dense linear-algebra or learned component
  demonstrates a GPU-relevant hotspot

Cluster:

- desirable for independent-chain statistical confirmation
- not required for F1–F3 mathematics or single-node integration

Intel Fortran + HDF5 Fortran 2003 + QE 6.5 remain the native build
stack unless someone re-ports Perturbo. That is an engineering project
of its own.

The LiF epwan file is ~404 MiB; other materials in the local dataset
reach ~1.8 GiB. Scratch is for **traces**, not for storing a second
copy of every HDF5 in each run directory (the closure tree did that;
do not repeat it).

---

## 8.6 Success criteria

A future continuation counts as scientifically successful **only if**:

1. grouped sampling / integration is mathematically legal;
2. a finite-domain independent oracle passes;
3. the real material provider is actually used;
4. R1 participates in the consumer (not a rename of CSE or of native
   BOUND_C);
5. the same physical observable \(Q\) is obtained;
6. statistical uncertainty is controlled under a **predeclared** rule;
7. any speedup is measured against an appropriate **optimized**
   baseline, at equal precision, with \(T\) and \(\mathrm{Var}\) from
   the same workload.

Failing F7 (R1≈CSE) with F1–F6 legal is a **valid scoped negative**,
same genre as M3/M4. That would still be a successful *scientific*
outcome. It would not be “R1 accelerated LiF”.

---

## 8.7 Known risks

- state-space explosion of local windows as order grows
- group overlap / double counting
- sign / phase degradation (\(\lvert\sum D\rvert\ll\sum\lvert D\rvert\))
- incorrect normalization of variable-order space
- noncommuting multiband matrix products
- excessive grouped-state memory
- compilation cost (M4 cold path already dominated by gfortran in toy
  tests)
- weak gain versus optimized CSE (already seen at fixed order)
- lower per-evaluation cost but **worse** Monte Carlo variance
- material provider integration complexity (open legs, SVD rank, q-grid)
- accidental rebrand of Luo–Bernardi compression or band-product
  summation as “R1 grouping”

---

## What already exists (do not redo)

- Scalar R1 compile-once / rebind-many correctness
- Symbolic/fused repeated binding
- Two-band n=2 untraced operator checks (n=3 two-band `NOT_COMPUTED`)
- M3 n1/n2 independent references; R1/CSE \(\approx 0.9992\)
- M4 finite-domain group/measure identities on a **positive scalar toy**
- M5 Route B local four-vertex group with complete boundary; outer
  consumer still explicit
- M6 selected native factors and full n1 integral; full n2 / all-order
  material consumer `NOT_COMPUTED`

Start from F1, not from “one more CSE microbenchmark”.
