"""Add the grouped-measure chain (bchain.f90) to a tree already prepared by
patches/base.py. Hooks go only into diagmc_EZ_matrix, each asserted once:
around update_drive (second-stage correction, mode refresh) and around
measure_EZ_wfn (grouped estimator). Inert unless FUTUREB_BCHAIN=1.

Usage: python -m future_b.fepdmc.patches.bchain <perturbo-fep-dmc dir>
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"


def once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"anchor for {label!r} found {n} times")
    return text.replace(old, new)


def main(root: str) -> None:
    src = Path(root) / "pert-src"
    shutil.copy(DATA / "bchain.f90", src / "bchain.f90")
    p = src / "diagMC_gt.f90"
    t = p.read_text()
    start = t.index("subroutine diagmc_EZ_matrix()")
    end = t.index("end subroutine", start)
    body = t[start:end]
    body = once(body, "   use multiphonon_update_matrix, only : update_drive\n",
                "   use multiphonon_update_matrix, only : update_drive\n"
                "   use bchain_mod, only : bchain_pre_update, bchain_post_update, "
                "bchain_pre_measure, bchain_post_measure\n", "EZ use")
    body = once(body, "         call update_drive(diagrams(i_omp),stat(i_omp),update)\n",
                "         call bchain_pre_update(diagrams(i_omp), stat(i_omp))\n"
                "         call update_drive(diagrams(i_omp),stat(i_omp),update)\n"
                "         call bchain_post_update(diagrams(i_omp), stat(i_omp))\n", "EZ update hooks")
    body = once(body, "            call measure_EZ_wfn(diagrams(i_omp),workspaces(i_omp),stat(i_omp))\n",
                "            call bchain_pre_measure(stat(i_omp))\n"
                "            call measure_EZ_wfn(diagrams(i_omp),workspaces(i_omp),stat(i_omp))\n"
                "            call bchain_post_measure(diagrams(i_omp), stat(i_omp))\n", "EZ measure hooks")
    p.write_text(t[:start] + body + t[end:])
    p = src / "makefile"
    p.write_text(once(p.read_text(), "rb_window.f90 \n", "rb_window.f90 \\\nbchain.f90 \n", "makefile bchain"))
    print("bchain hooks added to", root)


if __name__ == "__main__":
    main(sys.argv[1])
