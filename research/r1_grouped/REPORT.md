# R1 grouped consumer: Stage F1–F3 report

Scope: stages R1-F1 to F3 of
[`R1_REAL_MATERIAL_GROUPED_CONSUMER.md`](../../docs/future_work/R1_REAL_MATERIAL_GROUPED_CONSUMER.md).
This is a finite, enumerable toy with no material file. The derivation is
in [DERIVATION.md](DERIVATION.md).

The run below produces `evidence/*.json` and `evidence/run.log`, with
118/118 checks PASS:

```
.venv/bin/python research/r1_grouped/run_f1_f3.py --steps 400000
```

The regression tests are `tests/test_r1_grouped.py` (8 tests, about 2 s).

## Verdict

| Question | Answer |
|---|---|
| Can a grouped measure be written down legally, including variable order, multiplicity, reverse moves, open spectators and signed/complex non-commuting weights? | **Yes** (F1 closed) |
| Does R1 genuinely participate in that consumer? | **Yes.** The group weight is a product of summed window operators. In the compiler regime that operator *is* the compiled Diagram Compiler two-band n=2 `Op` (error 1.9e-16) |
| Does it pass an independent oracle and exact stationarity? | **Yes** (F2, F3) |
| Is it worth carrying to LiF (F4+) in this form? | **Not on this evidence.** See the efficiency section |

## Setup

- Configuration space: `G = 8` time points, `L = 2`, orders 0–4.
- 5,937 configurations, 4,801 groups, with group sizes {1, 3, 9}.
- **Measure A** is native `|Re D|` (BOUND_C). It is run with native moves
  only, and optionally with a window heat-bath.
- **Measure B** uses tiled groups: `w_B = |Re F(G)|/3^m`. It is run with
  native MH moves on `w_B`, and optionally with a free uniform refresh
  inside the group.

| regime | vertex | ⟨s⟩_A | ⟨s⟩_B | Z_A/Z_B | weight in configs with ≥1 tiled window |
|---|---|---|---|---|---|
| R0_compiler | `(g/√L)σz` (compiler family) | 1.000 | 1.000 | 1.000 | 0.548 |
| R1_signed_interband | complex, k-dependent, interband | 0.561 | 0.602 | 1.073 | 0.296 |
| R2_signed_mixed | complex, k-dependent, mixed | 0.700 | 0.747 | 1.068 | 0.457 |

## Legality results (all PASS)

- **Oracle agreement.** Per-diagram weights agree with an independent
  oracle to ≤ 5e-15. The oracle uses a Taylor exponential, time-stamped
  lines and key-based groups. `Z_phys`, `Z_B` and the group count also
  agree.
- **Lemma 3 (partition).** 0 violations. The negative control
  "first eligible window" breaks closure on 512 states.
- **Lemma 4 (factorization).** The product of summed window operators
  equals the explicit member sum to ≤ 3e-16 in every regime. With the
  compiled compiler `Op`, the error is 1.9e-16.
- **Sign theorem.** `Z_B ≤ Z_A`. Equality holds in the positive regime.
- **Unbiasedness.** `E_w[f_O]/E_w[f_1]` equals the signed physical ⟨n⟩ and
  ⟨crossings⟩ to ≤ 6e-15 for A, B, and the legal `|D|` + `Re D/|D|`
  variant.
- **Exact kernels.** Every legal kernel (A native, A heat-bath, B native,
  B refresh) satisfies `max|πP−π|/max π ≤ 2e-15` and detailed balance
  ≤ 2e-17, and is irreducible on its support.
- **Negative controls.** All fail as required:

  | control | observed failure |
  |---|---|
  | NC1: no `1/|G|` | biased 24–61% |
  | NC2: `|D|` with `sgn Re D` | biased 0.4–4% (complex regimes) |
  | NC3: non-partition grouping | biased 0.2–7%; refresh breaks `πP=π` by 1.5–9% |
  | NC4: heat-bath on eligible windows only | `πP≠π` by 1.6–11% |

