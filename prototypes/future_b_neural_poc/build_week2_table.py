# SIGNED FORMULA: H=2t*n-t*sum_PBC(c^dag c+h.c.)+Omega*b^dag*b+g*n*(b+b^dag), xi_k=2t*(1-cos k).
"""Week 2 analysis table: Born/SCBA vs ED on the frozen L=2 map.

Reads ``teacher_map_l2.csv`` as immutable input. Does not recompute ED,
Born, or SCBA. Does not train, call chain_scba.py, invent E0_Born_VC,
or start Week 3. Bands follow notes/WEEK2_METRICS_PREREGISTER.md.
"""

from __future__ import annotations

import csv
from pathlib import Path

T = 1.0
G_OVER_T = (0.15, 0.45, 0.75, 1.05)
OMEGA_OVER_T = (0.5, 0.8, 2.0)
WEAK_CUT = 0.08
STRONG_CUT = 0.80

CSV_HEADER = (
    "g_over_t,omega_over_t,lambda,band,E0_ED,E0_Born,E0_SCBA,"
    "delta_Born,delta_SCBA,rel_Born,rel_SCBA,scba_beats_born,note"
)
HEADER_FIELDS = tuple(CSV_HEADER.split(","))
FORBIDDEN_COLUMNS = ("E0_Born_VC",)

TEACHER_CSV = Path(__file__).resolve().parent / "teacher_map_l2.csv"
DEFAULT_CSV = Path(__file__).resolve().parent / "week2_born_scba_vs_ed.csv"
PREREGISTER_PATH = (
    Path(__file__).resolve().parents[2] / "notes" / "WEEK2_METRICS_PREREGISTER.md"
)

ACCEPTED_E0 = {
    (0.15, 0.5): {
        "E0_ED": -0.025011195833357803,
        "E0_Born": -0.023957948465816996,
        "E0_SCBA": -0.024501906084842373,
    },
    (0.15, 0.8): {
        "E0_ED": -0.016411995814594443,
        "E0_Born": -0.016120631607613123,
        "E0_SCBA": -0.016275845958501886,
    },
    (0.15, 2.0): {
        "E0_ED": -0.0075011729011287805,
        "E0_Born": -0.007476716472912221,
        "E0_SCBA": -0.0074897813038690775,
    },
    (0.45, 0.5): {
        "E0_ED": -0.22597056572509017,
        "E0_Born": -0.17227776087113264,
        "E0_SCBA": -0.19525771830517596,
    },
    (0.45, 0.8): {
        "E0_ED": -0.14813779739257232,
        "E0_Born": -0.1294724791890623,
        "E0_SCBA": -0.13849636859403075,
    },
    (0.45, 2.0): {
        "E0_ED": -0.06759567149368771,
        "E0_Born": -0.0657068991711276,
        "E0_SCBA": -0.06669421783604758,
    },
    (0.75, 0.5): {
        "E0_ED": -0.6337558805587407,
        "E0_Born": -0.37799064297560836,
        "E0_SCBA": -0.46706572919129363,
    },
    (0.75, 0.8): {
        "E0_ED": -0.4141522353421741,
        "E0_Born": -0.3087230871959763,
        "E0_SCBA": -0.35323367525640026,
    },
    (0.75, 2.0): {
        "E0_ED": -0.18824875576961658,
        "E0_Born": -0.1748658676873891,
        "E0_SCBA": -0.18158837132352318,
    },
    (1.05, 0.5): {
        "E0_ED": -1.2711554105515426,
        "E0_Born": -0.6062574864800551,
        "E0_SCBA": -0.7962863700566889,
    },
    (1.05, 0.8): {
        "E0_ED": -0.821257338852671,
        "E0_Born": -0.5209224545267934,
        "E0_SCBA": -0.6309483230714251,
    },
    (1.05, 2.0): {
        "E0_ED": -0.3704389369409427,
        "E0_Born": -0.32432865695364266,
        "E0_SCBA": -0.3462997255144582,
    },
}

WEEK2_BAND_BY_CELL = {
    (0.15, 0.5): "weak",
    (0.15, 0.8): "weak",
    (0.15, 2.0): "weak",
    (0.45, 0.5): "intermediate",
    (0.45, 0.8): "intermediate",
    (0.45, 2.0): "weak",
    (0.75, 0.5): "intermediate",
    (0.75, 0.8): "intermediate",
    (0.75, 2.0): "intermediate",
    (1.05, 0.5): "strong",
    (1.05, 0.8): "intermediate",
    (1.05, 2.0): "intermediate",
}

CELL_NOTE = (
    "week2_band;lambda=g^2/(2*t*Omega);source=teacher_map_l2.csv;"
    "no_recompute;E0_Born_VC=NOT_COMPUTED"
)


