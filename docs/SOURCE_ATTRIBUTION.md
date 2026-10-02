# Source attribution (maintenance, not a legal opinion)

Public excerpts are GPL-3 because they derive from Perturbo/FEP-DMC.

| path | donor | license | Future B change |
|---|---|---|---|
| `src/future_b/fortran/linear_da_mod.f90` | Perturbo FEP-DMC `pert-src` (Luo/Park/Bernardi) plus Future B DA helpers | GPL-3 | P1 score, `P1_FIXTURE`, counters; v1.0.1 gates `C2_FORCE_A1` |
| `src/future_b/fortran/update_swap_p1_excerpt.f90` | `diagMC_JJ_updates.f90` `update_swap` | GPL-3 | excerpt of DA insert; not the full file |
| `src/future_b/fortran/closure_observer.f90` | Future B C1 observer | GPL-3 | timers; physics path unchanged when profile off |
| `patches/p1_clean/apply_p1_clean.py` | Future B | GPL-3 | historical gating script |
| `src/future_b/*.py` | Future B analysis layer | GPL-3 | original |
| `src/future_b/fepdmc/data/bchain.f90`, `rb_window.f90` | Future B, written against FEP-DMC `pert-src` interfaces | GPL-3 | exact moves, chain B, measurement-side diagnostics |
| `src/future_b/fepdmc/data/mkl_vsl.f90` | Future B RNG shim for the MKL VSL symbols used by FEP-DMC | GPL-3 | xorshift64 uniforms when MKL is absent; no Metropolis change |
| `src/future_b/fepdmc/patches/*.py` | Future B source transforms of the pinned FEP-DMC tree | GPL-3 | anchored edits; the patched files remain Perturbo-derived |

Upstream citations: Luo, Park, Bernardi, Nat. Phys. **21**, 1275 (2025);
Perturbo https://perturbo-code.github.io/ ; QE 6.5.

The **public** FEP-DMC reference checkout is pinned in
[`provenance/UPSTREAM_FEP_DMC.json`](../provenance/UPSTREAM_FEP_DMC.json)
(`05d08449cffdbd0dfbbbf5009add5cc887bc754b`). That pin is a prospective
integration baseline. Equivalence to the **private timed donor** that
built binary `f9518a21…` is **not established**. Do not treat the binary
SHA256 as a source commit. C0 may be applied to the pin as a source
transform ([C0_PUBLIC_ADAPTER.md](C0_PUBLIC_ADAPTER.md)); that is not
P1 and not a compiled plugin.
See [UPSTREAM_FEP_DMC.md](UPSTREAM_FEP_DMC.md).

Team public-release permission is an owner confirmation, not something
this file certifies.
