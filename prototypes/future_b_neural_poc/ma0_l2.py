# SIGNED FORMULA: xi_k=2t*(1-cos k), L=2 k in {0, pi}, tadpole OFF.
"""Periodic L=2 Holstein MA(0) self-energy and E0 pole.

Berciu-Goodvin, Phys. Rev. B 76, 165109 (2007), Eqs. (10)-(12),
which is Goodvin-Berciu-Sawatzky, Phys. Rev. B 74, 245104 (2006),
Eqs. (17)-(19). Own module: not mixed into SCBA or Library I.

Must not import chain_scba or crossing_block.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

from keldysh4ai.future_b_atomic import exact_t0_linear_cfe, relative_l2, scba_constant_cfe
from prototypes.future_b_neural_poc.build_week2_table import ACCEPTED_E0, WEEK2_BAND_BY_CELL
from prototypes.future_b_neural_poc.l2_periodic_pole import (
    BISECTION_ITERS,
    COARSE_N,
    ETA,
    NOT_COMPUTED,
    OMEGA_MAX,
    OMEGA_MIN,
    RE_D_ZERO_TOL,
    SCBA_DEPTH,
    T,
    l2_dispersion,
)

# Frozen before twelve-cell E0_MA0. Same integer as SCBA_DEPTH; not retuned.
MA0_DEPTH = SCBA_DEPTH
WEAK_CUT = 0.08
STRONG_CUT = 0.80
T2_GAP_FRAC = 0.05
T1_GAIN = 0.10
BLOCK_ORDER = ("born", "scba", "ma0")
G_OVER_T = (0.15, 0.45, 0.75, 1.05)
OMEGA_OVER_T = (0.5, 0.8, 2.0)
STRONG_CELL = (1.05, 0.5)
ATOMIC_NU = np.geomspace(0.1, 20.0, 128)
ATOMIC_Z = 1.0j * ATOMIC_NU

CSV_HEADER = (
    "g_over_t,omega_over_t,lambda,band,E0_ED,E0_Born,E0_SCBA,E0_MA0,"
    "rel_Born,rel_SCBA,rel_MA0,best_block,lambda_if_block,note"
)
HEADER_FIELDS = tuple(CSV_HEADER.split(","))
FORBIDDEN_COLUMNS = ("E0_Born_VC",)

TEACHER_CSV = Path(__file__).resolve().parent / "teacher_map_l2.csv"
DEFAULT_CSV = Path(__file__).resolve().parent / "c2_ma0_vs_ed.csv"
PREREGISTER_PATH = Path(__file__).resolve().parents[2] / "notes" / "C2_METRICS_PREREGISTER.md"
FORMULA_PATH = Path(__file__).resolve().parents[2] / "notes" / "C2_MA0_FORMULA.md"
STOP_PATH = Path(__file__).resolve().parents[2] / "notes" / "C2_STOP.md"
REPORT_PATH = Path(__file__).resolve().parents[2] / "notes" / "C2_REPORT.md"

CELL_NOTE = (
    "c2_ma0;lambda=g^2/(2*t*Omega);source=teacher_map_l2.csv;"
    "no_recompute_ED_Born_SCBA;E0_Born_VC=NOT_COMPUTED;"
    "ma0=Berciu_PRB_76_165109_eq11_12;depth=64"
)


def _as_z(z: complex | NDArray[np.complex128] | float) -> NDArray[np.complex128]:
    return np.asarray(z, dtype=np.complex128)


def gbar0(z: complex | NDArray[np.complex128], *, t: float = T) -> NDArray[np.complex128]:
    """L=2 discrete momentum average of G0. Not the infinite-chain ḡ0."""

    sample = _as_z(z)
    xi = l2_dispersion(t=t)
    return 0.5 * (1.0 / (sample - xi[0]) + 1.0 / (sample - xi[1]))


def ma0_sigma(
    z: complex | NDArray[np.complex128],
    *,
    g: float,
    omega0: float,
    t: float = T,
    depth: int = MA0_DEPTH,
) -> NDArray[np.complex128]:
    """Σ_MA0(z) = g² A_1(z), Berciu-Goodvin 2007 Eqs. (11)-(12).

    Tail A_{N+1}(z) = (N+1) ḡ0(z-(N+1)Ω), frozen N=MA0_DEPTH.
    Tadpole off. No VC. Not a rainbow / SCBA kernel.
    """

    if depth < 0:
        raise ValueError("depth must be nonnegative")
    if not np.isfinite(g) or g < 0.0 or not np.isfinite(omega0) or omega0 <= 0.0:
        raise ValueError("invalid g or omega0")
    sample = _as_z(z)
    if g == 0.0:
        return np.zeros(sample.shape, dtype=np.complex128)
    g2 = g * g
    with np.errstate(divide="ignore", invalid="ignore"):
        a_next = (depth + 1) * gbar0(sample - (depth + 1) * omega0, t=t)
        for n in range(depth, 0, -1):
            gb = gbar0(sample - n * omega0, t=t)
            a_next = (n * gb) / (1.0 - g2 * gb * a_next)
        return g2 * a_next


def ma0_green(
    z: complex | NDArray[np.complex128],
    *,
    g: float,
    omega0: float,
    t: float = T,
    depth: int = MA0_DEPTH,
) -> NDArray[np.complex128]:
    """G(k=0,z) = 1/(z - ξ_0 - Σ_MA0(z)) with ξ_0=0."""

    sample = _as_z(z)
    return 1.0 / (sample - ma0_sigma(sample, g=g, omega0=omega0, t=t, depth=depth))


def denominator(
    omega: NDArray[np.float64] | float,
    *,
    g: float,
    omega0: float,
    t: float = T,
    eta: float = ETA,
    depth: int = MA0_DEPTH,
) -> NDArray[np.complex128]:
    """D(ω) = ω + iη - Σ_MA0(ω+iη), ξ_0=0."""

    sample = np.asarray(omega, dtype=np.float64)
    z = sample.astype(np.complex128) + 1.0j * eta
    return z - ma0_sigma(z, g=g, omega0=omega0, t=t, depth=depth)


def _bisection_root(
    *,
    g: float,
    omega0: float,
    t: float,
    depth: int,
    left: float,
    right: float,
    f_left: float,
) -> float:
    a = float(left)
    b = float(right)
    fa = float(f_left)
    for _ in range(BISECTION_ITERS):
        mid = 0.5 * (a + b)
        fmid = float(np.real(denominator(mid, g=g, omega0=omega0, t=t, depth=depth)))
        if abs(fmid) <= RE_D_ZERO_TOL:
            return float(mid)
        if fa * fmid <= 0.0:
            b = mid
        else:
            a = mid
            fa = fmid
    return float(0.5 * (a + b))


def lowest_real_pole(
    *,
    g: float,
    omega0: float,
    t: float = T,
    eta: float = ETA,
    depth: int = MA0_DEPTH,
) -> tuple[float | None, float | None, int]:
    """Lowest interior Re D=0 root, copied from l2_periodic_pole with Σ_MA0."""

    omega = np.linspace(OMEGA_MIN, OMEGA_MAX, COARSE_N, dtype=np.float64)
    real_d = np.real(denominator(omega, g=g, omega0=omega0, t=t, eta=eta, depth=depth))
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
                t=t,
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
    abs_d = float(np.abs(denominator(root, g=g, omega0=omega0, t=t, eta=eta, depth=depth)))
    return float(root), abs_d, n_crossings


@dataclass(frozen=True)
class PoleResult:
    kind: str
    g: float
    omega0: float
    depth: int
    E0: float | None
    abs_D: float | None
    n_crossings: int
    eta: float = ETA

    @property
    def csv_value(self) -> str:
        if self.E0 is None:
            return NOT_COMPUTED
        return repr(float(self.E0))


def e0_ma0(*, g: float, omega0: float, t: float = T, depth: int = MA0_DEPTH) -> PoleResult:
    energy, abs_d, n_crossings = lowest_real_pole(g=g, omega0=omega0, t=t, depth=depth)
    return PoleResult("ma0", float(g), float(omega0), int(depth), energy, abs_d, n_crossings)


def g0_pole(*, omega0: float = 0.8) -> PoleResult:
    """g=0 sanity (not a CSV row): pole must sit at 0."""

    return e0_ma0(g=0.0, omega0=omega0)


def coupling_lambda(g_over_t: float, omega_over_t: float, t: float = T) -> float:
    return (g_over_t * g_over_t) / (2.0 * t * omega_over_t)


def band_of(lam: float) -> str:
    if lam < WEAK_CUT:
        return "weak"
    if lam < STRONG_CUT:
        return "intermediate"
    return "strong"


def lambda_if_block(lam: float) -> str:
    """Frozen λ-only chooser from C2_METRICS_PREREGISTER.md."""

    if lam >= STRONG_CUT:
        return "ma0"
    return "scba"


def best_block(
    *,
    e0_ed: float,
    e0_born: float,
    e0_scba: float,
    e0_ma0: float | None,
) -> str:
    errors = {
        "born": abs(e0_born - e0_ed),
        "scba": abs(e0_scba - e0_ed),
    }
    if e0_ma0 is not None:
        errors["ma0"] = abs(e0_ma0 - e0_ed)
    ranked = sorted(errors, key=lambda name: (errors[name], BLOCK_ORDER.index(name)))
    return ranked[0]


def ma0_atomic_cells(*, depth: int = MA0_DEPTH) -> list[dict[str, float | str | bool]]:
    """t=0 check only: MA(0) vs exact 1,2,3,... versus SCBA 1,1,1,..."""

    cells: list[dict[str, float | str | bool]] = []
    for g in G_OVER_T:
        for omega0 in OMEGA_OVER_T:
            g_ma0 = np.asarray(
                ma0_green(ATOMIC_Z, g=g, omega0=omega0, t=0.0, depth=depth),
                dtype=np.complex128,
            )
            g_exact = np.asarray(
                exact_t0_linear_cfe(ATOMIC_Z, g, omega0, depth),
                dtype=np.complex128,
            )
            g_scba = np.asarray(
                scba_constant_cfe(ATOMIC_Z, g, omega0, depth),
                dtype=np.complex128,
            )
            d_ma0_exact = relative_l2(g_ma0, g_exact)
            d_scba_exact = relative_l2(g_scba, g_exact)
            d_ma0_scba = relative_l2(g_ma0, g_scba)
            cells.append(
                {
                    "g": g,
                    "omega0": omega0,
                    "relL2_MA0_vs_exact": d_ma0_exact,
                    "relL2_SCBA_vs_exact": d_scba_exact,
                    "relL2_MA0_vs_SCBA": d_ma0_scba,
                    "moves_toward_linear_cfe": bool(d_ma0_exact < d_scba_exact),
                }
            )
    return cells


def ma0_atomic_verdict(cells: list[dict[str, float | str | bool]] | None = None) -> dict[str, object]:
    if cells is None:
        cells = ma0_atomic_cells()
    flags = [bool(cell["moves_toward_linear_cfe"]) for cell in cells]
    passed = bool(flags) and all(flags)
    return {
        "MA0_ATOMIC": "PASS" if passed else "FAIL",
        "n_cells": len(cells),
        "n_toward_linear": int(sum(flags)),
        "cells": cells,
        "depth": MA0_DEPTH,
        "hopping": 0.0,
        "reference": "exact_t0_linear_cfe 1,2,3,... vs scba_constant_cfe 1,1,1,...",
    }


def load_teacher_map(path: Path = TEACHER_CSV) -> list[dict[str, str]]:
    if not path.is_file():
        raise RuntimeError(f"CONFLICT: teacher map not found: {path}")
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 12:
        raise RuntimeError(f"CONFLICT: expected 12 teacher-map rows, got {len(rows)}")
    return rows


def _parse_float(token: str, field: str, cell: tuple[float, float]) -> float:
    if token in (NOT_COMPUTED, ""):
        raise RuntimeError(
            f"CONFLICT: {field} missing for cell {cell}; C2 copies teacher "
            "E0_ED/E0_Born/E0_SCBA, not invented numbers."
        )
    return float(token)


def analyze_cells(
    teacher_rows: list[dict[str, str]],
    ma0_energies: dict[tuple[float, float], float | None],
) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    seen: set[tuple[float, float]] = set()
    for raw in teacher_rows:
        g = float(raw["g_over_t"])
        omega = float(raw["omega_over_t"])
        cell = (g, omega)
        if cell not in ACCEPTED_E0:
            raise RuntimeError(f"CONFLICT: unexpected teacher-map cell {cell}")
        if cell in seen:
            raise RuntimeError(f"CONFLICT: duplicate teacher-map cell {cell}")
        seen.add(cell)
        e0_ed = _parse_float(raw["E0_ED"], "E0_ED", cell)
        e0_born = _parse_float(raw["E0_Born"], "E0_Born", cell)
        e0_scba = _parse_float(raw["E0_SCBA"], "E0_SCBA", cell)
        accepted = ACCEPTED_E0[cell]
        for name, got, want in (
            ("E0_ED", e0_ed, accepted["E0_ED"]),
            ("E0_Born", e0_born, accepted["E0_Born"]),
            ("E0_SCBA", e0_scba, accepted["E0_SCBA"]),
        ):
            if got != want:
                raise RuntimeError(
                    f"CONFLICT: {name} at {cell} is {got!r}, accepted {want!r}. "
                    "Do not invent a replacement."
                )
        if raw.get("E0_Born_VC", NOT_COMPUTED) != NOT_COMPUTED:
            raise RuntimeError(f"CONFLICT: E0_Born_VC is not NOT_COMPUTED at {cell}")
        lam = coupling_lambda(g, omega)
        band = band_of(lam)
        if band != WEEK2_BAND_BY_CELL[cell]:
            raise RuntimeError(
                f"CONFLICT: band({cell})={band!r} != preregistered "
                f"{WEEK2_BAND_BY_CELL[cell]!r}"
            )
        abs_ed = abs(e0_ed)
        if abs_ed == 0.0:
            raise RuntimeError(f"CONFLICT: |E0_ED|=0 at {cell}; rel_X undefined")
        e0_ma0 = ma0_energies[cell]
        rel_born = abs(e0_born - e0_ed) / abs_ed
        rel_scba = abs(e0_scba - e0_ed) / abs_ed
        if e0_ma0 is None:
            rel_ma0_token = NOT_COMPUTED
            e0_ma0_token = NOT_COMPUTED
        else:
            rel_ma0_token = repr(abs(e0_ma0 - e0_ed) / abs_ed)
            e0_ma0_token = repr(float(e0_ma0))
        winner = best_block(
            e0_ed=e0_ed,
            e0_born=e0_born,
            e0_scba=e0_scba,
            e0_ma0=e0_ma0,
        )
        out.append(
            {
                "g_over_t": repr(g),
                "omega_over_t": repr(omega),
                "lambda": repr(lam),
                "band": band,
                "E0_ED": repr(e0_ed),
                "E0_Born": repr(e0_born),
                "E0_SCBA": repr(e0_scba),
                "E0_MA0": e0_ma0_token,
                "rel_Born": repr(rel_born),
                "rel_SCBA": repr(rel_scba),
                "rel_MA0": rel_ma0_token,
                "best_block": winner,
                "lambda_if_block": lambda_if_block(lam),
                "note": CELL_NOTE,
            }
        )
    missing = set(ACCEPTED_E0) - seen
    if missing:
        raise RuntimeError(f"CONFLICT: teacher map missing cells {sorted(missing)}")
    order = {
        (g, omega): i
        for i, (g, omega) in enumerate((g, omega) for g in G_OVER_T for omega in OMEGA_OVER_T)
    }
    out.sort(key=lambda row: order[(float(row["g_over_t"]), float(row["omega_over_t"]))])
    return out


def compute_ma0_energies() -> dict[tuple[float, float], float | None]:
    energies: dict[tuple[float, float], float | None] = {}
    for g in G_OVER_T:
        for omega0 in OMEGA_OVER_T:
            result = e0_ma0(g=g, omega0=omega0)
            energies[(g, omega0)] = result.E0
    return energies


def write_c2_csv(rows: list[dict[str, str]], path: Path = DEFAULT_CSV) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADER_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in HEADER_FIELDS})
    return path


def _block_energy(row: dict[str, str], name: str) -> float | None:
    token = {"born": row["E0_Born"], "scba": row["E0_SCBA"], "ma0": row["E0_MA0"]}[name]
    if token == NOT_COMPUTED:
        return None
    return float(token)


def evaluate_tests(
    rows: list[dict[str, str]],
    *,
    atomic: dict[str, object],
) -> dict[str, object]:
    """Evaluate C2-T1–T3 from the analysis table. Not used by the preregister."""

    parsed = []
    for row in rows:
        e0_ma0_token = row["E0_MA0"]
        parsed.append(
            {
                "g": float(row["g_over_t"]),
                "omega": float(row["omega_over_t"]),
                "lambda": float(row["lambda"]),
                "band": row["band"],
                "E0_ED": float(row["E0_ED"]),
                "E0_Born": float(row["E0_Born"]),
                "E0_SCBA": float(row["E0_SCBA"]),
                "E0_MA0": None if e0_ma0_token == NOT_COMPUTED else float(e0_ma0_token),
                "rel_Born": float(row["rel_Born"]),
                "rel_SCBA": float(row["rel_SCBA"]),
                "rel_MA0": None if row["rel_MA0"] == NOT_COMPUTED else float(row["rel_MA0"]),
                "best_block": row["best_block"],
                "lambda_if_block": row["lambda_if_block"],
            }
        )

    atomic_pass = atomic["MA0_ATOMIC"] == "PASS"
    strong = [r for r in parsed if (r["g"], r["omega"]) == STRONG_CELL]
    if len(strong) != 1:
        raise RuntimeError(f"CONFLICT: expected one strong cell, got {len(strong)}")
    strong_row = strong[0]
    rel_ma0 = strong_row["rel_MA0"]
    rel_scba = strong_row["rel_SCBA"]
    t1_numeric = (
        rel_ma0 is not None
        and strong_row["E0_MA0"] is not None
        and rel_ma0 <= rel_scba - T1_GAIN
    )
    t1 = {
        "name": "C2-T1",
        "pass": bool(t1_numeric and atomic_pass),
        "numeric_gain": bool(t1_numeric),
        "MA0_ATOMIC": atomic["MA0_ATOMIC"],
        "rel_MA0": rel_ma0,
        "rel_SCBA": rel_scba,
        "threshold": None if rel_scba is None else rel_scba - T1_GAIN,
        "cell": STRONG_CELL,
    }

    t2_cells = []
    for row, raw in zip(parsed, rows):
        best = row["best_block"]
        chosen = row["lambda_if_block"]
        if best == chosen:
            continue
        e_best = _block_energy(raw, best)
        e_chosen = _block_energy(raw, chosen)
        if e_best is None or e_chosen is None:
            continue
        gap = abs(e_best - e_chosen)
        if gap > T2_GAP_FRAC * abs(row["E0_ED"]):
            t2_cells.append(
                {
                    "cell": (row["g"], row["omega"]),
                    "best_block": best,
                    "lambda_if_block": chosen,
                    "gap": gap,
                    "gap_frac": gap / abs(row["E0_ED"]),
                }
            )
    t2 = {
        "name": "C2-T2",
        "count": len(t2_cells),
        "pass": len(t2_cells) > 0,
        "cells": t2_cells,
    }

    t3_fail = []
    for row in parsed:
        if row["E0_MA0"] is None:
            t3_fail.append((row["g"], row["omega"], "NOT_COMPUTED"))
            continue
        if not (row["E0_MA0"] < 0.0):
            t3_fail.append((row["g"], row["omega"], row["E0_MA0"]))
    g0 = g0_pole(omega0=0.8)
    g0_ok = g0.E0 is not None and abs(float(g0.E0)) <= 1.0e-12
    t3 = {
        "name": "C2-T3",
        "pass": len(t3_fail) == 0 and g0_ok,
        "n_fail": len(t3_fail),
        "g0_E0": g0.E0,
        "g0_ok": g0_ok,
        "failures": t3_fail,
    }

    candidate2_stop = (not t1["pass"]) or (not t3["pass"]) or (t2["count"] == 0)
    if not t1["pass"]:
        stop_reason = "T1"
    elif not t3["pass"]:
        stop_reason = "T3"
    elif t2["count"] == 0:
        stop_reason = "T2"
    else:
        stop_reason = None
    return {
        "n_cells": len(parsed),
        "T1": t1,
        "T2": t2,
        "T3": t3,
        "MA0_ATOMIC": atomic["MA0_ATOMIC"],
        "candidate2_stop": candidate2_stop,
        "stop_reason": stop_reason,
        "rows": parsed,
    }


def main() -> None:
    if not PREREGISTER_PATH.is_file() or not FORMULA_PATH.is_file():
        raise RuntimeError("CONFLICT: preregister and formula notes must exist before E0_MA0")
    atomic = ma0_atomic_verdict()
    print(f"MA0_ATOMIC={atomic['MA0_ATOMIC']} toward_linear={atomic['n_toward_linear']}/{atomic['n_cells']}")
    energies = compute_ma0_energies()
    rows = analyze_cells(load_teacher_map(), energies)
    path = write_c2_csv(rows)
    print(f"wrote {path}")
    verdict = evaluate_tests(rows, atomic=atomic)
    t1 = verdict["T1"]
    t2 = verdict["T2"]
    t3 = verdict["T3"]
    print(
        f"T1={'PASS' if t1['pass'] else 'FAIL'} "
        f"rel_MA0={t1['rel_MA0']} rel_SCBA={t1['rel_SCBA']}"
    )
    print(f"T2={'PASS' if t2['pass'] else 'FAIL'} count={t2['count']}")
    print(f"T3={'PASS' if t3['pass'] else 'FAIL'} g0={t3['g0_E0']}")
    print(f"candidate2_stop={verdict['candidate2_stop']} reason={verdict['stop_reason']}")


if __name__ == "__main__":
    main()
