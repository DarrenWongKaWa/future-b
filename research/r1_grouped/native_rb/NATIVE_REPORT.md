# Native follow-ups: window Rao–Blackwellization on LiF, and the sign of other materials

These are the two routes left open by
[lif_sign/LIF_SIGN.md](../lif_sign/LIF_SIGN.md).

1. **(a)** Rao–Blackwellize the LiF EZ energy estimator over the three
   re-pairings of every eligible four-vertex window. This is the
   material-level version of the toy's only positive result.
2. **(b)** Measure the native average sign ⟨s⟩ of the other dataset
   materials.

## Build and provenance

Everything runs natively on the host workstation (Apple M4 Pro; 12 CPUs
and 7.75 GiB inside the Docker VM).

- **Container.** `linux/amd64 r5p0-env:ubuntu2004`, with gfortran 9.4,
  OpenMPI and serial HDF5. `OMP_NUM_THREADS=1`, one chain per container.
- **Source.** Pinned public FEP-DMC
  `05d08449cffdbd0dfbbbf5009add5cc887bc754b`, overlaid on a QE 6.5 tree
  already compiled with gfortran. [patch_fepdmc.py](patch_fepdmc.py)
  applies, and asserts, three kinds of edit:
  - gfortran portability, plus an MKL VSL shim (xorshift64 in place of
    MT19937), with no Metropolis change;
  - the measurement-only [rb_window.f90](rb_window.f90), inert unless
    `FUTUREB_RB=1`;
  - an opt-in `FUTUREB_SEED` that replaces the wall-clock seed value.
- **Flags.** [make.sys](make.sys) needs `-fmax-stack-var-size=1` for EZ.
  Without it, the local `diagrams(200)` arrays overflow the stack and
  `perturbo.x` segfaults at start. The table steps (svd-elph,
  tabulate-H) use a second build of the same source without that flag,
  because it breaks their re-allocated local arrays. Binary hashes are in
  [evidence/BINARY_SHA256.txt](evidence/BINARY_SHA256.txt).
- **Driver.** [run_native.py](run_native.py) runs every chain with
  T = 50 K (β = 232.09 eV⁻¹), a 20³ grid, `nsvd = 20`, `Nmcmc = 200×10⁴`,
  `maxOrder = 500` and `DMC_Method = 0`. The band windows follow the
  paper's dataset notebooks.

## (a) Window Rao–Blackwellization of Q on LiF-electron

**Estimator.** The chain samples π(C) ∝ |Re D(C)|. Each eligible window
(four time-consecutive internal vertices holding two complete internal
lines) and its three local pairings form one fiber of a partition. The
window positions depend only on the order, so for each position `p`

```
E[f_O | fibre_p] = Σ_r Re D_r O_r / Σ_r |Re D_r|,
```

and averaging over all positions is unbiased with no larger variance.

In single band, `O = Σ_seg E Δτ + Σ ω|Δτ| − (order−1)`. This is exactly
the native `measure_EZ_wfn` increment divided by the sign. A re-pairing
changes only 3 segment energies, 4 couplings `g(k,q)` (recomputed with
the native `cal_ek_int` and `cal_gkq_vtex_int`) and 2 phonon lengths.

**Self-checks (all chains).** Every check passes:
- the sign agrees with native `gtrue` at every measurement;
- `sgn·O` equals the native Etrue increment to ≤ 5e-13 relative;
- for the current pairing, the recomputed g and segment energies equal
  the stored ones to ≤ 1e-14;
- the raw estimator reproduces the native `Etrue` exactly.

**Result** ([evidence/lif_elec_rb.json](evidence/lif_elec_rb.json)). This
is 12 independent chains of 15,000 measurements each, with the raw and RB
estimators computed on the same measurements:

| quantity | value |
|---|---|
| Q raw | −0.25112 ± 0.00147 eV |
| Q RB | −0.25112 ± 0.00147 eV |
| max \|E_RB − E_raw\| per chain | 1.5e-6 eV |
| paired SE² ratio RB/raw (mean over chains) | **1.00002 ± 0.00003** |
| between-chain variance ratio | 0.9999 |
| eligible windows / all windows | 5–9% |
| ⟨s⟩ raw → RB | identical to 4 decimals (0.903–0.963 by chain) |

**No-go.** Window Rao–Blackwellization gives no measurable variance
reduction on LiF Q. There are three reasons:
- fibers are rare: only about 7% of window positions are eligible;
- a fiber almost never mixes signs;
- a local re-pairing changes O by a phonon-energy and segment-energy
  difference that is tiny next to the order and total-energy fluctuations
  of a diagram of about 130 vertices.

The toy's 7–24% Rao–Blackwell gain was measured on a non-invariant toy
observable (crossing number). It does not carry over to Q.

## (b) Average sign of other materials

From [evidence/materials_sign.json](evidence/materials_sign.json) and
[evidence/materials_sign_lifhole_mo990.json](evidence/materials_sign_lifhole_mo990.json).
Each row uses independent seeded chains at T = 50 K, with τ = 232 eV⁻¹ in
EZ mode.

| material | bands | chains | ⟨s⟩ | Q (eV) | paper Q at 20³ | sign ceiling 1/⟨s⟩² |
|---|---|---|---|---|---|---|
| LiF-electron | 1 | 12 | 0.951 ± 0.005 | −0.2511 ± 0.0015 | ≈ −0.25 | 1.10 |
| SrTiO₃ (electron) | 3 (t2g) | 6 | **0.680 ± 0.008** | −0.1420 ± 0.0008 | −0.1419 | **2.17** |
| LiF-hole, maxOrder 500 | 3 | 6 | −0.004 ± 0.003 | (invalid) | — | — |
| LiF-hole, maxOrder 990 | 3 | 6 | **−0.0002 ± 0.004** | (invalid) | — | ∞ |
| TiO₂ anatase | 1 | (running) | | | −0.146 | |

The STO value reproduces the paper's 20³ energy, which validates the
multiband pipeline end to end.

LiF-hole has no usable sign at τ = 232 eV⁻¹. With maxOrder 500 the order
was pinned at the cap. At 990 the order stays at 667–755, below the cap,
but ⟨s⟩ is still zero within errors. This agrees with the paper's own
`dataset/Figure-1`. That figure compares matrix-product and band
sampling, which only makes sense for a multiband system. Its S(τ) has
fallen to 0.24 by τ = 14 eV⁻¹. So the long-τ EZ regime is simply out of
reach for LiF-hole. An energy from these runs means nothing.

## (a′) Multiband window Rao–Blackwellization and the exact grouped sign on STO

The general [rb_window.f90](rb_window.f90) handles any number of bands.
It builds prefix products X_s and suffix products Z_s once per
measurement, together with their H-insertion sums Y_s and V_s. Around a
window it then writes the chain as `M = R · W · L`, so that

```
N_H(r) = Re[tr(R W_r Λ) + tr(Ρ W_r L) + tr(R W^H_r L)],
```

and each re-pairing needs only its own 4 vertex matrices and 3 propagators.

