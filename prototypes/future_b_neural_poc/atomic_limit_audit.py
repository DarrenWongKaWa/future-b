"""t=0 / hop=0 atomic-limit audit of Library-I Born, Born+VC, and Library-II SCBA.

Does not call ``crossing_block_poc.PeriodicHolsteinModel`` (that API forces
``t>0`` and ``n_k>=4``). Momenta collapse: ``G0=1/z`` at the code origin.
Tadpole/Hartree remains off. Default remains: do not add Sigma_VC onto SCBA.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from keldysh4ai.future_b_atomic import exact_t0_linear_cfe, relative_l2, scba_constant_cfe

T = 1.0  # energy unit only; hopping is absent
G_OVER_T = (0.15, 0.45, 0.75, 1.05)
OMEGA_OVER_T = (0.5, 0.8, 2.0)
CFE_DEPTH = 64
NU = np.geomspace(0.1, 20.0, 128)
Z = 1.0j * NU
DEFAULT_JSON = Path(__file__).resolve().parent / "atomic_limit_audit.json"

# Declared before looking at residuals.
METRIC = (
    "relative L2 of G(z) versus exact_t0_linear_cfe on z=i*nu, "
    "nu=geomspace(0.1,20,128), CFE depth 64"
)
VERDICT_RULE = (
    "B_VC moves toward exact atomic series iff "
    "relL2(G_Born_VC, G_exact) < relL2(G_Born, G_exact) "
    "on every frozen (g, Omega) cell at hop=0; "
    "the opposite strict inequality on every cell is "
    "'B_VC does not move toward exact atomic series'; "
    "otherwise inconclusive"
)


def g0(z: np.ndarray) -> np.ndarray:
    return 1.0 / z


def sigma_born(z: np.ndarray, g: float, omega0: float) -> np.ndarray:
    """One-shot T=0 Born on G0: Sigma = g^2 G0(z-Omega)."""

    return (g * g) * g0(z - omega0)


def sigma_vc(z: np.ndarray, g: float, omega0: float) -> np.ndarray:
    """Bare App01 crossing block after t=0 collapse: g^4 G0(z-Omega)^2 G0(z-2Omega)."""

    one = g0(z - omega0)
    two = g0(z - 2.0 * omega0)
    return (g ** 4) * (one * one) * two


def green_from_sigma(z: np.ndarray, sigma: np.ndarray) -> np.ndarray:
    return 1.0 / (z - sigma)


def g4_series_coefficients() -> dict[str, float]:
    """O(g^4) coefficient of Sigma in units of 1/((z-Omega)^2 (z-2Omega)).

    SOURCE_DERIVED from the T=0 CFE expansions (constant 1,1,1,... versus
    exact linear 1,2,3,...) together with the collapsed App01 kernel.
    """

    return {
        "born_one_shot": 0.0,
        "born_plus_vc_on_G0": 1.0,
        "scba_constant_cfe": 1.0,
        "exact_t0_linear_cfe": 2.0,
    }


def evaluate_cell(g: float, omega0: float) -> dict[str, float | str]:
    born = sigma_born(Z, g, omega0)
    vc = sigma_vc(Z, g, omega0)
    g_born = green_from_sigma(Z, born)
    g_bvc = green_from_sigma(Z, born + vc)
    g_scba = np.asarray(scba_constant_cfe(Z, g, omega0, CFE_DEPTH), dtype=np.complex128)
    g_exact = np.asarray(exact_t0_linear_cfe(Z, g, omega0, CFE_DEPTH), dtype=np.complex128)
    d_born_exact = relative_l2(g_born, g_exact)
    d_bvc_exact = relative_l2(g_bvc, g_exact)
    d_scba_exact = relative_l2(g_scba, g_exact)
    d_born_scba = relative_l2(g_born, g_scba)
    d_bvc_scba = relative_l2(g_bvc, g_scba)
    moved = bool(d_bvc_exact < d_born_exact)
    return {
        "g": g,
        "omega0": omega0,
        "relL2_Born_vs_exact": d_born_exact,
        "relL2_Born_VC_vs_exact": d_bvc_exact,
        "relL2_SCBA_vs_exact": d_scba_exact,
        "relL2_Born_vs_SCBA": d_born_scba,
        "relL2_Born_VC_vs_SCBA": d_bvc_scba,
        "B_VC_closer_to_exact_than_Born": moved,
        "B_VC_closer_to_SCBA_than_Born": bool(d_bvc_scba < d_born_scba),
    }


def verdict_from_cells(cells: list[dict[str, float | str]]) -> str:
    flags = [bool(cell["B_VC_closer_to_exact_than_Born"]) for cell in cells]
    if all(flags):
        return "B_VC moves toward exact atomic series"
    if not any(flags):
        return "B_VC does not move toward exact atomic series"
    return "inconclusive"


def run_audit() -> dict:
    cells = [evaluate_cell(g, omega0) for g in G_OVER_T for omega0 in OMEGA_OVER_T]
    payload = {
        "hopping": 0.0,
        "geometry": "N=1 atomic / momenta collapsed",
        "G0": "1/z (code origin)",
        "tadpole": "OFF",
        "metric": METRIC,
        "verdict_rule": VERDICT_RULE,
        "g4_series_coefficients": g4_series_coefficients(),
        "cfe_depth": CFE_DEPTH,
        "nu": {"min": float(NU[0]), "max": float(NU[-1]), "n": int(NU.size), "spacing": "geometric"},
        "cells": cells,
        "verdict": verdict_from_cells(cells),
        "default_on_SCBA": "do not add Sigma_VC onto SCBA",
        "libraries": "Library I = bare Born + bare VC on G0; Library II = SCBA on dressed G; not mixed",
    }
    return payload


def main() -> None:
    payload = run_audit()
    DEFAULT_JSON.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {DEFAULT_JSON}")
    print(f"verdict={payload['verdict']}")
    print(f"g4_coeffs={payload['g4_series_coefficients']}")
    for cell in payload["cells"]:
        print(
            f"g={cell['g']} Omega={cell['omega0']} "
            f"Born_vs_exact={cell['relL2_Born_vs_exact']:.6e} "
            f"BVC_vs_exact={cell['relL2_Born_VC_vs_exact']:.6e} "
            f"SCBA_vs_exact={cell['relL2_SCBA_vs_exact']:.6e} "
            f"moved={cell['B_VC_closer_to_exact_than_Born']}"
        )


if __name__ == "__main__":
    main()
