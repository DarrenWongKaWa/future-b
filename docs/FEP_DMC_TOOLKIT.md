# FEP-DMC toolkit (`future_b.fepdmc`)

Source patches, a Docker run driver and estimators on top of upstream
FEP-DMC (Luo–Bernardi), pinned at `05d08449cffdbd0dfbbbf5009add5cc887bc754b`
([provenance/UPSTREAM_FEP_DMC.json](../provenance/UPSTREAM_FEP_DMC.json)).
It has three parts:

- **three native bug fixes**, all opt-in at run time (two new; the third is
  the C0 defect, made switchable);
- **exact Future B Monte Carlo moves**;
- **diagnostics and estimators** for the low-sign regime.

Results, failure lessons and retractions are in
[NATIVE_REPORT.md](../research/r1_grouped/native_rb/NATIVE_REPORT.md),
sections (a)–(j). The toolkit is a LEVEL 0 source transform plus Python
drivers. It is not a compiled plugin, and it makes no speedup claim.

## Install and quick start

```bash
pip install .                   # from a checkout; installs the future-b-fepdmc command

# 1. patch a pristine checkout at the pin
#    profile "research" = fixes + moves + diagnostics; "fixes" = fixes only
future-b-fepdmc prepare <path>/perturbo-fep-dmc --profile research

# 2. build pert-src inside the QE 6.5 tree (gfortran, serial make)
cd <ws>/build/q-e-qe-6.5/<build>/pert-src && make

# 3. run chains in Docker
export FUTUREB_FEPDMC_WS=<ws>  FUTUREB_FEPDMC_DATA=<FEP-DMC dataset dir>
future-b-fepdmc run prepare-tables lif_hole --alias <ws>/alias.py
future-b-fepdmc run ez lif_hole 8 --build <build> --temp 500 --maxorder 7 \
    --wqfix --extfix --extrmfix --tag my_runs

# 4. end-to-end exactness check (independent kernels must agree)
future-b-fepdmc validate --build <build>
```

`prepare` applied to a clean pin reproduces, byte for byte, the sources of
the research build mb32. Each patch asserts its anchors exactly once and
refuses a tree it does not recognise.

### Configuration

| flag | environment variable | default |
|---|---|---|
| `--ws` | `FUTUREB_FEPDMC_WS` | `./fepdmc_ws`, mounted at `/work` |
| `--data` | `FUTUREB_FEPDMC_DATA` | required; mounted read-only at `/data` |
| `--image` | `FUTUREB_FEPDMC_IMAGE` | `r5p0-env:ubuntu2004` (QE 6.5 toolchain) |
| `--build` | — | `perturbo-fep-dmc-pkg`, i.e. `<ws>/build/q-e-qe-6.5/<build>/pert-src/perturbo.x` |
| `--tables` | — | `<ws>/tables/<material>/gkq-20` |

Runs land in `<ws>/<tag>/<material>/chainNN` with `run_meta.json` (seed,
switches, command). Materials: `lif_elec`, `lif_hole`, `sto`, `anatase`,
`anatase_b3`. `tabulate-H` needs a build made without
`-fmax-stack-var-size=1`; pass it with `--tables-build`.

## Native bug fixes (upstream pin 05d08449)

| switch (`run` flag) | patch | bug |
|---|---|---|
| `FUTUREB_WQFIX=1` (`--wqfix`) | [wqfix](../src/future_b/fepdmc/patches/wqfix.py) | `add_external_ph` never calls `cal_wq_int`, so external pairs keep the stale phonon frequency of the recycled vertex slot. **Known since v1.0: the same defect C0 fixes** (below) |
| `FUTUREB_EXTRMFIX=1` (`--extrmfix`) | [extrmfix](../src/future_b/fepdmc/patches/extrmfix.py) | `remove_external_ph` builds the pair-less reference trace at momentum k − q instead of k; multiband only |
| `FUTUREB_EXTFIX=1` (`--extfix`) | [extfix](../src/future_b/fepdmc/patches/extfix.py) | `remove_external_ph` evaluates the reverse-add density without a range check, so pairs outside add's τ support are removable |

**Relation to C0.** The stale-frequency bug is not new in v1.3.0. Future B
recorded it in v1.0 and ships the unconditional fix as the C0 source
adapter ([C0_PUBLIC_ADAPTER.md](C0_PUBLIC_ADAPTER.md)), on the same line.
The toolkit re-found it independently and measured its effect on EZ
energies; `FUTUREB_WQFIX` makes it switchable for A/B runs against unfixed
native. The two `remove_external_ph` bugs are new. On a tree with C0
applied, `prepare` still works and `--wqfix` is redundant. C0 refuses a
tree that `prepare` has already patched.

**Effect of the fixes.** Use all three for a correct target.

| case | unfixed | all fixes |
|---|---|---|
| LiF-hole, T = 500 K, maxOrder 7 | −0.87311 | −0.8763 (11σ) |
| LiF-hole, T = 500 K, full order | ⟨s⟩ 0.090 | ⟨s⟩ 0.111, about 3 fewer external pairs, Q +0.095 eV (1.7σ) |
| LiF-electron and STO at β = 232 (paper cases) | — | unchanged within 1–3 meV |

The paper's LiF-hole case at β = 232 is 3-band and could be affected. There
the sign cannot be resolved, so the effect is not quantified.

## Recommended configuration

| goal | switches |
|---|---|
| correct native target | `--wqfix --extfix --extrmfix` |
| where external pairs are abundant (low sign, multiband, e.g. LiF-hole at T = 500 K) | the above plus `--extar 0.02` (anything in 0.02–0.1 reaches the same equilibrium) |

