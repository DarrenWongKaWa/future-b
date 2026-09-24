"""Stage an independent, reproducible Diagram Compiler wheel/sdist project.

The frozen Future B v1.2.0 metadata and checksum manifest stay untouched.
Stage only the experimental compiler and its exact-oracle dependencies.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "distribution" / "diagram_compiler"
SOURCE_DIRS = (
    "src/keldysh4ai",
    "research/diagram_compiler",
    "integration/diagram_compiler",
)
COMPILER_TESTS = frozenset(
    "test_cheap_cost test_cheap_evaluator test_cheap_independence test_cheap_p1 "
    "test_cheap_policy test_cheap_protection test_cheap_reciprocity "
    "test_da_algebra test_da_finite_state test_da_independence test_da_kernel "
    "test_da_protection test_dag_sharing test_dc_fep_dmc_validate "
    "test_diagram_ir test_evaluator_vs_r1 test_fortran_backend "
    "test_fortran_primitives test_fortran_protection test_native_kernel "
    "test_proposal_spec test_r1_import test_target_policy".split()
)


def _include(path: Path) -> bool:
    return path.is_file() and not any(part in {"__pycache__", ".pytest_cache"} for part in path.parts) and path.suffix not in {".pyc", ".o", ".mod", ".x"}


def _source_ref() -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def stage(destination: Path) -> None:
    if destination.exists():
        raise FileExistsError(f"stage destination exists: {destination}")
    destination.mkdir(parents=True)
    paths: list[Path] = [ROOT / "LICENSE"]
    paths.extend(path for path in TEMPLATE.rglob("*") if _include(path))
    for directory in SOURCE_DIRS:
        paths.extend(path for path in (ROOT / directory).rglob("*") if _include(path))
    paths.extend(path for path in (ROOT / "docs").glob("DIAGRAM_COMPILER*.md") if _include(path))
    paths.extend(path for path in (ROOT / "docs" / "diagrams").glob("*.drawio") if _include(path))
    paths.extend(path for path in (ROOT / "scripts").glob("diagram_compiler_task*.py") if _include(path))
    paths.append(ROOT / "examples" / "diagram_compiler" / "quickstart.py")
    paths.append(ROOT / "src" / "future_b" / "r1_fixed_order" / "__init__.py")
    for name in sorted(COMPILER_TESTS):
        paths.append(ROOT / "tests" / f"{name}.py")
    paths.append(ROOT / "benchmarks" / "r1_fixed_order" / "frozen_results.json")

    digests: dict[str, str] = {}
    for src in sorted(set(paths)):
        if not src.is_file():
            raise FileNotFoundError(src)
        rel = src.relative_to(TEMPLATE) if src.is_relative_to(TEMPLATE) else src.relative_to(ROOT)
        if str(rel) == "examples/diagram_compiler/quickstart.py":
            rel = Path("examples/quickstart.py")
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            raise ValueError(f"duplicate staged path: {rel}")
        shutil.copyfile(src, target)
        digests[rel.as_posix()] = hashlib.sha256(target.read_bytes()).hexdigest()

    manifest = {"schema": "future_b_diagram_compiler_source_v1", "source_ref": _source_ref(), "files": digests}
    (destination / "SOURCE_MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", type=Path, required=True, help="new empty staging directory")
    args = parser.parse_args()
    stage(args.stage.resolve())
    print(args.stage.resolve())