- **Monte Carlo.** 400k direct-draw steps per chain; all 12 estimates are
  within 1.3σ of the exact values.

## Efficiency results (exact, per Monte Carlo step)

These are exact asymptotic variances of the ratio estimator, from the
Poisson equation on the full transition matrix, written as
`σ² = static variance × τ_int`. Lower is better.

| regime | observable | A native | B native | A + heat-bath | B + refresh |
|---|---|---|---|---|---|
| R0 | ⟨n⟩ (group-invariant) | **15.8** | 16.1 | 22.7 | 23.3 |
| R0 | ⟨crossings⟩ | 8.76 | **6.63** | 11.0 | 9.47 |
| R1 | ⟨n⟩ | **18.9** | 23.6 | 26.7 | 33.3 |
| R1 | ⟨crossings⟩ | 38.4 | **35.6** | 54.6 | 51.9 |
| R2 | ⟨n⟩ | **24.5** | 25.3 | 30.6 | 34.4 |
| R2 | ⟨crossings⟩ | 12.5 | **11.5** | 17.5 | 16.9 |

What the decomposition shows:

1. **The sign gain is real but small.** B lowers the static variance by
   the expected amount: in R1, 1.33 against 1.53 for ⟨n⟩. But the gain
   is capped at `(Z_A/Z_B)² ≈ 1.15`. In a random scan of 90 parameter
   sets, the best `Z_A/Z_B` was 1.073. Only 30–55% of the weight sits in
   configurations that have any eligible tiled window at all, and most
   cancellation happens *between* groups (different times and momenta),
   not between re-pairings of one window.
2. **B mixes more slowly.** For the group-invariant observable ⟨n⟩,
   `τ_int` rises from 12.3 to 17.8 in R1 and from 25.0 to 29.6 in R2.
   This outweighs the sign gain, so B is 3–25% *worse* than native A.
3. **B's one clear win is Rao–Blackwellization.** For observables that
   vary inside a group, the conditional average `Ō(G)` lowers the static
   variance. B native beats A native by 7–24% on ⟨crossings⟩.
4. **Group moves at 30% never pay off per step.** The heat-bath or
   refresh takes steps away from native moves and cannot change `n`,
   times or `q`. The B refresh costs no weight evaluation, so its
   per-cost value is untested. That is F7 territory.
5. **Positive models get nothing from the sign.** The compiler family
   (`σz` vertices) is exactly sign-free in the tested regime (0 negative
   configurations). Single-band Fröhlich/Holstein diagrams are positive
   too. For those, B can only help through Rao–Blackwellization of
   non-invariant observables. The target `Q` (an energy from a ratio of
   sums) is not obviously of that kind.

## What this means for F4+

The legality obstacle that stopped Future B is removed, at toy scale. A
correct grouped measure with R1 as its consumer now exists, and it has
been checked exactly.

What the toy does *not* support is the hope that grouping four-vertex
windows buys material efficiency. Three questions have to be answered
before F4 is justified:

1. **LiF's average sign ⟨s⟩ under native `|Re D|` sampling. Answered in
   [lif_sign/LIF_SIGN.md](lif_sign/LIF_SIGN.md): ⟨s⟩ = 0.944 ± 0.002**
   (102 production chains, including the upstream authors' reference
   output). Even perfect grouping could lower the variance only by a
   factor of 1.12. Carrying the toy's 4-vertex recovery over gives about
   1.02. **The sign route is no-go for LiF-electron.**
2. **Whether the LiF estimator of `Q` varies inside a group.** If it
   does, the Rao–Blackwell gain seen here (7–24%) could carry over.
3. **Larger windows (6 vertices, 15 pairings).** These put more
   cancellation inside a group, but eligibility becomes rarer and group
   evaluation costs more. This can be tested on this same toy before any
   Fortran.

## Not established

This work does not establish:
- any LiF or material result;
- external phonon legs;
- continuous time (the proofs carry over, but that is untested);
- windows other than four vertices;
- wall-clock or evaluator cost (F7);
- equal-precision efficiency on `Q` (F8).
