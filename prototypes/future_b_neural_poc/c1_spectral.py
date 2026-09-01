# SIGNED FORMULA: xi_k=2t*(1-cos k), L=2 k in {0, pi}, tadpole OFF.
"""Candidate 1: A(ω), Z, M1 versus ED Lehmann on the frozen L=2 grid.

Does not edit holstein_ed.py or l2_periodic_pole.py. Does not train.
Does not retune θ. Depths come from Week-3 depth_gated.
Preregister notes/C1_METRICS_PREREGISTER.md must exist before any
spectral error is written.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from keldysh4ai.future_b.teacher.holstein_ed import HolsteinL2ED
from prototypes.future_b_neural_poc.build_week2_table import (
    ACCEPTED_E0,
    G_OVER_T,
    OMEGA_OVER_T,
    WEEK2_BAND_BY_CELL,
    band_of,
    coupling_lambda,
    load_teacher_map,
)
from prototypes.future_b_neural_poc.l2_periodic_pole import rainbow_sigma


T = 1.0
ETA_A = 0.05
ETA_POLE = 1.0e-4
OMEGA_MIN = -8.0
OMEGA_MAX = 4.0
N_OMEGA = 1601
SCBA_DEPTH = 64
BORN_DEPTH = 0
THETA_CLASS = 0.03
Z_MAX_STABLE = 2.0
T2_SPECTRAL_GAP = 0.05
T3_MEAN_TOL = 0.05
T3_CELL_TOL = 0.10
NOT_COMPUTED = "NOT_COMPUTED"

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

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREREGISTER_PATH = ROOT / "notes" / "C1_METRICS_PREREGISTER.md"
STOP_PATH = ROOT / "notes" / "C1_STOP.md"
TEACHER_CSV = HERE / "teacher_map_l2.csv"
WEEK3_CSV = HERE / "week3_gated_vs_fixed.csv"
DEFAULT_CSV = HERE / "c1_spectral_vs_ed.csv"

CSV_HEADER = (
    "g_over_t,omega_over_t,lambda,band,split,M_used,depth_gate,"
    "error_A_Born,error_A_SCBA64,error_A_SCBAgate,"
    "error_M1_Born,error_M1_SCBA64,error_M1_SCBAgate,"
    "Z_ED,Z_Born,Z_SCBA64,Z_SCBAgate,note"
)
HEADER_FIELDS = tuple(CSV_HEADER.split(","))
FORBIDDEN_COLUMNS = ("E0_Born_VC",)

CELL_NOTE = (
    "c1_spectral;A=-(1/pi)ImG^R;eta_A=0.05;omega=linspace(-8,4,1601);"
    "Z=int_QP A;M1=first_moment[-8,4];theta_class=0.03;"
    "depth_from=week3;E0_Born_VC=NOT_COMPUTED;no_train"
)


def _trapz(y: NDArray[np.float64], x: NDArray[np.float64]) -> float:
    trapz = getattr(np, "trapezoid", None)
    if trapz is None:
        trapz = np.trapz
    return float(trapz(y, x))


def omega_grid() -> NDArray[np.float64]:
    return np.linspace(OMEGA_MIN, OMEGA_MAX, N_OMEGA, dtype=np.float64)


def retarded_A(green: NDArray[np.complex128] | NDArray[np.float64]) -> NDArray[np.float64]:
    """A(ω) = -(1/π) Im G^R. Shared by ED, Born, SCBA64, SCBAgate."""

    return np.asarray(-np.imag(np.asarray(green, dtype=np.complex128)) / np.pi, dtype=np.float64)


def A_from_code_spectral(spectral: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert ED code array spectral=-2 Im G into A=-(1/π) Im G."""

    return np.asarray(spectral, dtype=np.float64) / (2.0 * np.pi)


def split_of(cell: tuple[float, float]) -> str:
    if cell in TRAIN_CELLS:
        return "train"
    if cell in TEST_CELLS:
        return "test"
    raise RuntimeError(f"CONFLICT: cell {cell} is not in the preregistered split")


