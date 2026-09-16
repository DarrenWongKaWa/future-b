#!/usr/bin/env python3
"""Recompute published Q summaries from frozen JSON (no HDF5, no perturbo.x)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from future_b.formation_energy import E_BARE_LIF_METHOD0, formation_energy_eV  # noqa: E402
from future_b.stats import classify_p1_wall_ratio  # noqa: E402


def main() -> int:
    c5 = json.loads((ROOT / "benchmarks/c5_dev/frozen_results.json").read_text())
    p1 = json.loads((ROOT / "benchmarks/p1_vs_bbest/frozen_results.json").read_text())
    print("E_bare =", E_BARE_LIF_METHOD0)
    print("C5 DEV formation energies (fixed setting, not 1% GS):")
    for name, arm in c5["arms"].items():
        q = formation_energy_eV(arm["ratio_eV"])
        assert abs(q - arm["Q_eV"]) < 1e-12
        print(
            f"  {name:6s}  Q={arm['Q_eV']:+.9f} eV  "
            f"relSE={100*arm['relative_JK_SE']:.3f}%  "
            f"relHW={100*arm['relative_point_95_halfwidth']:.3f}%"
        )
    cls = classify_p1_wall_ratio(p1["T_boot_2.5"], p1["T_boot_97.5"], p1["hac_ok"])
    print(
        "clean P1 / B-best T ratio "
        f"{p1['T_ratio_point']:.4f}  [{p1['T_boot_2.5']:.4f}, {p1['T_boot_97.5']:.4f}]  "
        f"class={cls}"
    )
    assert cls == "P1_UNRESOLVED_WITHIN_BUDGET"
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
