# Upstream vs Future B contributions

## Upstream (do not claim as Future B)

- Luo / Park / Bernardi FEP-DMC method and LiF results
  (Nat. Phys. **21**, 1275 (2025))
- Perturbo package and native DiagMC implementation
- Luo–Bernardi electron–phonon compression
- matrix-product multiband summation
- upstream epwan / H-table / SVD material datasets
- Quantum ESPRESSO 6.5 libraries used at link time

## Future B (only what the evidence supports)

- native bug audit and repairs (`add_external_ph` \(\omega_q\) refresh;
  `NEWUNIT` logger; reverse double-flip)
- v1.3.0: two further `remove_external_ph` bugs (reference trace at
  k − q in the multiband case; reverse-add density without a support check),
  the native ordering constraint on external vertices, and the external-pair
  under-equilibration of native chains in the low-sign multiband regime;
  the first measurement of the \(\omega_q\) bug's effect on EZ energies
- v1.3.0: exact change-q, general-span and ordered external add/remove
  moves; the pooled ratio estimator and the sign-variance decomposition
- exclusive nested timers and swap hotspot profile
- exact-corrected analytic P1 delayed acceptance in the swap update
- event-level validation (stage-1 g/env skip, occupancy reverse,
  `abs(Re M)` target)
- energy-zero correction in postprocessing
  (\(Q=\) ratio \(-E_{\mathrm{bare}}\))
- autocorrelation-aware / bootstrap benchmarking of clean P1 vs B-best
- fixed-order R1 reuse evaluator and the scoped CSE tie
- reproducible record of negative and unresolved claims

## Explicitly not demonstrated

- neural acceleration of FEP-DMC (P4/P5 not trained)
- R1 as a real-material grouped sampler
- 1% certified ground-state formation energy
- \(\ge 5\%\) practical wall-clock gain for clean P1
