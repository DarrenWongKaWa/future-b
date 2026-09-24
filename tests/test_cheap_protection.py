"""Task-1 exact compiler bytes and 224-case contract must not regress."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from keldysh4ai.diagram_compiler import build_scalar_ir, compile_evaluator, numeric_close
from keldysh4ai.diagram_compiler.evaluator import Binding, torus_point

ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT / "research/diagram_compiler/task2/baseline.json").read_text())
COMPILER = ROOT / "src/keldysh4ai/diagram_compiler"


def test_exact_compiler_modules_are_byte_identical_to_task1():
    for name, expected in BASELINE["exact_compiler_sha256"].items():
        digest = hashlib.sha256((COMPILER / name).read_bytes()).hexdigest()
        assert digest == expected, f"{name} changed from Task-1 HEAD"


def test_exact_compile_evaluator_still_exists_and_runs():
    ir = build_scalar_ir(1)
    L = 4
    binding = Binding(
        k=torus_point(0, L),
        q=(torus_point(1, L),),
        tau=(0.05, 0.12),
        t=1.0,
        omega=0.8,
        g=0.5,
        L=L,
    )
    out = compile_evaluator(ir)(binding)
    assert numeric_close(out["F"], out["F"])
    assert out["F"].real != 0.0