def require_preregister() -> str:
    if not PREREGISTER_PATH.is_file():
        raise RuntimeError(
            "CONFLICT: notes/C1_METRICS_PREREGISTER.md must exist on disk "
            "before computing A(ω) or M1"
        )
    text = PREREGISTER_PATH.read_text()
    if "T1 PASS" in text or "T1 FAIL" in text:
        raise RuntimeError(
            "CONFLICT: preregister evaluated T1; rewrite as rules only"
        )
    return text


def green_rainbow(
    omega: NDArray[np.float64],
    *,
    g: float,
    omega0: float,
    depth: int,
) -> NDArray[np.complex128]:
    z = np.asarray(omega, dtype=np.complex128) + 1.0j * ETA_A
    sigma = rainbow_sigma(z, g=g, omega0=omega0, t=T, depth=int(depth))
    return np.asarray(1.0 / (z - sigma), dtype=np.complex128)


def A_rainbow(
    omega: NDArray[np.float64],
    *,
    g: float,
    omega0: float,
    depth: int,
) -> NDArray[np.float64]:
    return retarded_A(green_rainbow(omega, g=g, omega0=omega0, depth=depth))


def A_ed(
    omega: NDArray[np.float64],
    *,
    g: float,
    omega0: float,
    total_cutoff: int,
) -> NDArray[np.float64]:
    model = HolsteinL2ED(t=T, g=g, omega0=omega0, total_cutoff=int(total_cutoff))
    spec = model.lehmann_spectrum(k=0.0, omega=omega, eta=ETA_A)
    from_green = retarded_A(spec.green)
    from_code = A_from_code_spectral(spec.spectral)
    if not np.allclose(from_green, from_code, rtol=0.0, atol=1.0e-14):
        raise RuntimeError("CONFLICT: ED spectral=-2 Im G conversion mismatch")
    return from_green


def first_moment(omega: NDArray[np.float64], spectral: NDArray[np.float64]) -> float:
    num = _trapz(omega * spectral, omega)
    den = _trapz(spectral, omega)
    if not np.isfinite(num) or not np.isfinite(den) or den <= 0.0:
        raise RuntimeError("CONFLICT: M1 denominator unusable; fail closed")
    value = num / den
    if not np.isfinite(value):
        raise RuntimeError("CONFLICT: M1 is not finite; fail closed")
    return float(value)


def error_A(A_x: NDArray[np.float64], A_teacher: NDArray[np.float64]) -> float:
    den = float(np.linalg.norm(A_teacher))
    if not np.isfinite(den) or den == 0.0:
        raise RuntimeError("CONFLICT: L2(A_ED)=0; fail closed")
    value = float(np.linalg.norm(A_x - A_teacher) / den)
    if not np.isfinite(value):
        raise RuntimeError("CONFLICT: error_A is not finite; fail closed")
    return value


def error_M1(m1_x: float, m1_ed: float, omega0: float) -> float:
    if not np.isfinite(omega0) or omega0 <= 0.0:
        raise RuntimeError("CONFLICT: Ω must be positive")
    value = abs(float(m1_x) - float(m1_ed)) / float(omega0)
    if not np.isfinite(value):
        raise RuntimeError("CONFLICT: error_M1 is not finite; fail closed")
    return float(value)


def qp_weight(
    omega: NDArray[np.float64],
    spectral: NDArray[np.float64],
    *,
    e0: float,
    omega0: float,
) -> float | None:
    lo = float(e0) - float(omega0)
    hi = float(e0) + 0.5 * float(omega0)
    mask = (omega >= lo) & (omega <= hi)
    if int(np.count_nonzero(mask)) < 2:
        return None
    weight = _trapz(spectral[mask], omega[mask])
    if not np.isfinite(weight) or weight < 0.0 or weight > Z_MAX_STABLE:
        return None
    return float(weight)


def _csv_z(value: float | None) -> str:
    if value is None or not np.isfinite(value):
        return NOT_COMPUTED
    return repr(float(value))


