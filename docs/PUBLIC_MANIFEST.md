# Public vs historical manifests

`release/2026-09-16/SHA256SUMS.txt` and
`archive/closure/2026-09-16-final/SHA256SUMS.txt` are **historical**.
Two referenced objects are intentionally absent from the public source
tree (not checksum mismatches):

| missing path | why |
|---|---|
| `FutureB_github_release_candidate_2026-09-16.tar.gz` | packaging byproduct; use git tag `v1.0.0` or `reveal/FutureB_v1.0.0_77835ca.tar.gz` |
| `archive/closure/.../logs/p1_clean_build.json` | private-path build log; not redistributed |

Existing hashed files that are in the tree still match those historical
lists. Do not treat a missing *external* object as “the archive was
corrupted”.
