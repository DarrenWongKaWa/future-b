#!/usr/bin/env python3
"""Prepare a pristine FEP-DMC tree (pin in evidence/FEP_DMC_PIN) in one step.

Copies make.sys (gfortran/OpenMP/HDF5 flags for the QE 6.5 build; skip with
--keep-make-sys), then applies, in order, each patch asserting its anchors once:
  1. patch_fepdmc.py   gfortran portability, MKL VSL shim, measurement hooks,
                       FUTUREB_SEED (required for the gfortran/QE 6.5 build)
  2. patch_bchain.py   Future B moves and diagnostics (bchain.f90; all inert
                       unless their FUTUREB_* switch is set)
  3. patch_wqfix.py    fix: add_external_ph stale phonon frequency (FUTUREB_WQFIX)
  4. patch_extfix.py   fix: remove_external_ph reverse-proposal support (FUTUREB_EXTFIX)
  5. patch_extrmfix.py fix: remove_external_ph reference trace (FUTUREB_EXTRMFIX)

Every native fix is opt-in at run time: without its switch the code path is
unchanged, so one binary serves both the upstream and the corrected target.

Usage:
  prepare_fepdmc.py <perturbo-fep-dmc dir> [--profile fixes|research] [--dry-run]

Profiles: "fixes" applies 1, 3, 4, 5 (native with the bug fixes available);
"research" (default) applies all five.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

STEPS = {
    "fixes": ["patch_fepdmc.py", "patch_wqfix.py", "patch_extfix.py", "patch_extrmfix.py"],
    "research": ["patch_fepdmc.py", "patch_bchain.py", "patch_wqfix.py", "patch_extfix.py", "patch_extrmfix.py"],
}


def check_pin(root: Path) -> str:
    """Return a note on the tree's git revision against evidence/FEP_DMC_PIN."""
    pin = (HERE / "evidence" / "FEP_DMC_PIN").read_text().split()[0]
    try:
        rev = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True,
                             text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return f"not a git checkout; expected pin {pin}"
    return "pin ok" if rev == pin else f"WARNING: tree at {rev}, expected pin {pin}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", type=Path, help="perturbo-fep-dmc directory (contains pert-src/)")
    ap.add_argument("--profile", choices=sorted(STEPS), default="research")
    ap.add_argument("--dry-run", action="store_true", help="list the steps without applying them")
    ap.add_argument("--keep-make-sys", action="store_true", help="do not replace the tree's make.sys")
    a = ap.parse_args()
    if not (a.root / "pert-src").is_dir():
        print(f"{a.root}: no pert-src/ directory", file=sys.stderr)
        return 2
    print(check_pin(a.root))
    if not a.keep_make_sys:
        print("+ make.sys ->", a.root / "make.sys")
        if not a.dry_run:
            shutil.copy(HERE / "make.sys", a.root / "make.sys")
    for step in STEPS[a.profile]:
        args = [sys.executable, str(HERE / step), str(a.root)]
        if step == "patch_fepdmc.py":
            args.append(str(HERE / "mkl_vsl.f90"))
        print("+", " ".join(Path(x).name if i else x for i, x in enumerate(args)))
        if not a.dry_run:
            r = subprocess.run(args)
            if r.returncode:
                print(f"{step} failed (exit {r.returncode}); tree left partially patched", file=sys.stderr)
                return r.returncode
    if not a.dry_run:
        print(f"done ({a.profile}). Build with make.sys (QE 6.5, gfortran; see README.md).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
