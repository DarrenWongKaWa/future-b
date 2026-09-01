# SIGNED FORMULA: xi_k=2t*(1-cos k), L=2 k in {0, pi}, tadpole OFF.
"""Week 3 classical SCBA stopping on the frozen periodic L=2 rainbow.

Does not edit holstein_ed.py or l2_periodic_pole.py. Does not train.
θ_class is chosen only on the preregistered train split.
"""

from __future__ import annotations

import csv
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

import numpy as np

from prototypes.future_b_neural_poc.build_week2_table import (
    ACCEPTED_E0,
    G_OVER_T,
    OMEGA_OVER_T,
    TEACHER_CSV,
    WEEK2_BAND_BY_CELL,
    band_of,
    coupling_lambda,
    load_teacher_map,
)
from prototypes.future_b_neural_poc.l2_periodic_pole import (
    COARSE_N,
    ETA,
    OMEGA_MAX,
    OMEGA_MIN,
    RE_D_ZERO_TOL,
    SCBA_DEPTH,
    _bisection_root,
    denominator,
    rainbow_sigma,
)

T = 1.0
EPS_NORM = 1.0e-30
MATCH_GRAIN = 1.0e-4
NOT_COMPUTED = "NOT_COMPUTED"
NOT_ADMISSIBLE = "NOT_ADMISSIBLE"

THETA_GRID: tuple[float, ...] = (
    1.0e-1,
    3.0e-2,
    1.0e-2,
    3.0e-3,
    1.0e-3,
    3.0e-4,
    1.0e-4,
    3.0e-5,
    1.0e-5,
    3.0e-6,
    1.0e-6,
    1.0e-7,
    1.0e-8,
)

TRAIN_CELLS: tuple[tuple[float, float], ...] = (
    (0.15, 0.5),
    (0.15, 2.0),
    (0.45, 0.8),
    (0.75, 0.5),
    (0.75, 2.0),
    (1.05, 0.5),
)
TEST_CELLS: tuple[tuple[float, float], ...] = (
    (0.15, 0.8),
    (0.45, 0.5),
    (0.45, 2.0),
    (0.75, 0.8),
    (1.05, 0.8),
    (1.05, 2.0),
)

N_LAYER_FIXED = SCBA_DEPTH + 1
N_GREEN_FIXED = 2 * N_LAYER_FIXED * COARSE_N

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREREGISTER_PATH = ROOT / "notes" / "WEEK3_METRICS_PREREGISTER.md"
STOP_PATH = ROOT / "notes" / "WEEK3_STOP.md"
SCAN_CSV = HERE / "week3_depth_scan.csv"
GATED_CSV = HERE / "week3_gated_vs_fixed.csv"
THETA_CSV = HERE / "week3_theta_selection.csv"

SCAN_FIELDS = (
    "g_over_t",
    "omega_over_t",
    "depth",
    "E0",
    "abs_D",
    "n_crossings",
    "sigma_diag_re",
    "sigma_diag_im",
    "rel_sigma_diag",
    "rel_sigma_l2",
    "note",
)
GATED_FIELDS = (
    "g_over_t",
    "omega_over_t",
    "lambda",
    "band",
    "split",
    "theta_class",
    "E0_ED",
    "E0_SCBA_fixed",
    "E0_gated",
    "depth_gated",
    "depth_oracle",
    "rel_sigma_at_stop",
    "delta_fixed",
    "delta_gated",
    "rel_fixed",
    "rel_gated",
    "match_grain_ok",
    "n_green_fixed",
    "n_green_gated_total",
    "note",
)
THETA_FIELDS = (
    "theta_class",
    "admissible",
    "n_train_match",
    "n_test_match",
    "mean_depth_gated_train",
    "mean_depth_gated_test",
    "mean_depth_oracle_test",
    "leftover_decision",
    "note",
)

SCAN_NOTE = (
    "week3_scan;z_diag=0+i*eta;origin=xi_k=2t(1-cos k);"
    "E0_Born_VC=NOT_COMPUTED;no_train"
)
GATED_NOTE = (
    "week3_gate;r_n=|dSigma|/max(|Sigma|,eps);z_diag=0+i*eta;"
    "match=|d_gated|<=|d_fixed|+1e-4t;E0_Born_VC=NOT_COMPUTED;no_train"
)


