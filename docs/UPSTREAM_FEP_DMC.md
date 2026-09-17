# Public FEP-DMC upstream pin

This pin identifies the **public reference upstream** used for Future B
integration *development*. It does **not** assert that this public
commit is byte-identical to the private source tree that produced the
frozen timing binary.

Pinned identity is **not** integration support. Future B cannot yet be
applied automatically to that upstream.

| field | value |
|---|---|
| repository | https://github.com/yaoluo/FEP-DMC |
| default branch | `main` |
| reference commit | `05d08449cffdbd0dfbbbf5009add5cc887bc754b` (2025-09-24) |
| role | prospective public integration baseline |
| historical donor | **not established** |

Native Fortran of interest is unchanged from first public source upload
`0f9b7aa` (2024-09-02) through this tip; later public commits only
edited `README.md`. Machine record:
[`provenance/UPSTREAM_FEP_DMC.json`](../provenance/UPSTREAM_FEP_DMC.json).

## Verify a checkout

```bash
git clone https://github.com/yaoluo/FEP-DMC
git -C FEP-DMC checkout 05d08449cffdbd0dfbbbf5009add5cc887bc754b
python tools/verify_fep_dmc_upstream.py ./FEP-DMC
```

The tool does not fetch, checkout, or edit the target.

Official identity (exit 0) requires **this directory to be its own git
toplevel**, **HEAD to equal the pinned commit**, **pinned file SHA256
values to match on-disk bytes**, and **those files to be clean in
`git status`**. A source snapshot without its own `.git` (including a
tree nested inside some other repository) may match file hashes and
still report `GIT_UNAVAILABLE` (exit 3). That is content identity, not
full upstream identity. SHA256 values are of on-disk bytes as GitHub
serves them (LF). `core.autocrlf` conversions will fail the hash check.

## Scope

Pinned files: `diagMC_JJ_updates.f90` (swap / `add_external_ph`),
`diagMC.f90` (`Gel` / `Dph`), `pert_param.f90` (`zeroTMC`, `DMC_Method`),
`pert-src/makefile` (object list a future module would join). This is
not a compile or runtime compatibility claim. Pinned upstream identity
does not yet mean Future B can be applied automatically to that
upstream.