def coupling_lambda(g_over_t: float, omega_over_t: float, t: float = T) -> float:
    return (g_over_t * g_over_t) / (2.0 * t * omega_over_t)


def band_of(lam: float) -> str:
    if lam < WEAK_CUT:
        return "weak"
    if lam < STRONG_CUT:
        return "intermediate"
    return "strong"


def _parse_float(token: str, field: str, cell: tuple[float, float]) -> float:
    if token in ("NOT_COMPUTED", ""):
        raise RuntimeError(
            f"CONFLICT: {field} missing for cell {cell}; Week 2 analysis "
            "requires real teacher-map energies, not invented numbers."
        )
    return float(token)


def load_teacher_map(path: Path = TEACHER_CSV) -> list[dict[str, str]]:
    if not path.is_file():
        raise RuntimeError(f"CONFLICT: teacher map not found: {path}")
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 12:
        raise RuntimeError(f"CONFLICT: expected 12 teacher-map rows, got {len(rows)}")
    return rows


def analyze_teacher_rows(teacher_rows: list[dict[str, str]]) -> list[dict[str, str]]:
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
        if raw.get("E0_Born_VC", "NOT_COMPUTED") != "NOT_COMPUTED":
            raise RuntimeError(
                f"CONFLICT: E0_Born_VC is not NOT_COMPUTED at {cell}"
            )
        lam = coupling_lambda(g, omega)
        band = band_of(lam)
        if band != WEEK2_BAND_BY_CELL[cell]:
            raise RuntimeError(
                f"CONFLICT: band({cell})={band!r} != preregistered "
                f"{WEEK2_BAND_BY_CELL[cell]!r}"
            )
        delta_born = e0_born - e0_ed
        delta_scba = e0_scba - e0_ed
        abs_ed = abs(e0_ed)
        if abs_ed == 0.0:
            raise RuntimeError(f"CONFLICT: |E0_ED|=0 at {cell}; rel_X undefined")
        rel_born = abs(delta_born) / abs_ed
        rel_scba = abs(delta_scba) / abs_ed
        beats = abs(delta_scba) < abs(delta_born)
        out.append(
            {
                "g_over_t": repr(g),
                "omega_over_t": repr(omega),
                "lambda": repr(lam),
                "band": band,
                "E0_ED": repr(e0_ed),
                "E0_Born": repr(e0_born),
                "E0_SCBA": repr(e0_scba),
                "delta_Born": repr(delta_born),
                "delta_SCBA": repr(delta_scba),
                "rel_Born": repr(rel_born),
                "rel_SCBA": repr(rel_scba),
                "scba_beats_born": "true" if beats else "false",
                "note": CELL_NOTE,
            }
        )
    missing = set(ACCEPTED_E0) - seen
    if missing:
        raise RuntimeError(f"CONFLICT: teacher map missing cells {sorted(missing)}")
    order = {(g, omega): i for i, (g, omega) in enumerate(
        (g, omega) for g in G_OVER_T for omega in OMEGA_OVER_T
    )}
    out.sort(key=lambda row: order[(float(row["g_over_t"]), float(row["omega_over_t"]))])
    return out


def write_week2_csv(rows: list[dict[str, str]], path: Path = DEFAULT_CSV) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADER_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in HEADER_FIELDS})
    return path


