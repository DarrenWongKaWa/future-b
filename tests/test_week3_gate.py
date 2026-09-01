# SIGNED FORMULA: xi_k=2t*(1-cos k), L=2 k in {0, pi}, tadpole OFF.
"""Week 3 classical-gate pins. Does not train. Does not rerun ED."""

from __future__ import annotations

import ast
import csv
from pathlib import Path

from prototypes.future_b_neural_poc.build_week2_table import ACCEPTED_E0, G_OVER_T, OMEGA_OVER_T
from prototypes.future_b_neural_poc.l2_periodic_pole import COARSE_N, SCBA_DEPTH
from prototypes.future_b_neural_poc.week3_classical_gate import (
    GATED_CSV,
    GATED_FIELDS,
    MATCH_GRAIN,
    N_GREEN_FIXED,
    NOT_ADMISSIBLE,
    PREREGISTER_PATH,
    SCAN_CSV,
    SCAN_FIELDS,
    STOP_PATH,
    TEST_CELLS,
    THETA_CSV,
    THETA_FIELDS,
    THETA_GRID,
    TRAIN_CELLS,
    gated_depth,
    leftover_decision,
    matches_ed_grain,
    n_green_gated_total,
    oracle_depth,
    split_of,
)

WEEK3_REPORT = Path("notes/WEEK3_REPORT.md")
SOURCE = Path("prototypes/future_b_neural_poc/week3_classical_gate.py")


def test_preregister_exists_and_does_not_evaluate_tests() -> None:
    assert PREREGISTER_PATH.is_file()
    text = PREREGISTER_PATH.read_text()
    assert "theta_class" in text or r"\theta_{\mathrm{class}}" in text
    assert "(0.15, 0.5)" in text and "(1.05, 0.5)" in text
    assert "NOT_ADMISSIBLE" in text
    assert "T1" in text and "T6" in text
    assert "rules only" in text.lower() or "not evaluated" in text.lower()
    assert "T1 PASS" not in text and "T1 FAIL" not in text
    assert "T6 PASS" not in text and "T6 FAIL" not in text
    assert "leftover_decision" in text
    assert "1e-4" in text or "10^{-4}" in text


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
        "holstein_ed",
    ):
        assert banned not in joined


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


def test_gated_depth_and_matching_formulas() -> None:
    rel = {n: 1.0 / (10.0**n) for n in range(1, SCBA_DEPTH + 1)}
    assert gated_depth(rel, 1.0e-1) == 2
    assert gated_depth(rel, 1.0e-8) == 9
    never = {n: 1.0 for n in range(1, SCBA_DEPTH + 1)}
    assert gated_depth(never, 1.0e-8) == SCBA_DEPTH
    assert matches_ed_grain(-1.0, -0.8, -1.2)
    assert matches_ed_grain(-0.8 + MATCH_GRAIN, -0.8, -1.2)
    assert not matches_ed_grain(-0.8 + MATCH_GRAIN + 1.0e-12, -0.8, -1.2)
    assert not matches_ed_grain(None, -0.8, -1.2)
    e0_by_n = {n: None for n in range(0, SCBA_DEPTH + 1)}
    e0_by_n[3] = -1.0
    e0_by_n[64] = -0.8
    assert oracle_depth(e0_by_n, -0.8, -1.2) == 3
    assert n_green_gated_total(64) > N_GREEN_FIXED
    assert n_green_gated_total(0) < N_GREEN_FIXED
    assert N_GREEN_FIXED == 2 * (SCBA_DEPTH + 1) * COARSE_N


def test_leftover_requires_all_four_conditions() -> None:
    def rows(*, match: str, depth: int, oracle: int) -> list[dict[str, str]]:
        out = []
        for cell in TRAIN_CELLS + TEST_CELLS:
            split = "train" if cell in TRAIN_CELLS else "test"
            out.append(
                {
                    "split": split,
                    "match_grain_ok": match,
                    "depth_gated": str(depth),
                    "depth_oracle": str(oracle),
                    "n_green_gated_total": str(n_green_gated_total(depth)),
                }
            )
        return out

    assert leftover_decision(None, rows(match="true", depth=10, oracle=2)) is False
    assert leftover_decision(1.0e-4, rows(match="false", depth=10, oracle=2)) is False
    assert leftover_decision(1.0e-4, rows(match="true", depth=64, oracle=2)) is False
    assert leftover_decision(1.0e-4, rows(match="true", depth=10, oracle=10)) is False
    assert leftover_decision(1.0e-4, rows(match="true", depth=10, oracle=2)) is True


