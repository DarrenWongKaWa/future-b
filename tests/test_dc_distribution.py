"""A scientist can stage a standalone compiler distribution from this tree."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_standalone_stage_contains_runtime_and_reproduction_inputs(tmp_path):
    stage = tmp_path / "standalone"
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_diagram_compiler_package.py"),
         "--stage", str(stage)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert (stage / "pyproject.toml").is_file()
    assert (stage / "src/keldysh4ai/diagram_compiler/fortran/native_kernel_runtime_v1.f90").is_file()
    assert (stage / "src/keldysh4ai/scheme_d/physics_first/symbolic/rebind_cases.csv").is_file()
    assert (stage / "research/diagram_compiler/task1/differential.csv").is_file()
    assert (stage / "src/future_b/r1_fixed_order/__init__.py").is_file()
    assert (stage / "research/diagram_compiler/task6/fixture_manifest.json").is_file()
    assert (stage / "integration/diagram_compiler/Dockerfile.u22").is_file()
    assert (stage / "examples/quickstart.py").is_file()
    manifest = json.loads((stage / "SOURCE_MANIFEST.json").read_text())
    assert manifest["source_ref"]
    assert manifest["files"]["src/keldysh4ai/diagram_compiler/fortran/native_kernel_runtime_v1.f90"]
