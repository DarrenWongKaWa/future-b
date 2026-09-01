# SIGNED FORMULA: H=2t*n-t*sum_PBC(c^dag c+h.c.)+Omega*b^dag*b+g*n*(b+b^dag), xi_k=2t*(1-cos k).
"""Build the frozen L=2 Holstein teacher-map CSV.

E0_ED is the periodic L=2 total-phonon-cutoff ground energy from
``keldysh4ai.future_b.teacher.holstein_ed``. E0_Born and E0_SCBA come
from the dedicated same-origin L=2 pole extractor, not from
chain_scba.py and not from n_k>=4 Library I. E0_Born_VC stays
NOT_COMPUTED. This builder does not train, mix libraries, or start
Week 2.
"""

from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from keldysh4ai.future_b.teacher.holstein_ed import (
    HolsteinL2ED,
    cutoff_scan,
    first_converged_cutoff,
)

from prototypes.future_b_neural_poc.l2_periodic_pole import (
    ETA,
    SCBA_DEPTH,
    e0_born,
    e0_scba,
    g0_poles,
)

NOT_COMPUTED = "NOT_COMPUTED"
CSV_HEADER = (
    "g_over_t,omega_over_t,M_used,dim,E0_ED,DeltaE_cutoff,"
    "E0_Born,E0_SCBA,E0_Born_VC,note"
)
HEADER_FIELDS = tuple(CSV_HEADER.split(","))
G_OVER_T = (0.15, 0.45, 0.75, 1.05)
OMEGA_OVER_T = (0.5, 0.8, 2.0)
T = 1.0
THRESHOLD = 1.0e-4
MAX_EVEN_M_DEFAULT = 20
ACCEPTED_STRONG_CORNER = {
    "g_over_t": 1.05,
    "omega_over_t": 0.5,
    "M_used": 14,
    "E0_ED": -1.2711554105515426,
    "DeltaE_cutoff": 3.689030338893673e-05,
}

# Preregistered in notes/WEEK1_LABELS_PREREGISTER.md (formula of g, Omega, t only).
LABEL_BY_CELL = {
    (0.15, 0.5): "weak",
    (0.15, 0.8): "weak",
    (0.15, 2.0): "weak",
    (0.45, 0.5): "intermediate",
    (0.45, 0.8): "weak",
    (0.45, 2.0): "weak",
    (0.75, 0.5): "intermediate",
    (0.75, 0.8): "intermediate",
    (0.75, 2.0): "weak",
    (1.05, 0.5): "strong",
    (1.05, 0.8): "intermediate",
    (1.05, 2.0): "intermediate",
}

DEFAULT_CSV = (
    Path(__file__).resolve().parent / "teacher_map_l2.csv"
)
DEFAULT_DIAGNOSTICS = (
    Path(__file__).resolve().parent / "l2_pole_diagnostics.json"
)
EXTRACTOR_NOTE = (
    "extractor=periodic_L2_k=0,pi;"
    f"eta={ETA};"
    f"scba_depth={SCBA_DEPTH};"
    "E0=lowest_ReD_root;"
    "E0_Born_VC=NOT_COMPUTED"
)


@dataclass(frozen=True)
class TeacherRow:
    g_over_t: float
    omega_over_t: float
    M_used: int
    dim: int
    E0_ED: float
    DeltaE_cutoff: float
    E0_Born: str
    E0_SCBA: str
    E0_Born_VC: str
    note: str
    label: str
    matched_accepted_E0: bool | None
    scan_extended_past_M20: bool
    born_abs_D: float | None
    scba_abs_D: float | None
    born_n_crossings: int
    scba_n_crossings: int


def _lambda(g: float, omega: float, t: float = T) -> float:
    return (g * g) / (2.0 * t * omega)


def _label(g: float, omega: float) -> str:
    key = (float(g), float(omega))
    return LABEL_BY_CELL[key]


