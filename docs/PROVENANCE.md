# Provenance — upstream vs Future B, and the 0.956 wall ratio

Read this before treating any number in the README as a released-binary
measurement.

## Upstream (not Future B)

| piece | role |
|---|---|
| Luo, Park, Bernardi, Nat. Phys. **21**, 1275 (2025) | FEP-DMC method, LiF physics, material data |
| Perturbo (GPL-3) | native DiagMC implementation |
| Quantum ESPRESSO 6.5 (GPL) | `libpw.a` at link time |
| Luo–Bernardi EPC compression; matrix-product band sums | native evaluation, not this project's invention |

Future B patches sit **on top of** Perturbo. Fortran excerpts under
`src/future_b/fortran/` and `patches/` are GPL-3 derived.

## Future B original work

- `add_external_ph` \(\omega_q\) refresh
- exclusive timers / swap hotspot profile
- exact-corrected analytic P1 delayed acceptance
- event fixture and independent `LINEAR_DA_COUNTS`
- \(E_{\mathrm{bare}}\) postprocessing
- HAC / bootstrap protocol
- scoped R1-vs-CSE evaluator study
- this documentation and public test layer

## The 0.956 wall ratio is the released clean binary

It is **not** a later, cleaner binary than the one that was timed.

Order of operations on 2026-09-16 (do not invert):

1. `patches/p1_clean/apply_p1_clean.py` copied the C2 fixture adapter
   and **inserted** `P1_FIXTURE` gates (default **off**).
2. That tree was compiled in Docker `r5p0-env:ubuntu2004` to
   `perturbo.x` SHA256
   `f9518a21fc2b8750fb3b7ed6f6e065db398cb2f425969cd718d1dcdef2b2c25c`
   (`closure/2026-09-16-final/logs/p1_clean_build.json`).
3. Correctness fixture ran **the same binary** with `P1_FIXTURE=1`.
4. Confirmation vs B-best ran **the same binary** with

   ```
   LINEAR_DA=on  LINEAR_DA_SCORE=prop  DMC_OBSERVER=1
   P1_FIXTURE=0  C2_DUMP=0
   ```

   All six P1 `run.json` files record that SHA256. Confirm directories
   contain **no** `c2_swap.tsv`.
5. GitHub excerpts `src/future_b/fortran/linear_da_mod.f90` are a
   byte-identical copy of the confirm-tree source
   (SHA256 `004b23b66e00f4ca20e2cc683c8e99124f12713549fcc02363e0e0afc37854df`).
   The `update_swap` excerpt is a substring of the same
   `diagMC_JJ_updates.f90`. No production-path edit was made after the
   timing batch.

Therefore the README may call 0.956 the **released clean-binary**
result. It was **not** rerun for form. B-best SHA256
`3c4f4bf9225b7a530303f3f414256a4c25b0a61e0d874a1ae42a46346f24efab`.

The public tarball does **not** ship `perturbo.x`. Rebuilding native
code requires upstream QE/Perturbo (see
[REPRODUCIBILITY.md](REPRODUCIBILITY.md)).

## What is not in a public clone

- `lif-sp3_epwan.h5` and other epwan files
- Nature PDFs
- Docker image layers
- compiled `.o` / `.mod` / `perturbo.x` / `libpw.a`
- private run directories under `closure/**/runs` and `research/`
