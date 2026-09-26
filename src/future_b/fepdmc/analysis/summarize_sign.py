"""Summarize native LiF average sign and bound the grouped-measure benefit.

Production campaigns only (Nmcmc(1e4) >= 100); fixture runs, advisor-pack and
prototype copies of other campaigns are excluded. Standard errors use the spread of
independent chains within a campaign.
"""

from __future__ import annotations

import csv
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


def campaign(run: str) -> str:
    return run.split("/runs/")[0] if "/runs/" in run else run.rsplit("/", 1)[0]


def main() -> None:
    rows = list(csv.DictReader(open(HERE / "native_sign_runs.csv")))
    groups = defaultdict(list)
    for r in rows:
        c = campaign(r["run"])
        if "_advisor_pack" in c or c.startswith("prototypes/") or "fixture" in c or int(r.get("Nmcmc_1e4") or 0) < 100:
            continue
        groups[c].append(float(r["sign_re"]))
    out = {"campaigns": {}}
    allv = []
    for c, v in sorted(groups.items()):
        se = statistics.stdev(v) / math.sqrt(len(v)) if len(v) > 1 else float("nan")
        out["campaigns"][c] = {"chains": len(v), "mean_sign": statistics.fmean(v), "stderr": se}
        allv += v
    s = statistics.fmean(allv)
    out["pooled"] = {"chains": len(allv), "mean_sign": s,
                     "stderr": statistics.stdev(allv) / math.sqrt(len(allv))}
    # Ceiling: a grouped measure that removed every cancellation would reach
    # <s>_B = 1; the ratio-estimator variance scales as 1/<s>^2.
    out["variance_ceiling_perfect_grouping"] = 1.0 / s ** 2
    # Toy transfer: fraction of the sign deficit (1 - <s>) recovered by
    # 4-vertex tiled groups in the signed toy regimes (evidence/*.json).
    toy = {}
    for name in ("R1_signed_interband", "R2_signed_mixed"):
        e = json.load(open(HERE.parent / "evidence" / f"{name}.json"))
        toy[name] = (e["sign_B"] - e["sign_A"]) / (1.0 - e["sign_A"])
    out["toy_deficit_recovered"] = toy
    best = max(toy.values())
    sB = s + best * (1.0 - s)
    out["lif_projection_best_toy_transfer"] = {"sign_A": s, "sign_B": sB,
                                               "variance_gain": (sB / s) ** 2}
    json.dump(out, open(HERE / "lif_sign_summary.json", "w"), indent=2)
    json.dump(out, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
