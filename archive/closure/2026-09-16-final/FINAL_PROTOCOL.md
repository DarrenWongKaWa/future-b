# FINAL_PROTOCOL — clean P1 vs B-best (frozen before confirmation)

Frozen 2026-09-16 **before** inspecting the confirmation batch
`closure/2026-09-16-final/p1_confirm/`. Historical C5_dev is prior evidence,
not this confirmation.

## Binaries

- B-best: `research/mainline/CLOSURE/2026-09-14/runs/night1/C1/trees/bbest/pert-src/perturbo.x`
- Clean P1: `closure/2026-09-16-final/trees/p1_clean/pert-src/perturbo.x`
- SHA256 recorded in `FINAL_PROVENANCE.json` after build, before confirm runs.

## Input / physics

Same as C5_dev: Method0, 20³, rank20, official QREF `diagMC.in` / `pert.in` / `temper.in`,
LiF `lif-sp3_epwan.h5`, `Nmcmc(1e4)=200`, `DMC_OBSERVER=1`, `OMP=1`, 6 GiB docker slot.
`E_bare` from log `D12 bare_energy_eV`. Formation energy

    Q = Re(sum_b N_b/tauMax_b / sum_b D_b) - E_bare

## Chains

- 6 independent replicates per arm (B-best, clean P1). B0 not required for the 5% claim.
- Seed master `9143600`; arm spawn 0=Bbest, 1=P1; 6 children each.
- Method order rotated by replicate: even r runs B-best then P1; odd r reverse.
- Warmup: native `warmup_flag==0` production blocks only.
- Do not drop chains. Do not add chains if HAC fails.

## Statistics (predeclared)

- Per-chain HAC Bartlett lag 2, 4, 8 on production blocks, ratio of means.
- Fail the **statistical-efficiency** claim if any chain has maxSE/minSE > 1.25.
- Six-chain delete-one jackknife on formation energy (shift does not change Var).
- Bootstrap 2000, seed `9143610`, resample 6 replicate indices jointly for both arms.
- Timing `T` = host `elapsed_s` of the same docker run that produced the blocks (same workload as Q).
- Primary ratio: `T_P1 / T_Bbest`. Secondary: `K = T * VarJK(Q)`.
- Practical-gain threshold: 0.95.

## Classification (do not edit after seeing confirm data)

- bootstrap 97.5% of T_P1/T_Bbest < 0.95 **and** HAC pass both arms → `P1_GAIN_ESTABLISHED`
- bootstrap 2.5% of T_P1/T_Bbest > 0.95 → `P1_NO_PRACTICAL_GAIN` for a ≥5% wall benefit
- interval crosses 0.95, or HAC fails, or K interval unusable → `P1_UNRESOLVED_WITHIN_BUDGET`
- correctness fixture fail → `P1_IMPLEMENTATION_NOT_CLOSED` (no performance claim)

Stop after this batch. No extra sampling.
