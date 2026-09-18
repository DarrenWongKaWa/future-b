"""Reproduce Task-3 delayed-acceptance evidence. No Fortran, no speedup claim."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

from keldysh4ai.diagram_compiler import (
    Binding,
    build_twoband_ir,
    compile_delayed_acceptance,
    positive_real_F_v1,
    transition_matrix,
)
from keldysh4ai.diagram_compiler.evaluator import torus_point
from keldysh4ai.diagram_compiler.proposal import ProposalSpec

ROOT = Path(__file__).resolve().parents[1]


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n")


def binding(variant: str) -> Binding:
    L = 4
    if variant == "x":
        k_idx, q0, tau_step, t, omega, g = 0, 1, 0.05, 1.0, 0.8, 0.5
    else:
        k_idx, q0, tau_step, t, omega, g = 1, 2, 0.07, 1.1, 0.9, 0.4
    return Binding(
        k=torus_point(k_idx, L),
        q=(torus_point(q0, L),),
        tau=(tau_step, 2 * tau_step),
        t=t,
        omega=omega,
        g=g,
        L=L,
        delta=0.35,
        gap=0.5,
    )


def result_row(name: str, x: Binding, y: Binding, log_q: float, u1: float, u2: float, result) -> dict:
    return {
        "accepted": result.accepted,
        "cheap_log_weight_x": result.cheap_log_weight_x,
        "cheap_log_weight_y": result.cheap_log_weight_y,
        "ell_R": result.ell_R,
        "ell_hat": result.ell_hat,
        "exact_log_weight_x": result.exact_log_weight_x,
        "exact_log_weight_y": result.exact_log_weight_y,
        "exact_y_evaluated": result.exact_y_evaluated,
        "g_x": x.g,
        "g_y": y.g,
        "k_x": x.k,
        "k_y": y.k,
        "log_q_reverse_minus_forward": log_q,
        "name": name,
        "stage1_pass": result.stage1_pass,
        "stage2_pass": result.stage2_pass,
        "u1": u1,
        "u2": u2,
    }


def main(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    ir = build_twoband_ir(1)
    kernel = compile_delayed_acceptance(ir, proposal_spec=ProposalSpec.provided_log_ratio())
    write_json(output / "DA_KERNEL_SPEC.json", kernel.spec.to_dict())
    write_json(output / "TARGET_POLICY.json", positive_real_F_v1().to_dict())
    write_json(output / "PROPOSAL_SPEC.json", ProposalSpec.provided_log_ratio().to_dict())
    x, y = binding("x"), binding("y")
    probe = kernel.evaluate_transition(x, y, 0.0, 1e-16, 1e-16)
    alpha2 = 1.0 if probe.ell_R - probe.ell_hat >= 0 else math.exp(probe.ell_R - probe.ell_hat)
    u2_reject = (alpha2 + 1.0) / 2.0
    cases = [
        ("stage1_reject", x, y, 0.0, 0.9, 0.1),
        ("stage2_reject", x, y, 0.0, 1e-16, u2_reject),
        ("accept", x, y, 0.0, 1e-16, 1e-16),
    ]
    rows = []
    n_s1_reject = n_s1_pass = n_exact_y = n_s2_reject = n_accept = 0
    for name, cx, cy, log_q, u1, u2 in cases:
        result = kernel.evaluate_transition(cx, cy, log_q, u1, u2)
        rows.append(result_row(name, cx, cy, log_q, u1, u2, result))
        if not result.stage1_pass:
            n_s1_reject += 1
        else:
            n_s1_pass += 1
            n_exact_y += int(result.exact_y_evaluated)
            if result.stage2_pass:
                n_accept += 1
            else:
                n_s2_reject += 1
    write_json(output / "demo_transitions.json", {"family": ir.family.family_id, "transitions": rows})
    write_csv(output / "call_counts.csv", [{
        "accepts": n_accept,
        "exact_candidate_evaluations": n_exact_y,
        "stage1_passes": n_s1_pass,
        "stage1_rejects": n_s1_reject,
        "stage2_rejects": n_s2_reject,
        "transitions_attempted": len(cases),
        "wall_speedup_claim": "NOT_CLAIMED",
    }])
    pi = np.array([0.5, 0.3, 0.2])
    cheap = np.array([0.1, 0.55, 0.35])
    q_sym = np.array([[0.0, 0.5, 0.5], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]])
    q_asy = np.array([[0.0, 0.8, 0.2], [0.3, 0.0, 0.7], [0.6, 0.4, 0.0]])
    balance_rows = []
    for name, q in (("symmetric", q_sym), ("asymmetric", q_asy)):
        p = transition_matrix(pi, cheap, q)
        residual = 0.0
        for i in range(3):
            for j in range(3):
                residual = max(residual, abs(pi[i] * p[i, j] - pi[j] * p[j, i]))
        stat = np.max(np.abs(pi @ p - pi))
        balance_rows.append({
            "max_balance_residual": residual,
            "max_stationarity_residual": stat,
            "proposal": name,
            "status": "PASS" if residual <= 1e-12 and stat <= 1e-12 else "FAIL",
        })
    write_csv(output / "finite_state_balance.csv", balance_rows)
    write_json(output / "verification.json", {
        "call_count_identity": n_exact_y == n_s1_pass,
        "design": "B",
        "demo_paths": [row["name"] for row in rows],
        "finite_state_pass": all(r["status"] == "PASS" for r in balance_rows),
        "target_policy": "positive_real_F_v1",
        "task2_head": "a79bdf4213a768db74401e6525b4c6e6eb62d768",
        "wall_speedup_claim": False,
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "research/diagram_compiler/task3")
    main(parser.parse_args().output)
