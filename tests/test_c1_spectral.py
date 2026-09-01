# SIGNED FORMULA: xi_k=2t*(1-cos k), L=2 k in {0, pi}, tadpole OFF.
"""Candidate 1 spectral pins. Does not train. Does not retune θ."""

from __future__ import annotations

import ast
import csv
import hashlib
from pathlib import Path

import numpy as np
import pytest

from keldysh4ai.future_b.teacher.holstein_ed import HolsteinL2ED
from prototypes.future_b_neural_poc.build_week2_table import (
    ACCEPTED_E0,
    G_OVER_T,
    OMEGA_OVER_T,
    WEEK2_BAND_BY_CELL,
    band_of,
    coupling_lambda,
)
from prototypes.future_b_neural_poc.c1_spectral import (
    BORN_DEPTH,
    CSV_HEADER,
    DEFAULT_CSV,
    ETA_A,
    FORBIDDEN_COLUMNS,
    HEADER_FIELDS,
    N_OMEGA,
    OMEGA_MAX,
    OMEGA_MIN,
    PREREGISTER_PATH,
    SCBA_DEPTH,
    STOP_PATH,
    TEST_CELLS,
    THETA_CLASS,
    TRAIN_CELLS,
    WEEK3_CSV,
    A_from_code_spectral,
    A_rainbow,
    error_A,
    evaluate_tests,
    load_c1_rows,
    load_teacher_index,
    load_week3_gate,
    omega_grid,
    require_preregister,
    retarded_A,
    split_of,
)

C1_REPORT = Path("notes/C1_REPORT.md")
SOURCE = Path("prototypes/future_b_neural_poc/c1_spectral.py")
WEEK4_VERDICT = Path("prototypes/future_b_neural_poc/week4_verdict.csv")
WEEK2_CSV = Path("prototypes/future_b_neural_poc/week2_born_scba_vs_ed.csv")
TEACHER_CSV = Path("prototypes/future_b_neural_poc/teacher_map_l2.csv")

PINNED_SHA256 = {
    TEACHER_CSV: "a65dcde29457de0d3935b01f48693d8febb6042749c40fa65e315679d65f836a",
    WEEK2_CSV: "73d7ccc625323c6372ea7aba95a850d589c72aaa48f899005cec02d8435303f4",
    WEEK3_CSV: "19d66c8a0f0c9c931ea02b67cb274f7cbe3cd1b8a78e7d1e996f05164e7d8d20",
}


def test_preregister_exists_and_does_not_contain_t1_pass() -> None:
    assert PREREGISTER_PATH.is_file()
    text = require_preregister()
    assert "T1 PASS" not in text
    assert "T1 FAIL" not in text
    assert "rules only" in text.lower() or "not evaluated in this file" in text.lower()
    assert "T1" in text and "T2" in text and "T3" in text
    assert "0.05 t" in text or "η_A = 0.05" in text or "eta_A = 0.05" in text
    assert "np.linspace(-8.0, 4.0, 1601)" in text
    assert "θ_class" in text or "theta_class" in text or "0.03" in text
    assert "PASS-SUFFICIENT" in text
    assert "no network" in text.lower() or "Do not train" in text or "do not train" in text.lower()


def test_source_does_not_import_training_or_wrong_geometry() -> None:
    tree = ast.parse(SOURCE.read_text())
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    joined = " ".join(names)
    for banned in (
        "torch",
        "sklearn",
        "chain_scba",
        "crossing_block",
        "week4_learned_gate",
    ):
        assert banned not in joined
    source_text = SOURCE.read_text()
    for banned in ("LogisticRegression", "MLP", "router", "sigmoid"):
        assert banned not in source_text
    assert "rainbow_sigma" in source_text
    assert THETA_CLASS == 0.03


def test_frozen_conventions_and_ed_spectral_conversion() -> None:
    omega = omega_grid()
    assert omega.shape == (N_OMEGA,)
    assert float(omega[0]) == OMEGA_MIN == -8.0
    assert float(omega[-1]) == OMEGA_MAX == 4.0
    assert ETA_A == 0.05
    assert BORN_DEPTH == 0
    assert SCBA_DEPTH == 64
    model = HolsteinL2ED(t=1.0, g=0.15, omega0=0.5, total_cutoff=4)
    spec = model.lehmann_spectrum(k=0.0, omega=omega, eta=ETA_A)
    from_green = retarded_A(spec.green)
    from_code = A_from_code_spectral(spec.spectral)
    np.testing.assert_allclose(from_green, from_code, rtol=0.0, atol=1.0e-14)
    mixed = np.asarray(-2.0 * np.imag(spec.green), dtype=np.float64)
    assert float(np.max(np.abs(mixed - from_green))) > 1.0e-3


def test_split_covers_twelve_cells_without_overlap() -> None:
    train = set(TRAIN_CELLS)
    test = set(TEST_CELLS)
    assert len(train) == 6
    assert len(test) == 6
    assert train.isdisjoint(test)
    expected = {(g, omega) for g in G_OVER_T for omega in OMEGA_OVER_T}
    assert train | test == expected
    assert (1.05, 0.5) in train
    for cell in expected:
        assert split_of(cell) in ("train", "test")


