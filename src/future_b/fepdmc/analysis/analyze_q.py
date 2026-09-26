"""One-line momentum group vs mode group on the same line (q_trace.dat).

Each q_trace row is one native sample (fixed stride) and one line chosen by a
state-independent rank rule; rho_q sums that line's q over the whole grid,
rho_mode sums its phonon mode. Under the native measure E[rho] = Z_B/Z_A for
each single-line grouping, so the numbers are directly comparable.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np


def main(runs: str, material: str, sign_a: float | None = None) -> None:
    per = []
    allrows = []
    for chain in sorted((Path(runs) / material).glob("chain*")):
        qt = chain / "q_trace.dat"
        if not qt.exists():
            continue
        q = np.atleast_2d(np.loadtxt(qt))
        r = np.loadtxt(chain / "rb_trace.dat")
        summ = dict(l.split() for l in (chain / "rb_summary.dat").read_text().splitlines())
        per.append(dict(chain=chain.name, n=len(q), sign_A=float(r[:, 1].mean()),
                        E_rho_q=float(q[:, 4].mean()), E_rho_mode=float(q[:, 5].mean()),
                        q_selfcheck=summ.get("n_q_mismatch"), max_q_rel=summ.get("max_q_rel")))
        allrows.append(q)
    a = np.vstack(allrows)
    span = a[:, 3]
    bins = [(1, 1), (2, 4), (5, 9), (10, 10**6)]
    by_span = {}
    for lo, hi in bins:
        m = (span >= lo) & (span <= hi)
        if m.any():
            by_span[f"{lo}-{hi}"] = dict(n=int(m.sum()), E_rho_q=float(a[m, 4].mean()),
                                        E_rho_mode=float(a[m, 5].mean()))
    rq = np.array([p["E_rho_q"] for p in per])
    rm = np.array([p["E_rho_mode"] for p in per])
    sA = sign_a if sign_a is not None else float(np.mean([p["sign_A"] for p in per]))
    n = len(per)
    out = dict(material=material, chains=n, samples=int(len(a)), per_chain=per, by_span=by_span,
               pooled=dict(sign_A=sA,
                           E_rho_q=float(rq.mean()), se_E_rho_q=float(rq.std(ddof=1) / math.sqrt(n)) if n > 1 else None,
                           E_rho_mode=float(rm.mean()), se_E_rho_mode=float(rm.std(ddof=1) / math.sqrt(n)) if n > 1 else None,
                           frac_rho_q_lt_0_9=float(np.mean(a[:, 4] < 0.9)),
                           frac_rho_mode_lt_0_9=float(np.mean(a[:, 5] < 0.9)),
                           deficit_per_line_q=float(1 - rq.mean()), deficit_per_line_mode=float(1 - rm.mean()),
                           mean_lines=float(a[:, 1].mean())))
    json.dump(out, sys.stdout, indent=2)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else None)
