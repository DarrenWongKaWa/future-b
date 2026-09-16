# Data audit (2026-09-16)

## Not in the public package

| file (local working tree) | bytes | sha256 | action |
|---|---:|---|---|
| `FEP-DMC-Data/FEP-DMC-Dataset/LiF-electron/lif-sp3_epwan.h5` | 423570352 | `4960618b64f4f1787e7a30aac4c2990ec5632ecbab83a9632f6c659f03da690b` | do not upload |
| copies under `closure/2026-09-16-final/**/lif-sp3_epwan.h5` | same payload | (copies) | do not upload |
| `FEP-DMC-Data/.../TiO2-anatase/tio2-gw-elec_epwan.h5` | 1828199696 | not hashed here | do not upload |
| Nature Physics PDF | (typeset) | — | do not upload |

How to obtain LiF data: Luo, Park, Bernardi, Nat. Phys. **21**, 1275
(2025) and the authors' FEP-DMC dataset. After download, compare SHA256
to the LiF row above.

## In the public package

- `benchmarks/**/*.json` and `benchmarks/c5_dev/c5_per_chain_diagnostics.csv`
  (derived numerical summaries; no wavefunctions)
- `data/small_public_fixture/swap_row.json` (synthetic)
- unit-test constants

## Docker / binaries

Not redistributed. Pin:
`r5p0-env:ubuntu2004` digest
`sha256:2082c5082f050fafc807ad1488e3498fe51e0c7951e4ddcf818b3ed39de5f7e1`.
Clean P1 `perturbo.x` SHA256
`f9518a21fc2b8750fb3b7ed6f6e065db398cb2f425969cd718d1dcdef2b2c25c`.
