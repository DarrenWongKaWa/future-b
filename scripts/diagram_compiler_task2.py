"""Reproduce Task-2 cheap-evaluator evidence. No delayed-acceptance, no speedup claim."""

from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

from keldysh4ai.diagram_compiler import (
    Binding,
    build_scalar_ir,
    build_twoband_ir,
    compile_cheap,
    compile_exact,
    evaluate_diagramwise,
    numeric_close,
    propagator_only_v1,
)
from keldysh4ai.diagram_compiler.cheap_cost import lower_exact_cost
from keldysh4ai.diagram_compiler.evaluator import torus_point

ROOT = Path(__file__).resolve().parents[1]


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n")


def binding_for(n: int, *, L: int = 4, variant: str = "x") -> Binding:
    if variant == "x":
        k_idx, q0, tau_step, t, omega, g = 0, 1, 0.05, 1.0, 0.8, 0.5
    else:
        k_idx, q0, tau_step, t, omega, g = 1, 2, 0.07, 1.1, 0.9, 0.4
    return Binding(
        k=torus_point(k_idx, L),
        q=tuple(torus_point(q0 + i, L) for i in range(n)),
        tau=tuple(tau_step * (i + 1) for i in range(2 * n)),
        t=t,
        omega=omega,
        g=g,
        L=L,
        delta=0.35,
        gap=0.5,
    )


def main(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    policy = propagator_only_v1()
    write_json(output / "CHEAP_POLICY.json", policy.to_dict())

    demo_ir = build_scalar_ir(2)
    demo_bind = binding_for(2)
    cheap = compile_cheap(demo_ir)
    exact = compile_exact(demo_ir)
    write_json(output / "example_cheap_ir.json", json.loads(cheap.to_json()))
    y = binding_for(2, variant="y")
    cheap_x = cheap.evaluate(demo_bind)
    cheap_y = cheap.evaluate(y)
    ell_fwd = cheap.transition_score(demo_bind, y)
    ell_rev = cheap.transition_score(y, demo_bind)
    demo = {
        "binding_x": {"g": demo_bind.g, "k": demo_bind.k, "omega": demo_bind.omega, "q": list(demo_bind.q), "t": demo_bind.t, "tau": list(demo_bind.tau)},
        "cheap_F_hat": [cheap_x["F_hat"].real, cheap_x["F_hat"].imag],
        "cheap_log_W_hat": cheap_x["log_W_hat"],
        "cheap_static_cost": cheap.cost.to_dict(),
        "dropped_categories": list(policy.drop),
        "exact_F": [exact.evaluate(demo_bind)["F"].real, exact.evaluate(demo_bind)["F"].imag],
        "exact_static_cost": lower_exact_cost(demo_ir).to_dict(),
        "family": demo_ir.family.family_id,
        "forward_score": ell_fwd,
        "kept_categories": list(policy.keep),
        "policy": policy.name,
        "reciprocity_residual": ell_fwd + ell_rev,
        "reverse_score": ell_rev,
        "y_cheap_F_hat": [cheap_y["F_hat"].real, cheap_y["F_hat"].imag],
    }
    write_json(output / "demo_result.json", demo)

    differential = []
    costs = []
    timings = []
    max_err = 0.0
    n_pass = 0
    n_cases = 0
    for model, orders, builder in (
        ("scalar", range(1, 5), build_scalar_ir),
        ("twoband", range(1, 4), build_twoband_ir),
    ):
        for n in orders:
            ir = builder(n)
            scalar_ir = build_scalar_ir(n)
            cheap_ev = compile_cheap(ir)
            exact_cost = lower_exact_cost(ir)
            cheap_cost = cheap_ev.cost
            costs.append({
                "cheap_expensive_primitives": cheap_cost.expensive_primitives,
                "cheap_n_eigh": cheap_cost.n_eigh,
                "cheap_n_matmul": cheap_cost.n_matmul,
                "cheap_n_trace": cheap_cost.n_trace,
                "cheap_n_vertex": cheap_cost.n_vertex,
                "cheap_unique_nodes": cheap_cost.unique_nodes,
                "exact_expensive_primitives": exact_cost.expensive_primitives,
                "exact_n_eigh": exact_cost.n_eigh,
                "exact_n_matmul": exact_cost.n_matmul,
                "exact_n_trace": exact_cost.n_trace,
                "exact_n_vertex": exact_cost.n_vertex,
                "exact_unique_nodes": exact_cost.unique_nodes,
                "model": model,
                "n": n,
            })
            x = binding_for(n)
            y_bind = binding_for(n, variant="y")
            cheap_x = cheap_ev.evaluate(x)
            family_exact = evaluate_diagramwise(ir, x)["F"]
            scalar_exact = evaluate_diagramwise(scalar_ir, x)["F"]
            err_scalar = abs(cheap_x["F_hat"] - scalar_exact)
            err_family = abs(cheap_x["F_hat"] - family_exact)
            max_err = max(max_err, float(err_scalar))
            ell_fwd = cheap_ev.transition_score(x, y_bind)
            ell_rev = cheap_ev.transition_score(y_bind, x)
            ok_scalar = numeric_close(cheap_x["F_hat"], scalar_exact)
            n_cases += 1
            n_pass += int(ok_scalar)
            differential.append({
                "abs_err_vs_family_exact": float(abs(err_family)),
                "abs_err_vs_scalar_exact": float(abs(err_scalar)),
                "cheap_F_hat_real": float(cheap_x["F_hat"].real),
                "ell_fwd": float(ell_fwd),
                "ell_rev": float(ell_rev),
                "exact_F_real": float(family_exact.real),
                "matches_scalar_exact": ok_scalar,
                "model": model,
                "n": n,
                "reciprocity_residual": float(ell_fwd + ell_rev),
                "scalar_exact_F_real": float(scalar_exact.real),
            })
            t0 = time.perf_counter()
            for _ in range(200):
                cheap_ev.evaluate(x)
            cheap_time = (time.perf_counter() - t0) / 200.0
            exact_ev = compile_exact(ir)
            t1 = time.perf_counter()
            for _ in range(200):
                exact_ev.evaluate(x)
            exact_time = (time.perf_counter() - t1) / 200.0
            timings.append({
                "cheap_eval_seconds_point_estimate": cheap_time,
                "exact_eval_seconds_point_estimate": exact_time,
                "model": model,
                "n": n,
                "repeats": 200,
                "wall_speedup_claim": "NOT_CLAIMED",
            })

    write_csv(output / "differential_results.csv", differential)
    write_csv(output / "graph_costs.csv", costs)
    write_csv(output / "microbenchmarks.csv", timings)
    write_json(output / "verification.json", {
        "cheap_matches_scalar_exact_cases": n_pass,
        "differential_cases": n_cases,
        "max_abs_err_vs_scalar_exact": max_err,
        "policy": policy.name,
        "reciprocity": "ell(y,x) := log W(y) - log W(x) antisymmetric by construction",
        "semantics": "STATE_WEIGHT",
        "task1_compiler_tests_expected": 281,
        "task2_tests": 52,
        "wall_speedup_claim": False,
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "research/diagram_compiler/task2")
    main(parser.parse_args().output)
