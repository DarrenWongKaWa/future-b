"""Native chain A vs grouped chain B by between-chain variance (no tau_int needed).

A: hook-free native runs; Q_i = Etrue_i - E_bare from each chain's stdout.
B: FUTUREB_BCHAIN runs; Q_i from bchain_trace.dat (sum f_O / (tau_max sum f_1)).
Reports Q +- SE for each, the variance ratio var_A/var_B with a 90% F interval,
and the wall-normalized efficiency (var_A t_A) / (var_B t_B).

Usage: python -m future_b.fepdmc.analysis.compare_between <runs_A_plain> <runs_B> <material> <E_bare> [tau_max]
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

import numpy as np


def wall(c: Path):
    """CPU user time of the single-threaded chain (robust to host contention)."""
    t = re.search(r"user\s+(\d+)m([\d.]+)s", (c / "stderr.log").read_text())
    return int(t.group(1)) * 60 + float(t.group(2)) if t else float("nan")


def main():
    from scipy import stats  # optional dependency: pip install 'future-b[analysis]'

    a_runs, b_runs, mat, e_bare = sys.argv[1:5]
    tau = float(sys.argv[5]) if len(sys.argv) > 5 else 232.09011
    e_bare = float(e_bare)
    A, B = [], []
    for c in sorted((Path(a_runs) / mat).glob("chain*")):
        m = re.search(r"Etrue =\s+(\S+)", (c / "stdout.log").read_text())
        g = re.search(r"<g/Z> =\s+(\S+)", (c / "stdout.log").read_text())
        if m:
            A.append(dict(chain=c.name, Q=float(m.group(1)) - e_bare, sign=float(g.group(1)), wall_s=wall(c)))
    for c in sorted((Path(b_runs) / mat).glob("chain*")):
        f = c / "bchain_trace.dat"
        if not (c / "parameter.dat-1").exists():
            continue
        a = np.loadtxt(f)
        B.append(dict(chain=c.name, Q=float(a[:, 0].sum() / (tau * a[:, 1].sum())) - e_bare,
                      sign=float(a[:, 1].mean()), wall_s=wall(c)))

    def summ(rows):
        q = np.array([r["Q"] for r in rows])
        return dict(n=len(rows), Q=float(q.mean()), se=float(q.std(ddof=1) / math.sqrt(len(q))),
                    var=float(q.var(ddof=1)), sign=float(np.mean([r["sign"] for r in rows])),
                    wall_s=float(np.nanmean([r["wall_s"] for r in rows])), per_chain=rows)

    sa, sb = summ(A), summ(B)
    ratio = sa["var"] / sb["var"]
    dfa, dfb = sa["n"] - 1, sb["n"] - 1
    lo = ratio / stats.f.ppf(0.95, dfa, dfb)
    hi = ratio / stats.f.ppf(0.05, dfa, dfb)
    out = dict(material=mat, A=sa, B=sb, comparison=dict(
        Q_difference=sb["Q"] - sa["Q"],
        Q_difference_sigma=(sb["Q"] - sa["Q"]) / math.hypot(sa["se"], sb["se"]),
        variance_ratio_A_over_B=ratio, variance_ratio_90CI=[lo, hi],
        wall_ratio_B_over_A=sb["wall_s"] / sa["wall_s"],
        efficiency_per_wall=ratio * sa["wall_s"] / sb["wall_s"],
        efficiency_per_wall_90CI=[lo * sa["wall_s"] / sb["wall_s"], hi * sa["wall_s"] / sb["wall_s"]]))
    json.dump(out, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
