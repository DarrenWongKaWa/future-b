# Method P1 — exact-corrected analytic delayed acceptance

## Native object

Swap of two phonon vertices on a Method0 (Luo EZ) diagram. The native
acceptance uses the local ratio of diagram weights. The weight that
enters the ratio is \(\mathrm{abs}(\mathrm{Re}\,M)\), implemented as

```fortran
ellR = log(abs(real(mat_new))) - log(abs(real(mat_old)))
```

plus the cheap electron/phonon propagator pieces already present in
\(P_{k\mathrm{change}}\). Using \(\lvert M\rvert_{\mathbb{C}}\) is a
different target and is rejected by tests.

## Two-stage delayed acceptance

1. **Stage 1 (cheap).** Eligible swaps evaluate the *unclipped*
   propagator log-score, then clip to \(\pm\ln 10\) to form
   \(\ell_{\mathrm{hat}}\). These are different objects. Draw
   \(u_1\sim U(0,1)\). If \(\log u_1 \ge \min(0,\ell_{\mathrm{hat}})\),
   reject and **return before** `cal_gkq` / environment contraction.
2. **Stage 2 (exact).** Otherwise compute the native matrix contraction
   and draw an independent \(u_2\sim U(0,1)\) (native `ran`). Accept if
   \(\log u_2 < \min(0, \ell_R - \ell_{\mathrm{hat}})\).
   This restores the exact native ratio (Christen–Fox / DA identity).
   The two uniforms are not the same draw.

`C2_FORCE_A1` is fixture-only (v1.0.1). Production with `P1_FIXTURE` off
ignores it.

The cheap score is **not** allowed to replace the exact target.

## Clean production path

Environment `P1_FIXTURE` defaults off. Then the timed path does **not**
run:

- `c2_dump_swap` event logging
- after-commit reverse `p1_prop_ell`
- dump-only `ellR` recomputation for TSV rows

It **does** run:

- `linear_da_eval` / `p1_prop_ell` once for the stage-1 score
- exact `ellR` for stage-2 when stage 1 passes
- independent counters `n_invoked, n_eligible, n_score, n_stage1_rej,
  n_stage2, n_accept` printed as `LINEAR_DA_COUNTS`

`C1_PROFILE=off` still increments in-memory `c1_ncall` on `c1_tic`, but
does not write `c1_timers.csv`. Production confirm therefore has
exclusive-time buckets in `e06_timers.csv` and DA counters, not printed
g/environment call totals. Call-count skip evidence is the fixture
(`P1_FIXTURE=1`): 4372 stage-1 rejects with recorded \(\Delta g=\Delta\mathrm{env}=0\).

## Reverse proposal

Occupancy reverse: swap the two phonons' frequencies and partner times,
keep the time-ordered skeleton, and swap the mid-band energies in the
score. Do **not** reverse by flipping both \(\Delta t\) and \(\Delta E\).

## What P1 is not

- Not a neural network.
- Not a change of Hamiltonian or observable.
- Not a proof of \(\ge 5\%\) wall-clock gain (see
  [STATISTICS.md](STATISTICS.md)).
- Not a 1% ground-state certification.
