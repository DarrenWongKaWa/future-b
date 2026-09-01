# SIGNED FORMULA: xi_k=2t*(1-cos k), L=2 k in {0, pi}, tadpole OFF.
"""Candidate 1+2 joint closeout pins. Does not train. Does not set paper1_go."""

from __future__ import annotations

import csv
from pathlib import Path

REPORT = Path("notes/C12_SWARM_REPORT.md")
VERDICT = Path("prototypes/future_b_neural_poc/week4_verdict.csv")

ALLOWED_SENTENCE = (
    "On this L=2 slice, classical θ=0.03 already matches depth-64 SCBA "
    "on A(ω) (no spectral leftover; Candidate 1 stops). MA(0) cuts the "
    "strong-cell E0 error versus SCBA by the declared margin and a "
    "λ-only chooser misses three remainder cells. No learned gate was "
    "trained. paper1_go stays false."
)


def test_c12_swarm_report_exists() -> None:
    assert REPORT.is_file()
    text = REPORT.read_text()
    assert ALLOWED_SENTENCE in text
    assert "paper1_go stays false" in text
    assert "NOT_COMPUTED" in text
    compact = text.replace(" ", "").lower()
    assert "paper1_go=true" not in compact
    assert "paper1_go true" not in text.lower()


def test_paper1_go_not_set_true_and_week4_verdict_still_false() -> None:
    with VERDICT.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 1
    assert rows[0]["paper1_go"] == "false"
    assert rows[0]["beats_classical"] == "false"
