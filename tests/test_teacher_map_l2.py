# SIGNED FORMULA: H=2t*n-t*sum_PBC(c^dag c+h.c.)+Omega*b^dag*b+g*n*(b+b^dag), xi_k=2t*(1-cos k).
from __future__ import annotations

import csv
from pathlib import Path

import pytest

from prototypes.future_b_neural_poc.build_teacher_map_l2 import (
    ACCEPTED_STRONG_CORNER,
    CSV_HEADER,
    HEADER_FIELDS,
    NOT_COMPUTED,
    compute_cell,
    g0_ground_energy,
)

CSV_PATH = Path("prototypes/future_b_neural_poc/teacher_map_l2.csv")


def test_g0_sanity_is_zero_at_code_origin() -> None:
    assert g0_ground_energy() == pytest.approx(0.0, abs=1.0e-12)


FROZEN_E0_ED = {
    (0.15, 0.5): -0.025011195833357803,
    (0.15, 0.8): -0.016411995814594443,
    (0.15, 2.0): -0.0075011729011287805,
    (0.45, 0.5): -0.22597056572509017,
    (0.45, 0.8): -0.14813779739257232,
    (0.45, 2.0): -0.06759567149368771,
    (0.75, 0.5): -0.6337558805587407,
    (0.75, 0.8): -0.4141522353421741,
    (0.75, 2.0): -0.18824875576961658,
    (1.05, 0.5): -1.2711554105515426,
    (1.05, 0.8): -0.821257338852671,
    (1.05, 2.0): -0.3704389369409427,
}


def test_weak_cell_cutoff_and_dimension() -> None:
    row = compute_cell(0.15, 2.0)
    assert row.M_used % 2 == 0
    assert row.dim == (row.M_used + 1) * (row.M_used + 2)
    assert row.DeltaE_cutoff < 1.0e-4
    assert row.E0_Born != NOT_COMPUTED
    assert row.E0_SCBA != NOT_COMPUTED
    float(row.E0_Born)
    float(row.E0_SCBA)
    assert row.E0_Born_VC == NOT_COMPUTED
    assert row.label == "weak"


def test_strong_corner_matches_accepted_e0() -> None:
    row = compute_cell(1.05, 0.5)
    assert row.M_used == ACCEPTED_STRONG_CORNER["M_used"]
    assert row.E0_ED == ACCEPTED_STRONG_CORNER["E0_ED"]
    assert row.DeltaE_cutoff == pytest.approx(ACCEPTED_STRONG_CORNER["DeltaE_cutoff"], rel=0.0, abs=0.0)
    assert row.matched_accepted_E0 is True


def test_written_csv_has_twelve_real_e0_ed() -> None:
    assert CSV_PATH.is_file()
    text = CSV_PATH.read_text()
    assert text.splitlines()[0] == CSV_HEADER
    with CSV_PATH.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert list(rows[0].keys()) == list(HEADER_FIELDS)
    assert len(rows) == 12
    for row in rows:
        e0 = float(row["E0_ED"])
        assert np_isfinite(e0)
        m_used = int(row["M_used"])
        assert m_used % 2 == 0
        assert int(row["dim"]) == (m_used + 1) * (m_used + 2)
        assert float(row["DeltaE_cutoff"]) < 1.0e-4
        g_over_t = float(row["g_over_t"])
        omega_over_t = float(row["omega_over_t"])
        assert e0 == FROZEN_E0_ED[(g_over_t, omega_over_t)]
        assert row["E0_Born"] != NOT_COMPUTED
        assert row["E0_SCBA"] != NOT_COMPUTED
        assert np_isfinite(float(row["E0_Born"]))
        assert np_isfinite(float(row["E0_SCBA"]))
        assert row["E0_Born_VC"] == NOT_COMPUTED


def np_isfinite(value: float) -> bool:
    return value == value and value not in (float("inf"), float("-inf"))
