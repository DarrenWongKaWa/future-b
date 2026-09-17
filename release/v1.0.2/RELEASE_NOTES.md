# Future B v1.0.2 — provenance repair (not a scientific release)

Maintenance only. This is not a new methods result.

- No scientific result changed (`P1_UNRESOLVED_WITHIN_BUDGET`, Q, wall
  ratio 0.956, bootstrap interval, HAC labels, K diagnostic).
- No performance experiment was rerun.
- No speedup claim was added.
- No P1 algorithmic behavior was changed.
- Provenance, checksum, and documentation inconsistencies were repaired
  so historical v1.0.0 checksums cannot be read as hashes of the current
  tree.
- Historical experiment evidence (`release/2026-09-16/`,
  `archive/closure/2026-09-16-final/`, frozen `benchmarks/` JSON) was
  preserved byte-for-byte.
- Current public `linear_da_mod.f90` (SHA256 `c541444f…`) is distinguished
  from the timed confirm-tree file (SHA256 `004b23b6…`). The difference is
  the v1.0.1 F03 `C2_FORCE_A1` fixture gate.
