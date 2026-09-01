# SIGNED FORMULA: H=2t*n-t*sum_PBC(c^dag c+h.c.)+Omega*b^dag*b+g*n*(b+b^dag), xi_k=2t*(1-cos k).
from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from keldysh4ai.future_b.teacher.holstein_ed import (
    HolsteinL2ED,
    code_dispersion,
    cutoff_scan,
    first_converged_cutoff,
    periodic_l2_electronic_hamiltonian,
    write_cutoff_table,
)


def test_code_origin_and_periodic_l2_double_link() -> None:
    xi = code_dispersion([0.0, np.pi])
    np.testing.assert_allclose(xi, [0.0, 4.0], rtol=0.0, atol=1.0e-14)
    electronic = periodic_l2_electronic_hamiltonian()
    np.testing.assert_allclose(electronic, [[2.0, -2.0], [-2.0, 2.0]])
    np.testing.assert_allclose(np.linalg.eigvalsh(electronic), [0.0, 4.0], atol=1.0e-14)


def test_total_cutoff_dimension_hermiticity_and_plus_g_matrix_element() -> None:
    model = HolsteinL2ED(t=1.0, g=0.7, omega0=0.8, total_cutoff=3)
    assert model.dimension == 20
    np.testing.assert_allclose(model.hamiltonian, model.hamiltonian.T, rtol=0.0, atol=0.0)
    g0 = HolsteinL2ED(t=1.0, g=0.0, omega0=0.8, total_cutoff=3)
    np.testing.assert_allclose(np.diag(model.hamiltonian), np.diag(g0.hamiltonian))
    assert model.hamiltonian[
        model.index_of(0, (0, 0)), model.index_of(0, (1, 0))
    ] == pytest.approx(+0.7)
    assert model.hamiltonian[
        model.index_of(0, (1, 0)), model.index_of(0, (2, 0))
    ] == pytest.approx(+0.7 * np.sqrt(2.0))


@pytest.mark.parametrize("omega0", [0.5, 0.8, 2.0])
@pytest.mark.parametrize("total_cutoff", [0, 4, 20])
def test_g_zero_ground_energy_is_zero(omega0: float, total_cutoff: int) -> None:
    model = HolsteinL2ED(t=1.0, g=0.0, omega0=omega0, total_cutoff=total_cutoff)
    assert model.ground_energy() == pytest.approx(0.0, abs=1.0e-12)


def test_strong_corner_converges_by_m20_and_checks_m_plus_two_spectra() -> None:
    rows = cutoff_scan()
    energies = np.asarray([row.E0 for row in rows])
    assert np.all(np.diff(energies) <= 1.0e-12)
    converged = first_converged_cutoff(rows)
    assert converged is not None and converged + 2 <= 20

    omega = np.linspace(-4.0, 8.0, 241)
    for total_cutoff in (converged, converged + 2):
        model = HolsteinL2ED(t=1.0, g=1.05, omega0=0.5, total_cutoff=total_cutoff)
        for k in (0.0, float(np.pi)):
            result = model.lehmann_spectrum(k=k, omega=omega, eta=0.05)
            assert float(np.sum(result.weights)) == pytest.approx(1.0, abs=1.0e-12)
            assert np.all(np.isfinite(result.green))
            assert np.all(np.isfinite(result.spectral))
            assert float(np.min(result.spectral)) >= -1.0e-13


def test_cutoff_csv_is_numeric_and_not_a_teacher_claim(tmp_path: Path) -> None:
    path = tmp_path / "ed_cutoff_table.csv"
    rows = write_cutoff_table(path)
    assert path.read_text().splitlines()[0] == (
        "L,t,g,omega0,cutoff_kind,M,dimension,E0,"
        "delta_E0_vs_M_minus_2,passes_1e_minus_4"
    )
    assert len(rows) == 11
    assert first_converged_cutoff(rows) is not None
    assert "TEACHER_COVERAGE_ESTABLISHED" not in path.read_text()