def g0_ground_energy(*, omega0: float = 0.8, total_cutoff: int = 4) -> float:
    """g=0 sanity (not a 13th CSV row): E0 must be 0 at the code origin."""

    model = HolsteinL2ED(t=T, g=0.0, omega0=omega0, total_cutoff=total_cutoff)
    return float(model.ground_energy())


def _scan_until_converged(g: float, omega0: float) -> tuple:
    max_m = MAX_EVEN_M_DEFAULT
    extended = False
    while True:
        rows = cutoff_scan(
            t=T,
            g=g,
            omega0=omega0,
            cutoffs=range(0, max_m + 1, 2),
            threshold=THRESHOLD,
        )
        m_used = first_converged_cutoff(rows)
        if m_used is not None:
            chosen = next(row for row in rows if row.M == m_used)
            return chosen, rows, extended
        if max_m >= 40:
            raise RuntimeError(
                f"no even M<= {max_m} with |E0(M)-E0(M-2)| < {THRESHOLD} t "
                f"for g/t={g}, Omega/t={omega0}"
            )
        max_m += 10
        extended = True


def compute_cell(g: float, omega0: float) -> TeacherRow:
    chosen, _rows, extended = _scan_until_converged(g, omega0)
    if chosen.delta_E0_vs_M_minus_2 is None:
        raise RuntimeError("converged row missing DeltaE_cutoff")
    matched: bool | None = None
    if g == ACCEPTED_STRONG_CORNER["g_over_t"] and omega0 == ACCEPTED_STRONG_CORNER["omega_over_t"]:
        matched = (
            chosen.M == ACCEPTED_STRONG_CORNER["M_used"]
            and chosen.E0 == ACCEPTED_STRONG_CORNER["E0_ED"]
        )
        if not matched:
            raise RuntimeError(
                "strong-corner E0/M did not match accepted "
                f"E0={ACCEPTED_STRONG_CORNER['E0_ED']}, M=14; "
                f"got E0={chosen.E0!r}, M={chosen.M}"
            )
    label = _label(g, omega0)
    born = e0_born(g=g, omega0=omega0)
    scba = e0_scba(g=g, omega0=omega0)
    note_parts = [
        f"label={label}",
        f"lambda={_lambda(g, omega0):.8g}",
        "cutoff_kind=total_phonon_M",
        "origin=xi_k=2t(1-cos k)",
    ]
    if matched is not None:
        note_parts.append(f"matched_accepted_E0={matched}")
    if extended:
        note_parts.append("scan_extended_past_M20=True")
    note_parts.append(EXTRACTOR_NOTE)
    if born.E0 is None:
        note_parts.append("E0_Born=NOT_COMPUTED:no_interior_ReD_root")
    if scba.E0 is None:
        note_parts.append("E0_SCBA=NOT_COMPUTED:no_interior_ReD_root")
    return TeacherRow(
        g_over_t=float(g),
        omega_over_t=float(omega0),
        M_used=int(chosen.M),
        dim=int(chosen.dimension),
        E0_ED=float(chosen.E0),
        DeltaE_cutoff=float(chosen.delta_E0_vs_M_minus_2),
        E0_Born=born.csv_value,
        E0_SCBA=scba.csv_value,
        E0_Born_VC=NOT_COMPUTED,
        note=";".join(note_parts),
        label=label,
        matched_accepted_E0=matched,
        scan_extended_past_M20=extended,
        born_abs_D=born.abs_D,
        scba_abs_D=scba.abs_D,
        born_n_crossings=born.n_crossings,
        scba_n_crossings=scba.n_crossings,
    )


def compute_table() -> tuple[TeacherRow, ...]:
    return tuple(compute_cell(g, omega0) for g in G_OVER_T for omega0 in OMEGA_OVER_T)


def _format_row(row: TeacherRow) -> dict[str, str]:
    return {
        "g_over_t": repr(row.g_over_t),
        "omega_over_t": repr(row.omega_over_t),
        "M_used": str(row.M_used),
        "dim": str(row.dim),
        "E0_ED": repr(row.E0_ED),
        "DeltaE_cutoff": repr(row.DeltaE_cutoff),
        "E0_Born": row.E0_Born,
        "E0_SCBA": row.E0_SCBA,
        "E0_Born_VC": row.E0_Born_VC,
        "note": row.note,
    }


