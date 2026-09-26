# Public vs historical manifests

Checksum files in this repository are **not interchangeable**.

| file | class | use as checksum of the current tree? |
|---|---|---|
| `release/v1.3.1/SHA256SUMS.txt` | **CURRENT** (this release: toolkit documentation correction) | **yes** |
| `release/v1.3.0/SHA256SUMS.txt` | **HISTORICAL** (FEP-DMC toolkit) | **no** |
| `release/v1.2.0/SHA256SUMS.txt` | **HISTORICAL** (public P1 source adapter) | **no** |
| `release/v1.1.0/SHA256SUMS.txt` | **HISTORICAL** (public C0 source adapter) | **no** |
| `release/v1.0.3/SHA256SUMS.txt` | **HISTORICAL** (packaging + upstream pin) | **no** |
| `release/v1.0.2/SHA256SUMS.txt` | **HISTORICAL** (v1.0.2 provenance repair) | **no** |
| `release/2026-09-16/SHA256SUMS.txt` | **HISTORICAL** (v1.0.0 wrap-up / GitHub candidate) | **no** |
| `archive/closure/2026-09-16-final/SHA256SUMS.txt` | **HISTORICAL** (closure dump) | **no** |
| `reveal/SHA256SUMS.txt` (not in this git tree) | **HISTORICAL** (v1.0.0 public archive only) | **no** |

## Historical lists (`release/2026-09-16/` and `archive/closure/`)

Those files are immutable evidence of an earlier state. They must not
be rewritten. Two referenced objects were intentionally absent from
the public source tree (not checksum mismatches):

| missing path | why |
|---|---|
| `FutureB_github_release_candidate_2026-09-16.tar.gz` | packaging byproduct; use git tag `v1.0.0` or `reveal/FutureB_v1.0.0_77835ca.tar.gz` |
| `archive/closure/.../logs/p1_clean_build.json` | private-path build log; not redistributed |

**Do not treat a missing *external* object as “the archive was
corrupted”.**

**Do not treat the historical lists as hashes of the current files.**
After v1.0.1, current `README.md` and `docs/SCIENTIFIC_RESULT.md` **no
longer** match `release/2026-09-16/SHA256SUMS.txt`. Frozen science
JSON/CSV listed there still match (the result was not rewritten).

Verify the **current** tree with `release/v1.3.1/SHA256SUMS.txt`.
Do not use `release/v1.3.0/SHA256SUMS.txt`, `release/v1.2.0/SHA256SUMS.txt`, `release/v1.1.0/SHA256SUMS.txt`,
`release/v1.0.3/SHA256SUMS.txt`, or
`release/v1.0.2/SHA256SUMS.txt` as hashes of later files.
