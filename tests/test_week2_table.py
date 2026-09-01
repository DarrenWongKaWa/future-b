# SIGNED FORMULA: H=2t*n-t*sum_PBC(c^dag c+h.c.)+Omega*b^dag*b+g*n*(b+b^dag), xi_k=2t*(1-cos k).
"""Week 2 analysis-table pins. Analysis only; does not rerun ED or poles."""

from __future__ import annotations

import csv
from pathlib import Path

from prototypes.future_b_neural_poc.build_week2_table import (
    ACCEPTED_E0,
    CSV_HEADER,
    FORBIDDEN_COLUMNS,
    HEADER_FIELDS,
    TEACHER_CSV,
    WEEK2_BAND_BY_CELL,
    analyze_teacher_rows,
    band_of,
    coupling_lambda,
    evaluate_tests,
    load_teacher_map,
)

WEEK2_CSV = Path("prototypes/future_b_neural_poc/week2_born_scba_vs_ed.csv")
PREREGISTER = Path("notes/WEEK2_METRICS_PREREGISTER.md")
WEEK2_REPORT = Path("notes/WEEK2_REPORT.md")
WEEK2_STOP = Path("notes/WEEK2_STOP.md")


def test_preregister_exists_and_does_not_evaluate_t1_t4() -> None:
    assert PREREGISTER.is_file()
    text = PREREGISTER.read_text()
    compact = " ".join(text.split())
    assert "g² / (2 t Ω)" in text or "g^2 / (2 t Omega)" in text or "g^2/(2*t*Omega)" in compact
    assert "weak" in text and "intermediate" in text and "strong" in text
    assert "T1" in text and "T2" in text and "T3" in text and "T4" in text
    assert "not evaluated" in text.lower() or "rules only" in text.lower()
    assert "Fail Week 2 if any weak cell violates" in compact
    # Preregister must not record a T1–T4 pass/fail verdict.
    assert "T1 PASS" not in text and "T1 FAIL" not in text
    assert "T4 PASS" not in text and "T4 FAIL" not in text


def test_week2_csv_has_twelve_rows_and_exact_header() -> None:
    assert WEEK2_CSV.is_file()
    lines = WEEK2_CSV.read_text().splitlines()
    assert lines[0] == CSV_HEADER
    with WEEK2_CSV.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert list(rows[0].keys()) == list(HEADER_FIELDS)
    assert len(rows) == 12
    for forbidden in FORBIDDEN_COLUMNS:
        assert forbidden not in rows[0]
        for row in rows:
            assert forbidden not in row
            assert "Born_VC" not in row["note"] or "E0_Born_VC=NOT_COMPUTED" in row["note"]


def test_e0_columns_match_teacher_map() -> None:
    teacher = { (float(r["g_over_t"]), float(r["omega_over_t"])): r
                for r in load_teacher_map(TEACHER_CSV) }
    with WEEK2_CSV.open(newline="") as handle:
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


def test_bands_follow_week2_lambda_cuts_not_week1() -> None:
    with WEEK2_CSV.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    counts = {"weak": 0, "intermediate": 0, "strong": 0}
    for row in rows:
        g = float(row["g_over_t"])
        omega = float(row["omega_over_t"])
        lam = float(row["lambda"])
        assert lam == coupling_lambda(g, omega)
        assert row["band"] == band_of(lam)
        assert row["band"] == WEEK2_BAND_BY_CELL[(g, omega)]
        counts[row["band"]] += 1
        if lam < 0.08:
            assert row["band"] == "weak"
        elif lam < 0.80:
            assert row["band"] == "intermediate"
        else:
            assert row["band"] == "strong"
    assert counts == {"weak": 4, "intermediate": 7, "strong": 1}
    # Week-1 cuts would have labelled (0.45, 0.8) and (0.75, 2.0) weak.
    by_cell = {(float(r["g_over_t"]), float(r["omega_over_t"])): r for r in rows}
    assert by_cell[(0.45, 0.8)]["band"] == "intermediate"
    assert by_cell[(0.75, 2.0)]["band"] == "intermediate"
    assert by_cell[(1.05, 0.5)]["band"] == "strong"


def test_metrics_and_scba_beats_born_from_definitions() -> None:
    with WEEK2_CSV.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        e0_ed = float(row["E0_ED"])
        e0_born = float(row["E0_Born"])
        e0_scba = float(row["E0_SCBA"])
        delta_born = float(row["delta_Born"])
        delta_scba = float(row["delta_SCBA"])
        assert delta_born == e0_born - e0_ed
        assert delta_scba == e0_scba - e0_ed
        assert float(row["rel_Born"]) == abs(delta_born) / abs(e0_ed)
        assert float(row["rel_SCBA"]) == abs(delta_scba) / abs(e0_ed)
        beats = abs(delta_scba) < abs(delta_born)
        assert row["scba_beats_born"] == ("true" if beats else "false")
        assert row["scba_beats_born"] in ("true", "false")


def test_t1_t4_evaluated_from_csv() -> None:
    with WEEK2_CSV.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    verdict = evaluate_tests(rows)
    assert verdict["n_cells"] == 12
    assert verdict["T1"]["n_weak"] == 4
    assert verdict["T1"]["pass"] is True
    assert verdict["T1"]["n_fail"] == 0
    assert verdict["T2"]["pass"] is True
    assert verdict["T2"]["rel_SCBA"] >= 0.20
    assert verdict["T3"]["n_exceptions"] <= 1
    assert verdict["T3"]["pass"] is True
    assert verdict["T4"]["pass"] is True
    assert verdict["T4"]["n_fail"] == 0
    assert verdict["T4"]["n_pass"] == 12
    assert verdict["n_scba_beats_born"] == 12
    assert verdict["stop_required"] is False
    assert WEEK2_REPORT.is_file()
    assert not WEEK2_STOP.is_file()


def test_builder_round_trip_does_not_invent_vc() -> None:
    rows = analyze_teacher_rows(load_teacher_map())
    assert len(rows) == 12
    for row in rows:
        assert "E0_Born_VC" not in row
        assert row["scba_beats_born"] in ("true", "false")
