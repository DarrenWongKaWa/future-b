# Future B v1.3.0 — FEP-DMC research toolkit in the package

- Not a scientific release of the frozen LiF result. Frozen classification
  `P1_UNRESOLVED_WITHIN_BUDGET` unchanged. No speedup claim.
- v1.0.2, v1.0.3, v1.1.0, and v1.2.0 release records are immutable. C0 and
  P1 adapters are unchanged.
- Adds `future_b.fepdmc` and the `future-b-fepdmc` command
  (`prepare`, `run`, `compare`, `validate`). Source patches of pinned
  FEP-DMC `05d08449cffdbd0dfbbbf5009add5cc887bc754b`, each asserting its
  anchors once. Profiles: `fixes` (three native fixes) and `research`
  (fixes plus exact Future B moves and diagnostics).
- Three opt-in native fixes in external-phonon add/remove
  (`FUTUREB_WQFIX`, `FUTUREB_EXTFIX`, `FUTUREB_EXTRMFIX`). With all three,
  LiF-hole T = 500 K at maxOrder 7 moves from −0.87311 to −0.8763 (11σ).
  The paper's β = 232 LiF-electron and STO cases are unchanged within
  1–3 meV.
- Recommended configuration in the low-sign multiband regime: the three
  fixes plus the ordered external move (`--extar 0.02`). Native
  under-equilibrates the external-pair count there; the move is exact and
  removes a ~10% bias in Q. Its benefit is correctness, not per-step
  variance.
- Exactness: independent kernels (fixed native, pure Future B moves,
  mixed) agree on pooled Q at maxOrder 7 (`future-b-fepdmc validate`).
  `prepare` on a clean pin reproduces the research build sources byte for
  byte, and a from-scratch gfortran build links.
- Adds `future_b.r1_grouped`, the finite R1 grouped toy with its dense
  oracle (F1–F3).
- The research evidence stays in `research/r1_grouped/` (GitHub only).
  Details: `docs/FEP_DMC_TOOLKIT.md` and
  `research/r1_grouped/native_rb/NATIVE_REPORT.md`.
- Unlike the C0/P1 adapters, the toolkit ships in the wheel. Docker, QE 6.5,
  the FEP-DMC dataset and the tables are not shipped.
