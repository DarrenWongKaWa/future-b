"""Pooled ratio estimator and exactness validator of research/r1_grouped/native_rb."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "r1_grouped" / "native_rb"))

import compare_pooled  # noqa: E402
import validate_exactness  # noqa: E402


def _chain(root: Path, i: int, etrue: float, sign: float, cpu: float) -> None:
    c = root / "lif_hole" / f"chain{i:02d}"
    c.mkdir(parents=True)
    (c / "stdout.log").write_text(f"            Etrue =    {etrue:.10E}    0.0E+00\n"
                                  f"            <g/Z> =     {sign:.10E}    0.0E+00\n")
    (c / "stderr.log").write_text(f"real\t1m0.0s\nuser\t0m{cpu:.3f}s\nsys\t0m0.1s\n")


def test_pooled_is_sign_weighted_not_mean_of_ratios(tmp_path):
    # Two chains: a high-sign chain at E=-1 and a low-sign chain at E=-3.
    _chain(tmp_path, 0, -1.0, 0.20, 10.0)
    _chain(tmp_path, 1, -3.0, 0.02, 10.0)
    tau, e_bare = 2.0, 0.0
    side = compare_pooled.side(str(tmp_path), "lif_hole", tau, e_bare)
    expected = (-1.0 * 0.20 + -3.0 * 0.02) / (0.20 + 0.02)
    assert side["Q_pooled"] == pytest.approx(expected)
    assert side["Q_mean_of_chain_ratios"] == pytest.approx(-2.0)
    assert side["cpu_s"] == pytest.approx(10.0)


def test_validator_pooled_matches_compare_pooled(tmp_path):
    rng = np.random.default_rng(0)
    for i in range(6):
        _chain(tmp_path, i, -0.87 + 0.001 * rng.standard_normal(), 0.999, 5.0)
    q, se, n = validate_exactness.pooled(tmp_path, "lif_hole")
    side = compare_pooled.side(str(tmp_path), "lif_hole", 1.0, 0.0)
    assert n == 6
    assert q == pytest.approx(side["Q_pooled"])
    assert se == pytest.approx(side["se_delta"])


def test_validator_needs_two_chains(tmp_path):
    _chain(tmp_path, 0, -0.87, 1.0, 1.0)
    q, se, n = validate_exactness.pooled(tmp_path, "lif_hole")
    assert n == 1 and np.isnan(q) and np.isnan(se)
