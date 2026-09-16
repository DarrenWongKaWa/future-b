# License audit (2026-09-16)

| component | license | in public tarball? | notes |
|---|---|---|---|
| Future B Python analysis / docs / tests | GPL-3.0-or-later | yes | chosen to match Perturbo-derived Fortran |
| `src/future_b/fortran/*.f90` excerpts | GPL-3 (Perturbo-derived) | yes | excerpts + patches, not a full Perturbo tree |
| Perturbo / FEP-DMC full source | GPL-3 | no | obtain upstream; apply `patches/` |
| Quantum ESPRESSO 6.5 | GPL | no | `libpw.a` is a local build artifact |
| Luo et al. Nat. Phys. typeset PDF | publisher copyright | **no** | cite DOI `10.1038/s41567-025-02954-1` |
| NSF PAR accepted manuscript PDF | check NSF PAR terms | **no** (not copied) | still not needed in the software tarball |
| arXiv PDFs in private `references/` | typically CC-BY-NC or arXiv non-exclusive | **no** | citations only |
| LiF / STO / TiO2 epwan HDF5 | not stated in local dataset README | **no** | treat as upstream data; download separately |
| Docker `r5p0-env:ubuntu2004` | mixed (Ubuntu + Intel + QE) | **no** | environment pin only |
| Intel Fortran / MKL | proprietary | no | |

Conclusion: the public candidate is GPL-3 source + documentation +
frozen numerical summaries. It is **not** a data release and **not** a
binary release.
