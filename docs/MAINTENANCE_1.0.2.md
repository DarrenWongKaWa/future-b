# v1.0.2 maintenance (provenance only)

No new LiF chains. No algorithm change. `P1_UNRESOLVED_WITHIN_BUDGET`
unchanged. v1.0.0 science files unchanged.

This release repairs release metadata so historical checksums and the
timed Fortran pin cannot be read as hashes of the current tree.

| id | action |
|---|---|
| P01 | Distinguish public source, timed historical source, and frozen result |
| P02 | Current `linear_da_mod.f90` SHA256 `c541444f…` recorded separately from timed `004b23b6…` |
| P03 | `docs/PUBLIC_MANIFEST.md` no longer claims v1.0.0 SHA256SUMS match current files |
| P04 | `release/v1.0.2/SHA256SUMS.txt` is the current-tree checksum file |
| P05 | Historical `release/2026-09-16/SHA256SUMS.txt` left immutable |
| P06 | Document that `FINAL_PROVENANCE.json` `6e5529f` is the private extract wrap-up commit, not public `e418d88` |