The same pass also computes an exact grouped-measure quantity, **E[ρ]**.
For each sample, ρ = |Σ_G D| / Σ_G |D| over the tiled group G(C): all 3^m
re-pairings of the first m = min(#eligible, 8) tiled windows. Truncating
to the first 8 windows depends only on the eligible set E(C), so the
groups remain a partition. Under the native measure, E[ρ] = Z_B/Z_A holds
exactly. Hence ⟨s⟩_B = ⟨s⟩_A / E[ρ], computed from native samples with no
new sampler.

**Validation.** Every check passed:
- **Single-band regression.** On LiF-electron chain00 with the same seed,
  the general code reproduces the single-band trace (raw and RB) to
  within 1e-14 on all 15,000 measurements.
- **STO self-checks, 6 chains:**
  - the sign agrees with native `gtrue`;
  - `N/|w|` equals the native Etrue increment to ≤ 5e-13;
  - the prefix and suffix environments agree;
  - the recomputed g matrices and all band energies match the stored ones
    (current pairing);
  - the current member of every tiled group reproduces w.
- **The measurement leaves the chain untouched.** The native `Etrue` and
  `<g/Z>` of every STO chain are bit-identical to the earlier runs made
  without the hook.

**STO result** ([evidence/sto_rb_mb.json](evidence/sto_rb_mb.json)). This
is 6 chains of 15,000 measurements each. About 15% of windows are
eligible; groups hold 3.2 tiled windows on average, and 3–4% of
measurements reach the 8-window cap.

| quantity | value |
|---|---|
| ⟨s⟩_A (native) | 0.680 ± 0.008 |
| E[ρ] tiled groups | 0.9872 ± 0.0004 |
| ⟨s⟩_B = ⟨s⟩_A / E[ρ] | 0.688 |
| variance gain from sign, grouped measure B | **1.026** |
| same, single random window | 1.0013 |
| ceiling if all cancellation were removed | 2.17 |
| fraction of the sign deficit recovered | **2.7%** |
| RB SE² ratio for Q (paired) | 0.9997 ± 0.0002 |
| wall time with the hook vs native | ~1.8–3.2× |

**LiF-electron with the same code**
([evidence/lif_elec_rb_mb.json](evidence/lif_elec_rb_mb.json)). This is 6
chains. The native Etrue is bit-identical to the runs without the hook.

| quantity | value |
|---|---|
| ⟨s⟩_A | 0.945 |
| E[ρ] tiled | 0.99585 ± 0.00014 |
| variance gain from sign, measure B | 1.008 |
| fraction of the sign deficit recovered | 7.1% |
| RB SE² ratio | 1.00005 |

A first LiF-electron pass reported E[ρ] = 0.983. That pass used a build
which wrote ρ = −1 for groups with more than 8 windows, and those values
entered the mean. The number was wrong and has been discarded.

**LiF-hole with the same code, maxOrder 990**
([evidence/lif_hole_rb_mb.json](evidence/lif_hole_rb_mb.json)). This is 2
chains; the order is about 600–640.

| quantity | value |
|---|---|
| ⟨s⟩_A | 0.0003 ± 0.0065 |
| eligible windows | **0.2%** |
| tiled windows per sample | 0.3 |
| E[ρ] tiled | 0.9926 ± 0.0001 |
| ⟨s⟩_B | still ≈ 0 |

At strong coupling the phonon lines are long. A four-vertex window almost
never holds two complete lines, so local re-pairing groups barely exist
where the sign problem is worst.

STO's sign problem is real: the ceiling is 2.17×. But **the four-vertex
re-pairings recover only 2.7% of it**. About 3% of groups do cancel
strongly (ρ < 0.9, occasionally near 0), yet on average the cancellation
that makes ⟨s⟩ = 0.68 is between diagrams that no local re-pairing
connects. Those diagrams differ in times, momenta, band paths or global
topology. The Q estimator gains nothing from Rao–Blackwellization either.
**The four-vertex grouped consumer is no-go on STO as well.**

## (c) Where the STO sign problem actually lives: phonon modes and momenta

The window results located the cancellation *outside* local topology. The
same exact device E[ρ] = Z_B/Z_A was applied to other degrees of freedom of
a line. Each grouping below is ν- or q-independent (lines chosen by opening
rank or a counter rule), so each is a partition. The data are native STO
chains, 15,000 measurements each; the self-checks (the current member
reproduces w) pass to ≤ 4e-13.

**Phonon-mode groups** (sum a line over all Nph = 15 modes;
[evidence/sto_modes_k4.json](evidence/sto_modes_k4.json),
[evidence/sto_modes_pairs.json](evidence/sto_modes_pairs.json)):

| group | E[ρ] | ⟨s⟩_B | variance gain from sign |
|---|---|---|---|
| 4-vertex tiled windows | 0.987 | 0.671 | 1.03 |
| one line's modes | 0.988 | 0.670 | 1.03 |
| first 2 lines jointly (exact) | 0.979 | 0.676 | 1.04 |
| first 3 lines jointly (exact) | 0.968 | 0.684 | 1.07 |
| first 4 lines jointly (exact) | 0.958 | 0.691 | 1.09 |
| greedy non-crossing set, ≈80% of lines (independent-line estimate) | ≈0.76 | ≈0.90 | ≈1.70 |
| all lines (independent-line estimate) | ≈0.71 | ≈0.94 | ≈1.9–2.0 |
| ceiling | — | 1 | 2.1–2.3 |

**Independence test.** The exact joint ρ over the product of single-line ρ
is:
- 0.9996 for the first 2 lines and 0.9993 for the first 3;
- 0.9998 for disjoint counter-chosen pairs, 0.9996–1.0011 for nested
  pairs, and 0.9997–1.0016 for crossing pairs.

Mode cancellations on different lines are independent to about 1e-3,
which is what justifies the product estimates.

**The sign problem of STO in EZ mode is mostly phonon-mode interference.**
Each line removes about 1.2% of the normalization, and a diagram carries
about 37 lines. Local re-pairing, by contrast, reaches only a few eligible
windows.

**Momentum groups** (sum one line's q over all 8,000 grid points,
recomputing every segment and vertex inside the line;
[evidence/sto_qgroup.json](evidence/sto_qgroup.json)). This is 3,000
samples:
- the per-line deficit is **2.6%** for q, against 1.2% for the mode on the
  same lines;
- it grows with the span of the line, from 0.988 (span 1) to 0.97, 0.94
  and 0.93 (span ≥ 10).

The q cancellation cannot compound independently over all lines, because
that would violate the bound E[ρ] ≥ ⟨s⟩_A. So momentum interference is
stronger per line but correlated across lines.

**LiF-electron** ([evidence/lif_elec_modes_pairs.json](evidence/lif_elec_modes_pairs.json)):
- the mode groups would remove about 96% of its (small) deficit if all
  lines were summed, a variance gain of 1.14 against a ceiling of 1.15;
- the non-crossing subset covers 68% of lines and gains 1.05.

## (d) The right ceiling for Q: how much of its variance is the sign?

The sign ceiling 1/⟨s⟩² assumes that removing the sign leaves everything
else unchanged. On the native chains it does not.
[decompose_native.py](decompose_native.py) compares two per-measurement
variances, each with a blocking τ_int:
- the actual ratio-estimator influence, `h = s(O − R)/⟨s⟩`;
- the same chain with the sign set to +1, `h_O = O − ⟨O⟩`.

| | ⟨s⟩ | 1/⟨s⟩² | σ²(h) | σ²(h_O) | share not from the sign | **Q ceiling from removing the sign** |
|---|---|---|---|---|---|---|
| LiF-electron (β = 232) | 0.951 | 1.10 | 0.270 | 0.267 | 99% | **1.01** |
| STO (β = 232) | 0.680 | 2.17 | 0.054 | 0.048 | 88% | **1.14** |
| LiF-hole (β = 23.2, T = 500 K) | 0.096 | 110 | 81.9 | 19.2 | 23% | **4.27** |

([evidence/*_variance_decomposition.json](evidence/)). The sign doubles
the static variance, but it is *fast* noise (τ_int(h) = 17 against
τ_int(h_O) = 32 in STO), so it also decorrelates the slow O fluctuations.
The slow part of O is set partly by the order (38% of var(O), with τ of
86–160 measurements) and partly by other slow collective variables.

**Consequence.** For LiF-electron and STO at β = 232, *no* sign-removal
method can help Q by more than 1–14%, whatever E[ρ] says. Sign removal
matters only where ⟨s⟩ ≪ 1. LiF-hole at T = 500 K is such a case; at
β = 232 its sign is below resolution (paper S(τ) extrapolates to ~e⁻²³).

**LiF-hole, T = 500 K, native diagnostics**
([evidence/lif_hole500_modes.json](evidence/lif_hole500_modes.json)).
This is 3 chains with order 93–97 and every self-check clean.
- **Single-line mode group:** ρ = 0.935, a **6.5% deficit per line**
  against 1.2% in STO. The first 2 and 3 lines jointly give 0.86 and 0.80.
- **Independence:** joint over product is 0.999 and 0.998; by pair class it
  is 0.9992–1.0004 (disjoint and nested) and 0.9973–1.0002 (crossing).
- **Non-crossing set:** it covers only about 37% of lines, because
  crossings are frequent. E[∏ρ] over it is ≈0.59, so ⟨s⟩_B ≈ 0.16. Over all
  lines E[∏ρ] ≈ 0.20, so ⟨s⟩ would be ≈0.47.
- **4-vertex windows:** 0.9996, useless.

## (e) A real grouped chain B on native FEP-DMC ([bchain.f90](bchain.f90), [patch_bchain.py](patch_bchain.py))

**Target.** w_B(C) = |Re F_G|/|G|. G sums the live phonon modes of every
line in the greedy non-crossing set. F_G is computed *exactly* by folding
the lines inside out: each fold is a matrix `Σ_ν Dph_ν g_b(ν) M g_a(ν)`,
and modes do not change momenta.

**Kernel.**
- The native updates act as a π_A-reversible proposal, followed by a second
  stage min(1, r′/r) with r = w_B/w_A, and snapshot/restore.
- A uniform live-mode Gibbs refresh inside the group runs every 10 steps.
- *Optionally*, B-native add/remove (`FUTUREB_BCHAIN_ADDREM=1`, native
  PA₁ = PA₂ = 0). Native add_ph creates span-1 lines, which never cross, so
  the new line always joins the group. Proposal: segment, q, τ₁ uniform, τ₂
  with a mode-independent decay, and a uniform live representative. The
  acceptance is W_B′ p_rem / (W_B p_topo), where W_B is the absolute group
  weight including every positive factor.

**Estimator.** f_O = Re Σ_G(D·O)/|Re F_G|, carried through the fold as
(value, energy insertion, phonon-energy insertion).

**Self-checks, every run.** All passed:
- the current-mode fold reproduces the native Etrue increment and sign
  (≤ 2e-8);
- the fold sums equal explicit enumeration of two forced lines (≤ 1e-10);
- with grouping disabled, the chain is **bit-identical** to the native one.

**STO results** (3–6 chains, Nmcmc = 200×10⁴). A is the native chain with
the same seeds:

| variant | Q (eV) | Δ vs A | ⟨s⟩ | static var A/B | τ_int(h) B/A | τ_order B/A | var per measurement A/B | wall B/A |
|---|---|---|---|---|---|---|---|---|
| native A | −0.1420 ± 0.0008 | — | 0.680 | — | — | — | — | 1 |
| B, native add/remove + correction | −0.1413 ± 0.0015 | 0.4σ | 0.920 | 2.09 | 4.16 | 1.82 | 0.45 | 6.7 |
| B, no native mode move | −0.1406 ± 0.0012 | 0.8σ | 0.916 | 2.27 | 3.95 | 1.69 | 0.62 | 9.0 |
| B, B-native add/remove | −0.1407 ± 0.0008 | 0.9σ | 0.907 | 1.98 | 2.36 | 1.19 | 0.80 | 19 |

([evidence/sto_bchain_*_vs_native.json](evidence/)).

**The grouped measure works as designed:**
- it is unbiased;
- the sign rises from 0.68 to about 0.91, matching the prediction of about
  0.90 from the independent-line estimate;
- the static variance halves.

B-native add/remove removes most of the mixing loss (τ_order 1.8 → 1.19).
**On STO, however, it cannot win on Q**, because its ceiling is 1.14
(section d). What remains of the τ_int increase is the loss of fast sign
noise that used to decorrelate O. The wall cost of this prototype (6.7–19×)
comes from full O(Nph·order) folds after every accepted move; it is not
intrinsic.

**LiF-hole, T = 500 K** (sign-dominated regime).
[evidence/lif_hole500_bchain_between.json](evidence/lif_hole500_bchain_between.json)
compares 12 independent chains each, B-native add/remove against
hook-free native:

| | ⟨s⟩ | Q (eV) | between-chain var A/B (90% CI) | wall B/A | efficiency per wall (90% CI) |
|---|---|---|---|---|---|
| native A | 0.087 (0.010–0.174 by chain) | −1.89 ± 0.08 | — | 1 | — |
| grouped B | **0.147** | −1.72 ± 0.07 | **1.38** (0.49–3.9) | 6.7 | 0.21 (0.07–0.58) |

- **Sign.** It rises 1.7×, as predicted (≈0.16 from the non-crossing set,
  which covers only ~37% of lines here).
- **Variance per step.** For the first time it points in B's favour, but
  it is not significant with 12 chains.
- **Q.** The two agree at 1.6σ. The native low-sign chains (⟨s⟩ ≈ 0.01)
  give the most negative Q. That is the small-⟨s⟩ ratio bias of both
  estimators; nothing in the B self-checks (all clean) indicates a B bias.
- **Wall time.** The prototype still loses.

## Summary of (c)–(e)

- **Located.** In STO the sign problem is mostly phonon-mode
  interference, independent per line. Momentum interference is stronger
  per line but correlated. Local topology accounts for almost nothing.
- **Re-framed.** The Q ceiling from removing the sign is 1.01×
  (LiF-electron), 1.14× (STO at β = 232) and 4.3× (LiF-hole at β = 23),
  not 1/⟨s⟩². The sign is fast noise that also decorrelates the slow
  energy fluctuations.
- **Built and validated.** An exact, legal grouped-measure chain inside
  native FEP-DMC. It is unbiased on STO, raises the sign 0.68 → 0.91 (STO)
  and 0.087 → 0.147 (LiF-hole 500 K), and halves the static variance.
- **Not yet positive in wall time.** The remaining levers are:
  1. include crossing lines, whose modes need carried indices (bounded
     crossing width). For LiF-hole the predicted all-line sign is ≈0.47
     against 0.15;
  2. incremental evaluation, to bring the wall cost from ~7–19× down
     towards ~1.5–2×;
  3. target sign-dominated regimes: multiband, strong coupling, moderate
     τ, and G(τ) mode.

## (f) Acceleration plan, iteration log

**Stage 1: cost of the B chain** (LiF-hole, T = 500 K; profile in
`bchain_summary.dat`). Two measures:
- a value-only `eval_state` that caches the absolute log W_B, log w_A and
  log |G| of the current state;
- no re-evaluation after rejected B moves, and only w_A after a mode
  refresh.

The chain is bit-identical to before (same accept counts); 474 cache
checks pass (≤ 5e-12). The profile wall time halves (50.7 s → 25.2 s).
**Measured by CPU user time, which excludes the native start-up I/O, the
cost ratio to native is 3.3–3.5×, not 1.5×.** The native updates inside B
already cost as much as a whole native run.

A composite second stage every k native steps (K_A^k is still
π_A-reversible) cuts the ratio to 2.6× (k = 5) or 2.1× (k = 10). The price
is that the block acceptance drops to 55% and 42%.

**12 chains, B (fast path, k = 1) vs native**
([evidence/lif_hole500_b9_between.json](evidence/lif_hole500_b9_between.json)):
the variance ratio is 1.38 (90% CI 0.49–3.9) at a CPU cost of 3.46×, so
the **net efficiency is 0.40 (CI 0.14–1.13)**.

**Stage 2: wider groups** (offline, from native topology dumps;
[estimate_groups.py](estimate_groups.py),
[evidence/lif_hole500_group_rules_estimate.json](evidence/lif_hole500_group_rules_estimate.json)).
Crossing lines are carried with a bounded width K, nested ones folded:

| rule | lines grouped | ⟨s⟩_B estimate (⟨s⟩_A = 0.063) | relative cost |
|---|---|---|---|
| non-crossing (K = 0 = K = 1) | 36% | 0.110 | 1 |
| K = 2 | 43% | 0.126 | ×12 |
| K = 3 | 49% | 0.140 | ×69 |
| all lines (not exactly computable) | 100% | 0.346 | — |

A maximum-cardinality non-crossing set (O(n²) chord DP) adds only 14% of
lines over the greedy one.

**Lesson.** In LiF-hole, most lines cross, and any exact contraction pays
Nph^width. The sign mass beyond the non-crossing set is not reachable
cheaply. **Stop widening groups; change the lever.**

**Stage 3, next lever: mode Rao–Blackwellization on the unchanged native
chain.** For each line, average over its modes (a fibre of a partition),
then average over lines. It is measurement-only (every 100 steps), so the
kernel and mixing are unchanged and the cost is ≈ 1. Implemented in
`rb_window.f90` (`FUTUREB_MODE_RB=1`); the current mode reproduces w and
the native numerator (≤ 1.4e-12).

**Stage 3 result: mode Rao–Blackwell on the native chain**
([analyze_mode_rb.py](analyze_mode_rb.py),
[evidence/lif_hole500_mode_rb.json](evidence/lif_hole500_mode_rb.json)).
Twelve chains, compared paired on identical trajectories:
- the SE² ratio raw/RB is **1.083 ± 0.037**;
- the between-chain variance ratio is 1.04;
- Q agrees, and every self-check is clean;
- the CPU cost is 1.42×, because each measurement rebuilds the
  environments and every line interior;
- the **net is 0.77**.

**Lesson.** Averaging single-line fibres captures about 8%. The sign
information sits in the *joint* mode sum over all lines (∏ρ ≈ 0.18), and a
mean of single-line conditionals cannot multiply it.

**Stage 4 probe: a sign-optimized local mode basis**
([analyze_svd.py](analyze_svd.py),
[evidence/lif_hole500_svd_basis.json](evidence/lif_hole500_svd_basis.json)).
Write a line's mode sum as a bilinear T = Σ_ν Dph_ν g_b(ν) ⊗ g_a(ν), whose
rank is ≤ Nph, and take its SVD. That gives effective modes μ with the same
total. Per line, γ = Σ_μ|D_μ| / Σ_ν|D_ν| ≈ 0.98–0.99; on single-line fibres
E_A[γ] is exactly Z_A(μ)/Z_A. The exact two-line test gives joint over
product = **0.9999**, and 0.9997 for ρ.

Estimated signs on LiF-hole at 500 K (⟨s⟩_A = 0.105, 3 chains):

| scheme | ⟨s⟩ estimate | × native |
|---|---|---|
| μ basis on every line | 0.153 | 1.46 |
| non-crossing groups (the current chain B) | 0.172 | 1.64 |
| **non-crossing groups + μ basis on the other lines** | **0.220** | **2.1** |
| all modes summed (not exactly computable) | 0.469 | 4.5 |

**Barrier.** In the μ basis a line's two vertex matrices depend on *both*
endpoints' momenta and on Δτ. Every native update, which assumes one local
matrix per vertex, would need to be rewritten as a two-point update. The
B-chain correction cannot map ν-labelled states to μ-labelled ones. The
μ basis therefore needs a new native sampler. Its projected payoff is a
per-step gain of about 2× against a cost of about 1.5–2×, so a net of
roughly 1–1.3×.

## (g) Low-sign regime: the metric, the slow variable, and the native kernel

**The metric was wrong.** At LiF-hole T = 500 K the sign of a single chain
ranges from 0.01 to 0.26. The mean of per-chain ratios is then biased by
the chains that sit in low-sign regions. All chains sample the same
measure, so the estimate is the **pooled** ratio Σn_i/Σd_i. Its variance
comes from the chain-level influence h_i = (n_i − R d_i)/d̄
([compare_pooled.py](compare_pooled.py)).

Re-analysed this way, the (e)/(f) comparison of chain B with native
changes:

| | per-chain-ratio mean | pooled |
|---|---|---|
| native A (12 chains) | Q = −1.89 | Q = −1.72 ± 0.07 |
| grouped B (12 chains) | Q = −1.72 | Q = −1.66 ± 0.07 |
| A vs B | 1.6σ apart | agree at 0.7σ |
| variance ratio A/B | 1.38 | **1.08 (delta method), 1.16 (jackknife)** |

So B gains only about 1.1× per step, and its net is ≈ 0.33 after the
3.4× cost. **The chain-level variance is heavy-tailed**: the top two of 24
chains carry about 50% of var(h). They are the *high-sign* chains
(⟨s⟩ ≈ 0.18, mean order ≈ 65). With 12 chains, the 90% F interval on a
variance ratio is about ×/÷ 2.8, and a single batch can mislead (below).

**Where the slow part lives.**
- *Order.* ⟨s⟩ falls from 0.54 at orders 30–39 to 0.05 at orders 90–99,
  and the chain mean order predicts the chain sign (65 → 0.17, 89 → 0.01).
  The order drifts over thousands of measurements.
- *Beyond the modes.* The block sign ÷ E[∏ρ], i.e. the sign left after an
  exact mode sum, swings slowly from −0.17 to 0.97 within one chain. The
  slow component therefore sits above the mode level: momenta and topology.
  No mode grouping can touch it.
- *Topology features.* At the sample level, the sign does not correlate
  with the crossing number, mean span or number of external vertices
  (|corr| ≤ 0.03).

**Lever 1: an exact change-q move for internal lines** (`FUTUREB_CHQ`, mb16,
`change_q` in [bchain.f90](bchain.f90)). The native kernel changes a line's
momentum only by removing the line, and only span-1 lines are removable
(3.6% of removal attempts). change_q:
- picks a line uniformly and draws q′ ~ Pq and ν′ ~ Pnu(q′);
- shifts every segment across the line and recomputes energies,
  eigenvectors and vertex matrices;
- accepts against the full native weight (`eval_state`) with the exact
  proposal ratio.

With FUTUREB_BCHAIN, change_q is one more π_A-reversible piece of the
composite proposal.

*Self-checks, per chain:*
- 1500 momentum-conservation and continuity checks, all clean;
- the native O and sign equal an independent `evaluate()` to ≤ 2e-12.

*Exactness:*

| test | native | change-q (p = 0.3) | difference |
|---|---|---|---|
| maxOrder 7 (mean span 1.6) | −0.87393 ± 0.00039 | −0.87373 ± 0.00049 | 0.3σ |
| maxOrder 31 (mean span 6.3) | −1.3654 ± 0.0089 | −1.3607 ± 0.0078 | 0.4σ |

*LiF-hole at 500 K, p = 0.05* (46% accepted, mean span 18,
[evidence/lif_hole500_chq_pooled.json](evidence/lif_hole500_chq_pooled.json)):

| | chains | pooled Q | var(h) | CPU |
|---|---|---|---|---|
| native | 24 | −1.673 ± 0.036 | 15.8 | 37.1 s |
| change-q | 24 | −1.678 ± 0.034 | 14.6 | 56.1 s |

- The two agree at 0.1σ.
- The variance ratio is 1.08 (F 90% interval 0.53–2.2; bootstrap 0.44–2.7).
- The cost is 1.51×, so the **net is 0.71**.
- τ_int(order) is unchanged (206 against 190).

*The first 12 chains gave a ratio of 3.1 (CI 1.1–8.8) and a net of 1.8.
That was a fluctuation of the heavy tail: the next 12 native chains alone
halved the native var(h).*

**Lesson.** Refreshing internal momenta faster does not reach the slow
component, and order mixing is unchanged. Any low-sign claim needs at least
24 chains and a bootstrap.

**Lever 2 (offline, not built): order reweighting φ(n) = e^{−λ(n−78)}.**
It uses the exact estimator s·O/φ ÷ s/φ, and its static factors can be
computed from native traces:

| λ | static variance factor | slow-part factor |
|---|---|---|
| 0.02 | 1.28 | 0.84 |
| 0.04 | 1.87 | 1.01 |
| 0.08 | 5.6 | 3.4 |

s·P(n) peaks at orders 70–79, so the signed weight is not concentrated at
low order. Pushing the chain down only inflates 1/φ. **Not a lever.**

**Lever 3, in progress: external pairs.** EZ diagrams carry about 10
boundary-wrapping phonon pairs (about 21 external vertices). These form the
polaron's phonon cloud. remove_external_ph removes only the outermost pair,
so it is LIFO (tried 5,540 times in 2×10⁶ steps). Their momenta and number
are therefore structurally frozen.

change_q_ext (`FUTUREB_CHQ_EXT`, mb17) moves a pair: q′ on the head-side
vertex, and every segment *outside* the pair shifts by −(q′ − q). The
head, tail and last vertex share one eigenvector set, as the native code
keeps the periodic segment. In smoke tests it accepts 26–31%, and every
check, including head/tail periodicity, is clean.

**An upstream bug, found by the round trip.** The change-q move for external
pairs failed the maxOrder-7 exactness test: native −0.87393 ± 0.00039
against −0.87232 ± 0.00014, 3.9σ. The internal-only move had passed. A
round-trip check (C → C′ → C, `FUTUREB_CHQ_RT`, mb18) restored g, u and Pnu
exactly (≤ 9e-16), but **log w was off by up to 0.44**.

The cause is in `multiphonon_update_matrix::add_external_ph` at pin 05d08449:
- it samples a new q for the pair but **never calls `cal_wq_int`**;
- vn1%wq, and vn2%wq = vn1%wq, keep the frequencies left in the recycled
  vertex slot, or uninitialized memory on first use;
- those enter the pair's Dph, its time sampling and the energy estimator.

add_ph makes the call at the same point, and every other update computes or
copies wq. [patch_wqfix.py](patch_wqfix.py) adds the call as an opt-in
(`FUTUREB_WQFIX=1`, mb19). With it, the round-trip error is **3.6e-15**.

*Effect of the fix, fixed minus native, pooled:*

| case | chains | ΔE (eV) | σ |
|---|---|---|---|
| LiF-hole, maxOrder 7 | 4 + 4 | +0.0008 ± 0.0008 | 1.0 |
| LiF-electron, β = 232 (paper case) | 12 + 12 | +0.0010 ± 0.0032 | 0.3 |
| STO, β = 232 (paper case) | 6 + 6 | −0.0002 ± 0.0011 | −0.2 |
| LiF-hole, T = 500 K | 24 + 24 | −0.049 ± 0.052 | −0.95 |

The bug is real but **not detectable** in these results at the 1–3 meV level
(β = 232). The stale values are mostly LO-branch frequencies of earlier
lines, and that branch is flat. The paper's numbers are therefore unaffected
at this resolution. The code is still wrong, and the error would matter
wherever external phonons carry strongly dispersive or acoustic modes.

**Lever 3 result, on the fixed target** (mb19, `FUTUREB_WQFIX=1`,
`FUTUREB_CHQ_EXT=1`, p = 0.05; accepts about 42% internal and 28% external;
[evidence/lif_hole500_chqxfix_pooled.json](evidence/lif_hole500_chqxfix_pooled.json)).

*Exactness with the fix:*

| test | fixed native | fixed change-q with external pairs | difference |
|---|---|---|---|
| maxOrder 7 | −0.87311 ± 0.00074 | −0.87310 ± 0.00044 | 0.01σ |
| maxOrder 31 (without the fix) | −1.3654 ± 0.0090 | −1.3599 ± 0.0041 | 0.6σ |

*LiF-hole at 500 K, 24 vs 24 chains, both fixed:*

| | pooled Q | var(h) | chain sign mean ± sd | CPU |
|---|---|---|---|---|
| fixed native | −1.722 ± 0.037 | 17.7 | 0.090 ± 0.059 | 41.7 s |
| fixed change-q with external pairs | −1.672 ± 0.032 | 13.2 | 0.068 ± **0.025** | 64.7 s |

- Q agrees at 1.0σ.
- The variance ratio is 1.34 (F 90% interval 0.67–2.7; bootstrap 0.60–3.1).
- The cost is 1.55×, so the **net is 0.86 (CI 0.43–1.74)**.
- τ_int(order) is still about 200.

**Lesson.** Moving the frozen external cloud *does* reach the slow sign
component: the chain-to-chain sign variance drops **5.7×**, so ⟨s⟩ itself
is estimated about 3.7× more efficiently per CPU second. Q gains only 1.34×.
In native, chains with a higher sign also carry a proportionally larger
numerator, and the ratio estimator already cancels most of that correlated
slow fluctuation. What remains in var(h) is the slow O and order part
(section d), which faster momentum mixing does not shorten.

## Summary of (g)

- **Metric.** The pooled ratio over at least 24 chains, with a bootstrap.
  12-chain variance ratios mislead in both directions (3.1 → 1.08).
- **Levers tried on LiF-hole at 500 K**, all exact and validated. Their net
  efficiency for Q:

  | lever | net for Q |
  |---|---|
  | grouped chain B | ≈ 0.33 |
  | mode Rao–Blackwellization | 0.77 |
  | change-q, internal lines | 0.71 |
  | change-q, internal and external | 0.86 |
  | order reweighting (offline) | < 1 |

- **Side result.** An upstream FEP-DMC bug (stale external-phonon frequency),
  with an opt-in fix and no detectable effect on the paper's energies.
- **Where Q's variance now sits.** In the slow order and energy
  fluctuation (τ_order ≈ 200 measurements, not shortened by any move so
  far). The sign's slow component is reachable (external moves), but for Q
  it was already mostly cancelled by the ratio estimator.

## (h) Native equilibration: an exact general-span add/remove, and what it exposes

**Tuning native update probabilities** (add/remove 0.1 → 0.25 each; PA
enters the native acceptance, so this is exact). Over 24 vs 24 chains the
variance ratio is 0.54 at 0.73× CPU, so the **net is 0.73**
([evidence/lif_hole500_pa25_pooled.json](evidence/lif_hole500_pa25_pooled.json)).
More attempts do not help: native can remove only span-1 lines, so the
supply of removable lines is the limit.

**An exact general-span add/remove** (`FUTUREB_ANY`, mb20; `any_add` and
`any_remove` in [bchain.f90](bchain.f90)).
- *Remove:* any internal line. The pair is relabelled into the last slots
  with native `swap_vertex`, the interior momenta shift by −q, the eigen-
  systems of each changed segment are re-synced (copied, not recomputed,
  across shared segments and the periodic head/tail segment), and the line
  is unlinked.
- *Add:* τ₁ ~ U(0, τ_max), q ~ Pq, ν ~ Pnu, and τ₂ from an exponential
  truncated to (τ₁, τ_max) with rate ω_ν. The span shifts by +q.
- *Acceptance:* the exact ratio against `eval_state`.
- *New check:* `g_check` confirms that each segment's eigenvectors are the
  same on both ends. It is also clean on native states.
- *Proposal gauge:* Pnu from stored and from fresh eigenvectors is
  identical (Δ = 0), so gauge dependence of the proposal is ruled out. A
  gauge-invariant option exists (`FUTUREB_PNU_FRO`, mb21).

At full order it accepts 38–41% of adds and 48–53% of removes, with a mean
span of about 16. It **halves τ_int(order)**, from about 200 to 92
measurements. The Q variance per chain rises, however: over 24 vs 24 chains
the ratio is 0.57, so the **net is 0.51**
([evidence/lif_hole500_anyfix_pooled.json](evidence/lif_hole500_anyfix_pooled.json)).

**The discrepancy that turned out to be native's.** At maxOrder 31, with
16 chains each and the wq fix on:

| chain | Q | ⟨s⟩ | spread of chain signs |
|---|---|---|---|
| native (mb20, no moves) | −1.3542 ± 0.0024 | 0.753 ± 0.018 | 0.072 (min 0.59) |
| general add/remove | −1.3632 ± 0.0014 | 0.777 ± 0.006 | 0.024 |
| change-q with external pairs | **−1.3628 ± 0.0015** | 0.764 ± 0.003 | **0.010** |

The two exact moves are built on different mechanisms. They agree on Q at
**0.2σ**, and each disagrees with native at **3.0–3.3σ**. Both matched
native at maxOrder 7, where native mixes well.

Native chains start from the bare electron. Three of the 16 sit at
⟨s⟩ = 0.59–0.67 against a typical 0.78, and those same chains give the
highest E. They are stuck in metastable, low-sign regions and never leave
within 2×10⁶ steps. **Native's pooled Q therefore carries an initialization
bias of about +0.009 eV (0.7%) at this order**, and neither of the new
moves has it.

The residual 2σ tension in ⟨s⟩ between the two moves fits the picture:
general add/remove does not move the external cloud, and its chains are
still somewhat heterogeneous.

At full order (T = 500 K) the moved chains relax *downwards* in ⟨s⟩
during the run (by quarter, 0.089 → 0.056 and 0.072 → 0.047). Every native
set sits at 0.090–0.097 with no trend. Confirmation runs are in progress:
- native at 5× length at maxOrder 31;
- native against all moves combined at full order, at 5× length.

**Update: resolved, and the first net gain.** A fresh native set at
maxOrder 31 (16 chains with traces, seeds 16–31) gives
Q = **−1.3632 ± 0.0036**, which agrees with both moves. The first native set
of 16 gave −1.3542 ± 0.0024, so the two native sets differ from *each
other* by 2.1σ. Native's chain-to-chain scatter is heavier than its naive
SE: it has stuck chains, with ⟨s⟩ from 0.59 to 0.86. A 16-chain native
estimate is therefore unreliable at this order.

The stationary structure agrees across native, general add/remove and
change-q with external pairs, within errors, for:
- P(order), bin by bin to ≤ 0.5%;
- E[s | order];
- ⟨order⟩ (28.68, 28.70, 28.66).

There is **no evidence for a bias in either move**. A 5× native run
(8 chains, −1.3568 ± 0.0025) is also consistent within that scatter.

At full order (T = 500 K), native at 5× length drops its sign from
0.090 ± 0.012 to **0.061 ± 0.012**. That lands on the moves' 1× values
(0.060 and 0.068) and on all moves at 5× (0.057 ± 0.004, spread 0.011).
Native at 1× has not relaxed there either.

**Efficiency at maxOrder 31**, against all 32 native chains, pooled with a
bootstrap over chains:

| move (p = 0.3) | var(h) ratio | CPU ratio | **net** | bootstrap 90% |
|---|---|---|---|---|
| general add/remove | 5.49 | 2.34 | **2.35** | **1.40–4.37** |
| change-q with external pairs | 4.67 | 3.66 | 1.28 | 0.77–2.27 |

Evidence: [evidence/medo31_anyfix_vs_native32.json](evidence/medo31_anyfix_vs_native32.json)
and [evidence/medo31_chqxfix_vs_native32.json](evidence/medo31_chqxfix_vs_native32.json).

**Lesson.** Where native has metastable basins, an exact move that mixes
order (general span) or the phonon cloud removes the stuck chains. That
cuts the chain-level variance about 5× and gives the first net gain in this
project. Where the variance is not basin-dominated (LiF-hole at full order),
faster mixing buys nothing for Q.

**Correction to the "first net gain" above: not robust yet.** Adding two
more native batches (64 native chains in all) and move probabilities
0.1 and 0.6 changes the picture. All at maxOrder 31, 16 chains per set,
against the 64 native chains:

| general add/remove, p | var(h) ratio | CPU | net | bootstrap 90% | Q |
|---|---|---|---|---|---|
| 0.1 | 1.33 | 1.49 | 0.89 | 0.50–2.13 | −1.3575 |
| 0.3 | 4.94 | 2.31 | 2.14 | 1.40–3.96 | −1.3632 |
| 0.6 | 2.41 | 3.66 | 0.66 | 0.43–1.33 | −1.3583 |
| change-q with external pairs, 0.3 | 4.20 | 3.61 | 1.16 | 0.78–2.10 | −1.3628 |
| native (64) | 1 | 1 | 1 | — | −1.3588 |

- The gain is **not monotone in p**. Seven 16-chain batches are
  heterogeneous (χ² 15.4 on 6 dof, p = 0.017).
- The two low-variance batches are also the two at Q ≈ −1.363. The rest
  sit at about −1.358.
- A p-proportional bias is rejected: p = 0.6 is back with native.

**The cause: rare sign dips.**
- In both native and moved chains, the block sign (10 blocks per chain)
  drops episodically to 0.2–0.4 for about 10% of a run, against a typical
  0.8–0.9.
- Chains with dips have a higher mean order and more time at the cap:
  corr(chain sign, ⟨O⟩) = −0.65, corr(chain sign, ⟨order⟩) = −0.56 and
  corr(chain sign, P(cap)) = −0.59.
- How many dips a 16-chain batch catches sets both its Q and its variance.
- No move tried so far removes the dips (a p = 0.6 chain: 0.35–0.85).

The p = 0.3 advantage was most likely a batch that caught few dips. A
replicate p = 0.3 batch, run beside a fresh native batch, is in progress.

**Lesson (reinforced).** In this regime the error of a 16-chain batch is
set by rare-dip counting. Batch SEs understate the scatter by about 1.6×,
so a claimed variance ratio needs replicate batches, not one batch plus a
bootstrap.

**Replicate: the p = 0.3 gain is confirmed.** A second independent
p = 0.3 batch (16 chains, seeds 64–79) ran beside a fifth native batch.
Against all 80 native chains (5 batches):

| set | var(h) | CPU | net | bootstrap 90% |
|---|---|---|---|---|
| native batches (5) | 0.93–2.61e-4, pooled 1.80e-4 | 1 | 1 | — |
| p = 0.3, batch a | 3.07e-5 | 2.30 | 2.54 | 1.70–4.59 |
| p = 0.3, batch b | 2.26e-5 | 2.40 | 3.31 | 2.10–7.18 |
| **p = 0.3, a + b (32)** | — | 2.35 | **2.62** | **1.78–4.25** |

**Every** p = 0.3 batch has at least 3× lower var(h) than **every** native
batch. That is a clean separation between batches, not a bootstrap
inference. The "fewer dips" explanation given above was wrong: batch b
has native-like sign spread (0.051) yet 8× lower var(h). With the move,
each chain's numerator and sign fluctuate coherently, and the ratio
estimator cancels them. p ≈ 0.3 is near the optimum (p = 0.1 gives a net
of 1.05, and p = 0.6 gives 0.78).

**Open item: Q at maxOrder 31.** Native gives −1.3573 ± 0.0013 (5 batches)
and the moves give −1.3609 ± 0.0007 (5 batches), a gap of 0.27%.
- Both groups scatter beyond their SEs: χ² 8.2/4 for native, 9.0/4 for the
  moves.
- After inflating each group's SE by √(χ²/dof), the gap is **1.7σ**. That
  is not significant, but it is not excluded either.

**Full order, 10⁷ steps (5×)**
([evidence/lif_hole500_long_mix_vs_native.json](evidence/lif_hole500_long_mix_vs_native.json)):

| | ⟨s⟩ by quarter | τ_int(order) | τ_int(sign) | Q |
|---|---|---|---|---|
| native (12 chains) | **0.112 → 0.055 → 0.041 → 0.038** | 1327 | 14.3 | −1.735 ± 0.043 |
| all moves (11 chains; 1 OOM) | 0.074 → 0.055 → 0.059 → 0.050 | 532 | 2.7 | −1.788 ± 0.036 |

- Native relaxes about 3× over the whole 10⁷ steps. **A standard native
  run (2×10⁶ steps, 25% burn-in) reports ⟨s⟩ ≈ 0.09, biased high by
  about 2×.**
- The short-run τ_int(order) ≈ 190 was an artefact of blocking within a
  chain that is too short; the true value is about 1300 measurements.
- The combined moves relax within the first quarter, decorrelate order
  2.5× faster and the sign 5× faster.
- For Q, the two agree (0.95σ), and the variance efficiency is 0.74 at
  1.96× CPU.

**Summary of (h).**
1. **A net gain, replicated.** The exact general-span add/remove at
   p ≈ 0.3 gains 2.6× (90% 1.8–4.3) at maxOrder 31 over 32 vs 80 chains,
   and every batch is separated.
2. **Native is not equilibrated at full order.** At LiF-hole T = 500 K, a
   standard native run overstates ⟨s⟩ about 2×, and τ_order is about 1300
   measurements. The new moves equilibrate several times faster, though Q
   stays within noise.
3. **Open.** A possible 0.27% (1.7σ) Q offset at maxOrder 31.

**Correction to "Replicate: the p = 0.3 gain is confirmed": it is not.** A
third p = 0.3 batch (seeds 80–95) has var(h) = 1.13e-4, *inside* the range
of the native batches (0.93–2.61e-4, now 6 batches). That breaks the
batch-separation argument.

| | chains | var(h) | CPU | net | bootstrap 90% | Q |
|---|---|---|---|---|---|---|
| native | 96 (6 batches) | pooled | 1 | 1 | — | −1.3584 ± 0.0012 |
| general add/remove, p = 0.3 | 48 (3 batches) | 2.3e-5, 3.1e-5, 1.1e-4 | 2.42 | **1.08** | **0.67–1.92** | −1.3604 ± 0.0009 |

The Q gap is now −1.3σ raw and −0.7σ after inflating by batch χ², so
the 0.27% "open item" is gone.

**Lesson, the most important one of (h).**
- In this heavy-tailed regime, var(h) *itself* varies about 5× between
  16-chain batches of the same method.
- A net-efficiency claim based on between-chain variance was made and
  reversed twice here: 2.35 → retracted → "confirmed" 2.62 → 1.08.
- Robust efficiency claims need either many more batches (to estimate the
  distribution of batch variances) or a different estimator, e.g. long
  chains with the tail handled explicitly.
- What survives in (h):
  - both moves are exact, with P(order) and E[s | order] matching
    native;
  - there is evidence (drift over the quarters of the 5×-length native
    run, 2.5σ) that a standard native run at full order overstates ⟨s⟩;
  - the moves relax faster.

## (i) What is slow: the size of the phonon cloud

**Full order, p = 0.3 general add/remove** (24 chains,
[evidence/lif_hole500_any03_pooled.json](evidence/lif_hole500_any03_pooled.json)).
The net is **0.21** (0.10–0.46) at 3.25× CPU, and the sign still drifts
over the run (0.116 → 0.058).

**Moves only during burn-in** (`FUTUREB_MV_UNTIL`, mb22; 24 chains,
[evidence/lif_hole500_burnmix_pooled.json](evidence/lif_hole500_burnmix_pooled.json)).
The sign by quarter is 0.072, 0.058, 0.073, 0.090 (flat within noise, mean
0.073). Q is −1.772 ± 0.036 against native −1.722 ± 0.037, the CPU cost is
1.66× and the net is 0.70. Not a win.

**Slow-variable diagnostic** (mb23 adds nph_ext, the head |k|² and the
internal-line count to the trace). 12 native chains of 10⁷ steps:

| variable | τ_int (meas.) | corr(block ⟨s⟩, block mean) | E[s \| variable] |
|---|---|---|---|
| order | 1328 | −0.38 | — |
| **external pairs nph_ext** | **1788** | −0.30 | **0.125 (5) → ≈0.02 (≥18)** |
| internal lines | 1163 | −0.30 | 0.133 (18–21) → 0.021 (42–45) |
| head \|k\|² | 958 | −0.06 | flat |
| sign | 11.6 | — | — |

- Chain level: chains averaging 9–11 external pairs have ⟨s⟩ = 0.05–0.13,
  and chains at 13–15 have 0.01–0.08.
- nph_ext and the internal-line count explain 14% of the block-sign
  variance. Fast sign noise alone gives a block SD of about 0.08, so this is
  a large share of the slow part.

**Conclusion.** The slow component of the sign is the size of the phonon
cloud. Its slowest coordinate is the external-pair count, which native
changes only by LIFO add/remove at the outermost positions.

**A targeted move** (`FUTUREB_EXTAR`, mb24; `ext_add`, `ext_remove` and
`resync_shift`):
- a boundary-wrapping pair is inserted or removed at *any* position;
- τ₁ ~ U(0, τ_max), q ~ Pq and ν ~ Pnu; τ_max − τ₂ is drawn from an
  exponential truncated to (0, τ_max − τ₁) with rate ω_ν;
- every segment outside [τ₁, τ₂] shifts by −q (+q on removal);
- acceptance is exact against `eval_state`.

In smoke tests it accepts 16% of adds and 37% of removes at full order, and
the momentum, gauge, O/sign and Pnu-gauge checks are all clean. Validation
at maxOrder 7 and 31, and 24 full-order chains, are in progress.

## (j) A general external add/remove, and two more native bugs it exposed

**The move.** `ext_add` and `ext_remove` (`FUTUREB_EXTAR`, mb24+) insert or
remove a boundary-wrapping pair at any position. A generic `resync_shift`
applies the momentum shift of the outside region, keeps each segment's
eigen-system identical on both ends and on the periodic head/tail segment,
and recomputes the vertex matrices that changed. A round trip (C → add →
remove the same pair) returns log w and both proposal probabilities to
≤ 4e-15.

**What it found** (LiF-hole T = 500 K, maxOrder 7, 8 chains per set):

| kernel | Q |
|---|---|
| native, pin 05d08449 (wq fix only) | −0.87311 ± 0.00040 |
| native + support fix only | −0.87177 ± 0.00022 |
| native + reference-trace fix only | −0.87728 ± 0.00014 |
| **native + both removal fixes** | **−0.87630 ± 0.00033** |
| replica of native's external add/remove (same support, same signed truncated-exponential τ densities, ν before τ), `eval_state` weight, native external moves off | −0.87643 ± 0.00029 |
| my outermost-only move (uniform τ), native external off | −0.87641 ± 0.00040 |
| my outermost-only move, any τ | −0.87670 ± 0.00034 |
| **ordered** general move + native (external off) | −0.87673 ± 0.00027 |
| pure own moves (ordered general external, any-span, change-q), native mode changes only | −0.87630 ± 0.00022 |

**Bug 2, `remove_external_ph` reference trace.** For a non-empty diagram,
the trace of the configuration *without* the pair uses `v_head%ekout` for
the wrap segment. The pair still exists at that point, so this is momentum
k − q; the pair-less wrap carries k (`vn1%ekout`). `add_external_ph`'s
identical line is correct, and so is the removal's empty-diagram branch.
The removal acceptance therefore compares the with-pair trace with a
reference on the wrong band energies. This only matters for multiband
systems: with one band, E − E_min = 0 and the error cancels exactly.
Opt-in fix: [patch_extrmfix.py](patch_extrmfix.py) (`FUTUREB_EXTRMFIX=1`).

**Bug 3, `remove_external_ph` support.**
- `add_external_ph` draws τ₁ only on [0, min(τ_first, τ_max/2)] and τ₂
  only on [max(τ_last, τ_max/2), τ_max].
- Vertex-time moves let outermost external vertices drift outside those
  ranges.
- The removal evaluates the reverse-add densities with `exp_sample_omp`
  in density mode, which has no range check, so such pairs are removable
  although add can never recreate them.
- Opt-in fix: [patch_extfix.py](patch_extfix.py) (`FUTUREB_EXTFIX=1`). Fixing
  the trace alone still leaves a 3σ offset.

**The crux.** With both fixes, native (−0.87630) equals the
`eval_state`-weighted replica of its own proposal (−0.87643). The replica
differs from native only in how the weight ratio is computed, so this
isolates native's acceptance ratio as the error.

**A constraint, not a bug.** `update_swap` refuses to swap a head-attached
external vertex with a tail-attached one ("should not cross"). Native adds
pairs outermost, and time moves cannot reorder vertices, so native's
diagram space has the invariant **every head-attached external vertex
precedes every tail-attached one**. It is part of the estimator's
definition.

My first general move did not enforce it and sampled a larger space. That
gave a consistent group B at about −0.8749:
- pure own moves −0.87488;
- general move + native −0.87503;
- general move + fixed native −0.87507.

Two restricted variants separate the causes:
- outermost-only insertion cannot violate the invariant, and gave group A;
- insertion restricted to τ₁ < τ_max/2 < τ₂ at any position violates it
  only rarely, and fell in between (−0.87534).

The general add now rejects placements that break the ordering. Every
exact kernel then agrees at −0.8763 to −0.8767.

The table's other false leads were cleared along the way:
- a gauge-dependent Pnu (stored and fresh Pnu agree exactly);
- non-hermitian SVD tables (deviation 7e-16);
- native internal add/remove and swaps, which were swapped out one at a
  time.

**Effect of all three native fixes on the paper's cases (β = 232).**

| material | native | all fixes | shift |
|---|---|---|---|
| LiF-electron (12 + 12) | 9.10376 ± 0.00148 | 9.10477 ± 0.00279 | +1.0 ± 3.2 meV (0.3σ); the removal fixes are bit-identical to the wq-only run (single band, and the support case never occurred) |
| STO (6 + 6) | 11.68550 ± 0.00079 | 11.68575 ± 0.00064 | +0.25 ± 1.01 meV (0.2σ); the fixes act (multiband) but the effect is below 1 meV |

The published energies are unaffected at the 1–3 meV level. The bugs are
real and shift low-order results: LiF-hole at maxOrder 7 moves 0.37% (11σ).

**Lessons.**
1. An exact replica of a native move, with only the weight computation
   swapped, is the sharpest detailed-balance probe. It found bug 2 in one
   step once the proposal was matched.
2. Before blaming detailed balance, check that both kernels sample the
   *same state space*. A constraint hidden in an unrelated move (the swap
   rule) produced a stable, reproducible 4σ discrepancy between two exact
   samplers.

## (k) Toolkit, and the open full-order question for the external move

**Toolkit** (see [README.md](README.md)).
- [prepare_fepdmc.py](prepare_fepdmc.py) patches a pristine FEP-DMC tree at
  the pin in one step: make.sys, portability, the moves and the three opt-in
  native fixes. Applied to a clean checkout, it reproduces the mb32 sources
  byte for byte, and a from-scratch build succeeds.
- [validate_exactness.py](validate_exactness.py) is the end-to-end check:
  independent kernels (fixed native, pure Future B moves, mixed) must agree
  on pooled Q at low order. It passes on the maxOrder-7 runs (−0.02σ).
- The pooled estimator is unit-tested in `tests/test_native_rb_tools.py`.

**Full order, LiF-hole T = 500 K, all native fixes on, 24 vs 24 chains**
([evidence/lif_hole500_ext_allfix_pooled.json](evidence/lif_hole500_ext_allfix_pooled.json),
[evidence/lif_hole500_allfix_vs_wqfix.json](evidence/lif_hole500_allfix_vs_wqfix.json)):

| kernel | Q | ⟨s⟩ | external pairs (by quarter) | τ_int(ext. pairs) |
|---|---|---|---|---|
| fixed native | −1.627 ± 0.041 | 0.111 | 8.4, 9.5, 8.9, 9.2 | 231 |
| fixed native + ordered external move (p = 0.1) | −1.798 ± 0.042 | 0.062 | 12.1, 11.7, 11.8, 11.9 | 56 |

Both kernels are flat over the quarters, yet they disagree by 2.9σ in Q and
decisively in the pair count. At low and intermediate order every kernel
agrees:

| cap | fixed native | ordered move (native ext off) | ordered move + fixed native | pairs |
|---|---|---|---|---|
| maxOrder 7 | −0.87630 | −0.87673 | — | ≤ 3 |
| maxOrder 21 | −1.16939 ± 0.00212 | −1.16812 ± 0.00083 (0.6σ) | −1.17048 ± 0.00072 (−0.5σ) | ≈ 2.2 |

maxOrder 51 (about 6.5 pairs per diagram) also agrees. Fixed native
gives −1.7461 ± 0.0103 with 6.77 ± 0.24 pairs. The move without native
external moves gives −1.7548 ± 0.0033 with 6.40 ± 0.05 pairs (−0.8σ), and
the move plus fixed native gives −1.7415 ± 0.0051 with 6.43 ± 0.06 pairs
(+0.4σ).

**Resolution: native does not equilibrate the external-pair count at full
order.** 24 chains used the external moves only during burn-in
(`FUTUREB_MV_UNTIL`), then ran pure fixed native
([evidence/lif_hole500_burnext_vs_allfix.json](evidence/lif_hole500_burnext_vs_allfix.json)):

| kernel | pairs by quarter | ⟨s⟩ | Q |
|---|---|---|---|
| fixed native from the empty start | 8.4, 9.5, 8.9, 9.2 | 0.111 | −1.627 ± 0.041 |
| moves in burn-in, then pure fixed native | **11.4, 11.6, 10.9, 11.4** | **0.053** | **−1.771 ± 0.103** |
| fixed native + external move throughout | 12.1, 11.7, 11.8, 11.9 | 0.062 | −1.798 ± 0.042 |

Once equilibrated, pure native *stays* at about 11.3 pairs. The 9.0 it
reaches from the empty start is a quasi-stationary state of its slow
dynamics (native τ_int(pairs) ≳ 1800 measurements; the external move gives
56).

**A standard native run at LiF-hole T = 500 K is therefore biased by
about 10% in Q and about 2× in ⟨s⟩ even with all three fixes.** Fixed
native plus the ordered external move (p ≈ 0.1) is exact (validated at
maxOrder 7, 21 and 51) and reaches the equilibrium. This is the
recommended configuration where external pairs are abundant. Its value is
correctness, not per-step variance: CPU is 1.84× and var(h) is similar.

**Paper cases with full external-pair equilibration** (β = 232; all three
fixes, and in the last column also the ordered external move at p = 0.1;
[evidence/external_pair_validation.json](evidence/external_pair_validation.json)):

| material | native | all fixes | all fixes + external move | CPU per chain |
|---|---|---|---|---|
| LiF-electron (12 chains each) | 9.10376 ± 0.00148 | 9.10477 ± 0.00279 | 9.10632 ± 0.00128 | 33 / 45 / 333 s |
| STO (6 chains each) | 11.68550 ± 0.00079 | 11.68575 ± 0.00064 | 11.68587 ± 0.00066 | 42 / 54 / 315 s |

Every entry agrees within 1.3σ (≤ 3 meV). **The published energies of both
paper cases are robust** to the three native bugs and to native's slow
external-pair equilibration.

At β = 232 there are only about 1.9 pairs per diagram, and the external
move accepts about 0.6% of adds, so it costs about 7× CPU for no change. It
belongs in the regime where external pairs are abundant (low sign,
multiband, e.g. LiF-hole at T = 500 K). There it removes a bias of about
10% in Q.

**Independent confirmation: long native from the empty start.** 6 chains
of 10⁷ steps (5×) of fixed native, no Future B move:

| run | mean external pairs | ⟨s⟩ | Q |
|---|---|---|---|
| fixed native, 2×10⁶ steps | 9.0 | 0.111 | −1.627 ± 0.041 |
| fixed native, 10⁷ steps | ≈ 10.6 (chain means 8.8–13.1) | 0.069 | −1.727 ± 0.069 |
| fixed native + external move, 2×10⁶ steps | 11.9 | 0.062 | −1.798 ± 0.042 |

Given 5× more steps, pure native drifts most of the way to the external
move's equilibrium, with the large chain-to-chain spread expected from
τ_int(pairs) ≳ 1800. This confirms the diagnosis: the difference is native
under-equilibration, not a bias of the move.

## Summary of (i)–(k)

- **The slow variable is the size of the phonon cloud.** Its slowest
  coordinate is the external-pair count.
- **Three upstream FEP-DMC bugs, all in external-pair handling.** Each has
  an opt-in fix:
  1. stale phonon frequency in `add_external_ph`;
  2. wrong reference trace in `remove_external_ph` (multiband);
  3. missing support check in `remove_external_ph`.
- **Native's diagram space has a constraint** that exact moves must
  respect: head-attached external vertices precede tail-attached ones.
- **Native under-equilibrates the external-pair count** in the low-sign
  multiband regime. At LiF-hole T = 500 K a standard run is biased by about
  10% in Q and about 2× in ⟨s⟩. The ordered external move is exact and
  removes that bias; its benefit is correctness, not per-step variance.
- **The paper's β = 232 cases (LiF-electron, STO) are unaffected** by all of
  the above within 1–3 meV.
- **Toolkit:** `prepare_fepdmc.py`, `validate_exactness.py` and `README.md`,
  verified from a pristine pin to a working build.

**Move-probability scan** (all fixes, 24 chains each,
[evidence/lif_hole500_ext_pscan.json](evidence/lif_hole500_ext_pscan.json)):

| p | Q | ⟨s⟩ | pairs (by quarter) | τ_int(pairs) | CPU |
|---|---|---|---|---|---|
| 0, fixed native | −1.627 ± 0.040 | 0.111 | 8.4, 9.5, 8.9, 9.2 | 231* | 41 s |
| 0.02 | −1.772 ± 0.044 | 0.053 | 12.0, 12.1, 12.0, 12.1 | 135 | 78 s |
| 0.05 | −1.791 ± 0.033 | 0.063 | 11.9, 11.9, 11.8, 12.0 | 94 | 85 s |
| 0.1 | −1.798 ± 0.041 | 0.062 | 12.1, 11.7, 11.8, 11.9 | 56 | 75 s |

\* Blocking within 2×10⁶-step chains; the long runs give ≳ 1800.

Already p = 0.02 reaches the equilibrium. The CPU is nearly independent of
p, so the cost relative to native reflects the larger equilibrium diagrams,
not move overhead. **Recommended: `FUTUREB_EXTAR=1 FUTUREB_EXTAR_P=0.02`
with the three native fixes.**