def write_teacher_map(
    path: Path | None = None,
    rows: tuple[TeacherRow, ...] | None = None,
) -> tuple[TeacherRow, ...]:
    path = DEFAULT_CSV if path is None else Path(path)
    rows = compute_table() if rows is None else rows
    if len(rows) != 12:
        raise RuntimeError(f"expected 12 cells, got {len(rows)}")
    for row in rows:
        if (row.M_used + 1) * (row.M_used + 2) != row.dim:
            raise RuntimeError("dim != (M+1)(M+2)")
        if row.E0_Born_VC != NOT_COMPUTED:
            raise RuntimeError("E0_Born_VC is not defined by this extractor")
        for value, name in ((row.E0_Born, "E0_Born"), (row.E0_SCBA, "E0_SCBA")):
            if value == NOT_COMPUTED:
                continue
            number = float(value)
            if number != number or number in (float("inf"), float("-inf")):
                raise RuntimeError(f"{name} is not finite")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADER_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(_format_row(row))
    written_header = path.read_text().splitlines()[0]
    if written_header != CSV_HEADER:
        raise RuntimeError(f"header mismatch: {written_header!r}")
    return rows


def write_diagnostics(
    rows: tuple[TeacherRow, ...],
    path: Path | None = None,
) -> None:
    path = DEFAULT_DIAGNOSTICS if path is None else Path(path)
    payload = {
        "eta": ETA,
        "scba_depth": SCBA_DEPTH,
        "omega_window": [-8.0, 0.25],
        "definition": "lowest interior Re D(omega)=0 of G(k=0)",
        "claim_ceiling": (
            "same-origin L=2 E0_Born/E0_SCBA columns only; "
            "not C0-complete, not Week 2, not VC-validated"
        ),
        "cells": [
            {
                "g_over_t": row.g_over_t,
                "omega_over_t": row.omega_over_t,
                "E0_ED": row.E0_ED,
                "E0_Born": row.E0_Born,
                "E0_SCBA": row.E0_SCBA,
                "E0_Born_VC": row.E0_Born_VC,
                "born_abs_D": row.born_abs_D,
                "scba_abs_D": row.scba_abs_D,
                "born_n_crossings": row.born_n_crossings,
                "scba_n_crossings": row.scba_n_crossings,
            }
            for row in rows
        ],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> None:
    e0_g0 = g0_ground_energy()
    if abs(e0_g0) > 1.0e-12:
        raise RuntimeError(f"g=0 sanity failed: E0={e0_g0!r}")
    born0, scba0 = g0_poles()
    if born0.E0 is None or scba0.E0 is None:
        raise RuntimeError("g=0 diagrammatic pole missing")
    if abs(born0.E0) > 1.0e-10 or abs(scba0.E0) > 1.0e-10:
        raise RuntimeError(f"g=0 poles must be 0: Born={born0.E0!r} SCBA={scba0.E0!r}")
    rows = write_teacher_map()
    write_diagnostics(rows)
    print(f"wrote {DEFAULT_CSV}")
    print(f"wrote {DEFAULT_DIAGNOSTICS}")
    print(f"g0_sanity_E0_ED={e0_g0!r}")
    print(f"g0_sanity_E0_Born={born0.E0!r}")
    print(f"g0_sanity_E0_SCBA={scba0.E0!r}")
    print(f"n_cells={len(rows)}")
    for row in rows:
        print(
            f"g/t={row.g_over_t} Omega/t={row.omega_over_t} "
            f"M={row.M_used} dim={row.dim} E0_ED={row.E0_ED!r} "
            f"E0_Born={row.E0_Born} E0_SCBA={row.E0_SCBA} "
            f"E0_Born_VC={row.E0_Born_VC} label={row.label}"
        )


if __name__ == "__main__":
    main()
