# Independent release audit (2026-09-16, post wrap-up)

Not a new research cycle. Question: may README call 0.956 the
released clean binary?

## Verdict

**Yes.** Gating was applied **before** compile and **before** the
timing batch. Production confirm used `P1_FIXTURE=0` on binary
`f9518a21fc2b8750fb3b7ed6f6e065db398cb2f425969cd718d1dcdef2b2c25c`.
GitHub Fortran excerpts match that tree. **Do not rerun** the 6+6
chains for form.

| check | result |
|---|---|
| `apply_p1_clean.py` inserts `p1_fixture_on` default false | yes |
| compile log binary SHA256 | `f9518a21…` |
| all 6 P1 `run.json` SHA256 | same |
| confirm env | `LINEAR_DA=on`, `P1_FIXTURE=0`, `C2_DUMP=0` |
| `c2_swap.tsv` in confirm | absent |
| current `perturbo.x` still `f9518a21…` | yes |
| `linear_da_mod.f90` release vs confirm tree | byte-identical `004b23b6…` |
| `update_swap` excerpt ⊆ confirm `diagMC_JJ_updates.f90` | yes |
| post-timing production-path Fortran edit | none |

## Public-tree hygiene (this audit)

- Dropped from the GitHub candidate: local working-tree notes and
  `src/keldysh4ai` (those files contained machine-local absolute paths).
- `CITATION.cff`: no fake GitHub URL; version `1.0.0`.
- Tag name: **`v1.0.0`** (closed methods study, not beta).
- LICENSE GPL-3.0-or-later matches Perturbo-derived excerpts.
