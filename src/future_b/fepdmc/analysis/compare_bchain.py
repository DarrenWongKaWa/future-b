"""Native chain A vs grouped chain B (laminar phonon-mode groups) on the same material.

A: per-measurement native estimator (raw_num, raw_den) from rb_trace.dat of runs
   whose trajectories are bit-identical to hook-free native runs; A wall time is
   taken from the hook-free runs (fair cost baseline).
B: bchain_trace.dat (f_O, f_1) from FUTUREB_BCHAIN=1 runs.
E = sum(num)/(tau_max sum(den)), Q = E - E_bare; 50-block jackknife per chain.

Usage: python -m future_b.fepdmc.analysis.compare_bchain <runs_A_trace> <runs_A_walltime> <runs_B> <material> <E_bare> [tau_max]
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

import numpy as np

NBLOCK = 50


def jk(num, den, tau):
    nb = len(num) // NBLOCK
    bn = num[: nb * NBLOCK].reshape(NBLOCK, nb).sum(1)
    bd = den[: nb * NBLOCK].reshape(NBLOCK, nb).sum(1)
    est = bn.sum() / bd.sum() / tau
    j = np.array([(bn.sum() - bn[i]) / (bd.sum() - bd[i]) / tau for i in range(NBLOCK)])
    return float(est), float(math.sqrt((NBLOCK - 1) / NBLOCK * np.sum((j - j.mean()) ** 2)))


def tau_int(x):
    """Blocking estimate of the integrated autocorrelation time (plateau max)."""
    x = np.asarray(x, float)
    v0 = x.var()
    best = 1.0
    b = 1
    while len(x) // b >= 30:
        n = len(x) // b
        m = x[: n * b].reshape(n, b).mean(1)
        best = max(best, b * m.var() / v0)
        b *= 2
    return float(best)


def wall(chain: Path):
    t = re.search(r"real\s+(\d+)m([\d.]+)s", (chain / "stderr.log").read_text())
    return int(t.group(1)) * 60 + float(t.group(2)) if t else None


def side(chains, tau, e_bare, cols, wall_dirs=None):
    rows = []
    for c in chains:
        tr = c / ("bchain_trace.dat" if cols == "B" else "rb_trace.dat")
        a = np.loadtxt(tr)
        num, den = (a[:, 0], a[:, 1])
        e, se = jk(num, den, tau)
        w = wall(wall_dirs[c.name]) if wall_dirs else wall(c)
        R = num.sum() / den.sum()
        h = (num - R * den) / den.mean() / tau
        order = a[:, 6]
        row = dict(chain=c.name, n_meas=len(a), Q=e - e_bare, se=se, sign=float(den.mean()), wall_s=w,
                   static_var=float(h.var()), tau_int_h=tau_int(h), tau_int_order=tau_int(order),
                   mean_order=float(order.mean()))
        if cols == "B":
            row["mean_S_eff"] = float(a[:, 2].mean())
            summ = dict(l.split(None, 1) for l in (c / "bchain_summary.dat").read_text().splitlines())
            row["selfcheck"] = {k: summ[k] for k in summ if "mismatch" in k or k.startswith("max_") or "accepted" in k}
        rows.append(row)
    q = np.array([r["Q"] for r in rows])
    se = np.array([r["se"] for r in rows])
    n = len(rows)
    return dict(per_chain=rows,
                Q=float(q.mean()), se_Q_between=float(q.std(ddof=1) / math.sqrt(n)),
                se_Q_jackknife_pooled=float(math.sqrt(np.sum(se ** 2)) / n),
                mean_var_per_chain=float(np.mean(se ** 2)), between_chain_var=float(q.var(ddof=1)),
                sign=float(np.mean([r["sign"] for r in rows])),
                static_var=float(np.mean([r["static_var"] for r in rows])),
                tau_int_h=float(np.mean([r["tau_int_h"] for r in rows])),
                tau_int_order=float(np.mean([r["tau_int_order"] for r in rows])),
                mean_order=float(np.mean([r["mean_order"] for r in rows])),
                mean_wall_s=float(np.mean([r["wall_s"] for r in rows if r["wall_s"]])))


def main():
    a_trace, a_wall, b_runs, mat, e_bare = sys.argv[1:6]
    tau = float(sys.argv[6]) if len(sys.argv) > 6 else 232.09011
    e_bare = float(e_bare)
    b_chains = sorted((Path(b_runs) / mat).glob("chain*"))
    names = [c.name for c in b_chains]
    a_chains = [Path(a_trace) / mat / n for n in names]
    wall_dirs = {n: Path(a_wall) / mat / n for n in names}
    A = side(a_chains, tau, e_bare, "A", wall_dirs)
    B = side(b_chains, tau, e_bare, "B")
    out = dict(material=mat, chains=len(names), A=A, B=B,
               comparison=dict(
                   Q_difference=B["Q"] - A["Q"],
                   static_var_ratio_A_over_B=A["static_var"] / B["static_var"],
                   tau_int_ratio_B_over_A=B["tau_int_h"] / A["tau_int_h"],
                   tau_order_ratio_B_over_A=B["tau_int_order"] / A["tau_int_order"],
                   Q_difference_sigma=(B["Q"] - A["Q"]) / math.hypot(A["se_Q_between"], B["se_Q_between"]),
                   variance_ratio_per_measurement_jackknife=A["mean_var_per_chain"] / B["mean_var_per_chain"],
                   variance_ratio_between_chains=A["between_chain_var"] / B["between_chain_var"],
                   wall_ratio_B_over_A=B["mean_wall_s"] / A["mean_wall_s"],
                   net_efficiency_per_wall_jackknife=A["mean_var_per_chain"] / B["mean_var_per_chain"]
                   * A["mean_wall_s"] / B["mean_wall_s"]))
    json.dump(out, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
