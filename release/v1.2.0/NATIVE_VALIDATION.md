# Native validation of the public P1 adapter (v1.2.0)

This is kernel-level native evidence on a **short public JJ fixture**.
It is **not** a LiF 50 K production run, not the historical 0.956 binary,
and not a speedup result.

## Original 50 K blocker

Public LiF `lif-sp3_epwan.h5` + `calc_mode=diagmc-JJ` + `zeroTMC=.true.`
+ `T=50 K` sets `tauMax = 1/kT ≈ 232 eV⁻¹`. Native

`Gel(ek,tau) = exp(-ek*tau)`

underflows independently in the numerator and denominator of `P_kchange`
(`ek ≈ 9.35–10.24 eV`, `tau12 ≈ 127 eV⁻¹` → `exp(-1186) = 0/0 = NaN`).
`Re(mat_old/new)` and `factor` were finite; both `Dph` ratios were finite.
Vanilla computes the same NaN `P_accept` (`ran < NaN` is false → reject).
P1 ON `error stop`s, as designed. **Not a P1 formula bug.**

## Replacement fixture

Same public HDF5 (SHA256 `4960618b64f4f1787e7a30aac4c2990ec5632ecbab83a9632f6c659f03da690b`).
`T=1000 K` so `tauMax ≈ 11.6 eV⁻¹` and each `Gel` stays finite.
`zeroTMC=.true.` still (approved domain). SVD + `tabulate-H` nk=20/nsvd=20
with production `perturbo.x`. `Nmcmc=1` (10⁴ steps). Scratch seed pin
`P1_VALIDATE_SEED=12345` (time-based native seed otherwise).

No public upstream `diagmc-JJ` example exists (demo is `diagmc-EZ`).

## What this proves / does not prove

Proves: public pinned FEP-DMC **builds**; P1 OFF matches pristine JJ
update/acceptance counts; P1 ON Stage-1 rejects skip `cal_gkq*`; Stage 2
uses native `P_accept`; counters close; unsupported domains `error stop`.

Does not prove: 50 K LiF statistics, ≥5% speedup, equal-precision gain,
historical 0.956 binary identity, finite-T / multiband / other methods.
