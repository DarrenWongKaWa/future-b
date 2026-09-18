"""Reproduce the bounded exact compiler demonstration and numerical evidence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from dataclasses import asdict, replace
from pathlib import Path

import numpy as np

from keldysh4ai.diagram_compiler import (
    DiagramIR, compile_evaluator, evaluate_dag, evaluate_diagramwise,
    import_r1_binding, import_r1_spec, lower_diagramwise, lower_grouped, numeric_close,
)
from keldysh4ai.scheme_d.exec import interpret
from keldysh4ai.scheme_d.physics_first.contract import HolsteinRing, TwoBandHolstein
from keldysh4ai.scheme_d.physics_first.index_oracle import group_sum_scalar, group_sum_matrix_twoband
from keldysh4ai.scheme_d.physics_first.symbolic.bindings import base_binding, apply_scenario
from keldysh4ai.scheme_d.physics_first.symbolic.plan_spec import scalar_spec, twoband_spec
from keldysh4ai.scheme_d.physics_first.symbolic.r1 import r1_symbolic_build
from keldysh4ai.scheme_d.physics_first.symbolic.r1_twoband import r1_twoband_build, structural_eye
from keldysh4ai.scheme_d.physics_first.symbolic.reference_binder import ReferenceBinder

ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    'src/keldysh4ai/scheme_d/physics_first/contract.py',
    'src/keldysh4ai/scheme_d/physics_first/index_oracle.py',
    'src/keldysh4ai/scheme_d/physics_first/fock_witness.py',
    'src/keldysh4ai/scheme_d/physics_first/interface.py',
    'src/keldysh4ai/scheme_d/physics_first/r1_open_dp.py',
    'src/keldysh4ai/scheme_d/physics_first/symbolic/r1.py',
    'src/keldysh4ai/scheme_d/physics_first/symbolic/r1_twoband.py',
    'src/keldysh4ai/scheme_d/physics_first/symbolic/leaves.py',
    'src/keldysh4ai/scheme_d/physics_first/symbolic/reference_binder.py',
    'src/keldysh4ai/scheme_d/physics_first/symbolic/plan_spec.py',
    'src/keldysh4ai/scheme_d/physics_first/symbolic/guards.py',
    'src/keldysh4ai/scheme_d/physics_first/symbolic/bindings.py',
    'src/keldysh4ai/scheme_d/ir.py',
    'src/keldysh4ai/scheme_d/exec.py',
    'src/keldysh4ai/scheme_d/numeric.py',
    'src/keldysh4ai/scheme_d/oracle.py',
    'src/future_b/r1_fixed_order/__init__.py',
    'benchmarks/r1_fixed_order/frozen_results.json',
)


def write_csv(path, rows):
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def write_json(path, payload):
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + '\n')


def main(output):
    output.mkdir(parents=True, exist_ok=True)
    rows, stats = [], []
    scenarios = ('base', 'change_k', 'change_q', 'change_tau', 'change_t', 'change_omega',
                 'change_g', 'g_zero', 'joint_parameters', 'joint_sample',
                 'repeat_q_then_separate', 'repeat_dtau_then_separate', 'change_L_analytic',
                 'small_nonzero_g', 'longer_legal_intervals', 'same_input_repeat')
    for model, orders in [('scalar', range(1, 5)), ('twoband', range(1, 4))]:
        for n in orders:
            spec = scalar_spec(n) if model == 'scalar' else twoband_spec(n)
            ir = import_r1_spec(spec)
            revived = DiagramIR.from_json(ir.to_json())
            assert revived == ir
            evaluator = compile_evaluator(revived)
            dags = [lower_diagramwise(revived), lower_diagramwise(revived, share=True), lower_grouped(revived)]
            plan = r1_symbolic_build(spec) if model == 'scalar' else r1_twoband_build(spec)
            binder = ReferenceBinder(spec, plan.leaves)
            fanout = Counter(i for node in dags[1].nodes for i in node.inputs)
            stats.append({
                'model': model, 'n': n, 'diagrams': len(ir.diagrams),
                'naive_nodes': len(dags[0].nodes), 'unique_dag_nodes': len(dags[1].nodes),
                'nodes_eliminated': len(dags[0].nodes) - len(dags[1].nodes),
                'shared_nodes': sum(v > 1 for v in fanout.values()),
                'shared_arithmetic_nodes': sum(v > 1 and dags[1].nodes[i].op not in ('input', 'const')
                                               for i, v in fanout.items()),
                'estimated_operations': sum(node.op not in ('input', 'const') for node in dags[1].nodes),
                'recovered_dp_nodes': len(dags[2].nodes), 'r1_nodes': plan.report.dag_nodes,
                'comparison': 'COUNTS_ONLY_NOT_ISOMORPHISM_OR_SPEEDUP',
            })
            for split in ('DEV', 'RESERVED_CONFIRMATION'):
                base = base_binding(spec, split)
                for scenario in scenarios:
                    rt = base if scenario == 'base' else apply_scenario(base, spec, scenario, 20260918 + n)
                    b = import_r1_binding(rt)
                    env = binder.bind(rt)
                    if model == 'twoband':
                        env.update(structural_eye())
                    reference = interpret(plan.graph, env)
                    naive = evaluate_diagramwise(revived, b)
                    outputs = [evaluate_dag(dag, b, revived) for dag in dags] + [evaluator(b)]
                    if model == 'scalar':
                        physical = HolsteinRing(L=rt.L, t=rt.t, omega=rt.omega, g=rt.g)
                        independent = {'F': group_sum_scalar(n, rt.tau_array(), rt.q_array(), rt.k, physical)}
                    else:
                        physical = TwoBandHolstein(L=rt.L, t=rt.t, omega=rt.omega, g=rt.g, delta=rt.delta, gap=rt.gap)
                        op = group_sum_matrix_twoband(n, rt.tau_array(), rt.q_array(), rt.k, physical)
                        independent = {'F': np.trace(op), 'Op': op}
                    errors = []
                    for out in [naive, *outputs]:
                        for key in independent:
                            assert numeric_close(out[key], reference[key]), (model, n, split, scenario, key)
                            assert numeric_close(out[key], independent[key]), (model, n, split, scenario, key)
                            errors.append(float(np.max(np.abs(out[key] - reference[key]))))
                    rows.append({'case': f'{spec.spec_id}/{split}/{scenario}',
                                 'r1_result': repr(complex(np.asarray(reference['F']).item())),
                                 'naive_generated_result': repr(naive['F']),
                                 'dag_result': repr(outputs[1]['F']),
                                 'max_error_including_Op': max(errors), 'status': 'PASS'})
            if model == 'scalar' and n == 2:
                (output / 'r1_scalar_n2.json').write_text(ir.to_json() + '\n')
                rt = replace(base_binding(spec, 'DEV'), L=8, k=np.pi / 4,
                             q=(np.pi / 2, 3*np.pi/4), tau=(.1,.27,.63,.94), g=.8)
                b = import_r1_binding(rt)
                write_json(output / 'binding.json', asdict(b))
                reference = complex(np.asarray(interpret(plan.graph, binder.bind(rt))['F']).item())
                write_json(output / 'demo_result.json', {
                    'case': spec.spec_id, 'r1': [reference.real, reference.imag],
                    'compiled': [evaluator(b)['F'].real, evaluator(b)['F'].imag],
                    'ir_file': 'r1_scalar_n2.json', 'binding_file': 'binding.json',
                })
    write_csv(output / 'differential.csv', rows)
    write_csv(output / 'graph_stats.csv', stats)
    write_json(output / 'R1_ORACLE.json', {
        'status': 'EXPERIMENTAL_BOUNDED_EXACT', 'physics_object': 'PF_G_FIXED_TIME_ORDER_G2n',
        'graph_object': 'SHARED_X_GROUP', 'atol': 1e-12, 'rtol': 1e-10,
        'numeric_oracle': 'r1_symbolic_build/r1_twoband_build + ReferenceBinder + exec.interpret',
        'independent_oracle': 'index_oracle.group_sum_scalar/group_sum_matrix_twoband',
        'frontend': 'PlanSpec structure adapter; not reverse engineering arbitrary Graph objects',
        'primary_lowering': 'explicit diagram factor chains with ordered structural hash-consing',
        'recovered_dp': 'manual R1 recurrence transcription; not automatic CSE rediscovery',
        'validated_orders': {'scalar': [1,2,3,4], 'twoband': [1,2,3]},
        'rule_limit': '1 <= n <= 6; higher admitted orders not validated by this campaign',
        'source_hashes': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in SOURCES},
        'source_tracking': 'Many R1 files were untracked at task start; content hashes are authoritative here.',
        'exclusions': ['BOUND_C', 'SUMMED_KERNEL', 'time integrals', 'external propagators',
                       'native D(C)', 'C0/P1 generation', 'cheap evaluator', 'variable order', 'native codegen'],
        'frozen_results': 'Read-only historical evidence; no performance inference from node counts.',
    })
    print(json.dumps({'differential_cases': len(rows), 'max_error': max(r['max_error_including_Op'] for r in rows),
                      'output': str(output)}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT/'research/diagram_compiler/task1')
    main(parser.parse_args().output)
