from __future__ import annotations

import numpy as np

from prototypes.future_b_neural_poc.atomic_limit_audit import (
    Z,
    g0,
    g4_series_coefficients,
    run_audit,
    sigma_born,
    sigma_vc,
    verdict_from_cells,
)


def test_g0_is_code_origin_and_tadpole_free_born() -> None:
    z = np.array([0.3 + 0.4j, 1.0j, 2.0 + 1.5j])
    np.testing.assert_allclose(g0(z), 1.0 / z)
    g = 0.45
    omega0 = 0.8
    born = sigma_born(z, g, omega0)
    vc = sigma_vc(z, g, omega0)
    np.testing.assert_allclose(born, g**2 / (z - omega0))
    np.testing.assert_allclose(vc, g**4 / ((z - omega0) ** 2 * (z - 2.0 * omega0)))
    assert np.allclose(Z.real, 0.0)


def test_g4_coefficients_place_vc_between_born_and_exact() -> None:
    coeffs = g4_series_coefficients()
    assert coeffs["born_one_shot"] == 0.0
    assert coeffs["born_plus_vc_on_G0"] == 1.0
    assert coeffs["scba_constant_cfe"] == 1.0
    assert coeffs["exact_t0_linear_cfe"] == 2.0


def test_verdict_tokens_and_mixed_cells_are_inconclusive() -> None:
    assert verdict_from_cells(
        [{"B_VC_closer_to_exact_than_Born": True}, {"B_VC_closer_to_exact_than_Born": True}]
    ) == "B_VC moves toward exact atomic series"
    assert verdict_from_cells(
        [{"B_VC_closer_to_exact_than_Born": False}, {"B_VC_closer_to_exact_than_Born": False}]
    ) == "B_VC does not move toward exact atomic series"
    assert verdict_from_cells(
        [{"B_VC_closer_to_exact_than_Born": True}, {"B_VC_closer_to_exact_than_Born": False}]
    ) == "inconclusive"


def test_hop_zero_audit_does_not_use_periodic_poc_model() -> None:
    import prototypes.future_b_neural_poc.atomic_limit_audit as module

    assert not hasattr(module, "PeriodicHolsteinModel")
    payload = run_audit()
    assert payload["hopping"] == 0.0
    assert payload["verdict"] in {
        "B_VC moves toward exact atomic series",
        "B_VC does not move toward exact atomic series",
        "inconclusive",
    }
    assert payload["default_on_SCBA"] == "do not add Sigma_VC onto SCBA"
    assert len(payload["cells"]) == 12
