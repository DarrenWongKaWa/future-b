"""Future B public Python surface.

This package is the closed-project analysis layer: delayed-acceptance algebra,
formation-energy postprocessing, and frozen-benchmark statistics.

It does not replace the native Perturbo/FEP-DMC consumer.
"""

from .formation_energy import E_BARE_LIF_METHOD0, formation_energy_eV
from .p1_da import delayed_acceptance_prob, native_re_ratio

__version__ = "1.2.0"

__all__ = [
    "E_BARE_LIF_METHOD0",
    "formation_energy_eV",
    "delayed_acceptance_prob",
    "native_re_ratio",
]