def split_of(cell: tuple[float, float]) -> str:
    if cell in TRAIN_CELLS:
        return "train"
    if cell in TEST_CELLS:
        return "test"
    raise RuntimeError(f"CONFLICT: cell {cell} is not in the preregistered split")


def n_green_discover(depth_used: int) -> int:
    return (depth_used + 1) * (depth_used + 2)


def n_green_pole(depth_used: int) -> int:
    return 2 * (depth_used + 1) * COARSE_N


def n_green_gated_total(depth_used: int) -> int:
    return n_green_pole(depth_used) + n_green_discover(depth_used)


def residual_ratio(current: complex, previous: complex) -> float:
    return float(abs(current - previous) / max(abs(current), EPS_NORM))


def l2_residual_ratio(current: np.ndarray, previous: np.ndarray) -> float:
    diff = float(np.linalg.norm(current - previous))
    norm = float(np.linalg.norm(current))
    return diff / max(norm, EPS_NORM)


def gated_depth(rel_by_n: dict[int, float], theta: float) -> int:
    for depth in range(1, SCBA_DEPTH + 1):
        if rel_by_n[depth] < theta:
            return depth
    return SCBA_DEPTH


def matches_ed_grain(
    e0_gated: float | None,
    e0_fixed: float,
    e0_ed: float,
    *,
    grain: float = MATCH_GRAIN,
) -> bool:
    if e0_gated is None or not np.isfinite(e0_gated):
        return False
    return abs(e0_gated - e0_ed) <= abs(e0_fixed - e0_ed) + grain


def oracle_depth(
    e0_by_n: dict[int, float | None],
    e0_fixed: float,
    e0_ed: float,
    *,
    grain: float = MATCH_GRAIN,
) -> int:
    for depth in range(1, SCBA_DEPTH + 1):
        if matches_ed_grain(e0_by_n[depth], e0_fixed, e0_ed, grain=grain):
            return depth
    return SCBA_DEPTH


def _csv_float(value: float | None) -> str:
    if value is None or not np.isfinite(value):
        return NOT_COMPUTED
    return repr(float(value))


def _coarse_grid() -> np.ndarray:
    return np.linspace(OMEGA_MIN, OMEGA_MAX, COARSE_N, dtype=np.float64)


def pole_from_sigma_grid(
    omega: np.ndarray,
    sigma_grid: np.ndarray,
    *,
    g: float,
    omega0: float,
    depth: int,
) -> tuple[float | None, float | None, int]:
    """Same root rule as lowest_real_pole, using a precomputed coarse Σ."""

    real_d = np.real(omega.astype(np.complex128) + 1.0j * ETA - sigma_grid)
    n_crossings = 0
    root: float | None = None
    for index in range(COARSE_N - 1):
        left = float(real_d[index])
        right = float(real_d[index + 1])
        if not np.isfinite(left) or not np.isfinite(right):
            continue
        hit = False
        if abs(left) <= RE_D_ZERO_TOL:
            candidate = float(omega[index])
            hit = True
        elif left * right < 0.0:
            candidate = _bisection_root(
                g=g,
                omega0=omega0,
                depth=depth,
                left=float(omega[index]),
                right=float(omega[index + 1]),
                f_left=left,
            )
            hit = True
        if not hit:
            continue
        if candidate <= OMEGA_MIN or candidate >= OMEGA_MAX:
            continue
        n_crossings += 1
        if root is None:
            root = candidate
    if root is None:
        return None, None, n_crossings
    abs_d = float(np.abs(denominator(root, g=g, omega0=omega0, depth=depth)))
    return float(root), abs_d, n_crossings


def scan_cell(g: float, omega0: float) -> list[dict[str, Any]]:
    omega = _coarse_grid()
    z_grid = omega.astype(np.complex128) + 1.0j * ETA
    zero_index = int(np.argmin(np.abs(omega)))
    if abs(float(omega[zero_index])) > 1.0e-12:
        raise RuntimeError("CONFLICT: z_diag=0 is not on the frozen coarse grid")
    previous_grid: np.ndarray | None = None
    rows: list[dict[str, Any]] = []
    for depth in range(0, SCBA_DEPTH + 1):
        sigma_grid = rainbow_sigma(z_grid, g=g, omega0=omega0, depth=depth)
        energy, abs_d, n_crossings = pole_from_sigma_grid(
            omega, sigma_grid, g=g, omega0=omega0, depth=depth
        )
        sigma_diag = complex(sigma_grid[zero_index])
        if previous_grid is None:
            rel_diag: float | None = None
            rel_l2: float | None = None
        else:
            rel_diag = residual_ratio(sigma_diag, complex(previous_grid[zero_index]))
            rel_l2 = l2_residual_ratio(sigma_grid, previous_grid)
        previous_grid = sigma_grid
        rows.append(
            {
                "g": g,
                "omega": omega0,
                "depth": depth,
                "E0": energy,
                "abs_D": abs_d,
                "n_crossings": n_crossings,
                "sigma_diag": sigma_diag,
                "rel_sigma_diag": rel_diag,
                "rel_sigma_l2": rel_l2,
            }
        )
    return rows


