# v1.1.0 maintenance (first public source adapter)

No new LiF chains. No P1 algorithm change.
`P1_UNRESOLVED_WITHIN_BUDGET` unchanged. v1.0.2 and v1.0.3 provenance
records are immutable.

v1.0.3 prepared packaging and pinned public FEP-DMC identity. v1.1.0
adds the C0 `wq` refresh adapter against that pin.

| id | action |
|---|---|
| C0-1 | Fail-closed apply/verify for pinned `add_external_ph` |
| C0-2 | Exact preimage/postimage SHA256 in `provenance/C0_PUBLIC_PATCH.json` |
| C0-3 | `integration/c0` is GitHub + sdist; not in the wheel |
| C0-4 | Historical `patches/c0_wq` night1 lock left untouched |