**Why the external move is needed there.** From the empty start, native
equilibrates the external-pair count far too slowly (τ_int ≳ 1800
measurements). A standard 2×10⁶-step run sits in a quasi-stationary state
with about 9 pairs instead of about 11.5. That biases Q by about 10% and
⟨s⟩ by about 2×. The ordered external move reaches the equilibrium and is
exact (maxOrder 7, 21, 51). p = 0.02, 0.05 and 0.1 all give the same
Q (−1.77 to −1.80) and pair count (11.9–12.0)
([lif_hole500_ext_pscan.json](../research/r1_grouped/native_rb/evidence/lif_hole500_ext_pscan.json)).
CPU is about 1.9× native at every p. That is mostly physical: the correct
equilibrium has larger diagrams, so native moves cost more. It is not move
overhead, and the move does not reduce per-step variance.

## Future B moves (all exact; inert unless enabled)

| switch (`run` flag) | move |
|---|---|
| `FUTUREB_CHQ`, `FUTUREB_CHQ_P` (`--chq P`) | change-q: new momentum for an internal line, span shifted |
| `FUTUREB_CHQ_EXT` (`--chq-ext`) | change-q also for boundary-wrapping external pairs |
| `FUTUREB_ANY`, `FUTUREB_ANY_P` (`--any P`) | general-span add/remove of internal lines (native: span-1 only) |
| `FUTUREB_EXTAR`, `FUTUREB_EXTAR_P` (`--extar P`) | external-pair add/remove at any position, respecting native's ordering (every head-attached external vertex precedes every tail-attached one) |
| `FUTUREB_MV_UNTIL=N` (`--mv-until N`) | apply the moves only for the first N steps (burn-in) |
| `FUTUREB_BCHAIN` (+ `_GROUP`, `_ADDREM`, `_BLOCK`, `_SRULE`, `_REFRESH`, `_PAR`) (`--bchain`, `--block`, `--srule`) | grouped-measure chain B (phonon modes folded over non-crossing lines) |

Moves and chain B need the `research` profile. With the `fixes` profile
only the three fix switches exist.

Validation. Every move passes a round trip (C → C′ → C restores log w and
the proposal probabilities to ≤ 4e-15) and per-chain momentum, gauge and
O/sign self-checks. At maxOrder 7 every exact kernel reproduces fixed native
(`future-b-fepdmc validate`).

**Efficiency.** No move has a demonstrated net gain for Q.

| lever | net efficiency |
|---|---|
| chain B | ≈ 0.33 |
| mode RB | 0.77 |
| change-q | 0.71 / 0.86 |
| general add/remove | 0.51 (full order), ≈ 1.1 (maxOrder 31) |
| moves in burn-in only | 0.70 |

They do mix the slow variables faster. τ_int(external pairs) drops from
≳1800 to 56, and the chain-to-chain sign spread shrinks 2–6×. For the
external move this corrects a native equilibration bias (see above).

## Diagnostics and switches for experiments

- `FUTUREB_SEED` reproducible chains (`run` sets `--seed0 + 7919·i`).
- `FUTUREB_RB`, `FUTUREB_MODES*`, `FUTUREB_QGROUP`, `FUTUREB_MODE_RB`,
  `FUTUREB_MODE_SVD` measurement-side grouping and mode diagnostics.
- `FUTUREB_CHQ_RT` round-trip check.
- `FUTUREB_HERM_TEST` hermiticity of the vertex tables.
- `FUTUREB_EXTAR_OUTER`, `_RPOS`, `_RTAU`, `_MIMIC`, `_UNORDERED`
  restricted and replica variants of the external move, used to isolate the
  native bugs.
- `FUTUREB_PNU_FRO` gauge-invariant mode proposal.

Traces: `chq_trace.dat` (numerator, sign, order, external pairs, head |k|²,
internal lines) and `chq_summary.dat` (acceptances and self-checks).

## Estimators

Use `future-b-fepdmc compare` (Python: `future_b.fepdmc.pooled_side`). It
pools the ratio Σn/Σd over chains and gives the chain-level variance, an F
interval (needs scipy), the CPU ratio and the efficiency. In low-sign runs,
do **not** average per-chain ratios. Do not trust a variance ratio from
fewer than several batches of about 16 chains: the same method's var(h)
varied about 5× between batches.

The analysis scripts behind the report run as modules, for example
`python -m future_b.fepdmc.analysis.analyze_svd`.

## Layout

| path | content |
|---|---|
| `future_b/fepdmc/patches/` | `base` (make.sys, build hooks), `bchain`, `wqfix`, `extfix`, `extrmfix`; registry `ORDER`, `PROFILES` |
| `future_b/fepdmc/data/` | `bchain.f90` (moves, chain B, checks), `rb_window.f90` (measurement-side diagnostics), `mkl_vsl.f90` (MKL VSL RNG shim, used when MKL is absent), `make.sys` |
| `future_b/fepdmc/prepare.py`, `runner.py`, `pooled.py`, `validate.py`, `cli.py` | the four `future-b-fepdmc` commands |
| `future_b/fepdmc/analysis/` | `analyze_*`, `compare_*`, `decompose_native`, `estimate_groups`, `summarize_*`, `collect_sign` |
| `tests/test_fepdmc_tools.py` | estimator, registry, CLI and configuration tests |
| `research/r1_grouped/native_rb/evidence/` | the JSON behind every number in the report; binary hashes in `BINARY_SHA256.txt` |

The patched Fortran is GPL-3 derived from Perturbo, like the other
excerpts under `src/future_b/`.
