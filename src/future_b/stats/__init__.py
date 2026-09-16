"""Correlated-MC diagnostics used in the frozen P1 protocol.

HAC Bartlett lags 2/4/8 with maxSE/minSE <= 1.25 was predeclared.
Do not retune lags after seeing results.
"""

from __future__ import annotations

from typing import Iterable, Sequence

import numpy as np

T_CRIT_DF5_975 = 2.5705818366147395  # Student-t, two-sided 95%, df=5 (6 chains)
HAC_STABILITY_MAX = 1.25
PRACTICAL_GAIN_THRESHOLD = 0.95


def jackknife_se(values: Sequence[float]) -> float:
    x = np.asarray(values, dtype=np.float64)
    n = x.size
    if n < 2:
        return float("nan")
    mean = x.mean()
    leave = np.array([(n * mean - x[i]) / (n - 1) for i in range(n)])
    return float(np.sqrt((n - 1) / n * np.sum((leave - leave.mean()) ** 2)))


def point_halfwidth_t975(se: float, t_crit: float = T_CRIT_DF5_975) -> float:
    return abs(float(se)) * float(t_crit)


def hac_pass(se_lags: Iterable[float], max_ratio: float = HAC_STABILITY_MAX) -> bool:
    se = [float(s) for s in se_lags if np.isfinite(s) and s > 0.0]
    if len(se) < 2:
        return False
    return (max(se) / min(se)) <= max_ratio


def classify_p1_wall_ratio(
    boot_low: float,
    boot_high: float,
    hac_ok: bool,
    threshold: float = PRACTICAL_GAIN_THRESHOLD,
) -> str:
    """Frozen classification. Do not edit after seeing confirmation data."""
    if boot_high < threshold and hac_ok:
        return "P1_GAIN_ESTABLISHED"
    if boot_low > threshold:
        return "P1_NO_PRACTICAL_GAIN"
    return "P1_UNRESOLVED_WITHIN_BUDGET"
