# SIGNED FORMULA: xi_k=2t*(1-cos k), L=2 k in {0, pi}, tadpole OFF.
from __future__ import annotations

import ast
from pathlib import Path

import numpy as np
import pytest

from prototypes.future_b_neural_poc.l2_periodic_pole import (
    ETA,
    K_POINTS,
    NOT_COMPUTED,
    SCBA_DEPTH,
    born_sigma,
    e0_born,
    e0_scba,
    g0_poles,
    l2_dispersion,
    rainbow_sigma,
    xi_k,
)

EXTRACTOR = Path("prototypes/future_b_neural_poc/l2_periodic_pole.py")
BUILDER = Path("prototypes/future_b_neural_poc/build_teacher_map_l2.py")
DEFINITION = Path("notes/L2_POLE_DEFINITION.md")


def test_definition_file_froze_eta_and_window_before_use() -> None:
    text = DEFINITION.read_text()
    assert "10^{-4}" in text or "10^{-4}t" in text
    assert "[-8.0, 0.25]" in text
    assert "NOT_COMPUTED" in text
    assert "chain_scba" in text
    assert "Week 2" in text


def _imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text())
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return names


def test_extractor_source_does_not_import_wrong_geometry() -> None:
    banned = ("chain_scba", "crossing_block", "crossing_block_poc")
    for path in (EXTRACTOR, BUILDER):
        imported = _imported_modules(path)
        joined = " ".join(imported)
        for name in banned:
            assert name not in joined
        assert "l2_periodic_pole" in EXTRACTOR.name


def test_l2_momenta_and_signed_dispersion() -> None:
    assert K_POINTS == (0.0, float(np.pi))
    xi = l2_dispersion(t=1.0)
    np.testing.assert_allclose(xi, [0.0, 4.0], rtol=0.0, atol=1.0e-15)
    np.testing.assert_allclose(xi_k(np.asarray(K_POINTS)), xi)


def test_g0_poles_sit_at_code_origin() -> None:
    born, scba = g0_poles(omega0=0.8)
    assert born.E0 == pytest.approx(0.0, abs=1.0e-12)
    assert scba.E0 == pytest.approx(0.0, abs=1.0e-12)
    assert born.depth == 0
    assert scba.depth == SCBA_DEPTH
    assert born.eta == ETA


def test_born_is_one_shot_g0_and_tadpole_free() -> None:
    z = np.array([0.2 + 1.0e-4j, -1.0 + 1.0e-4j], dtype=np.complex128)
    g = 0.45
    omega0 = 0.8
    direct = born_sigma(z, g=g, omega0=omega0)
    g0_sum = 1.0 / (z - omega0 - 0.0) + 1.0 / (z - omega0 - 4.0)
    np.testing.assert_allclose(direct, (g * g / 2.0) * g0_sum)
    np.testing.assert_allclose(direct, rainbow_sigma(z, g=g, omega0=omega0, depth=0))


def test_t0_kernel_collapses_to_atomic_born() -> None:
    z = 0.3 + 0.4j
    g = 0.45
    omega0 = 0.8
    collapsed = rainbow_sigma(z, g=g, omega0=omega0, t=0.0, depth=0)
    np.testing.assert_allclose(collapsed, np.array(g**2 / (z - omega0)))


def test_born_pole_matches_eta_zero_cubic_within_eta() -> None:
    g = 0.15
    omega0 = 0.5
    t = 1.0
    coeffs = [
        1.0,
        -(2.0 * omega0 + 4.0 * t),
        omega0 * (omega0 + 4.0 * t) - g * g,
        g * g * (omega0 + 2.0 * t),
    ]
    roots = np.roots(coeffs)
    real_roots = [float(r.real) for r in roots if abs(r.imag) < 1.0e-8]
    assert real_roots
    cubic_e0 = min(real_roots)
    extracted = e0_born(g=g, omega0=omega0)
    assert extracted.E0 is not None
    assert extracted.E0 == pytest.approx(cubic_e0, abs=10.0 * ETA)
    assert extracted.csv_value != NOT_COMPUTED
