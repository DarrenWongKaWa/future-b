# Provenance — three identities that must not be mixed

Read this before treating any number in the README as a released-binary
measurement, and before treating any checksum file as a hash of *this*
checkout.

There are **three** identities:

| identity | what it is | where it lives |
|---|---|---|
| **A. Public repository source** | the GitHub tree you cloned (`v1.0.3` maintenance) | this checkout; `release/v1.0.3/` |
| **B. Historical timed experiment source** | Fortran compiled into the 0.956 binary | SHA256 pins below; **not** byte-identical to A |
| **C. Frozen scientific result** | LiF Q, wall ratio, HAC, K, classification | `benchmarks/` from **v1.0.0**; unchanged since |

A is **not** B. v1.0.1 gated `C2_FORCE_A1` behind `P1_FIXTURE` (F03).
That is a fixture-safety edit. It is **not** a new timing run and it
does **not** change the frozen result (C).

Canonical machine-readable record: [`release/v1.0.3/PROVENANCE.json`](../release/v1.0.3/PROVENANCE.json).
Current-tree checksums: [`release/v1.0.3/SHA256SUMS.txt`](../release/v1.0.3/SHA256SUMS.txt).
v1.0.2 provenance is historical and immutable:
[`release/v1.0.2/`](../release/v1.0.2/).
Do **not** use [`release/2026-09-16/SHA256SUMS.txt`](../release/2026-09-16/SHA256SUMS.txt)
as a checksum of the current tree (see [PUBLIC_MANIFEST.md](PUBLIC_MANIFEST.md)).

## Upstream (not Future B)

| piece | role |
|---|---|
| Luo, Park, Bernardi, Nat. Phys. **21**, 1275 (2025) | FEP-DMC method, LiF physics, material data |
| Perturbo (GPL-3) | native DiagMC implementation |
| Quantum ESPRESSO 6.5 (GPL) | `libpw.a` at link time |
| Luo–Bernardi EPC compression; matrix-product band sums | native evaluation, not this project's invention |

Future B patches sit **on top of** Perturbo. Fortran excerpts under
`src/future_b/fortran/` and `patches/` are GPL-3 derived.

The public yaoluo/FEP-DMC checkout Future B will target for later
integration work is pinned in
[`provenance/UPSTREAM_FEP_DMC.json`](../provenance/UPSTREAM_FEP_DMC.json).
That pin is **not** the proven private timed donor and is **not** a
working adapter. See [UPSTREAM_FEP_DMC.md](UPSTREAM_FEP_DMC.md).

## Future B original work

- `add_external_ph` \(\omega_q\) refresh
- exclusive timers / swap hotspot profile
- exact-corrected analytic P1 delayed acceptance
- event fixture and independent `LINEAR_DA_COUNTS`
- \(E_{\mathrm{bare}}\) postprocessing
- HAC / bootstrap protocol
- scoped R1-vs-CSE evaluator study
- this documentation and public test layer

## B. The 0.956 wall ratio is the released clean binary

It is **not** a later, cleaner binary than the one that was timed.
No performance experiment was rerun for v1.0.1 or v1.0.2.

Order of operations on 2026-09-16 (do not invert):

1. `patches/p1_clean/apply_p1_clean.py` copied the C2 fixture adapter
   and **inserted** `P1_FIXTURE` gates (default **off**).
2. That tree was compiled in Docker `r5p0-env:ubuntu2004` to
   `perturbo.x` SHA256
   `f9518a21fc2b8750fb3b7ed6f6e065db398cb2f425969cd718d1dcdef2b2c25c`
   (`closure/2026-09-16-final/logs/p1_clean_build.json`; not in the
   public tree).
3. Correctness fixture ran **the same binary** with `P1_FIXTURE=1`.
4. Confirmation vs B-best ran **the same binary** with

   ```
   LINEAR_DA=on  LINEAR_DA_SCORE=prop  DMC_OBSERVER=1
   P1_FIXTURE=0  C2_DUMP=0
   ```

   All six P1 `run.json` files record that SHA256. Confirm directories
   contain **no** `c2_swap.tsv`.
5. The **timed** confirm-tree `linear_da_mod.f90` SHA256 is
   `004b23b66e00f4ca20e2cc683c8e99124f12713549fcc02363e0e0afc37854df`.
   That file is what v1.0.0 shipped. The `update_swap` excerpt is a
   substring of the same confirm-tree `diagMC_JJ_updates.f90`. No
   production-path edit was made **after the timing batch** and before
   that v1.0.0 pin.

Therefore the README may call 0.956 the **released clean-binary**
result. It was **not** rerun for form. B-best SHA256
`3c4f4bf9225b7a530303f3f414256a4c25b0a61e0d874a1ae42a46346f24efab`.

## A. Current public `linear_da_mod.f90` (not the timed file)

The current public maintenance source SHA256 is
`c541444f2d591d4e280e12c28958534b6a89a2fd7f91dabb7df46223fac9acd8`.

The current public maintenance source contains additional audit/test
gating (v1.0.1 F03: `C2_FORCE_A1` only if `p1_fixture_on()`) and
therefore is **not** byte-identical to the Fortran source used for the
frozen timing experiment. The historical timed-source hash is retained
as immutable provenance. With `P1_FIXTURE` off (the timed production
path), the extra gate is inactive.

The public tarball does **not** ship `perturbo.x`. Rebuilding native
code requires upstream QE/Perturbo (see
[REPRODUCIBILITY.md](REPRODUCIBILITY.md)).

## C. Frozen scientific result

Origin release: **v1.0.0** (`77835ca`). Classification
`P1_UNRESOLVED_WITHIN_BUDGET`. Records:
`benchmarks/p1_vs_bbest/frozen_results.json`,
`benchmarks/c5_dev/frozen_results.json`.
v1.0.1, v1.0.2, and v1.0.3 did not change those files.

## Historical wrap-up git commit `6e5529f`

`release/2026-09-16/FINAL_PROVENANCE.json` records
`git_commit` `6e5529f481bf0751d6b619bd427aff250c712d55`.
That is a commit on the **private live extract** (2026-09-01,
“Record Candidate 1 spectral stop…”), noted there as a dirty wrap-up
tree. It is **not** public GitHub `v1.0.0` (`77835ca`) and **not**
`v1.0.1` (`e418d88`). Native confirm used the binary SHA256s above,
not that extract commit. The JSON is left unchanged.

## What is not in a public clone

- `lif-sp3_epwan.h5` and other epwan files
- Nature PDFs
- Docker image layers
- compiled `.o` / `.mod` / `perturbo.x` / `libpw.a`
- private run directories under `closure/**/runs` and `research/`
