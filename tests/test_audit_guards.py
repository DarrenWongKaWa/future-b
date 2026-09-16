"""Independent-audit guards (F01/F02/F04/F08). Algebra + script safety.

Layer: invalid-input behavior and patch failure-safety. Not native LiF.
"""

from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from future_b.event_trace import parse_linear_da_counts
from future_b.p1_da import delayed_acceptance_prob, stage2_exact_accept
from future_b.stats import (
    classify_p1_wall_ratio,
    hac_pass,
    mean_jackknife_se,
    ratio_of_sums_jackknife_se,
)

ROOT = Path(__file__).resolve().parents[1]


def test_hac_invalid_windows_do_not_pass():
    with pytest.raises(ValueError):
        hac_pass([1.0, 1.1, float("nan")])
    with pytest.raises(ValueError):
        hac_pass([1.0, 1.1, 0.0])
    with pytest.raises(ValueError):
        hac_pass([1.0, 1.1, -0.1])
    with pytest.raises(ValueError):
        hac_pass([1.0, 1.1, float("inf")])
    assert hac_pass([1.0, 1.24, 1.24]) is True
    assert hac_pass([1.0, 1.26, 1.0]) is False


def test_da_rejects_negative_weight():
    with pytest.raises(ValueError):
        delayed_acceptance_prob(1.0, -1.0, 1.0)


def test_classify_rejects_reversed_or_nan_interval():
    with pytest.raises(ValueError):
        classify_p1_wall_ratio(0.97, 0.93, True)
    with pytest.raises(ValueError):
        classify_p1_wall_ratio(float("nan"), 0.94, True)


def test_negative_counts_do_not_parse():
    with pytest.raises(ValueError):
        parse_linear_da_counts("LINEAR_DA_COUNTS on prop 10 10 10 -1 1 10 1")


def test_mean_jk_is_not_ratio_of_sums_jk():
    n = np.array([1.0, 2.0, 30.0])
    d = np.array([1.0, 1.0, 10.0])
    mean_se = mean_jackknife_se(n / d)
    ratio_se = ratio_of_sums_jackknife_se(n, d)
    assert abs(mean_se - 0.5773502691896257) < 1e-12
    assert abs(ratio_se - 0.9106048000798012) < 1e-12
    assert abs(mean_se - ratio_se) > 0.2


def test_stage2_correction_changes_accept():
    # u=0.5 -> log u ~ -0.693. Uncorrected min(0, ellR=0)=0 accepts.
    # Corrected min(0, 0 - (-1))= min(0,1)=0 still accepts.
    # Use ellR=0, ell_hat=1: corrected min(0,-1)=-1, log(0.5)>-1 so reject.
    assert stage2_exact_accept(0.5, 0.0, 1.0) is False
    uncorrected = math.log(0.5) < min(0.0, 0.0)
    assert uncorrected is True


def test_missing_source_does_not_delete_patch_destination(tmp_path):
    script = ROOT / "patches/p1_clean/apply_p1_clean.py"
    dst = tmp_path / "p1_clean"
    dst.mkdir()
    sentinel = dst / "audit_sentinel.txt"
    sentinel.write_text("Disposable audit fixture only.\n")
    src = tmp_path / "missing_adapter"
    proc = subprocess.run(
        [sys.executable, str(script), "--src", str(src), "--dst", str(dst)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert proc.returncode != 0
    assert dst.is_dir()
    assert sentinel.read_text() == "Disposable audit fixture only.\n"
