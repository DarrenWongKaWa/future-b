"""Task 6: FEP-DMC-toolchain validation of the Task-5 generated kernel."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from keldysh4ai.diagram_compiler import (
    build_twoband_ir,
    compile_delayed_acceptance,
    emit_fortran,
    lower_native_kernel,
)
from keldysh4ai.diagram_compiler.fortran_compile import ATOL, RTOL, RUNTIME_FILE
from keldysh4ai.diagram_compiler.fortran_docker import (
    DEFAULT_IMAGE,
    compile_in_docker,
    docker_available,
    run_in_docker,
)
from keldysh4ai.diagram_compiler.fortran_fixtures import twoband_oracle_cases

ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT / "research/diagram_compiler/task6/baseline.json").read_text())
PIN = json.loads((ROOT / "integration/diagram_compiler/UPSTREAM_FEP_DMC.json").read_text())
FEP_DEFAULT = Path("/Users/kawawong/Research/future-b-worktrees/_scratch/FEP-DMC")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_task5_generated_source_and_runtime_unchanged():
    kernel = compile_delayed_acceptance(build_twoband_ir(1))
    nir = lower_native_kernel(kernel)
    src = emit_fortran(nir)
    assert hashlib.sha256(src.encode("utf-8")).hexdigest() == BASELINE["generated_twoband_n1_sha256"]
    assert _sha(RUNTIME_FILE) == BASELINE["runtime_sha256"]
    artifact = ROOT / "research/diagram_compiler/task5/generated_twoband_n1.f90"
    assert _sha(artifact) == BASELINE["generated_twoband_n1_sha256"]
    assert _sha(ROOT / "src/keldysh4ai/diagram_compiler/native_ir.py") == BASELINE["native_ir_py_sha256"]
    assert _sha(ROOT / "src/keldysh4ai/diagram_compiler/native_interpret.py") == BASELINE["native_interpret_sha256"]


def test_backend_still_does_not_import_diagramir():
    import ast

    tree = ast.parse((ROOT / "src/keldysh4ai/diagram_compiler/fortran_codegen.py").read_text())
    imported = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            imported.append(node.module)
    assert "ir" not in imported
    assert "da_kernel" not in imported
    assert "cheap_policy" not in imported


def test_fep_dmc_pin_pristine():
    import sys

    sys.path.insert(0, str(ROOT / "integration" / "diagram_compiler"))
    import dc_lib as dc

    if not FEP_DEFAULT.is_dir():
        pytest.skip("pinned FEP-DMC clone not present")
    pin = dc.load_json(ROOT / "integration/diagram_compiler/UPSTREAM_FEP_DMC.json")
    state, detail = dc.classify(FEP_DEFAULT, pin)
    assert state == dc.STATE_PUBLIC_PRISTINE, detail
    assert dc.compiler_kernel_needles_in_tree(FEP_DEFAULT) == []
    assert dc.git_head(FEP_DEFAULT) == PIN["reference_commit"]


@pytest.mark.skipif(not docker_available(), reason="docker not available")
def test_ubuntu_gfortran_kernel_matches_oracle(tmp_path):
    from keldysh4ai.diagram_compiler import emit_driver

    kernel = compile_delayed_acceptance(build_twoband_ir(1))
    nir = lower_native_kernel(kernel)
    generated = tmp_path / "generated_da_kernel.f90"
    driver = tmp_path / "futureb_dc_validate.f90"
    generated.write_text(emit_fortran(nir), newline="\n")
    driver.write_text(emit_driver(nir), newline="\n")
    workdir = tmp_path / "build"
    compile_in_docker(runtime=RUNTIME_FILE, generated=generated, driver=driver, workdir=workdir, image=DEFAULT_IMAGE)
    cases = twoband_oracle_cases(nir, kernel)
    for case in cases:
        ft = run_in_docker("futureb_dc_validate.x", case.text, workdir=workdir, image=DEFAULT_IMAGE)
        exp = case.expected
        assert ft.status == exp["status"]
        if exp["status"] != 0:
            assert ft.accepted is False
            continue
        assert ft.accepted == exp["accepted"]
        assert ft.reject_stage == exp["reject_stage"]
        assert ft.exact_y_evaluated == exp["exact_y_evaluated"]
        if exp["ell_hat"] is not None:
            assert ft.ell_hat == pytest.approx(exp["ell_hat"], abs=ATOL, rel=RTOL)
        if exp["ell_R"] is None:
            assert ft.ell_R_valid is False
        else:
            assert ft.ell_R_valid is True
            assert ft.ell_R == pytest.approx(exp["ell_R"], abs=ATOL, rel=RTOL)
        if case.name == "stage1_reject":
            assert ft.n_exact_graph == 0
            assert ft.n_electron_twoband == 0
            assert ft.n_trace == 0
        if case.name in ("accept", "stage2_reject", "asymmetric_q", "uncached_exact_x"):
            assert ft.n_exact_graph > 0
        if case.name == "cached_exact_x":
            assert ft.n_exact_graph == 1
