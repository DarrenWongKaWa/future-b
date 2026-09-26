"""Host-side driver for native FEP-DMC diagmc-EZ runs in Docker.

  prepare-tables <material>   svd-elph + tabulate-H (20^3) + alias tables
  ez <material> <n_chains>    diagmc-EZ chains, one FUTUREB_SEED per chain

Configuration (flag, else environment variable, else default):
  --ws      FUTUREB_FEPDMC_WS     workspace mounted at /work; builds live in
                                  <ws>/build/q-e-qe-6.5/<build>/pert-src/perturbo.x,
                                  runs in <ws>/<tag>/<material>/chainNN   (./fepdmc_ws)
  --data    FUTUREB_FEPDMC_DATA   FEP-DMC dataset directory, mounted read-only at /data
  --image   FUTUREB_FEPDMC_IMAGE  Docker image with the QE 6.5 toolchain
                                  (r5p0-env:ubuntu2004)
  --build   tree prepared with `future-b-fepdmc prepare` (perturbo-fep-dmc-pkg)
  --tables  per-material table directory (<ws>/tables/<material>/gkq-20)
  --alias   upstream example/pert-Htable/alias.py, for prepare-tables (<ws>/alias.py)

tabulate-H must use a build made without -fmax-stack-var-size=1 (it re-allocates
local allocatables); pass that tree with --tables-build.

Each container: linux/amd64, OMP_NUM_THREADS=1, the dataset read-only at /data,
the tables read-only at /tables. The Future B switches map one to one onto
FUTUREB_* environment variables (docs/FEP_DMC_TOOLKIT.md).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DEFAULT_IMAGE = "r5p0-env:ubuntu2004"
DEFAULT_BUILD = "perturbo-fep-dmc-pkg"
QE_DIR = "build/q-e-qe-6.5"

# Band windows follow the paper's dataset notebooks (Figures 2-4): LiF-hole and STO
# use three bands, anatase and LiF-electron one band. The anatase H table needs about
# 4.8 GB per process: run its chains with --parallel 1.
MATERIALS = {
    "lif_elec": dict(prefix="lif-sp3", h5="LiF-electron/lif-sp3_epwan.h5", bands=(1, 1), hole=False),
    "lif_hole": dict(prefix="lif", h5="LiF-hole/lif_epwan.h5", bands=(1, 3), hole=True),
    "sto": dict(prefix="sto-200K", h5="STO/sto-200K_epwan.h5", bands=(1, 3), hole=False),
    "anatase": dict(prefix="tio2-gw-elec", h5="TiO2-anatase/tio2-gw-elec_epwan.h5", bands=(1, 1), hole=False),
    "anatase_b3": dict(prefix="tio2-gw-elec", h5="TiO2-anatase/tio2-gw-elec_epwan.h5", bands=(1, 3), hole=False),
}
T_KELVIN = 50.0
NK = 20
NSVD = 20
NMCMC_1E4 = 200
NATIVE_PA = "0.1 0.1 0.1 0.1 0.10 0.10 0.1"


def namelist(**kv) -> str:
    def fmt(v):
        if isinstance(v, bool):
            return ".true." if v else ".false."
        if isinstance(v, str):
            return f"'{v}'"
        return str(v)
    return "&perturbo\n" + "\n".join(f" {k} = {fmt(v)}" for k, v in kv.items()) + "\n/\n"


def binary(build: str) -> str:
    """Container path of perturbo.x for a build tree name (or an explicit path)."""
    return build if build.startswith("/") else f"/work/{QE_DIR}/{build}/pert-src/perturbo.x"


def docker(image: str, mounts: dict, workdir: str, cmd: str, env: dict | None = None) -> int:
    args = ["docker", "run", "--platform", "linux/amd64", "--rm", "-w", workdir]
    for host, (guest, mode) in mounts.items():
        args += ["-v", f"{host}:{guest}:{mode}"]
    env = {"OMP_NUM_THREADS": "1", "OMP_STACKSIZE": "512M", "OMPI_ALLOW_RUN_AS_ROOT": "1",
           "OMPI_ALLOW_RUN_AS_ROOT_CONFIRM": "1", **(env or {})}
    for k, v in env.items():
        args += ["-e", f"{k}={v}"]
    args += [image, "bash", "-lc", "ulimit -s unlimited; " + cmd]
    return subprocess.call(args)


def tables_dir(a, mat: str) -> Path:
    return Path(a.tables) if a.tables else Path(a.ws) / "tables" / mat / f"gkq-{NK}"


def prepare_tables(a, mat: str) -> int:
    m = MATERIALS[mat]
    ws = Path(a.ws)
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
    alias = Path(a.alias) if a.alias else ws / "alias.py"
    if not alias.is_file():
        print(f"{alias}: missing; copy example/pert-Htable/alias.py from the FEP-DMC checkout", file=sys.stderr)
        return 2
    tbin = binary(a.tables_build or a.build)
    h5 = Path(m["h5"]).name
    cmd = (f"ln -sfn /data/{m['h5']} {h5} && "
           f"mpirun -np 1 {tbin} -npools 1 -i pert_svd.in > svd.log 2>&1 && "
           f"for f in eph_S.dat eph_U.dat eph_V.dat g_Rp.dat; do ln -sfn ../gkq/$f gkq-{NK}/$f; done && "
           f"mpirun -np 1 {tbin} -npools 1 -i pert_htable.in > htable.log 2>&1 && "
           f"python3 /alias/alias.py gkq-{NK} > alias.log 2>&1")
    return docker(a.image, {str(ws): ("/work", "rw"), str(a.data): ("/data", "ro"),
                            str(alias.parent): ("/alias", "ro")}, f"/work/tables/{mat}", cmd)


def switch_env(a, mat: str) -> tuple[dict, str]:
    """FUTUREB_* environment for one chain, and the FUTUREB_RB value used."""
    m = MATERIALS[mat]
    rb = "1" if (a.rb or (m["bands"] == (1, 1) and not m["hole"])) else "0"
    on = lambda flag: "1" if flag else "0"  # noqa: E731
    env = {
        "FUTUREB_RB": rb, "FUTUREB_MODES": on(a.modes), "FUTUREB_MODES_K4": on(a.k4),
        "FUTUREB_QGROUP": on(a.qgroup), "FUTUREB_Q_EVERY": str(a.q_every),
        "FUTUREB_BCHAIN": on(a.bchain), "FUTUREB_BCHAIN_GROUP": "0" if a.bchain == "control" else "1",
        "FUTUREB_BCHAIN_ADDREM": on(a.bchain == "addrem"), "FUTUREB_BCHAIN_SRULE": a.srule,
        "FUTUREB_BCHAIN_BLOCK": str(a.block), "FUTUREB_MODES_DUMP": on(a.modes or a.mode_svd),
        "FUTUREB_MODE_RB": on(a.mode_rb), "FUTUREB_RB_WINDOWS": "0" if (a.mode_rb or a.mode_svd) else "1",
        "FUTUREB_MODE_SVD": on(a.mode_svd),
        "FUTUREB_CHQ": on(a.chq > 0), "FUTUREB_CHQ_P": str(a.chq), "FUTUREB_CHQ_EXT": on(a.chq_ext),
        "FUTUREB_CHQ_RT": on(a.chq_rt), "FUTUREB_WQFIX": on(a.wqfix),
        "FUTUREB_ANY": on(a.any > 0), "FUTUREB_ANY_P": str(a.any), "FUTUREB_PNU_FRO": on(a.pnu_fro),
        "FUTUREB_EXTAR": on(a.extar > 0), "FUTUREB_EXTAR_P": str(a.extar), "FUTUREB_EXTFIX": on(a.extfix),
        "FUTUREB_EXTAR_OUTER": on(a.ext_outer), "FUTUREB_HERM_TEST": on(a.herm_test),
        "FUTUREB_EXTAR_MIMIC": on(a.ext_mimic), "FUTUREB_EXTRMFIX": on(a.extrmfix),
        "FUTUREB_EXTAR_RPOS": on(a.rpos), "FUTUREB_EXTAR_RTAU": on(a.rtau),
    }
    if a.mv_until > 0:
        env["FUTUREB_MV_UNTIL"] = str(a.mv_until)
    return env, rb


def ez_chain(a, mat: str, i: int) -> int:
    m = MATERIALS[mat]
    ws = Path(a.ws)
    seed = a.seed0 + 7919 * i
    run = ws / a.tag / mat / f"chain{i:02d}"
    run.mkdir(parents=True, exist_ok=True)
    kv = dict(prefix=m["prefix"], calc_mode="diagmc-EZ", DMC_Method=0,
              band_min=m["bands"][0], band_max=m["bands"][1], zeroTMC=True, read_H=True,
              nsvd=NSVD, nk_svd=NK, tauMin=0.0, alpha_frohlich=1.0, svd_dir="/tables",
              ftemper="temper.in", phfreq_cutoff=1.0, print_sign=False)
    if m["hole"]:
        kv["hole"] = True
    (run / "pert.in").write_text(namelist(**kv))
    (run / "temper.in").write_text(f"1 T\n{a.temp:.2f} 11.5 1.0E+18\n")
    (run / "diagMC.in").write_text(
        "Nmcmc(1e4)      Px  Py   Pz      mu(eV)  se_check   nq_se_checkmaxOrder \n"
        f"{a.nmcmc} 0 0 0 0.0 0 50000 {a.maxorder}\ntypes of update\n7\n"
        "prob for each update, for green-function, there are 7 updates  \n"
        f"{a.pa}\n")
    env, rb = switch_env(a, mat)
    meta = dict(material=mat, chain=i, seed=seed, T=a.temp, nk=NK, nsvd=NSVD, Nmcmc_1e4=a.nmcmc,
                maxOrder=a.maxorder, binary=binary(a.build), update_probs=a.pa, switches=env, **m)
    (run / "run_meta.json").write_text(json.dumps(meta, indent=2))
    h5 = Path(m["h5"]).name
    cmd = (f"ln -sfn /data/{m['h5']} {h5} && "
           f"( time mpirun -np 1 {binary(a.build)} -npools 1 -i pert.in ) > stdout.log 2> stderr.log")
    return docker(a.image, {str(ws): ("/work", "rw"), str(a.data): ("/data", "ro"),
                            str(tables_dir(a, mat)): ("/tables", "ro")},
                  f"/work/{a.tag}/{mat}/chain{i:02d}", cmd, env={"FUTUREB_SEED": str(seed), **env})


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="future-b-fepdmc run", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["prepare-tables", "ez"])
    ap.add_argument("material", choices=list(MATERIALS))
    ap.add_argument("n_chains", nargs="?", type=int, default=6)
    ap.add_argument("--ws", default=os.environ.get("FUTUREB_FEPDMC_WS", "fepdmc_ws"))
    ap.add_argument("--data", default=os.environ.get("FUTUREB_FEPDMC_DATA"))
    ap.add_argument("--image", default=os.environ.get("FUTUREB_FEPDMC_IMAGE", DEFAULT_IMAGE))
    ap.add_argument("--build", default=DEFAULT_BUILD, help="build tree name or container path of perturbo.x")
    ap.add_argument("--tables-build", default=None, help="build for tabulate-H (no -fmax-stack-var-size=1)")
    ap.add_argument("--tables", default=None, help="table directory for the material")
    ap.add_argument("--alias", default=None, help="upstream alias.py for prepare-tables")
    ap.add_argument("--first", type=int, default=0)
    ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--seed0", type=int, default=20260925)
    ap.add_argument("--nmcmc", type=int, default=NMCMC_1E4, help="steps in units of 1e4")
    ap.add_argument("--tag", default="runs")
    ap.add_argument("--temp", type=float, default=T_KELVIN, help="temperature (K); EZ uses tau_max = 1/kT")
    ap.add_argument("--maxorder", type=int, default=500, help="<= 997 (maxN = 1000 vertices)")
    ap.add_argument("--pa", default=NATIVE_PA, help="7 native update probabilities")
    g = ap.add_argument_group("native fixes")
    g.add_argument("--wqfix", action="store_true", help="FUTUREB_WQFIX: phonon frequency in add_external_ph")
    g.add_argument("--extfix", action="store_true", help="FUTUREB_EXTFIX: support check in remove_external_ph")
    g.add_argument("--extrmfix", action="store_true", help="FUTUREB_EXTRMFIX: reference trace in remove_external_ph")
    g = ap.add_argument_group("Future B moves")
    g.add_argument("--extar", type=float, default=0.0, help="ordered external add/remove probability per step")
    g.add_argument("--any", type=float, default=0.0, help="general-span add/remove probability per step")
    g.add_argument("--chq", type=float, default=0.0, help="change-q probability per step")
    g.add_argument("--chq-ext", action="store_true", help="change-q also on external pairs")
    g.add_argument("--mv-until", type=int, default=0, help="apply the moves only for the first N steps")
    g.add_argument("--bchain", choices=["", "group", "control", "addrem"], default="",
                   help="grouped chain B: group, control (no grouping), addrem (use --pa with PA1=PA2=0)")
    g.add_argument("--block", type=int, default=1, help="native steps per B second stage (divides 100)")
    g.add_argument("--srule", choices=["greedy", "max"], default="greedy", help="B-chain line-set rule")
    g = ap.add_argument_group("diagnostics and experiment variants")
    g.add_argument("--rb", action="store_true", help="force FUTUREB_RB=1")
    g.add_argument("--modes", action="store_true")
    g.add_argument("--k4", action="store_true")
    g.add_argument("--qgroup", action="store_true")
    g.add_argument("--q-every", type=int, default=50)
    g.add_argument("--mode-rb", action="store_true")
    g.add_argument("--mode-svd", action="store_true")
    g.add_argument("--chq-rt", action="store_true", help="round-trip check of the external moves")
    g.add_argument("--pnu-fro", action="store_true", help="gauge-invariant mode proposal")
    g.add_argument("--herm-test", action="store_true", help="hermiticity test of the vertex tables")
    g.add_argument("--ext-outer", action="store_true")
    g.add_argument("--ext-mimic", action="store_true")
    g.add_argument("--rpos", action="store_true")
    g.add_argument("--rtau", action="store_true")
    return ap


def main(argv: list[str] | None = None) -> int:
    a = parser().parse_args(argv)
    if not a.data:
        print("dataset directory required: --data or FUTUREB_FEPDMC_DATA", file=sys.stderr)
        return 2
    if a.action == "prepare-tables":
        return prepare_tables(a, a.material)
    idx = range(a.first, a.first + a.n_chains)
    with ThreadPoolExecutor(a.parallel) as ex:
        codes = list(ex.map(lambda i: ez_chain(a, a.material, i), idx))
    print(a.material, "exit codes", codes)
    return max(codes)


if __name__ == "__main__":
    sys.exit(main())