def scan_all_cells() -> list[dict[str, Any]]:
    cells = [(g, omega0) for g in G_OVER_T for omega0 in OMEGA_OVER_T]
    rows: list[dict[str, Any]] = []
    with ProcessPoolExecutor(max_workers=min(12, len(cells))) as pool:
        futures = [pool.submit(scan_cell, g, omega0) for g, omega0 in cells]
        for future in futures:
            rows.extend(future.result())
    return rows


def index_scan(
    scan_rows: list[dict[str, Any]],
) -> dict[tuple[float, float], dict[int, dict[str, Any]]]:
    out: dict[tuple[float, float], dict[int, dict[str, Any]]] = {}
    for row in scan_rows:
        cell = (float(row["g"]), float(row["omega"]))
        out.setdefault(cell, {})[int(row["depth"])] = row
    expected = {(g, omega) for g in G_OVER_T for omega in OMEGA_OVER_T}
    if set(out) != expected:
        raise RuntimeError(f"CONFLICT: scan cells {sorted(out)} != {sorted(expected)}")
    for cell, by_depth in out.items():
        if set(by_depth) != set(range(0, SCBA_DEPTH + 1)):
            raise RuntimeError(f"CONFLICT: incomplete depth scan at {cell}")
    return out


def select_theta(
    indexed: dict[tuple[float, float], dict[int, dict[str, Any]]],
    teacher: dict[tuple[float, float], dict[str, float]],
) -> tuple[float | None, dict[tuple[float, float], bool]]:
    train_match_by_theta: dict[float, dict[tuple[float, float], bool]] = {}
    for theta in THETA_GRID:
        flags: dict[tuple[float, float], bool] = {}
        for cell in TRAIN_CELLS:
            by_depth = indexed[cell]
            rel = {n: float(by_depth[n]["rel_sigma_diag"]) for n in range(1, SCBA_DEPTH + 1)}
            depth = gated_depth(rel, theta)
            e0_gated = by_depth[depth]["E0"]
            flags[cell] = matches_ed_grain(
                e0_gated, teacher[cell]["E0_SCBA"], teacher[cell]["E0_ED"]
            )
        train_match_by_theta[theta] = flags
    admissible = [
        theta for theta in THETA_GRID if all(train_match_by_theta[theta].values())
    ]
    if not admissible:
        return None, train_match_by_theta[THETA_GRID[-1]]
    chosen = max(admissible)
    return chosen, train_match_by_theta[chosen]


