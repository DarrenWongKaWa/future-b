# SIGNED FORMULA: xi_k=2t*(1-cos k), L=2 k in {0, pi}, tadpole OFF.
"""Slice closeout pins. Not CERTIFY. Does not upgrade claim strength."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

CLOSEOUT = Path("notes/SLICE_CLOSEOUT.md")
METHOD = Path("notes/METHOD_NOTE.md")
VERDICT = Path("prototypes/future_b_neural_poc/week4_verdict.csv")
TEACHER = Path("prototypes/future_b_neural_poc/teacher_map_l2.csv")
WEEK2 = Path("prototypes/future_b_neural_poc/week2_born_scba_vs_ed.csv")
WEEK3 = Path("prototypes/future_b_neural_poc/week3_gated_vs_fixed.csv")

CSV_SHA256 = {
    TEACHER: "a65dcde29457de0d3935b01f48693d8febb6042749c40fa65e315679d65f836a",
    WEEK2: "73d7ccc625323c6372ea7aba95a850d589c72aaa48f899005cec02d8435303f4",
    WEEK3: "19d66c8a0f0c9c931ea02b67cb274f7cbe3cd1b8a78e7d1e996f05164e7d8d20",
}


def test_closeout_is_slice_not_certification() -> None:
    assert CLOSEOUT.is_file()
    assert METHOD.is_file()
    text = CLOSEOUT.read_text()
    assert "切片结项，不是认证" in text
    assert "not a certification" in text.lower() or "不是认证" in text
    assert "CERTIFY" in text
    assert "Paper 1" in text and "not GO" in text
    assert "Physics-for-AI" in text
    assert "Do not merge" in text or "不要并" in text or "Do **not** merge" in text
    lower = text.lower()
    assert "succeeded" in lower
    assert "do not" in lower
    method = METHOD.read_text()
    assert "切片结项，不是认证" in method


def test_three_claim_csvs_match_pinned_hashes() -> None:
    for path, digest in CSV_SHA256.items():
        assert path.is_file()
        got = hashlib.sha256(path.read_bytes()).hexdigest()
        assert got == digest, path


def test_week4_verdict_remains_negative() -> None:
    with VERDICT.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 1
    assert rows[0]["paper1_go"] == "false"
    assert rows[0]["beats_classical"] == "false"
    assert rows[0]["n_test_match"] == "5"