def test_csv_has_twelve_rows_header_and_finite_errors() -> None:
    assert DEFAULT_CSV.is_file()
    lines = DEFAULT_CSV.read_text().splitlines()
    assert lines[0] == CSV_HEADER
    rows = load_c1_rows()
    assert list(rows[0].keys()) == list(HEADER_FIELDS)
    assert len(rows) == 12
    teacher = load_teacher_index()
    week3 = load_week3_gate()
    seen: set[tuple[float, float]] = set()
    for row in rows:
        for forbidden in FORBIDDEN_COLUMNS:
            assert forbidden not in row
        assert "E0_Born_VC=NOT_COMPUTED" in row["note"]
        assert "no_train" in row["note"]
        cell = (float(row["g_over_t"]), float(row["omega_over_t"]))
        assert cell not in seen
        seen.add(cell)
        lam = coupling_lambda(cell[0], cell[1])
        assert float(row["lambda"]) == pytest.approx(lam, rel=0.0, abs=1.0e-15)
        assert row["band"] == band_of(lam) == WEEK2_BAND_BY_CELL[cell]
        assert row["split"] == split_of(cell)
        assert int(row["M_used"]) == teacher[cell]["M_used"]
        assert int(row["depth_gate"]) == week3[cell]["depth_gated"]
        for field in (
            "error_A_Born",
            "error_A_SCBA64",
            "error_A_SCBAgate",
            "error_M1_Born",
            "error_M1_SCBA64",
            "error_M1_SCBAgate",
        ):
            value = float(row[field])
            assert np.isfinite(value), field
            assert "nan" not in row[field].lower()
        for field in ("Z_ED", "Z_Born", "Z_SCBA64", "Z_SCBAgate"):
            token = row[field]
            if token != "NOT_COMPUTED":
                weight = float(token)
                assert np.isfinite(weight)
                assert 0.0 <= weight <= 2.0
    assert seen == set(ACCEPTED_E0)


def test_t1_t3_from_csv_and_stop_file() -> None:
    rows = load_c1_rows()
    verdict = evaluate_tests(rows)
    t1 = verdict["T1"]
    assert t1["n_comparisons"] == 17
    assert t1["n_fail"] == 2
    assert t1["n_pass"] == 15
    assert t1["pass"] is False
    joined = " ".join(t1["exceptions"])
    assert "fixed Omega=0.5" in joined
    assert "fixed g=1.05" in joined
    t2 = verdict["T2"]
    assert t2["found_leftover"] is False
    assert t2["n_leftover_cells"] == 0
    assert t2["message"] == "no extra spectral leftover on this grid"
    t3 = verdict["T3"]
    assert t3["verdict"] == "PASS-SUFFICIENT"
    assert t3["sufficient"] is True
    assert t3["n_test"] == 6
    assert t3["n_test_within_0p10"] == 6
    assert t3["mean_gap"] == pytest.approx(0.00046173854387754343, rel=0.0, abs=1.0e-15)
    assert t3["worst_test_gap"] <= 0.10
    assert verdict["write_c1_stop"] is True
    assert verdict["no_network"] is True
    assert STOP_PATH.is_file()
    stop = STOP_PATH.read_text()
    assert "T1" in stop and "FAIL" in stop
    assert "not softened" in stop.lower() or "were not softened" in stop
    assert C1_REPORT.is_file()
    report = C1_REPORT.read_text()
    assert "T1" in report and "FAIL" in report
    assert "PASS-SUFFICIENT" in report
    assert "no extra spectral leftover on this grid" in report
    assert "Physics-for-AI" in report
    assert "Do not train" in report or "do not train" in report.lower()
    assert "learned gate" in report.lower() or "No network" in report


def test_one_cell_round_trip_matches_csv() -> None:
    rows = { (float(r["g_over_t"]), float(r["omega_over_t"])): r for r in load_c1_rows() }
    cell = (0.15, 2.0)
    omega = omega_grid()
    teacher = load_teacher_index()[cell]
    a_ed_model = HolsteinL2ED(
        t=1.0, g=cell[0], omega0=cell[1], total_cutoff=teacher["M_used"]
    )
    spec = a_ed_model.lehmann_spectrum(k=0.0, omega=omega, eta=ETA_A)
    a_ed = retarded_A(spec.green)
    a_64 = A_rainbow(omega, g=cell[0], omega0=cell[1], depth=SCBA_DEPTH)
    got = error_A(a_64, a_ed)
    assert got == pytest.approx(float(rows[cell]["error_A_SCBA64"]), rel=0.0, abs=1.0e-14)


def test_prior_csvs_and_paper1_go_untouched() -> None:
    for path, digest in PINNED_SHA256.items():
        got = hashlib.sha256(path.read_bytes()).hexdigest()
        assert got == digest, path
    with WEEK4_VERDICT.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["paper1_go"] == "false"
    assert rows[0]["beats_classical"] == "false"
