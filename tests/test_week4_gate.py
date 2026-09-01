# SIGNED FORMULA: xi_k=2t*(1-cos k), L=2 k in {0, pi}, tadpole OFF.
"""Week 4 learned-gate pins. No retune. No teacher features."""

from __future__ import annotations

import ast
import csv
from pathlib import Path

from prototypes.future_b_neural_poc.build_week2_table import ACCEPTED_E0
from prototypes.future_b_neural_poc.week4_learned_gate import (
    FEATURE_NAMES,
    LEARNED_CSV,
    LEARNED_FIELDS,
    PREREGISTER_PATH,
    STOP_PATH,
    THETA_CLASS,
    VERDICT_CSV,
    WEIGHTS_CSV,
    leakage_source_ok,
    raw_features,
)

WEEK4_REPORT = Path("notes/WEEK4_REPORT.md")
SOURCE = Path("prototypes/future_b_neural_poc/week4_learned_gate.py")


def test_preregister_exists_and_does_not_evaluate_tests() -> None:
    assert PREREGISTER_PATH.is_file()
    text = PREREGISTER_PATH.read_text()
    assert "paper1_go" in text
    assert "Forbidden as features" in text or "forbidden" in text.lower()
    assert "T1 PASS" not in text and "T3 FAIL" not in text
    assert "0.03" in text
    assert "4000" in text


def test_source_has_no_torch_and_no_teacher_features_in_raw_features() -> None:
    tree = ast.parse(SOURCE.read_text())
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    joined = " ".join(names)
    for banned in ("torch", "sklearn", "chain_scba", "crossing_block", "holstein_ed"):
        assert banned not in joined
    assert leakage_source_ok(SOURCE) is True
    phi = raw_features(g=0.75, omega=0.8, depth=2, r_n=0.01, abs_sigma=1.0)
    assert phi.shape == (len(FEATURE_NAMES),)
    assert FEATURE_NAMES == (
        "g",
        "omega",
        "lambda",
        "n_over_64",
        "log10_r_n",
        "abs_sigma_diag",
    )


def test_learned_csv_locks_and_negative_verdict() -> None:
    assert LEARNED_CSV.is_file()
    assert VERDICT_CSV.is_file()
    assert WEIGHTS_CSV.is_file()
    with LEARNED_CSV.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert list(rows[0].keys()) == list(LEARNED_FIELDS)
    assert len(rows) == 12
    assert "E0_Born_VC" not in rows[0]
    n_train_match = n_test_match = 0
    n_train = n_test = 0
    by_cell = {}
    for row in rows:
        cell = (float(row["g_over_t"]), float(row["omega_over_t"]))
        by_cell[cell] = row
        assert float(row["theta_class"]) == THETA_CLASS
        assert float(row["E0_SCBA_fixed"]) == ACCEPTED_E0[cell]["E0_SCBA"]
        assert float(row["E0_ED"]) == ACCEPTED_E0[cell]["E0_ED"]
        if row["split"] == "train":
            n_train += 1
            n_train_match += int(row["match_grain_ok"] == "true")
        else:
            n_test += 1
            n_test_match += int(row["match_grain_ok"] == "true")
    assert n_train == 6 and n_test == 6
    assert n_train_match == 6
    assert n_test_match == 5
    assert by_cell[(0.75, 0.8)]["match_grain_ok"] == "false"
    assert by_cell[(0.75, 0.8)]["split"] == "test"
    with VERDICT_CSV.open(newline="") as handle:
        verdict = list(csv.DictReader(handle))
    assert len(verdict) == 1
    assert verdict[0]["beats_classical"] == "false"
    assert verdict[0]["paper1_go"] == "false"
    assert verdict[0]["n_test_match"] == "5"
    assert not STOP_PATH.is_file()
    assert WEEK4_REPORT.is_file()
    report = WEEK4_REPORT.read_text().lower()
    assert "paper 1 is not go" in report or "paper1_go=false" in report
    assert "not" in report and "physics-for-ai" in report
