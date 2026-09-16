# Application project summary

I worked on first-principles diagrammatic Monte Carlo for the LiF
electron polaron (Luo EZ / Perturbo FEP-DMC). The project closed as a
bounded methods study of exact-corrected delayed acceptance and scoped
graph reuse, not as a general AI-for-many-body framework.

I audited native Fortran updates, identified and repaired a phonon-frequency
refresh bug in `add_external_ph`, and implemented exclusive nested timers
that located the swap update at about 21% of coarse Monte Carlo time,
with environments remaining a major cost.

I derived and implemented analytic delayed acceptance (P1) for legal
swaps: a cheap stage-1 score from energies and phonon times, followed
by the exact native stage-2 correction using \(\mathrm{abs}(\mathrm{Re}\,M)\).
A bounded fixture showed thousands of early rejects with zero recorded
g/environment increment and antisymmetric occupancy reverse on committed
diagrams. Independent production counters were separated from diagnostic
dumps.

On the frozen LiF \(20^3\)/rank-20 setting, six-chain DEV runs give a
formation energy \(Q=E_{\mathrm{polaron}}-E_{\mathrm{bare}}\approx-0.25\,\mathrm{eV}\)
after subtracting the documented bare-band energy (the unshifted
\(\sim+9.105\,\mathrm{eV}\) ratio is not \(Q\)). Statistical diagnostics
are at the few-percent level. A 1% ground-state certification was not
attempted.

A protocol frozen before looking at confirmation data compared a clean
P1 binary to B-best. The wall-time ratio was 0.956 with bootstrap
interval [0.940, 0.972], which crosses the predeclared 5% threshold, and
HAC stability failed on some chains. I classified the practical-gain
claim as unresolved within budget rather than as a success.

I also evaluated a recursive/symbolic graph-reuse evaluator (R1) against
an optimized common-subexpression baseline in a fixed-order domain:
correctness and reuse held, with a total-time ratio \(\approx 0.9992\).
A native material grouped consumer was not implemented; learning-based
P4/P5 recipes were documented as future work and not trained.

I did not claim that neural networks accelerated FEP-DMC, that R1
accelerated real-material LiF, or that a 1% ground-state formation
energy was certified.
