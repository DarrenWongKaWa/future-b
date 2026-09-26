# native_rb: FEP-DMC fixes, exact moves and diagnostics

Research toolkit on top of upstream FEP-DMC (Luo–Bernardi; pin in
[evidence/FEP_DMC_PIN](evidence/FEP_DMC_PIN)). It has three parts:

- **three native bug fixes**, all opt-in at run time;
- **exact Future B Monte Carlo moves**;
- **diagnostics and estimators** for the low-sign regime.

Results, failure lessons and retractions are in
[NATIVE_REPORT.md](NATIVE_REPORT.md), sections (a)–(j). This directory is
research code and is not part of the installable `future_b` package.

## Quick start

```bash
# 1. patch a pristine checkout (profile "research" = fixes + moves; "fixes" = fixes only)
python3 prepare_fepdmc.py <path>/perturbo-fep-dmc --profile research

# 2. build pert-src inside the QE 6.5 tree (gfortran, serial make)
cd <qe-6.5>/perturbo-fep-dmc/pert-src && make

# 3. run chains (Docker image, datasets and tables are set in run_native.py)
python3 run_native.py ez lif_hole 8 --bin <build> --temp 500 --maxorder 7 \
    --wqfix --extfix --extrmfix --tag my_runs

# 4. end-to-end exactness check (independent kernels must agree)
python3 validate_exactness.py --bin <build>
```

`prepare_fepdmc.py` applied to a clean pin reproduces the sources of the
research build mb32 byte for byte.

## Native bug fixes (upstream pin 05d08449)

| switch | patch | bug |
|---|---|---|
| `FUTUREB_WQFIX=1` | [patch_wqfix.py](patch_wqfix.py) | `add_external_ph` never calls `cal_wq_int`, so external pairs keep the stale phonon frequency of the recycled vertex slot |
| `FUTUREB_EXTRMFIX=1` | [patch_extrmfix.py](patch_extrmfix.py) | `remove_external_ph` builds the pair-less reference trace at momentum k − q instead of k; multiband only |
| `FUTUREB_EXTFIX=1` | [patch_extfix.py](patch_extfix.py) | `remove_external_ph` evaluates the reverse-add density without a range check, so pairs outside add's τ support are removable |

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
| correct native target | `FUTUREB_WQFIX=1 FUTUREB_EXTFIX=1 FUTUREB_EXTRMFIX=1` |
| where external pairs are abundant (low sign, multiband, e.g. LiF-hole at T = 500 K) | the above plus `FUTUREB_EXTAR=1 FUTUREB_EXTAR_P=0.02` (anything in 0.02–0.1 reaches the same equilibrium) |

**Why the external move is needed there.** From the empty start, native
equilibrates the external-pair count far too slowly (τ_int ≳ 1800
measurements). A standard 2×10⁶-step run sits in a quasi-stationary state
with about 9 pairs instead of about 11.5. That biases Q by about 10% and
⟨s⟩ by about 2×. The ordered external move reaches the equilibrium and is
exact (maxOrder 7, 21, 51). p = 0.02, 0.05 and 0.1 all give the same
Q (−1.77 to −1.80) and pair count (11.9–12.0)
([evidence/lif_hole500_ext_pscan.json](evidence/lif_hole500_ext_pscan.json)).
CPU is about 1.9× native at every p. That is mostly physical: the correct
equilibrium has larger diagrams, so native moves cost more. It is not move
overhead, and the move does not reduce per-step variance.

## Future B moves (all exact; inert unless enabled)

| switch | move |
|---|---|
| `FUTUREB_CHQ=1`, `FUTUREB_CHQ_P` | change-q: new momentum for an internal line, span shifted |
| `FUTUREB_CHQ_EXT=1` | change-q also for boundary-wrapping external pairs |
| `FUTUREB_ANY=1`, `FUTUREB_ANY_P` | general-span add/remove of internal lines (native: span-1 only) |
| `FUTUREB_EXTAR=1`, `FUTUREB_EXTAR_P` | external-pair add/remove at any position, respecting native's ordering (every head-attached external vertex precedes every tail-attached one) |
| `FUTUREB_MV_UNTIL=N` | apply the moves only for the first N steps (burn-in) |
| `FUTUREB_BCHAIN=1` (+ `_GROUP`, `_ADDREM`, `_BLOCK`, `_SRULE`, `_REFRESH`, `_PAR`) | grouped-measure chain B (phonon modes folded over non-crossing lines) |

Validation. Every move passes a round trip (C → C′ → C restores log w and
the proposal probabilities to ≤ 4e-15) and per-chain momentum, gauge and
O/sign self-checks. At maxOrder 7 every exact kernel reproduces fixed native.

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

- `FUTUREB_SEED` reproducible chains.
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

Use [compare_pooled.py](compare_pooled.py). It pools the ratio Σn/Σd over
chains and gives the chain-level variance, an F interval, the CPU ratio and
the efficiency. In low-sign runs, do **not** average per-chain ratios. Do
not trust a variance ratio from fewer than several batches of about 16
chains: the same method's var(h) varied about 5× between batches.

## Files

- **Patches:** `prepare_fepdmc.py`, `patch_*.py`, `make.sys`, `mkl_vsl.f90`
- **Fortran:** `bchain.f90` (moves, chain B, checks), `rb_window.f90`
  (measurement-side diagnostics)
- **Runner:** `run_native.py`
- **Analysis:** `compare_*.py`, `analyze_*.py`, `decompose_native.py`,
  `estimate_groups.py`, `summarize_materials.py`
- **Validation:** `validate_exactness.py`; unit tests in
  `tests/test_native_rb_tools.py`
- **Evidence:** `evidence/`, the JSON behind every number in the report;
  binary hashes are in `evidence/BINARY_SHA256.txt`
