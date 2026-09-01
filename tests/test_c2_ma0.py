# SIGNED FORMULA: xi_k=2t*(1-cos k), L=2 k in {0, pi}, tadpole OFF.
"""Candidate 2 MA(0) pins. No learned gate. No VC mix."""

from __future__ import annotations

import ast
import csv
from pathlib import Path

import numpy as np
import pytest

from prototypes.future_b_neural_poc.build_week2_table import ACCEPTED_E0
from prototypes.future_b_neural_poc.ma0_l2 import (
    CSV_HEADER,
    DEFAULT_CSV,
    FORBIDDEN_COLUMNS,
    FORMULA_PATH,
    HEADER_FIELDS,
    MA0_DEPTH,
    PREREGISTER_PATH,
    REPORT_PATH,
    STOP_PATH,
    STRONG_CELL,
    TEACHER_CSV,
    band_of,
    coupling_lambda,
    evaluate_tests,
    g0_pole,
    gbar0,
    lambda_if_block,
    load_teacher_map,
    ma0_atomic_verdict,
    ma0_green,
    ma0_sigma,
)
from prototypes.future_b_neural_poc.l2_periodic_pole import ETA, SCBA_DEPTH, born_sigma

SOURCE = Path("prototypes/future_b_neural_poc/ma0_l2.py")


def _imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text())
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return names


def test_preregister_exists_and_has_no_t1_pass() -> None:
    assert PREREGISTER_PATH.is_file()
    text = PREREGISTER_PATH.read_text()
    compact = " ".join(text.split())
    assert "T1 PASS" not in text
    assert "T1 FAIL" not in text
    assert "C2-T1" in text
    assert "rules only" in text.lower()
    assert "if λ < 0.08" in text or "if λ < 0.08" in compact or "λ < 0.08" in text
    assert "MA0" in text
    assert "SCBA" in text
    assert "0.80" in text
    assert "do not train" in text.lower() or "Do **not** train" in text
    assert "paper1_go" not in text.lower() or "setting `paper1_go` true" in text


def test_formula_quotes_ma0_equation() -> None:
    assert FORMULA_PATH.is_file()
    text = FORMULA_PATH.read_text()
    assert "Eqs. (10)–(12)" in text or "Eqs. (10)-(12)" in text
    assert "Eq. (11)" in text or "their Eq. (11)" in text
    assert "165109" in text
    assert "245104" in text
    assert "chain_scba" in text
    assert "infinite-chain" in text or "N\\to\\infty" in text or r"N\to\infty" in text


def test_source_does_not_import_banned_or_mix_vc() -> None:
    imported = _imported_modules(SOURCE)
    joined = " ".join(imported)
    for name in ("chain_scba", "crossing_block", "crossing_block_poc", "holstein_ed"):
        assert name not in joined
    assert "sklearn" not in joined
    assert "torch" not in joined
    source_text = SOURCE.read_text()
    assert "Sigma_VC" not in source_text
    assert "sigma_vc" not in source_text
    assert "MA0_DEPTH" in source_text
    assert MA0_DEPTH == SCBA_DEPTH == 64


def test_g0_pole_sits_at_code_origin() -> None:
    pole = g0_pole(omega0=0.8)
    assert pole.E0 == pytest.approx(0.0, abs=1.0e-12)
    assert pole.kind == "ma0"
    assert pole.eta == ETA
    z = np.array([0.2 + 1.0e-4j, -1.0 + 1.0e-4j], dtype=np.complex128)
    np.testing.assert_allclose(ma0_sigma(z, g=0.0, omega0=0.8), 0.0)


def test_gbar0_is_l2_two_point_average() -> None:
    z = 0.3 + 0.4j
    got = gbar0(z, t=1.0)
    want = 0.5 * (1.0 / z + 1.0 / (z - 4.0))
    np.testing.assert_allclose(got, np.array(want))
    collapsed = gbar0(z, t=0.0)
    np.testing.assert_allclose(collapsed, np.array(1.0 / z))


def test_ma0_first_order_matches_l2_born() -> None:
    z = np.array([0.2 + 1.0e-4j, -1.0 + 1.0e-4j], dtype=np.complex128)
    g = 0.45
    omega0 = 0.8
    first = (g * g) * gbar0(z - omega0, t=1.0)
    np.testing.assert_allclose(first, born_sigma(z, g=g, omega0=omega0))
    full = ma0_sigma(z, g=g, omega0=omega0)
    assert np.all(np.isfinite(full))
    assert not np.allclose(full, first)