def build_gated_rows(
    indexed: dict[tuple[float, float], dict[int, dict[str, Any]]],
    teacher: dict[tuple[float, float], dict[str, float]],
    theta_class: float | None,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for g in G_OVER_T:
        for omega0 in OMEGA_OVER_T:
            cell = (g, omega0)
            by_depth = indexed[cell]
            e0_ed = teacher[cell]["E0_ED"]
            e0_fixed = teacher[cell]["E0_SCBA"]
            e0_by_n = {n: by_depth[n]["E0"] for n in range(0, SCBA_DEPTH + 1)}
            n_orac = oracle_depth(e0_by_n, e0_fixed, e0_ed)
            if theta_class is None:
                depth = SCBA_DEPTH
                theta_token = NOT_ADMISSIBLE
            else:
                rel = {
                    n: float(by_depth[n]["rel_sigma_diag"])
                    for n in range(1, SCBA_DEPTH + 1)
                }
                depth = gated_depth(rel, theta_class)
                theta_token = repr(float(theta_class))
            e0_gated = by_depth[depth]["E0"]
            rel_stop = by_depth[depth]["rel_sigma_diag"]
            delta_fixed = e0_fixed - e0_ed
            match = matches_ed_grain(e0_gated, e0_fixed, e0_ed)
            if e0_gated is None:
                delta_gated = None
                rel_gated = None
            else:
                delta_gated = float(e0_gated) - e0_ed
                rel_gated = abs(delta_gated) / abs(e0_ed)
            lam = coupling_lambda(g, omega0)
            band = band_of(lam)
            if band != WEEK2_BAND_BY_CELL[cell]:
                raise RuntimeError(
                    f"CONFLICT: band({cell})={band!r} != {WEEK2_BAND_BY_CELL[cell]!r}"
                )
            rows.append(
                {
                    "g_over_t": repr(g),
                    "omega_over_t": repr(omega0),
                    "lambda": repr(lam),
                    "band": band,
                    "split": split_of(cell),
                    "theta_class": theta_token,
                    "E0_ED": repr(e0_ed),
                    "E0_SCBA_fixed": repr(e0_fixed),
                    "E0_gated": _csv_float(
                        None if e0_gated is None else float(e0_gated)
                    ),
                    "depth_gated": str(depth),
                    "depth_oracle": str(n_orac),
                    "rel_sigma_at_stop": (
                        "" if rel_stop is None else repr(float(rel_stop))
                    ),
                    "delta_fixed": repr(delta_fixed),
                    "delta_gated": _csv_float(delta_gated),
                    "rel_fixed": repr(abs(delta_fixed) / abs(e0_ed)),
                    "rel_gated": _csv_float(rel_gated),
                    "match_grain_ok": "true" if match else "false",
                    "n_green_fixed": str(N_GREEN_FIXED),
                    "n_green_gated_total": str(n_green_gated_total(depth)),
                    "note": GATED_NOTE,
                }
            )
    return rows


def leftover_decision(
    theta_class: float | None,
    gated_rows: list[dict[str, str]],
) -> bool:
    if theta_class is None:
        return False
    test = [r for r in gated_rows if r["split"] == "test"]
    if len(test) != 6:
        raise RuntimeError("CONFLICT: expected 6 test rows")
    if any(r["match_grain_ok"] != "true" for r in test):
        return False
    mean_green = sum(int(r["n_green_gated_total"]) for r in test) / 6.0
    if not (mean_green < N_GREEN_FIXED):
        return False
    mean_gated = sum(int(r["depth_gated"]) for r in test) / 6.0
    mean_oracle = sum(int(r["depth_oracle"]) for r in test) / 6.0
    return mean_oracle < mean_gated


def evaluate_tests(
    scan_rows: list[dict[str, Any]],
    gated_rows: list[dict[str, str]],
    theta_class: float | None,
    teacher: dict[tuple[float, float], dict[str, float]],
) -> dict[str, Any]:
    indexed = index_scan(scan_rows)
    t1_fail: list[tuple[float, float]] = []
    for cell, accepted in ACCEPTED_E0.items():
        e0_64 = indexed[cell][SCBA_DEPTH]["E0"]
        want = accepted["E0_SCBA"]
        if e0_64 is None or float(e0_64) != float(want):
            t1_fail.append(cell)
        elif float(e0_64) != teacher[cell]["E0_SCBA"]:
            t1_fail.append(cell)
    t1 = {
        "name": "T1",
        "n_fail": len(t1_fail),
        "n_pass": 12 - len(t1_fail),
        "pass": len(t1_fail) == 0,
        "violations": t1_fail,
    }

    train = [r for r in gated_rows if r["split"] == "train"]
    test = [r for r in gated_rows if r["split"] == "test"]
    n_train_match = sum(1 for r in train if r["match_grain_ok"] == "true")
    n_test_match = sum(1 for r in test if r["match_grain_ok"] == "true")
    t2 = {
        "name": "T2",
        "n_fail": 6 - n_train_match if theta_class is not None else 6,
        "n_pass": n_train_match if theta_class is not None else 0,
        "pass": theta_class is not None and n_train_match == 6,
    }
    t3 = {
        "name": "T3",
        "n_fail": 6 - n_test_match,
        "n_pass": n_test_match,
        "pass": theta_class is not None and n_test_match == 6,
    }
    mean_depth_test = sum(int(r["depth_gated"]) for r in test) / 6.0
    mean_green_test = sum(int(r["n_green_gated_total"]) for r in test) / 6.0
    t4 = {
        "name": "T4",
        "n_fail": int(not (mean_green_test < N_GREEN_FIXED and mean_depth_test < 64.0)),
        "n_pass": int(mean_green_test < N_GREEN_FIXED and mean_depth_test < 64.0),
        "pass": mean_green_test < N_GREEN_FIXED and mean_depth_test < 64.0,
        "mean_depth_test": mean_depth_test,
        "mean_green_test": mean_green_test,
    }

    exceptions: list[str] = []
    by_cell = {
        (float(r["g_over_t"]), float(r["omega_over_t"])): r for r in gated_rows
    }
    for omega0 in OMEGA_OVER_T:
        gs = list(G_OVER_T)
        for g_lo, g_hi in zip(gs, gs[1:]):
            lo = int(by_cell[(g_lo, omega0)]["depth_gated"])
            hi = int(by_cell[(g_hi, omega0)]["depth_gated"])
            if hi < lo:
                exceptions.append(
                    f"fixed Omega={omega0}: depth({g_lo})={lo} > depth({g_hi})={hi}"
                )
    for g in G_OVER_T:
        omegas_decreasing = (2.0, 0.8, 0.5)
        for w_hi, w_lo in zip(omegas_decreasing, omegas_decreasing[1:]):
            a = int(by_cell[(g, w_hi)]["depth_gated"])
            b = int(by_cell[(g, w_lo)]["depth_gated"])
            if b < a:
                exceptions.append(
                    f"fixed g={g}: depth(Omega={w_hi})={a} > depth(Omega={w_lo})={b}"
                )
    n_comparisons = 3 * 3 + 4 * 2
    t5 = {
        "name": "T5",
        "n_comparisons": n_comparisons,
        "n_exceptions": len(exceptions),
        "exceptions": exceptions,
        "pass": len(exceptions) <= 1,
        "n_pass": n_comparisons - len(exceptions),
        "n_fail": len(exceptions),
    }

    t6_fail: list[tuple[float, float]] = []
    for r in gated_rows:
        cell = (float(r["g_over_t"]), float(r["omega_over_t"]))
        if r["E0_gated"] == NOT_COMPUTED:
            t6_fail.append(cell)
            continue
        e0_ed = float(r["E0_ED"])
        e0_gated = float(r["E0_gated"])
        if not (e0_ed < e0_gated < 0.0):
            t6_fail.append(cell)
    t6 = {
        "name": "T6",
        "n_fail": len(t6_fail),
        "n_pass": 12 - len(t6_fail),
        "pass": len(t6_fail) == 0,
        "violations": t6_fail,
    }
    leftover = leftover_decision(theta_class, gated_rows)
    stop_required = (not t1["pass"]) or (not t2["pass"]) or (not t6["pass"])
    return {
        "T1": t1,
        "T2": t2,
        "T3": t3,
        "T4": t4,
        "T5": t5,
        "T6": t6,
        "n_cells": 12,
        "theta_class": theta_class,
        "leftover_decision": leftover,
        "stop_required": stop_required,
        "n_train_match": n_train_match,
        "n_test_match": n_test_match,
        "mean_depth_gated_train": sum(int(r["depth_gated"]) for r in train) / 6.0,
        "mean_depth_gated_test": mean_depth_test,
        "mean_depth_oracle_test": sum(int(r["depth_oracle"]) for r in test) / 6.0,
        "mean_green_test": mean_green_test,
    }


def teacher_e0() -> dict[tuple[float, float], dict[str, float]]:
    out: dict[tuple[float, float], dict[str, float]] = {}
    for raw in load_teacher_map(TEACHER_CSV):
        cell = (float(raw["g_over_t"]), float(raw["omega_over_t"]))
        out[cell] = {
            "E0_ED": float(raw["E0_ED"]),
            "E0_Born": float(raw["E0_Born"]),
            "E0_SCBA": float(raw["E0_SCBA"]),
        }
        accepted = ACCEPTED_E0[cell]
        if out[cell]["E0_ED"] != accepted["E0_ED"]:
            raise RuntimeError(f"CONFLICT: teacher E0_ED drift at {cell}")
        if out[cell]["E0_SCBA"] != accepted["E0_SCBA"]:
            raise RuntimeError(f"CONFLICT: teacher E0_SCBA drift at {cell}")
        if raw.get("E0_Born_VC", NOT_COMPUTED) != NOT_COMPUTED:
            raise RuntimeError(f"CONFLICT: E0_Born_VC filled at {cell}")
    return out


def write_scan_csv(scan_rows: list[dict[str, Any]], path: Path = SCAN_CSV) -> Path:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCAN_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in scan_rows:
            writer.writerow(
                {
                    "g_over_t": repr(float(row["g"])),
                    "omega_over_t": repr(float(row["omega"])),
                    "depth": str(int(row["depth"])),
                    "E0": _csv_float(row["E0"]),
                    "abs_D": _csv_float(row["abs_D"]),
                    "n_crossings": str(int(row["n_crossings"])),
                    "sigma_diag_re": repr(float(np.real(row["sigma_diag"]))),
                    "sigma_diag_im": repr(float(np.imag(row["sigma_diag"]))),
                    "rel_sigma_diag": (
                        ""
                        if row["rel_sigma_diag"] is None
                        else repr(float(row["rel_sigma_diag"]))
                    ),
                    "rel_sigma_l2": (
                        ""
                        if row["rel_sigma_l2"] is None
                        else repr(float(row["rel_sigma_l2"]))
                    ),
                    "note": SCAN_NOTE,
                }
            )
    return path


def write_gated_csv(rows: list[dict[str, str]], path: Path = GATED_CSV) -> Path:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=GATED_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in GATED_FIELDS})
    return path


