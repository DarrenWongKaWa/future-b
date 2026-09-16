# Reproducibility

## What a public clone can reproduce

Without LiF HDF5, Docker, or QE:

1. Install Python 3.11+, then `python -m pip install --upgrade pip` and
   `pip install -e ".[dev]"`.
2. Run the unit tests listed in the README.
3. Recompute published summary numbers from
   `benchmarks/c5_dev/` and `benchmarks/p1_vs_bbest/`
   (`examples/lif_small_fixture/recompute_q.py`).

That path checks algebra, energy zero, frozen statistics, and the
clean-P1 source gates. It does **not** rebuild `perturbo.x`.

## What requires the private/upstream stack

Native LiF chains need:

| piece | how to obtain | redistributed here? |
|---|---|---|
| Quantum ESPRESSO 6.5 | https://gitlab.com/QEF/q-e/-/tags/qe-6.5 | no (`libpw.a` is local) |
| Perturbo / FEP-DMC | https://perturbo-code.github.io/ (GPL-3) | patches only |
| `lif-sp3_epwan.h5` | Luo et al. dataset / authors | **no** (~404 MiB) |
| `gkq-20` tables | built from the epwan file | no |
| Docker `r5p0-env:ubuntu2004` linux/amd64 digest `sha256:2082c5082f050fafc807ad1488e3498fe51e0c7951e4ddcf818b3ed39de5f7e1` | local image | **no** |
| Intel Fortran + HDF5 Fortran 2003 | vendor | no |

Pins: B0 `479b854f…`, B-best `3c4f4bf9…`, clean P1 `f9518a21…`
(`release/2026-09-16/FINAL_PROVENANCE.json`). Those hashes identify
**binaries**, not a public upstream git revision. `patches/p1_clean`
is historical-only and needs a private adapter tree.

## Historical run directories

Night-1 C0–C5 and `closure/2026-09-16-final/p1_confirm/` are the
authoritative native evidence. They contain copies of `lif-sp3_epwan.h5`
and compiled objects. They are **not** part of the public tarball.

Do not overwrite those directories. Do not reuse a stale `run.json` as a
new result.

## Seeds (clean P1 confirm)

- master `9143600`; arm spawn 0 = B-best, 1 = P1; six children each
- bootstrap `9143610`
- `Nmcmc(1e4)=200`, OMP=1, 6 GiB Docker slot, SINGLE_HOST