def test_ma0_atomic_moves_toward_linear_cfe() -> None:
    verdict = ma0_atomic_verdict()
    assert verdict["hopping"] == 0.0
    assert verdict["n_cells"] == 12
    assert verdict["MA0_ATOMIC"] == "PASS"
    assert verdict["n_toward_linear"] == 12
    z = ATOMIC_SAMPLE = 0.4j
    g = 0.45
    omega0 = 0.8
    g_ma0 = ma0_green(ATOMIC_SAMPLE, g=g, omega0=omega0, t=0.0)
    from keldysh4ai.future_b_atomic import exact_t0_linear_cfe, scba_constant_cfe

    g_exact = exact_t0_linear_cfe(ATOMIC_SAMPLE, g, omega0, MA0_DEPTH)
    g_scba = scba_constant_cfe(ATOMIC_SAMPLE, g, omega0, MA0_DEPTH)
    np.testing.assert_allclose(g_ma0, np.asarray(g_exact), rtol=1.0e-10, atol=1.0e-12)
    assert abs(complex(g_ma0) - complex(g_scba)) > 1.0e-8


def test_csv_has_twelve_rows_and_exact_header() -> None:
    assert DEFAULT_CSV.is_file()
    lines = DEFAULT_CSV.read_text().splitlines()
    assert lines[0] == CSV_HEADER
    with DEFAULT_CSV.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert list(rows[0].keys()) == list(HEADER_FIELDS)
    assert len(rows) == 12
    for forbidden in FORBIDDEN_COLUMNS:
        assert forbidden not in rows[0]
        for row in rows:
            assert forbidden not in row
            assert "E0_Born_VC=NOT_COMPUTED" in row["note"]
            assert row["best_block"] in ("born", "scba", "ma0")
            assert row["lambda_if_block"] in ("scba", "ma0")
            if row["E0_MA0"] == "NOT_COMPUTED":
                assert row["best_block"] != "ma0"


def test_e0_columns_copied_from_teacher_map() -> None:
    teacher = {
        (float(r["g_over_t"]), float(r["omega_over_t"])): r
        for r in load_teacher_map(TEACHER_CSV)
    }
    with DEFAULT_CSV.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 12
    for row in rows:
        cell = (float(row["g_over_t"]), float(row["omega_over_t"]))
        src = teacher[cell]
        assert float(row["E0_ED"]) == float(src["E0_ED"])
        assert float(row["E0_Born"]) == float(src["E0_Born"])
        assert float(row["E0_SCBA"]) == float(src["E0_SCBA"])
        accepted = ACCEPTED_E0[cell]
        assert float(row["E0_ED"]) == accepted["E0_ED"]
        assert float(row["E0_Born"]) == accepted["E0_Born"]
        assert float(row["E0_SCBA"]) == accepted["E0_SCBA"]
        assert src["E0_Born_VC"] == "NOT_COMPUTED"


def test_lambda_chooser_and_rel_definitions() -> None:
    with DEFAULT_CSV.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    n_ma0_if = 0
    for row in rows:
        g = float(row["g_over_t"])
        omega = float(row["omega_over_t"])
        lam = float(row["lambda"])
        assert lam == coupling_lambda(g, omega)
        assert row["band"] == band_of(lam)
        assert row["lambda_if_block"] == lambda_if_block(lam)
        if lam >= 0.80:
            assert row["lambda_if_block"] == "ma0"
            n_ma0_if += 1
        else:
            assert row["lambda_if_block"] == "scba"
        e0_ed = float(row["E0_ED"])
        assert float(row["rel_Born"]) == abs(float(row["E0_Born"]) - e0_ed) / abs(e0_ed)
        assert float(row["rel_SCBA"]) == abs(float(row["E0_SCBA"]) - e0_ed) / abs(e0_ed)
        if row["E0_MA0"] != "NOT_COMPUTED":
            assert float(row["rel_MA0"]) == abs(float(row["E0_MA0"]) - e0_ed) / abs(e0_ed)
    assert n_ma0_if == 1
    by_cell = {(float(r["g_over_t"]), float(r["omega_over_t"])): r for r in rows}
    assert by_cell[STRONG_CELL]["band"] == "strong"
    assert by_cell[STRONG_CELL]["lambda_if_block"] == "ma0"


def test_report_exists_and_stop_file_matches_t1() -> None:
    assert REPORT_PATH.is_file()
    report = REPORT_PATH.read_text()
    assert "router" not in report.lower() or "do not" in report.lower()
    with DEFAULT_CSV.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    verdict = evaluate_tests(rows, atomic=ma0_atomic_verdict())
    if not verdict["T1"]["pass"]:
        assert STOP_PATH.is_file()
        stop = STOP_PATH.read_text()
        assert "STOP" in stop
        assert "router" in stop.lower()
    else:
        assert "Candidate 2 STOPS" not in report
        assert not STOP_PATH.is_file()
        assert "do not" in report.lower()
        assert "router" in report.lower()
