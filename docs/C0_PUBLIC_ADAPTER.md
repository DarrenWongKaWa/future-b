# Public C0 adapter

C0 is a **source transform** of pinned public FEP-DMC. It is not P1,
not a compiled `perturbo.x` plugin, and not a production LiF result.

## What C0 changes

In `add_external_ph`, `sample_q_omp_int` writes a new `vn1%i_q` and
does not set `vn1%wq`. Later the same update copies `vn2%wq = vn1%wq`,
samples imaginary time with `vn1%wq(vn1%nu)`, and evaluates `Dph` with
those frequencies. Sibling update `add_ph` already calls
`cal_wq_int( vn1%i_q, vn1%wq )` after its sampler. C0 inserts that
same native refresh after the external sampler.

Only one file is written:

`perturbo-fep-dmc/pert-src/diagMC_JJ_updates.f90`

## Supported upstream

| field | value |
|---|---|
| repository | https://github.com/yaoluo/FEP-DMC |
| commit | `05d08449cffdbd0dfbbbf5009add5cc887bc754b` |
| preimage SHA256 | `6c97c694f76df18e9adee7b79666b480f1de5b00f30e8bb5ba08510289e43571` |
| postimage SHA256 | `be3a2215ab257e12aaaba1a0a3cca8714a4174c0fee890bb881cd75a32b9a235` |

Machine record: [`provenance/C0_PUBLIC_PATCH.json`](../provenance/C0_PUBLIC_PATCH.json).
Identity pin: [`provenance/UPSTREAM_FEP_DMC.json`](../provenance/UPSTREAM_FEP_DMC.json).

The public pin is **not** proven identical to the private tree that
produced the frozen 0.956 binary.

## Why the refresh is required

`sample_q_omp_int` (in `diagMC.f90`) samples a grid index into `ixqt`
(`vn1%i_q`) and a proposal probability. It does not compute phonon
frequencies. `cal_wq_int` is the native grid-index frequency routine
(`solve_phonon_fast`, then Ry→eV). Without it, `add_external_ph` keeps
whatever `wq` the recycled vertex slot last held.

## How to verify pristine upstream

```bash
git clone https://github.com/yaoluo/FEP-DMC
git -C FEP-DMC checkout 05d08449cffdbd0dfbbbf5009add5cc887bc754b
python tools/verify_fep_dmc_upstream.py ./FEP-DMC
```

Official identity requires this directory to be its own git toplevel.
The tools do not fetch, checkout, or reset your tree.

## Dry-run

```bash
python integration/c0/apply_c0.py --tree ./FEP-DMC --dry-run
```

Same validation as apply. Prints a unified diff and the expected
postimage SHA256. **Zero writes.**

## Apply

```bash
python integration/c0/apply_c0.py --tree ./FEP-DMC
```

States:

| state | apply |
|---|---|
| PRISTINE | insert exactly one `cal_wq_int` after the external sampler |
| APPLIED | print `ALREADY_APPLIED`, exit 2, no write |
| UNKNOWN | refuse, exit 1, no write |

UNKNOWN includes wrong commit, dirty unrelated pinned files, missing
anchor, duplicate anchor, partial edits, and snapshots without git
identity.

## Verify post-state

```bash
python integration/c0/verify_c0.py --tree ./FEP-DMC
```

Prints `C0_STATE=PRISTINE|APPLIED|UNKNOWN`. UNKNOWN is a nonzero exit.
A C0-patched tree **must not** pass `tools/verify_fep_dmc_upstream.py`.
That tool remains a pristine-identity check.

## Revert

The adapter does not run git restore. From the FEP-DMC checkout:

```bash
git restore perturbo-fep-dmc/pert-src/diagMC_JJ_updates.f90
```

## What has not been established

- No P1 support.
- No speedup claim.
- No change to the frozen LiF benchmark (`P1_UNRESOLVED_WITHIN_BUDGET`,
  wall ratio 0.956…).
- No production LiF validation of this public adapter (LEVEL 0 source
  transform only).
- Public reference upstream is not proven identical to the historical
  timed donor.
- No compile of `perturbo.x` and no runtime check from this adapter.
