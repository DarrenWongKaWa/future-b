"""FEP-DMC toolkit: native bug fixes, exact Monte Carlo moves and low-sign estimators.

Works on an upstream FEP-DMC checkout at ``FEP_DMC_PIN`` (Luo-Bernardi). It does not
ship FEP-DMC itself; patches are applied to a user-provided tree and built in the
user's QE 6.5 toolchain.

  prepare    one-step patching of a pristine tree (profiles "fixes", "research")
  patches    the individual patches; the three native fixes are opt-in at run time
             (FUTUREB_WQFIX, FUTUREB_EXTFIX, FUTUREB_EXTRMFIX)
  runner     Docker driver for diagmc-EZ chains with the Future B switches
  pooled     pooled ratio estimator over chains, variance ratio and efficiency
  validate   end-to-end exactness check: independent kernels must agree
  analysis   research analyses behind research/r1_grouped (python -m ...)

Command line: ``future-b-fepdmc {prepare,run,compare,validate}``.
Documentation: docs/FEP_DMC_TOOLKIT.md.
"""

from __future__ import annotations

FEP_DMC_PIN = "05d08449cffdbd0dfbbbf5009add5cc887bc754b"

from .pooled import side as pooled_side  # noqa: E402
from .prepare import check_pin, prepare_tree  # noqa: E402

__all__ = ["FEP_DMC_PIN", "check_pin", "prepare_tree", "pooled_side"]
