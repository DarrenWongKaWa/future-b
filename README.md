# Future B: Exact-corrected delayed acceptance and validation tools for first-principles diagrammatic Monte Carlo

A reproducible methods study on LiF polarons, including native proposal
screening, event-level correctness checks, correlated-Monte-Carlo
statistics, fixed-order graph reuse, and negative/unresolved benchmark
results.

**Project status: CLOSED** (`v1.0.0` science frozen; `v1.0.1`–`v1.0.3`
maintenance). This is a **methods-study archive**, not an AI
acceleration framework and not a drop-in FEP-DMC plugin.

Future B is a source-and-results archive of exact-corrected analytic
delayed acceptance in first-principles DiagMC. The public snapshot
provides Python algebra and summary-consistency checks, native Fortran
excerpts, and frozen benchmark records. Full native reconstruction, raw
block-level statistical reproduction, and the historical R1 evaluator
are **not** included. See [docs/CAPABILITIES.md](docs/CAPABILITIES.md).

| Result | Status |
| --- | --- |
| LiF fixed-setting \(Q\) | \(\sim-0.25\) eV |
| P1 native integration | validated |
| expensive early rejection | ~33.2% eligible swaps |
| observed P1/B-best wall ratio | 0.956 |
| ≥5% wall gain | not established |
| equal-precision \(K=T\cdot\mathrm{Var}\) | diagnostic point \(\sim 2.49\); interval unusable |
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
Classification remains **`P1_UNRESOLVED_WITHIN_BUDGET`**: the wall
bootstrap [0.940, 0.972] crosses 0.95 and HAC was not clean. That is
neither `GAIN` nor `FAIL`. The JK-variance **point** estimate is larger
for P1; the cost–variance ratio is a diagnostic, not a certified
slowdown. See [docs/SCIENTIFIC_RESULT.md](docs/SCIENTIFIC_RESULT.md).

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
  tests/test_c5_formation_q.py tests/test_audit_guards.py \
  tests/test_provenance_identities.py -q
.venv/bin/python examples/lif_small_fixture/recompute_q.py
```

This checks algebra, energy zero, frozen statistics, and that the
shipped Fortran excerpts keep the timed production path while recording
that the public `linear_da_mod.f90` is **not** byte-identical to the
timed confirm-tree file (v1.0.1 F03 gating). It does **not** run native
`perturbo.x`. See [docs/PROVENANCE.md](docs/PROVENANCE.md).

## Full LiF native runs

Quantum ESPRESSO 6.5, Perturbo/FEP-DMC, Intel Fortran, HDF5 Fortran
2003, `lif-sp3_epwan.h5`, and in this work Docker
`r5p0-env:ubuntu2004`. Those files are **not** in the public package.
[docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md),
[docs/DATA_AND_LICENSE.md](docs/DATA_AND_LICENSE.md).

## Documentation

- [What is actually shipped](docs/CAPABILITIES.md)
- [GitHub vs sdist vs wheel](docs/DISTRIBUTIONS.md)
- [Public FEP-DMC pin (identity, not an adapter)](docs/UPSTREAM_FEP_DMC.md)
- [v1.0.1 maintenance](docs/MAINTENANCE_1.0.1.md)
- [v1.0.2 provenance repair](docs/MAINTENANCE_1.0.2.md)
- [v1.0.3 packaging and public FEP-DMC pin](docs/MAINTENANCE_1.0.3.md)
- [Provenance (public source vs timed source vs frozen result)](docs/PROVENANCE.md)
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