def write_theta_csv(verdict: dict[str, Any], path: Path = THETA_CSV) -> Path:
    theta = verdict["theta_class"]
    row = {
        "theta_class": NOT_ADMISSIBLE if theta is None else repr(float(theta)),
        "admissible": "true" if theta is not None else "false",
        "n_train_match": str(verdict["n_train_match"]),
        "n_test_match": str(verdict["n_test_match"]),
        "mean_depth_gated_train": repr(float(verdict["mean_depth_gated_train"])),
        "mean_depth_gated_test": repr(float(verdict["mean_depth_gated_test"])),
        "mean_depth_oracle_test": repr(float(verdict["mean_depth_oracle_test"])),
        "leftover_decision": "true" if verdict["leftover_decision"] else "false",
        "note": GATED_NOTE,
    }
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=THETA_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)
    return path


def write_stop(reason: str) -> None:
    STOP_PATH.write_text(
        "# Week 3 stop\n\n"
        "Thresholds were not softened. Neural escalation is not opened.\n\n"
        f"{reason.rstrip()}\n"
    )


def main() -> None:
    if not PREREGISTER_PATH.is_file():
        raise RuntimeError(
            "CONFLICT: notes/WEEK3_METRICS_PREREGISTER.md must exist on disk "
            "before writing Week 3 CSVs"
        )
    teacher = teacher_e0()
    scan_rows = scan_all_cells()
    write_scan_csv(scan_rows)
    indexed = index_scan(scan_rows)
    theta_class, _ = select_theta(indexed, teacher)
    gated_rows = build_gated_rows(indexed, teacher, theta_class)
    write_gated_csv(gated_rows)
    verdict = evaluate_tests(scan_rows, gated_rows, theta_class, teacher)
    write_theta_csv(verdict)
    if verdict["stop_required"]:
        reasons = []
        for key in ("T1", "T2", "T6"):
            if not verdict[key]["pass"]:
                reasons.append(f"{key} FAIL n_fail={verdict[key]['n_fail']}")
        write_stop("; ".join(reasons))
    print(f"wrote {SCAN_CSV}")
    print(f"wrote {GATED_CSV}")
    print(f"wrote {THETA_CSV}")
    print(f"theta_class={verdict['theta_class']!r}")
    print(f"leftover_decision={verdict['leftover_decision']}")
    for key in ("T1", "T2", "T3", "T4", "T5", "T6"):
        item = verdict[key]
        status = "PASS" if item["pass"] else "FAIL"
        extra = ""
        if key == "T4":
            extra = (
                f" mean_depth_test={item['mean_depth_test']!r}"
                f" mean_green_test={item['mean_green_test']!r}"
            )
        if key == "T5":
            extra = f" n_exceptions={item['n_exceptions']}"
            for note in item["exceptions"]:
                extra += f"\n  exception: {note}"
        print(f"{key} {status} n_pass={item['n_pass']} n_fail={item['n_fail']}{extra}")
    print(f"WEEK3_STOP_required={verdict['stop_required']}")


if __name__ == "__main__":
    main()
