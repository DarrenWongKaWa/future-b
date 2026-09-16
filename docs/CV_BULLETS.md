# CV bullets (evidence-backed)

- Implemented and audited exact-corrected delayed acceptance inside a
  first-principles diagrammatic Monte Carlo (FEP-DMC) swap update for
  the LiF electron polaron, keeping the native \(\mathrm{abs}(\mathrm{Re}\,M)\)
  second-stage correction.
- Identified and repaired native scientific-software defects (unread
  phonon frequency after external-phonon insertion; Fortran `NEWUNIT`
  logger overwrite; reverse-score double-flip of \(\Delta t\) and
  \(\Delta E\)).
- Built proposal-level validation: stage-1 rejects skip recorded
  g/environment work; occupancy reverse is antisymmetric; production
  counters are independent of dump flags.
- Benchmarked six-chain LiF formation-energy calculations at a frozen
  \(20^3\)/rank-20 setting, \(Q\approx-0.25\,\mathrm{eV}\) after the
  correct \(E_{\mathrm{bare}}\) shift, and reported HAC failures rather
  than calling the batch a statistical pass.
- Performed autocorrelation-aware (HAC) and replicate-bootstrap
  comparison of clean P1 vs B-best; classified a \(\sim 4\%\) wall-time
  point estimate as unresolved against a predeclared 5% rule.
- Evaluated recursive graph reuse (R1) against an optimized CSE
  baseline in a fixed-order domain (ratio \(\approx 0.9992\)) and
  separated that scoped result from an unimplemented material grouped
  sampler.
- Wrote a closed, reproducible methods record with explicit negative
  and unresolved claims; did not train undeclared neural models or
  certify a 1% ground-state energy.
