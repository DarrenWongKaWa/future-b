"""Source patches for a pristine FEP-DMC tree (upstream pin in future_b.fepdmc.FEP_DMC_PIN).

Each module exposes ``main(root)`` and asserts every anchor it edits exactly once,
so a patch either applies cleanly to the pinned tree or refuses.

  base      gfortran portability, MKL VSL shim, measurement hooks, FUTUREB_SEED
  bchain    Future B moves and diagnostics (bchain.f90; inert unless switched on)
  wqfix     fix: stale phonon frequency in add_external_ph   (FUTUREB_WQFIX=1)
  extfix    fix: reverse-proposal support in remove_external_ph (FUTUREB_EXTFIX=1)
  extrmfix  fix: reference trace in remove_external_ph       (FUTUREB_EXTRMFIX=1)

The three fixes are opt-in at run time: without the switch the code path is the
upstream one.
"""

from __future__ import annotations

from importlib import import_module

ORDER = ("base", "bchain", "wqfix", "extfix", "extrmfix")

PROFILES = {
    "fixes": ("base", "wqfix", "extfix", "extrmfix"),
    "research": ORDER,
}


def apply(root, name: str) -> None:
    """Apply one named patch to the perturbo-fep-dmc directory ``root``."""
    if name not in ORDER:
        raise ValueError(f"unknown patch {name!r}; expected one of {ORDER}")
    import_module(f"{__name__}.{name}").main(str(root))
