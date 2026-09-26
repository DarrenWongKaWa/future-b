#!/usr/bin/env python3
"""Native FEP-DMC runs for the grouped-consumer follow-ups (host-side driver).

  prepare-tables <material>   svd-elph + tabulate-H (20^3) + alias tables
  ez <material> <n_chains>    native diagmc-EZ chains, FUTUREB_SEED per chain
                              (FUTUREB_RB=1 for single-band electron materials)

Runs live in the scratch workspace (--ws, default below), outside the repo.
Each container: linux/amd64 r5p0-env:ubuntu2004, OMP_NUM_THREADS=1, the
patched binary from patch_fepdmc.py, dataset mounted read-only at /data.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

WS = Path("/Users/kawawong/Research/future-b-worktrees/_scratch/rb_native")
DATA = Path("/Users/kawawong/Research/future-b/FEP-DMC-Data/FEP-DMC-Dataset")
IMAGE = "r5p0-env:ubuntu2004"
BIN = "/work/build/q-e-qe-6.5/perturbo-fep-dmc/pert-src/perturbo.x"
# Same patched source built without -fmax-stack-var-size=1: tabulate-H re-allocates
# local allocatables (phonon_dispersion exp_ikr), which static locals forbid.
BIN_TABLES = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-tables/pert-src/perturbo.x"
# Same source with the general (multiband) rb_window.f90: RB + exact tiled-group sign ratio.
BIN_MB = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb/pert-src/perturbo.x"
# mb + phonon-mode grouping diagnostics (FUTUREB_MODES=1).
BIN_MB2 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb2/pert-src/perturbo.x"
# mb2 + per-line rho, joint 4-line mode group (FUTUREB_MODES_K4=1) and prod over lines.
BIN_MB3 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb3/pert-src/perturbo.x"
# mb3 + one-line momentum group over the whole grid (FUTUREB_QGROUP=1).
BIN_MB4 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb4/pert-src/perturbo.x"
# mb4 + line-pair independence test and greedy non-crossing (laminar) line set.
BIN_MB5 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb5/pert-src/perturbo.x"
# mb5 + grouped-measure chain B (bchain.f90, FUTUREB_BCHAIN=1).
BIN_MB6 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb6/pert-src/perturbo.x"
# mb6 + B-native add/remove moves (FUTUREB_BCHAIN_ADDREM=1).
BIN_MB7 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb7/pert-src/perturbo.x"
# mb7 + wall-clock profile of the B chain.
BIN_MB8 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb8/pert-src/perturbo.x"
# mb8 + fast value-only state evaluation with cached logs (stage-1 acceleration).
BIN_MB9 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb9/pert-src/perturbo.x"
# mb9 + line-set rule option (FUTUREB_BCHAIN_SRULE=max: maximum non-crossing set).
BIN_MB10 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb10/pert-src/perturbo.x"
# mb10 + composite-block second stage (FUTUREB_BCHAIN_BLOCK=k).
BIN_MB11 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb11/pert-src/perturbo.x"
# mb11 + line-topology dump for offline group-rule studies (FUTUREB_MODES_DUMP=1).
BIN_MB12 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb12/pert-src/perturbo.x"
# mb12 + measurement-side mode Rao-Blackwell (FUTUREB_MODE_RB=1), windows switch.
BIN_MB13 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb13/pert-src/perturbo.x"
# mb13 + SVD mode-basis sign diagnostic (FUTUREB_MODE_SVD=1).
BIN_MB14 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb14/pert-src/perturbo.x"
# mb14 + per-line gamma dump and exact two-line basis-change test.
BIN_MB15 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb15/pert-src/perturbo.x"
# mb15 + exact change-q move for existing lines (FUTUREB_CHQ=1, FUTUREB_CHQ_P).
BIN_MB16 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb16/pert-src/perturbo.x"
# mb16 + change-q on external (boundary-wrapping) pairs (FUTUREB_CHQ_EXT=1).
BIN_MB17 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb17/pert-src/perturbo.x"
# mb17 + round-trip detailed-balance check of the external move (FUTUREB_CHQ_RT=1).
BIN_MB18 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb18/pert-src/perturbo.x"
# mb18 + opt-in fix of the stale external-phonon frequency in add_external_ph (FUTUREB_WQFIX=1).
BIN_MB19 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb19/pert-src/perturbo.x"
# mb19 + general-span add/remove of internal lines (FUTUREB_ANY=1, FUTUREB_ANY_P).
BIN_MB20 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb20/pert-src/perturbo.x"
# mb20 + gauge diagnostic and gauge-invariant mode proposal option (FUTUREB_PNU_FRO=1).
BIN_MB21 = "/work/build/q-e-qe-6.5/perturbo-fep-dmc-mb21/pert-src/perturbo.x"

# Band windows follow the paper's dataset notebooks (Figure-2/3/4):
# LiF-hole and STO use three bands, anatase and LiF-electron one band.
MATERIALS = {
    "lif_elec": dict(prefix="lif-sp3", h5="LiF-electron/lif-sp3_epwan.h5", bands=(1, 1), hole=False,
                     tables="/Users/kawawong/Research/future-b/research/luo_energy_1pct/2026-09-11/runs/prep/htable/gkq-20"),
    "lif_hole": dict(prefix="lif", h5="LiF-hole/lif_epwan.h5", bands=(1, 3), hole=True,
                     tables="/Users/kawawong/Research/future-b/prototypes/r5_p0_native_chain_audit/runs/lif_hole_20/gkq-20"),
    "sto": dict(prefix="sto-200K", h5="STO/sto-200K_epwan.h5", bands=(1, 3), hole=False, tables=None),
    "anatase": dict(prefix="tio2-gw-elec", h5="TiO2-anatase/tio2-gw-elec_epwan.h5", bands=(1, 1), hole=False,
                    tables=None),
    # Single-band anatase gives Q = -0.087 eV vs the paper's -0.146 eV (20^3); test a 3-band window.
    "anatase_b3": dict(prefix="tio2-gw-elec", h5="TiO2-anatase/tio2-gw-elec_epwan.h5", bands=(1, 3), hole=False,
                       tables=None),
}
# The anatase H table needs ~4.8 GB per process: run its chains with --parallel 1.
T_KELVIN = 50.0
NK = 20
NSVD = 20
NMCMC_1E4 = 200


def namelist(**kv) -> str:
    def fmt(v):
        if isinstance(v, bool):
            return ".true." if v else ".false."
        if isinstance(v, str):
            return f"'{v}'"
        return str(v)
    return "&perturbo\n" + "\n".join(f" {k} = {fmt(v)}" for k, v in kv.items()) + "\n/\n"


def docker(mounts: dict, workdir: str, cmd: str, env: dict | None = None) -> int:
    args = ["docker", "run", "--platform", "linux/amd64", "--rm", "-w", workdir]
    for host, (guest, mode) in mounts.items():
        args += ["-v", f"{host}:{guest}:{mode}"]
    env = {"OMP_NUM_THREADS": "1", "OMP_STACKSIZE": "512M", "OMPI_ALLOW_RUN_AS_ROOT": "1",
           "OMPI_ALLOW_RUN_AS_ROOT_CONFIRM": "1", **(env or {})}
    for k, v in env.items():
        args += ["-e", f"{k}={v}"]
    args += [IMAGE, "bash", "-lc", "ulimit -s unlimited; " + cmd]
    return subprocess.call(args)


def tables_dir(ws: Path, mat: str) -> Path:
    m = MATERIALS[mat]
    return Path(m["tables"]) if m["tables"] else ws / "tables" / mat / f"gkq-{NK}"


def prepare_tables(ws: Path, mat: str) -> int:
    m = MATERIALS[mat]
    if m["tables"]:
        print(f"{mat}: using existing tables {m['tables']}")
        return 0
    d = ws / "tables" / mat
    (d / "gkq").mkdir(parents=True, exist_ok=True)
    (d / f"gkq-{NK}").mkdir(exist_ok=True)
    common = dict(prefix=m["prefix"], band_min=m["bands"][0], band_max=m["bands"][1], nsvd=NSVD)
    if m["hole"]:
        common["hole"] = True
    (d / "pert_svd.in").write_text(namelist(calc_mode="svd-elph", svd_dir="./gkq", read_svd=False,
                                            apply_svd=True, **common))
    (d / "pert_htable.in").write_text(namelist(calc_mode="tabulate-H", nk_svd=NK, read_svd=True,
                                               apply_svd=True, svd_dir=f"./gkq-{NK}", **common))
    h5 = Path(m["h5"]).name
    cmd = (f"ln -sfn /data/{m['h5']} {h5} && "
           f"mpirun -np 1 {BIN_TABLES} -npools 1 -i pert_svd.in > svd.log 2>&1 && "
           f"for f in eph_S.dat eph_U.dat eph_V.dat g_Rp.dat; do ln -sfn ../gkq/$f gkq-{NK}/$f; done && "
           f"mpirun -np 1 {BIN_TABLES} -npools 1 -i pert_htable.in > htable.log 2>&1 && "
           f"python3 /work/alias.py gkq-{NK} > alias.log 2>&1")
    return docker({str(ws): ("/work", "rw"), str(DATA): ("/data", "ro")},
                  f"/work/tables/{mat}", cmd)


def ez_chain(ws: Path, mat: str, i: int, seed: int, nmcmc: int = NMCMC_1E4, tag: str = "runs",
             max_order: int = 500, bin_path: str = BIN, rb_force: bool = False,
             modes: bool = False, k4: bool = False, qgroup: bool = False, q_every: int = 50,
             bchain: str = "", pa: str = "0.1 0.1 0.1 0.1 0.10 0.10 0.1", temp: float = T_KELVIN,
             srule: str = "greedy", block: int = 1, mode_rb: bool = False, mode_svd: bool = False,
             chq: float = 0.0, chq_ext: bool = False, chq_rt: bool = False,
             wqfix: bool = False, any_p: float = 0.0, pnu_fro: bool = False) -> int:
    m = MATERIALS[mat]
    run = ws / tag / mat / f"chain{i:02d}"
    run.mkdir(parents=True, exist_ok=True)
    kv = dict(prefix=m["prefix"], calc_mode="diagmc-EZ", DMC_Method=0,
              band_min=m["bands"][0], band_max=m["bands"][1], zeroTMC=True, read_H=True,
              nsvd=NSVD, nk_svd=NK, tauMin=0.0, alpha_frohlich=1.0, svd_dir="/tables",
              ftemper="temper.in", phfreq_cutoff=1.0, print_sign=False)
    if m["hole"]:
        kv["hole"] = True
    (run / "pert.in").write_text(namelist(**kv))
    (run / "temper.in").write_text(f"1 T\n{temp:.2f} 11.5 1.0E+18\n")
    (run / "diagMC.in").write_text(
        "Nmcmc(1e4)      Px  Py   Pz      mu(eV)  se_check   nq_se_checkmaxOrder \n"
        f"{nmcmc} 0 0 0 0.0 0 50000 {max_order}\ntypes of update\n7\n"
        "prob for each update, for green-function, there are 7 updates  \n"
        f"{pa}\n")
    rb = "1" if (rb_force or (m["bands"] == (1, 1) and not m["hole"])) else "0"
    meta = dict(material=mat, chain=i, seed=seed, FUTUREB_RB=rb, T=temp, nk=NK, nsvd=NSVD,
                Nmcmc_1e4=nmcmc, maxOrder=max_order, binary=bin_path, bchain=bchain, update_probs=pa, srule=srule, block=block, chq=chq, chq_ext=chq_ext, wqfix=wqfix, any_p=any_p, pnu_fro=pnu_fro, **{k: v for k, v in m.items() if k != "tables"})
    (run / "run_meta.json").write_text(json.dumps(meta, indent=2))
    h5 = Path(m["h5"]).name
    cmd = (f"ln -sfn /data/{m['h5']} {h5} && "
           f"( time mpirun -np 1 {bin_path} -npools 1 -i pert.in ) > stdout.log 2> stderr.log")
    return docker({str(ws): ("/work", "rw"), str(DATA): ("/data", "ro"),
                   str(tables_dir(ws, mat)): ("/tables", "ro")},
                  f"/work/{tag}/{mat}/chain{i:02d}", cmd,
                  env={"FUTUREB_SEED": str(seed), "FUTUREB_RB": rb, "FUTUREB_MODES": "1" if modes else "0",
                       "FUTUREB_MODES_K4": "1" if k4 else "0", "FUTUREB_QGROUP": "1" if qgroup else "0",
                       "FUTUREB_Q_EVERY": str(q_every),
                       "FUTUREB_BCHAIN": "1" if bchain else "0",
                       "FUTUREB_BCHAIN_GROUP": "0" if bchain == "control" else "1",
                       "FUTUREB_BCHAIN_ADDREM": "1" if bchain == "addrem" else "0",
                       "FUTUREB_BCHAIN_SRULE": srule, "FUTUREB_BCHAIN_BLOCK": str(block),
                       "FUTUREB_MODES_DUMP": "1" if (modes or mode_svd) else "0",
                       "FUTUREB_MODE_RB": "1" if mode_rb else "0",
                       "FUTUREB_RB_WINDOWS": "0" if (mode_rb or mode_svd) else "1",
                       "FUTUREB_MODE_SVD": "1" if mode_svd else "0",
                       "FUTUREB_CHQ": "1" if chq > 0 else "0", "FUTUREB_CHQ_P": str(chq),
                       "FUTUREB_CHQ_EXT": "1" if chq_ext else "0", "FUTUREB_CHQ_RT": "1" if chq_rt else "0",
                       "FUTUREB_WQFIX": "1" if wqfix else "0",
                       "FUTUREB_ANY": "1" if any_p > 0 else "0", "FUTUREB_ANY_P": str(any_p),
                       "FUTUREB_PNU_FRO": "1" if pnu_fro else "0"})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["prepare-tables", "ez"])
    ap.add_argument("material", choices=list(MATERIALS))
    ap.add_argument("n_chains", nargs="?", type=int, default=6)
    ap.add_argument("--first", type=int, default=0)
    ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--seed0", type=int, default=20260925)
    ap.add_argument("--ws", default=str(WS))
    ap.add_argument("--nmcmc", type=int, default=NMCMC_1E4)
    ap.add_argument("--tag", default="runs")
    ap.add_argument("--bin", choices=["default", "mb", "mb2", "mb3", "mb4", "mb5", "mb6", "mb7", "mb8", "mb9", "mb10", "mb11", "mb12", "mb13", "mb14", "mb15", "mb16", "mb17", "mb18", "mb19", "mb20", "mb21"], default="default")
    ap.add_argument("--modes", action="store_true", help="FUTUREB_MODES=1 (needs --bin mb2/mb3 --rb)")
    ap.add_argument("--k4", action="store_true", help="FUTUREB_MODES_K4=1 (mb3)")
    ap.add_argument("--qgroup", action="store_true", help="FUTUREB_QGROUP=1 (mb4)")
    ap.add_argument("--q-every", type=int, default=50)
    ap.add_argument("--mode-svd", action="store_true", help="SVD mode-basis sign diagnostic (mb14, --rb)")
    ap.add_argument("--mode-rb", action="store_true", help="measurement-side mode Rao-Blackwell only (mb13, --rb)")
    ap.add_argument("--chq", type=float, default=0.0, help="change-q move probability per step (mb16)")
    ap.add_argument("--chq-ext", action="store_true", help="also move external pairs (mb17)")
    ap.add_argument("--chq-rt", action="store_true", help="round-trip check of the external move (mb18)")
    ap.add_argument("--wqfix", action="store_true", help="fix stale external-phonon frequency (mb19)")
    ap.add_argument("--any", type=float, default=0.0, help="general-span add/remove probability per step (mb20)")
    ap.add_argument("--pnu-fro", action="store_true", help="gauge-invariant mode proposal in the Future B moves (mb21)")
    ap.add_argument("--block", type=int, default=1, help="native steps per B second stage (divides 100)")
    ap.add_argument("--srule", choices=["greedy", "max"], default="greedy", help="B-chain line-set rule")
    ap.add_argument("--temp", type=float, default=T_KELVIN, help="temperature (K); EZ uses tau_max = 1/kT")
    ap.add_argument("--pa", default="0.1 0.1 0.1 0.1 0.10 0.10 0.1", help="7 native update probabilities")
    ap.add_argument("--bchain", choices=["", "group", "control", "addrem"], default="",
                    help="grouped chain B (mb6): group = laminar mode sum, control = no grouping, "
                         "addrem = group + B-native add/remove (use --pa with PA1=PA2=0)")
    ap.add_argument("--rb", action="store_true", help="force FUTUREB_RB=1 (needs --bin mb for multiband)")
    ap.add_argument("--maxorder", type=int, default=500, help="<= 997 (maxN = 1000 vertices)")
    a = ap.parse_args()
    ws = Path(a.ws)
    if a.action == "prepare-tables":
        return prepare_tables(ws, a.material)
    idx = range(a.first, a.first + a.n_chains)
    with ThreadPoolExecutor(a.parallel) as ex:
        codes = list(ex.map(lambda i: ez_chain(ws, a.material, i, a.seed0 + 7919 * i, a.nmcmc, a.tag, a.maxorder,
                                                       {"mb": BIN_MB, "mb2": BIN_MB2, "mb3": BIN_MB3, "mb4": BIN_MB4, "mb5": BIN_MB5, "mb6": BIN_MB6, "mb7": BIN_MB7, "mb8": BIN_MB8, "mb9": BIN_MB9, "mb10": BIN_MB10, "mb11": BIN_MB11, "mb12": BIN_MB12, "mb13": BIN_MB13, "mb14": BIN_MB14, "mb15": BIN_MB15, "mb16": BIN_MB16, "mb17": BIN_MB17, "mb18": BIN_MB18, "mb19": BIN_MB19, "mb20": BIN_MB20, "mb21": BIN_MB21}.get(a.bin, BIN), a.rb,
                                                       a.modes, a.k4, a.qgroup, a.q_every, a.bchain, a.pa, a.temp, a.srule, a.block, a.mode_rb, a.mode_svd, a.chq, a.chq_ext, a.chq_rt, a.wqfix, a.any, a.pnu_fro), idx))
    print(a.material, "exit codes", codes)
    return max(codes)


if __name__ == "__main__":
    sys.exit(main())
