"""Prepare a pristine FEP-DMC tree at the upstream pin in one step.

The ``base`` patch installs make.sys (gfortran/OpenMP/HDF5 flags for the QE 6.5
build) and the build hooks; the other patches follow in the order of
``future_b.fepdmc.patches.ORDER``, each asserting its anchors exactly once.

Profiles:
  fixes     base + the three opt-in native fixes (wqfix, extfix, extrmfix)
  research  fixes + the Future B moves and diagnostics (bchain), the default

Usage:
  future-b-fepdmc prepare <perturbo-fep-dmc dir> [--profile fixes|research] [--dry-run]
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from . import FEP_DMC_PIN
from .patches import PROFILES, apply


def check_pin(root: Path) -> str:
    """Return a note on the tree's git revision against the upstream pin."""
    try:
        rev = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True,
                             text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return f"not a git checkout; expected pin {FEP_DMC_PIN}"
    return "pin ok" if rev == FEP_DMC_PIN else f"WARNING: tree at {rev}, expected pin {FEP_DMC_PIN}"


def prepare_tree(root: Path, profile: str = "research", dry_run: bool = False) -> list[str]:
    """Apply the patches of ``profile`` to ``root``; return the patch names applied."""
    root = Path(root)
    if not (root / "pert-src").is_dir():
        raise FileNotFoundError(f"{root}: no pert-src/ directory")
    if profile not in PROFILES:
        raise ValueError(f"unknown profile {profile!r}; expected one of {sorted(PROFILES)}")
    steps = list(PROFILES[profile])
    if not dry_run:
        for name in steps:
            apply(root, name)
    return steps


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="future-b-fepdmc prepare", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", type=Path, help="perturbo-fep-dmc directory (contains pert-src/)")
    ap.add_argument("--profile", choices=sorted(PROFILES), default="research")
    ap.add_argument("--dry-run", action="store_true", help="list the steps without applying them")
    a = ap.parse_args(argv)
    if not (a.root / "pert-src").is_dir():
        print(f"{a.root}: no pert-src/ directory", file=sys.stderr)
        return 2
    print(check_pin(a.root))
    try:
        steps = prepare_tree(a.root, a.profile, a.dry_run)
    except SystemExit as exc:  # a patch refused an anchor
        print(f"patch failed: {exc}; tree left partially patched", file=sys.stderr)
        return 1
    for name in steps:
        print(("would apply " if a.dry_run else "applied ") + name)
    if not a.dry_run:
        print(f"done ({a.profile}). Build pert-src with make inside the QE 6.5 tree.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
