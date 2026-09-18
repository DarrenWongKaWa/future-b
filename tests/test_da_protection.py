"""Task-1/Task-2 protection hashes must remain unchanged."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT / "research/diagram_compiler/task3/baseline.json").read_text())
COMPILER = ROOT / "src/keldysh4ai/diagram_compiler"


def test_exact_and_cheap_task2_modules_are_byte_identical():
    for name, expected in BASELINE["exact_compiler_sha256"].items():
        digest = hashlib.sha256((COMPILER / name).read_bytes()).hexdigest()
        assert digest == expected, name
    assert hashlib.sha256((COMPILER / "cheap_policy.py").read_bytes()).hexdigest() == BASELINE["cheap_policy_py_sha256"]
    assert hashlib.sha256((COMPILER / "cheap_evaluator.py").read_bytes()).hexdigest() == BASELINE["cheap_evaluator_sha256"]
    policy = ROOT / "research/diagram_compiler/task2/CHEAP_POLICY.json"
    assert hashlib.sha256(policy.read_bytes()).hexdigest() == BASELINE["cheap_policy_json_sha256"]
