"""Task-4 NativeKernelIR sources must remain byte-identical during Task 5."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT / "research/diagram_compiler/task5/baseline.json").read_text())
COMPILER = ROOT / "src/keldysh4ai/diagram_compiler"


def test_task4_native_modules_unchanged():
    mapping = {
        "native_ir.py": "native_ir_py_sha256",
        "native_interpret.py": "native_interpret_sha256",
        "native_lower.py": "native_lower_sha256",
        "native_validate.py": "native_validate_sha256",
        "da_kernel.py": "da_kernel_sha256",
    }
    for name, key in mapping.items():
        digest = hashlib.sha256((COMPILER / name).read_bytes()).hexdigest()
        assert digest == BASELINE[key], name
    ir_json = ROOT / "research/diagram_compiler/task4/NATIVE_KERNEL_IR.json"
    assert hashlib.sha256(ir_json.read_bytes()).hexdigest() == BASELINE["native_ir_json_sha256"]
    assert BASELINE["task4_head"] == "0110f22abc9831b20f69d7a5228af8d4773fa3d5"
    assert BASELINE["differential_cases"] == 224
    assert BASELINE["max_absolute_error_from_r1_including_Op"] == 2.7755575615628914e-17