def test_scan_csv_has_780_rows_and_depth64_matches_teacher() -> None:
    assert SCAN_CSV.is_file()
    with SCAN_CSV.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert list(rows[0].keys()) == list(SCAN_FIELDS)
    assert len(rows) == 12 * (SCBA_DEPTH + 1)
    by_cell_depth = {
        (float(r["g_over_t"]), float(r["omega_over_t"]), int(r["depth"])): r
        for r in rows
    }
    for cell, accepted in ACCEPTED_E0.items():
        locked = by_cell_depth[(cell[0], cell[1], SCBA_DEPTH)]
        assert float(locked["E0"]) == accepted["E0_SCBA"]
        born = by_cell_depth[(cell[0], cell[1], 0)]
        assert float(born["E0"]) == accepted["E0_Born"]
        assert born["rel_sigma_diag"] == ""
        assert by_cell_depth[(cell[0], cell[1], 1)]["rel_sigma_diag"] != ""
        assert "E0_Born_VC=NOT_COMPUTED" in locked["note"]


def test_gated_csv_split_and_theta_from_train_only() -> None:
    assert GATED_CSV.is_file()
    assert THETA_CSV.is_file()
    with GATED_CSV.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert list(rows[0].keys()) == list(GATED_FIELDS)
    assert len(rows) == 12
    assert "E0_Born_VC" not in rows[0]
    with THETA_CSV.open(newline="") as handle:
        selection = list(csv.DictReader(handle))
    assert list(selection[0].keys()) == list(THETA_FIELDS)
    assert len(selection) == 1
    token = selection[0]["theta_class"]
    if token != NOT_ADMISSIBLE:
        theta = float(token)
        assert theta in THETA_GRID
    n_train = n_test = 0
    for row in rows:
        cell = (float(row["g_over_t"]), float(row["omega_over_t"]))
        assert row["split"] == split_of(cell)
        assert row["theta_class"] == token
        if row["split"] == "train":
            n_train += 1
        else:
            n_test += 1
        assert row["n_green_fixed"] == str(N_GREEN_FIXED)
        assert int(row["depth_gated"]) >= 1
        assert int(row["depth_gated"]) <= SCBA_DEPTH
        assert int(row["depth_oracle"]) >= 1
        assert row["match_grain_ok"] in ("true", "false")
    assert n_train == 6 and n_test == 6


def test_t1_t6_from_csv_match_report_files() -> None:
    with SCAN_CSV.open(newline="") as handle:
        scan = list(csv.DictReader(handle))
    with GATED_CSV.open(newline="") as handle:
        gated = list(csv.DictReader(handle))
    with THETA_CSV.open(newline="") as handle:
        selection = list(csv.DictReader(handle))[0]
    for row in scan:
        if int(row["depth"]) != SCBA_DEPTH:
            continue
        cell = (float(row["g_over_t"]), float(row["omega_over_t"]))
        assert float(row["E0"]) == ACCEPTED_E0[cell]["E0_SCBA"]
    leftover = selection["leftover_decision"]
    assert leftover in ("true", "false")
    if leftover == "true":
        assert selection["admissible"] == "true"
        assert int(selection["n_test_match"]) == 6
        assert float(selection["mean_depth_oracle_test"]) < float(
            selection["mean_depth_gated_test"]
        )
    assert WEEK3_REPORT.is_file()
    report = WEEK3_REPORT.read_text()
    assert "Physics-for-AI" not in report or "not Physics-for-AI" in report.lower() or "not neural" in report.lower()
    if selection["admissible"] == "false":
        assert STOP_PATH.is_file()
    if leftover == "false":
        assert "router" not in report.lower() or "no router" in report.lower() or "not open" in report.lower() or "not started" in report.lower() or "skip" in report.lower()