def evaluate_tests(rows: list[dict[str, str]]) -> dict[str, object]:
    """Evaluate T1–T4 from the analysis table. Not used by the preregister."""
    parsed = []
    for row in rows:
        parsed.append(
            {
                "g": float(row["g_over_t"]),
                "omega": float(row["omega_over_t"]),
                "lambda": float(row["lambda"]),
                "band": row["band"],
                "E0_ED": float(row["E0_ED"]),
                "E0_Born": float(row["E0_Born"]),
                "E0_SCBA": float(row["E0_SCBA"]),
                "delta_Born": float(row["delta_Born"]),
                "delta_SCBA": float(row["delta_SCBA"]),
                "rel_Born": float(row["rel_Born"]),
                "rel_SCBA": float(row["rel_SCBA"]),
                "scba_beats_born": row["scba_beats_born"] == "true",
            }
        )

    weak = [r for r in parsed if r["lambda"] < WEAK_CUT]
    t1_violations = [
        r for r in weak if not (abs(r["delta_SCBA"]) < abs(r["delta_Born"]))
    ]
    t1 = {
        "name": "T1",
        "n_weak": len(weak),
        "n_pass": len(weak) - len(t1_violations),
        "n_fail": len(t1_violations),
        "pass": len(weak) == 4 and len(t1_violations) == 0,
        "violations": [(r["g"], r["omega"]) for r in t1_violations],
    }

    strong = [r for r in parsed if r["g"] == 1.05 and r["omega"] == 0.5]
    if len(strong) != 1:
        raise RuntimeError(f"CONFLICT: expected one strong cell, got {len(strong)}")
    rel_strong = strong[0]["rel_SCBA"]
    t2 = {
        "name": "T2",
        "n_strong": 1,
        "rel_SCBA": rel_strong,
        "threshold": 0.20,
        "n_pass": int(rel_strong >= 0.20),
        "n_fail": int(rel_strong < 0.20),
        "pass": rel_strong >= 0.20,
    }

    exceptions: list[str] = []
    by_cell = {(r["g"], r["omega"]): r for r in parsed}
    for omega in OMEGA_OVER_T:
        gs = list(G_OVER_T)
        for g_lo, g_hi in zip(gs, gs[1:]):
            lo = by_cell[(g_lo, omega)]
            hi = by_cell[(g_hi, omega)]
            if not (hi["rel_SCBA"] > lo["rel_SCBA"]):
                exceptions.append(
                    f"fixed Omega={omega}: rel_SCBA({g_lo})={lo['rel_SCBA']!r} "
                    f"!< rel_SCBA({g_hi})={hi['rel_SCBA']!r}"
                )
    for g in G_OVER_T:
        omegas_decreasing = (2.0, 0.8, 0.5)
        for w_hi, w_lo in zip(omegas_decreasing, omegas_decreasing[1:]):
            a = by_cell[(g, w_hi)]
            b = by_cell[(g, w_lo)]
            if not (b["rel_SCBA"] > a["rel_SCBA"]):
                exceptions.append(
                    f"fixed g={g}: rel_SCBA(Omega={w_hi})={a['rel_SCBA']!r} "
                    f"!< rel_SCBA(Omega={w_lo})={b['rel_SCBA']!r}"
                )
    n_pairs_omega = 3 * 3  # 3 omega values × 3 consecutive g pairs
    n_pairs_g = 4 * 2      # 4 g values × 2 consecutive omega-down pairs
    t3 = {
        "name": "T3",
        "n_comparisons": n_pairs_omega + n_pairs_g,
        "n_exceptions": len(exceptions),
        "exceptions": exceptions,
        "pass": len(exceptions) <= 1,
        "n_pass": (n_pairs_omega + n_pairs_g) - len(exceptions),
        "n_fail": len(exceptions),
    }

    t4_violations = []
    for r in parsed:
        ed, scba, born = r["E0_ED"], r["E0_SCBA"], r["E0_Born"]
        if not (ed < scba < born < 0.0):
            t4_violations.append((r["g"], r["omega"], ed, scba, born))
    t4 = {
        "name": "T4",
        "n_cells": len(parsed),
        "n_pass": len(parsed) - len(t4_violations),
        "n_fail": len(t4_violations),
        "pass": len(t4_violations) == 0,
        "violations": t4_violations,
    }

    beats_count = sum(1 for r in parsed if r["scba_beats_born"])
    return {
        "T1": t1,
        "T2": t2,
        "T3": t3,
        "T4": t4,
        "n_cells": len(parsed),
        "n_scba_beats_born": beats_count,
        "n_weak": len(weak),
        "n_intermediate": sum(1 for r in parsed if r["band"] == "intermediate"),
        "n_strong": sum(1 for r in parsed if r["band"] == "strong"),
        "strong_rel_SCBA": rel_strong,
        "stop_required": (not t1["pass"]) or (not t4["pass"]),
    }


def main() -> None:
    if not PREREGISTER_PATH.is_file():
        raise RuntimeError(
            "CONFLICT: notes/WEEK2_METRICS_PREREGISTER.md must exist on disk "
            "before writing week2_born_scba_vs_ed.csv"
        )
    teacher_rows = load_teacher_map()
    rows = analyze_teacher_rows(teacher_rows)
    path = write_week2_csv(rows)
    verdict = evaluate_tests(rows)
    print(f"wrote {path}")
    print(f"n_cells={verdict['n_cells']}")
    print(
        f"bands weak={verdict['n_weak']} "
        f"intermediate={verdict['n_intermediate']} "
        f"strong={verdict['n_strong']}"
    )
    print(f"scba_beats_born {verdict['n_scba_beats_born']}/12")
    for key in ("T1", "T2", "T3", "T4"):
        item = verdict[key]
        status = "PASS" if item["pass"] else "FAIL"
        print(f"{key} {status} n_pass={item['n_pass']} n_fail={item['n_fail']}")
        if key == "T2":
            print(f"  rel_SCBA(1.05,0.5)={item['rel_SCBA']!r} threshold={item['threshold']}")
        if key == "T3":
            for note in item["exceptions"]:
                print(f"  exception: {note}")
    print(f"WEEK2_STOP_required={verdict['stop_required']}")


if __name__ == "__main__":
    main()
