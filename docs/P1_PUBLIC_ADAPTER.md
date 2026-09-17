# Public P1 adapter (source transform)

This is the **how-to** for the public P1 source adapter. The contract is
[`P1_PUBLIC_ADAPTER_DESIGN.md`](P1_PUBLIC_ADAPTER_DESIGN.md).

## Implemented (LEVEL 0)

A third party with Future B and a pin checkout can verify, dry-run,
apply, and verify P1 (and compose with C0) with no private tree.

Pinned upstream: `https://github.com/yaoluo/FEP-DMC` commit
`05d08449cffdbd0dfbbbf5009add5cc887bc754b`.

```bash
python tools/verify_fep_dmc_upstream.py ./FEP-DMC
python integration/p1/apply_p1.py --tree ./FEP-DMC --dry-run
python integration/p1/apply_p1.py --tree ./FEP-DMC
python integration/p1/verify_p1.py --tree ./FEP-DMC
```

C0 then P1, or P1 then C0, yield the same
`PUBLIC_C0_P1_APPLIED` file hashes.

Revert:

```bash
git restore perturbo-fep-dmc/pert-src/diagMC_JJ_updates.f90 \
            perturbo-fep-dmc/pert-src/makefile \
            perturbo-fep-dmc/pert-src/diagMC_JJ.f90
rm perturbo-fep-dmc/pert-src/linear_da_mod.f90
```

## Exactness

Stage 2 uses `ell_R = log(P_accept)` after vanilla computes
`P_accept = abs(factor) * P_kchange`. There is no second Gel/Dph
re-sum for the exact ratio.

Stage 1 runs after the time-order stop and before the first
`cal_gkq_vtex_int`.

## Operating domain (`LINEAR_DA=on`)

Refuses (`error stop` in `linear_da_ensure`): `DMC_Method/=0`,
`dmc_band/=1`, `sample_gt=.true.`, `zeroTMC=.false.`, score other
than `prop`, `LINEAR_DA` other than `off`/`on`.

Default `LINEAR_DA=off`: no aux RNG, no extra `cal_ek_int`, native
`ran < P_accept`.

`Re(mat_old)=0` with P1 on is `error stop` (not vanilla `Inf` accept).

## Not established

- Compile of `perturbo.x` (LEVEL 1/2)
- Native P1-off seed-sequence equality on a running binary
- LiF runtime / target-equivalence (LEVEL 3B/4)
- Speedup
- Identity with the historical 0.956 timed donor