def _finite_error(value: float, field: str, cell: tuple[float, float]) -> float:
    if not np.isfinite(value):
        raise RuntimeError(f"CONFLICT: {field} is not finite at {cell}")
    return float(value)


def load_week3_gate(path: Path = WEEK3_CSV) -> dict[tuple[float, float], dict[str, Any]]:
    if not path.is_file():
        raise RuntimeError(f"CONFLICT: Week-3 gate table not found: {path}")
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 12:
        raise RuntimeError(f"CONFLICT: expected 12 Week-3 rows, got {len(rows)}")
    out: dict[tuple[float, float], dict[str, Any]] = {}
    for raw in rows:
        cell = (float(raw["g_over_t"]), float(raw["omega_over_t"]))
        if cell in out:
            raise RuntimeError(f"CONFLICT: duplicate Week-3 cell {cell}")
        theta = float(raw["theta_class"])
        if theta != THETA_CLASS:
            raise RuntimeError(
                f"CONFLICT: Week-3 theta_class at {cell} is {theta!r}, not {THETA_CLASS}"
            )
        split = raw["split"]
        if split != split_of(cell):
            raise RuntimeError(
                f"CONFLICT: Week-3 split at {cell} is {split!r}, preregister {split_of(cell)!r}"
            )
        out[cell] = {
            "depth_gated": int(raw["depth_gated"]),
            "E0_gated": float(raw["E0_gated"]),
            "match_grain_ok": raw["match_grain_ok"] == "true",
            "split": split,
            "E0_ED": float(raw["E0_ED"]),
            "E0_SCBA_fixed": float(raw["E0_SCBA_fixed"]),
        }
    missing = set(ACCEPTED_E0) - set(out)
    if missing:
        raise RuntimeError(f"CONFLICT: Week-3 table missing cells {sorted(missing)}")
    return out


def load_teacher_index(
    path: Path = TEACHER_CSV,
) -> dict[tuple[float, float], dict[str, Any]]:
    out: dict[tuple[float, float], dict[str, Any]] = {}
    for raw in load_teacher_map(path):
        cell = (float(raw["g_over_t"]), float(raw["omega_over_t"]))
        accepted = ACCEPTED_E0[cell]
        e0_ed = float(raw["E0_ED"])
        e0_born = float(raw["E0_Born"])
        e0_scba = float(raw["E0_SCBA"])
        if e0_ed != accepted["E0_ED"] or e0_born != accepted["E0_Born"] or e0_scba != accepted["E0_SCBA"]:
            raise RuntimeError(f"CONFLICT: teacher-map E0 drift at {cell}")
        if raw.get("E0_Born_VC", NOT_COMPUTED) != NOT_COMPUTED:
            raise RuntimeError(f"CONFLICT: E0_Born_VC filled at {cell}")
        out[cell] = {
            "M_used": int(raw["M_used"]),
            "E0_ED": e0_ed,
            "E0_Born": e0_born,
            "E0_SCBA": e0_scba,
        }
    return out


