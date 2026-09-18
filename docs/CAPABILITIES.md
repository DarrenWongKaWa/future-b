# What the public snapshot actually provides

v1.2.0 is a **methods-study archive** (science frozen at v1.0.0;
v1.0.1–v1.2.0 are maintenance), not a general DiagMC library.

| Capability | In this snapshot | Entry |
|---|---|---|
| Python DA algebra (`abs(Re M)`, occupancy reverse, stage-2 accept) | yes | `future_b.p1_da` |
| Formation-energy shift \(Q=\) ratio \(-E_{\mathrm{bare}}\) | yes | `future_b.formation_energy` |
| Mean jackknife SE | yes | `mean_jackknife_se` |
| Ratio-of-sums jackknife SE | yes (toy N/D; not a full HAC/bootstrap pipeline) | `ratio_of_sums_jackknife_se` |
| Bartlett HAC / replicate bootstrap engines | **no** | frozen endpoints only |
| Frozen LiF summaries + C5 per-chain CSV | yes (source archive) | `benchmarks/` |
| Raw clean-P1 block \(N,D,\tau\) series | **no** | summary-only |
| Fortran excerpts (`linear_da_mod`, `update_swap`) | source archive; also wheel package-data | `future_b/fortran/` |
| One-click native P1 plugin from public Perturbo | **no** | historical `patches/p1_clean` |
| Public FEP-DMC source identity | pin | `provenance/UPSTREAM_FEP_DMC.json` |
| C0 `wq` refresh on pinned public source | source transform only | `integration/c0` |
| Public P1 delayed acceptance on pinned FEP-DMC | source transform + native JJ validation fixture (not 50 K 0.956) | `integration/p1`, `release/v1.2.0/NATIVE_VALIDATION.md` |
| R1 recursive evaluator / CSE kernels | **no** | `r1_fixed_order` is metadata |
| Wheel = full research archive | **no** | wheel is the Python helper |

Native LiF still needs QE 6.5, Perturbo, Intel Fortran, HDF5, `lif-sp3_epwan.h5`, and a private adapter tree. Binary hash \(\neq\) source commit. Docker digest \(\neq\) Dockerfile.
