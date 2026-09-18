"""Reproduce Task-4 NativeKernelIR evidence. No Fortran emission."""

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
    interpret_native_kernel,
    lower_native_kernel,
    native_acceptance_probability,
)
from keldysh4ai.diagram_compiler.evaluator import torus_point
from keldysh4ai.diagram_compiler.native_validate import (
    exact_candidate_ops_on_reject_path,
    reachable,
    stage1_reject_blocks,
    validate_native_ir,
)

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
        k=torus_point(k_idx, L), q=(torus_point(q0, L),), tau=(tau_step, 2 * tau_step),
        t=t, omega=omega, g=g, L=L, delta=0.35, gap=0.5,
    )


def main(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    kernel = compile_delayed_acceptance(build_twoband_ir(1))
    nir = lower_native_kernel(kernel)
    validate_native_ir(nir)
    write_json(output / "NATIVE_KERNEL_IR.json", json.loads(nir.to_json()))
    write_json(output / "binding_layout.json", nir.layout.to_dict())
    write_json(output / "primitive_inventory.json", {
        "cheap_ops": sorted({op.op for op in nir.graph("cheap").ops}),
        "control_ops": sorted({op.op for block in nir.blocks for op in block.ops}),
        "exact_ops": sorted({op.op for op in nir.graph("exact").ops}),
        "primitive_set": "native_kernel_v1",
        "schema_version": 1,
        "signatures": {
            "prim.electron_scalar": "(k_eff:f64, t:f64, dtau:f64) -> c128; Gel=exp(-2t(1-cos k_eff) dtau)",
            "prim.electron_twoband": "(k_eff,t,dtau,delta,gap) -> c128_m2; U=exp(-H dtau) via eigh",
            "prim.phonon": "(omega:f64, dtau:f64) -> c128; D=exp(-omega dtau)",
            "prim.prefactor": "(g:f64, L:f64; n:i64 attr) -> c128; (g/sqrt(L))**(2n)",
            "prim.vertex_sigmaz": "(g:f64, L:f64) -> c128_m2; (g/sqrt(L))*diag(1,-1)",
        },
    })
    write_json(output / "cfg_paths.json", {
        "blocks": [block.id for block in nir.blocks],
        "entry": nir.entry,
        "exact_ops_on_stage1_reject": exact_candidate_ops_on_reject_path(nir),
        "reachable_from_entry": sorted(reachable(nir, nir.entry)),
        "stage1_reject_blocks": sorted(stage1_reject_blocks(nir)),
    })
    x, y = binding("x"), binding("y")
    py_probe = kernel.evaluate_transition(x, y, 0.0, 1e-16, 1e-16)
    alpha2 = math.exp(min(0.0, py_probe.ell_R - py_probe.ell_hat))
    cases = [
        ("stage1_reject", 0.0, 0.9, 0.1),
        ("stage2_reject", 0.0, 1e-16, (alpha2 + 1.0) / 2.0),
        ("accept", 0.0, 1e-16, 1e-16),
        ("asymmetric_q", 0.4, 1e-16, 1e-16),
    ]
    rows = []
    for name, log_q, u1, u2 in cases:
        py = kernel.evaluate_transition(x, y, log_q, u1, u2)
        native = interpret_native_kernel(nir, x=x, y=y, log_q=log_q, u1=u1, u2=u2)
        rows.append({
            "accepted_match": py.accepted == native.accepted,
            "ell_R_native": native.ell_R,
            "ell_hat_native": native.ell_hat,
            "exact_y_match": py.exact_y_evaluated == native.exact_y_evaluated,
            "name": name,
            "native_accepted": native.accepted,
            "py_accepted": py.accepted,
        })
    write_csv(output / "differential_results.csv", rows)
    pi = np.array([0.5, 0.3, 0.2])
    cheap = np.array([0.1, 0.55, 0.35])
    q = np.array([[0.0, 0.8, 0.2], [0.3, 0.0, 0.7], [0.6, 0.4, 0.0]])
    p = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            log_q = math.log(q[j, i]) - math.log(q[i, j])
            a = native_acceptance_probability(
                math.log(cheap[i]), math.log(cheap[j]), math.log(pi[i]), math.log(pi[j]), log_q,
            )
            p[i, j] = q[i, j] * a
        p[i, i] = 1.0 - p[i].sum()
    residual = max(abs(pi[i] * p[i, j] - pi[j] * p[j, i]) for i in range(3) for j in range(3))
    write_csv(output / "finite_state_native.csv", [{
        "max_balance_residual": residual,
        "max_stationarity_residual": float(np.max(np.abs(pi @ p - pi))),
        "status": "PASS" if residual <= 1e-12 else "FAIL",
    }])
    write_json(output / "verification.json", {
        "cfg_laziness": exact_candidate_ops_on_reject_path(nir) == [],
        "differential_pass": bool(all(r["accepted_match"] and r["exact_y_match"] for r in rows)),
        "finite_state_pass": bool(residual <= 1e-12),
        "ir_kind": "NativeKernelIR",
        "representation": "typed_ssa_cfg",
        "wall_speedup_claim": False,
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "research/diagram_compiler/task4")
    main(parser.parse_args().output)