def compute_cell(
    g: float,
    omega0: float,
    *,
    teacher: dict[str, Any],
    gate: dict[str, Any],
    omega: NDArray[np.float64] | None = None,
) -> dict[str, str]:
    cell = (float(g), float(omega0))
    if omega is None:
        omega = omega_grid()
    if omega.shape != (N_OMEGA,):
        raise RuntimeError("CONFLICT: ω grid is not the frozen 1601-point lock")
    lam = coupling_lambda(g, omega0)
    band = band_of(lam)
    if band != WEEK2_BAND_BY_CELL[cell]:
        raise RuntimeError(f"CONFLICT: band({cell})={band!r}")
    depth_gate = int(gate["depth_gated"])
    if depth_gate < 1 or depth_gate > SCBA_DEPTH:
        raise RuntimeError(f"CONFLICT: depth_gated={depth_gate} at {cell}")
    if float(gate["E0_ED"]) != float(teacher["E0_ED"]):
        raise RuntimeError(f"CONFLICT: Week-3 E0_ED drift at {cell}")
    if float(gate["E0_SCBA_fixed"]) != float(teacher["E0_SCBA"]):
        raise RuntimeError(f"CONFLICT: Week-3 E0_SCBA_fixed drift at {cell}")

    a_ed = A_ed(omega, g=g, omega0=omega0, total_cutoff=int(teacher["M_used"]))
    a_born = A_rainbow(omega, g=g, omega0=omega0, depth=BORN_DEPTH)
    a_64 = A_rainbow(omega, g=g, omega0=omega0, depth=SCBA_DEPTH)
    a_gate = A_rainbow(omega, g=g, omega0=omega0, depth=depth_gate)

    m1_ed = first_moment(omega, a_ed)
    m1_born = first_moment(omega, a_born)
    m1_64 = first_moment(omega, a_64)
    m1_gate = first_moment(omega, a_gate)

    err_a_born = _finite_error(error_A(a_born, a_ed), "error_A_Born", cell)
    err_a_64 = _finite_error(error_A(a_64, a_ed), "error_A_SCBA64", cell)
    err_a_gate = _finite_error(error_A(a_gate, a_ed), "error_A_SCBAgate", cell)
    err_m1_born = _finite_error(error_M1(m1_born, m1_ed, omega0), "error_M1_Born", cell)
    err_m1_64 = _finite_error(error_M1(m1_64, m1_ed, omega0), "error_M1_SCBA64", cell)
    err_m1_gate = _finite_error(error_M1(m1_gate, m1_ed, omega0), "error_M1_SCBAgate", cell)

    z_ed = qp_weight(omega, a_ed, e0=float(teacher["E0_ED"]), omega0=omega0)
    z_born = qp_weight(omega, a_born, e0=float(teacher["E0_Born"]), omega0=omega0)
    z_64 = qp_weight(omega, a_64, e0=float(teacher["E0_SCBA"]), omega0=omega0)
    z_gate = qp_weight(omega, a_gate, e0=float(gate["E0_gated"]), omega0=omega0)

    return {
        "g_over_t": repr(float(g)),
        "omega_over_t": repr(float(omega0)),
        "lambda": repr(float(lam)),
        "band": band,
        "split": split_of(cell),
        "M_used": str(int(teacher["M_used"])),
        "depth_gate": str(depth_gate),
        "error_A_Born": repr(err_a_born),
        "error_A_SCBA64": repr(err_a_64),
        "error_A_SCBAgate": repr(err_a_gate),
        "error_M1_Born": repr(err_m1_born),
        "error_M1_SCBA64": repr(err_m1_64),
        "error_M1_SCBAgate": repr(err_m1_gate),
        "Z_ED": _csv_z(z_ed),
        "Z_Born": _csv_z(z_born),
        "Z_SCBA64": _csv_z(z_64),
        "Z_SCBAgate": _csv_z(z_gate),
        "note": CELL_NOTE,
    }


def build_rows() -> list[dict[str, str]]:
    require_preregister()
    teacher = load_teacher_index()
    gate = load_week3_gate()
    omega = omega_grid()
    rows: list[dict[str, str]] = []
    for g in G_OVER_T:
        for omega0 in OMEGA_OVER_T:
            cell = (float(g), float(omega0))
            rows.append(
                compute_cell(
                    float(g),
                    float(omega0),
                    teacher=teacher[cell],
                    gate=gate[cell],
                    omega=omega,
                )
            )
    if len(rows) != 12:
        raise RuntimeError(f"CONFLICT: expected 12 C1 rows, got {len(rows)}")
    return rows


def write_csv(rows: list[dict[str, str]], path: Path = DEFAULT_CSV) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADER_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in HEADER_FIELDS})
    return path


def load_c1_rows(path: Path = DEFAULT_CSV) -> list[dict[str, str]]:
    if not path.is_file():
        raise RuntimeError(f"CONFLICT: C1 CSV not found: {path}")
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if list(rows[0].keys()) != list(HEADER_FIELDS):
        raise RuntimeError("CONFLICT: C1 CSV header drift")
    if len(rows) != 12:
        raise RuntimeError(f"CONFLICT: expected 12 C1 rows, got {len(rows)}")
    return rows


