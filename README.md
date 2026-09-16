# Future B: Exact-corrected delayed acceptance and validation tools for first-principles diagrammatic Monte Carlo

A reproducible methods study on LiF polarons, including native proposal
screening, event-level correctness checks, correlated-Monte-Carlo
statistics, fixed-order graph reuse, and negative/unresolved benchmark
results.

**Project status: CLOSED** (`v1.0.0`, 2026-09-16). This is not an
“AI acceleration framework”.

| Result | Status |
| --- | --- |
| LiF fixed-setting \(Q\) | \(\sim-0.25\) eV |
| P1 native integration | validated |
| expensive early rejection | ~33.2% eligible swaps |
| observed P1/B-best wall ratio | 0.956 |
| ≥5% gain | not established |
| R1 fixed-order reuse | validated in scope |
| R1 vs optimized CSE | no additional gain established |
| P4/P5 | future work |
| grouped material R1 | future work |
| 1% ground state | not pursued |

\(Q=E_{\mathrm{polaron}}-E_{\mathrm{bare}}\) with
\(E_{\mathrm{bare}}=9.35487318746596053\,\mathrm{eV}\). Do not report the
unshifted \(\sim+9.105\,\mathrm{eV}\) ratio as formation energy.

The 0.956 wall ratio was measured with the **released clean binary**
(SHA256 `f9518a21…`), after `P1_FIXTURE` gating was compiled in and with
`P1_FIXTURE=0` at runtime. See [docs/PROVENANCE.md](docs/PROVENANCE.md).
Classification remains **`P1_UNRESOLVED_WITHIN_BUDGET`**: the bootstrap
interval [0.940, 0.972] crosses the predeclared 0.95 threshold and HAC
was not clean. That is neither `GAIN` nor `FAIL`.

Start here: [docs/SCIENTIFIC_RESULT.md](docs/SCIENTIFIC_RESULT.md).
Upstream FEP-DMC / Perturbo / Luo–Bernardi compression are cited, not
claimed as Future B inventions ([docs/CONTRIBUTIONS.md](docs/CONTRIBUTIONS.md)).

## Minimal reproduction (no LiF HDF5, no Docker)

```bash
# Python 3.11+ required (macOS /usr/bin/python3 may still be 3.9)
python3.12 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest tests/test_da_balance.py tests/test_forward_reverse.py \
  tests/test_energy_zero.py tests/test_statistics.py tests/test_r1_oracles.py \
  tests/test_p1_clean_source.py tests/test_reject_state.py \
  tests/test_c5_formation_q.py -q
.venv/bin/python examples/lif_small_fixture/recompute_q.py
```

This checks algebra, energy zero, frozen statistics, and that the
shipped Fortran excerpts still match the timed clean source. It does
**not** run native `perturbo.x`.

## Full LiF native runs

Quantum ESPRESSO 6.5, Perturbo/FEP-DMC, Intel Fortran, HDF5 Fortran
2003, `lif-sp3_epwan.h5`, and in this work Docker
`r5p0-env:ubuntu2004`. Those files are **not** in the public package.
[docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md),
[docs/DATA_AND_LICENSE.md](docs/DATA_AND_LICENSE.md).

## Documentation

- [Provenance (binary ↔ 0.956)](docs/PROVENANCE.md)
- [Scientific result](docs/SCIENTIFIC_RESULT.md)
- [P1 method](docs/METHOD_P1.md)
- [Statistics](docs/STATISTICS.md)
- [Validation](docs/VALIDATION.md)
- [Limitations](docs/LIMITATIONS.md)
- [Future work: R1 grouped consumer](docs/future_work/R1_REAL_MATERIAL_GROUPED_CONSUMER.md)
- [Future work: P4/P5](docs/future_work/P4_P5_LEARNING_CANDIDATES.md)
- [Future work: 1% ground state](docs/future_work/GROUND_STATE_1PCT.md)

## License

GPL-3.0-or-later (compatible with Perturbo-derived Fortran excerpts).
See `LICENSE`, `NOTICE`, and [docs/DATA_AND_LICENSE.md](docs/DATA_AND_LICENSE.md).
