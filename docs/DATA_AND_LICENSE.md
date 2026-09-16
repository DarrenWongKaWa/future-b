# Data and license

This file is the public redistribution policy. Details of the 2026-09-16
audit are in `release/2026-09-16/LICENSE_AUDIT.md` and `DATA_AUDIT.md`.

## What is distributed in the GitHub candidate

- Original Future B Python analysis, tests, frozen JSON/CSV summaries,
  documentation, and Fortran **patches/excerpts**.
- License: GNU GPL v3, because Perturbo-derived Fortran is GPL-3 and
  the analysis layer is released with the same terms.

## What is not distributed

| item | reason |
|---|---|
| `lif-sp3_epwan.h5` and other epwan HDF5 | upstream material data, hundreds of MiB–GiB; no explicit public-redistribution grant in the local README |
| Nature Physics typeset PDF | publisher copyright |
| Docker image layers | not a source distribution; local build environment |
| QE `libpw.a`, `.o`, `.mod`, `perturbo.x` | compiled artifacts; rebuild from upstream |
| Full `p1_confirm/runs/*` working directories | contain copied HDF5 |
| Intel compiler runtimes | proprietary |

arXiv PDFs in `references/` of the **private** working tree are not
copied into the public tarball (keep citations, not binary PDFs).

## How to obtain upstream data

1. Read Luo, Park, Bernardi, Nat. Phys. **21**, 1275 (2025),
   DOI `10.1038/s41567-025-02954-1`.
2. Obtain FEP-DMC / Perturbo from https://perturbo-code.github.io/ .
3. Obtain LiF `lif-sp3_epwan.h5` from the authors' FEP-DMC dataset
   (local copy lived at `FEP-DMC-Data/FEP-DMC-Dataset/LiF-electron/`).
4. Build QE 6.5 with Intel Fortran and HDF5 Fortran 2003, then Perturbo
   `make perturbo`.
5. Apply `patches/c0_wq/apply_wq_refresh.py` and
   `patches/p1_clean/apply_p1_clean.py` to an owned tree; do not patch
   historical evidence directories.

## Checksums (LiF electron epwan, local copy)

Computed on this host from
`FEP-DMC-Data/FEP-DMC-Dataset/LiF-electron/lif-sp3_epwan.h5`
(size 423 570 352 bytes). The public package does not include the file;
recompute SHA256 after download and compare to
`release/2026-09-16/DATA_AUDIT.md`.

## Upstream citations (not Future B claims)

- Y. Luo, J. Park, M. Bernardi, Nat. Phys. **21**, 1275 (2025).
- Perturbo: Zhou, Parke, Bernardi et al. (see perturbo-code.github.io).
- Quantum ESPRESSO 6.5 (GPL).

## Redistribution concerns

If you fork this repository publicly:

- Do **not** add the Nature PDF or epwan HDF5 “for convenience”.
- Keep GPL-3 on Perturbo-derived Fortran.
- Attribute Luo/Park/Bernardi and Perturbo clearly.
- Do not describe this package as “official Perturbo” or as a 1%
  LiF ground-state release.