def evaluate_tests(
    rows: list[dict[str, str]],
    *,
    week3: dict[tuple[float, float], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Evaluate T1–T3 from the analysis table. Not used by the preregister."""

    if week3 is None:
        week3 = load_week3_gate()
    parsed: list[dict[str, Any]] = []
    for row in rows:
        cell = (float(row["g_over_t"]), float(row["omega_over_t"]))
        parsed.append(
            {
                "g": cell[0],
                "omega": cell[1],
                "lambda": float(row["lambda"]),
                "band": row["band"],
                "split": row["split"],
                "error_A_Born": float(row["error_A_Born"]),
                "error_A_SCBA64": float(row["error_A_SCBA64"]),
                "error_A_SCBAgate": float(row["error_A_SCBAgate"]),
                "error_M1_Born": float(row["error_M1_Born"]),
                "error_M1_SCBA64": float(row["error_M1_SCBA64"]),
                "error_M1_SCBAgate": float(row["error_M1_SCBAgate"]),
                "match_grain_ok": bool(week3[cell]["match_grain_ok"]),
                "depth_gate": int(row["depth_gate"]),
            }
        )
        for field in (
            "error_A_Born",
            "error_A_SCBA64",
            "error_A_SCBAgate",
            "error_M1_Born",
            "error_M1_SCBA64",
            "error_M1_SCBAgate",
        ):
            if not np.isfinite(parsed[-1][field]):
                raise RuntimeError(f"CONFLICT: NaN/inf in {field} at {cell}")

    by_cell = {(r["g"], r["omega"]): r for r in parsed}
    exceptions: list[str] = []
    for omega0 in OMEGA_OVER_T:
        gs = list(G_OVER_T)
        for g_lo, g_hi in zip(gs, gs[1:]):
            lo = by_cell[(g_lo, omega0)]["error_A_SCBA64"]
            hi = by_cell[(g_hi, omega0)]["error_A_SCBA64"]
            if not (hi > lo):
                exceptions.append(
                    f"fixed Omega={omega0}: error_A_SCBA64({g_lo})={lo!r} "
                    f"!< error_A_SCBA64({g_hi})={hi!r}"
                )
    omegas_decreasing = (2.0, 0.8, 0.5)
    for g in G_OVER_T:
        for w_hi, w_lo in zip(omegas_decreasing, omegas_decreasing[1:]):
            a = by_cell[(g, w_hi)]["error_A_SCBA64"]
            b = by_cell[(g, w_lo)]["error_A_SCBA64"]
            if not (b > a):
                exceptions.append(
                    f"fixed g={g}: error_A_SCBA64(Omega={w_hi})={a!r} "
                    f"!< error_A_SCBA64(Omega={w_lo})={b!r}"
                )
    n_comparisons = 3 * 3 + 4 * 2
    t1 = {
        "name": "T1",
        "n_comparisons": n_comparisons,
        "n_exceptions": len(exceptions),
        "exceptions": exceptions,
        "pass": len(exceptions) <= 1,
        "n_pass": n_comparisons - len(exceptions),
        "n_fail": len(exceptions),
    }

    leftover_cells: list[str] = []
    n_match_true = 0
    n_match_false = 0
    n_match_true_gap = 0
    n_match_false_close = 0
    for r in parsed:
        delta = r["error_A_SCBAgate"] - r["error_A_SCBA64"]
        if r["match_grain_ok"]:
            n_match_true += 1
            if delta > T2_SPECTRAL_GAP:
                n_match_true_gap += 1
                leftover_cells.append(
                    f"match_ok ({r['g']},{r['omega']}): "
                    f"error_A_gate-error_A_64={delta!r} > {T2_SPECTRAL_GAP}"
                )
        else:
            n_match_false += 1
            if abs(delta) <= T2_SPECTRAL_GAP:
                n_match_false_close += 1
                leftover_cells.append(
                    f"match_fail ({r['g']},{r['omega']}): "
                    f"|error_A_gate-error_A_64|={abs(delta)!r} <= {T2_SPECTRAL_GAP}"
                )
    t2_found = len(leftover_cells) > 0
    t2 = {
        "name": "T2",
        "found_leftover": t2_found,
        "n_leftover_cells": len(leftover_cells),
        "leftover_cells": leftover_cells,
        "n_match_true": n_match_true,
        "n_match_false": n_match_false,
        "n_match_true_gap": n_match_true_gap,
        "n_match_false_close": n_match_false_close,
        "message": (
            leftover_cells[0]
            if t2_found
            else "no extra spectral leftover on this grid"
        ),
    }

    test = [r for r in parsed if r["split"] == "test"]
    if len(test) != 6:
        raise RuntimeError(f"CONFLICT: expected 6 test rows, got {len(test)}")
    mean_gate = sum(r["error_A_SCBAgate"] for r in test) / 6.0
    mean_64 = sum(r["error_A_SCBA64"] for r in test) / 6.0
    cell_excess = [r["error_A_SCBAgate"] - r["error_A_SCBA64"] for r in test]
    worst = max(cell_excess)
    mean_ok = mean_gate <= mean_64 + T3_MEAN_TOL
    cell_ok = all(delta <= T3_CELL_TOL for delta in cell_excess)
    sufficient = mean_ok and cell_ok
    t3 = {
        "name": "T3",
        "sufficient": sufficient,
        "verdict": "PASS-SUFFICIENT" if sufficient else "FAIL-SUFFICIENT",
        "mean_test_error_A_SCBAgate": mean_gate,
        "mean_test_error_A_SCBA64": mean_64,
        "mean_gap": mean_gate - mean_64,
        "worst_test_gap": worst,
        "n_test": 6,
        "n_test_within_0p10": sum(1 for delta in cell_excess if delta <= T3_CELL_TOL),
        "mean_ok": mean_ok,
        "cell_ok": cell_ok,
    }

    stop_t1 = not bool(t1["pass"])
    stop_t3_sufficient = bool(sufficient)
    return {
        "T1": t1,
        "T2": t2,
        "T3": t3,
        "n_cells": len(parsed),
        "n_weak": sum(1 for r in parsed if r["band"] == "weak"),
        "n_intermediate": sum(1 for r in parsed if r["band"] == "intermediate"),
        "n_strong": sum(1 for r in parsed if r["band"] == "strong"),
        "stop_t1": stop_t1,
        "stop_t3_sufficient": stop_t3_sufficient,
        "candidate_1_stops": stop_t1 or stop_t3_sufficient or True,
        "no_network": True,
        "write_c1_stop": stop_t1,
    }


def main() -> None:
    rows = build_rows()
    path = write_csv(rows)
    verdict = evaluate_tests(rows)
    print(f"wrote {path}")
    print(f"n_cells={verdict['n_cells']}")
    t1 = verdict["T1"]
    print(
        f"T1 {'PASS' if t1['pass'] else 'FAIL'} "
        f"n_pass={t1['n_pass']} n_fail={t1['n_fail']} "
        f"n_comparisons={t1['n_comparisons']}"
    )
    for note in t1["exceptions"]:
        print(f"  exception: {note}")
    t2 = verdict["T2"]
    print(
        f"T2 leftover={t2['found_leftover']} "
        f"n_leftover_cells={t2['n_leftover_cells']} "
        f"message={t2['message']!r}"
    )
    t3 = verdict["T3"]
    print(
        f"T3 {t3['verdict']} mean_test_gate={t3['mean_test_error_A_SCBAgate']!r} "
        f"mean_test_64={t3['mean_test_error_A_SCBA64']!r} "
        f"mean_gap={t3['mean_gap']!r} worst_test_gap={t3['worst_test_gap']!r}"
    )
    print(f"write_c1_stop={verdict['write_c1_stop']}")
    print(f"no_network={verdict['no_network']}")


if __name__ == "__main__":
    main()
