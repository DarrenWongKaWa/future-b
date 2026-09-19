"""Task-6 evidence: Task-5 generated kernel on the public FEP-DMC gfortran toolchain."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
import tempfile
from pathlib import Path

import numpy as np

from keldysh4ai.diagram_compiler import (
    build_twoband_ir,
    compile_delayed_acceptance,
    emit_driver,
    emit_fortran,
    interpret_native_kernel,
    lower_native_kernel,
    lower_native_score_kernel,
)
from keldysh4ai.diagram_compiler.fortran_codegen import native_ir_digest
from keldysh4ai.diagram_compiler.fortran_compile import ATOL, RTOL, RUNTIME_FILE
from keldysh4ai.diagram_compiler.fortran_docker import (
    DEFAULT_IMAGE,
    FFLAGS,
    compile_in_docker,
    gfortran_version,
    run_in_docker,
)
from keldysh4ai.diagram_compiler.fortran_fixtures import (
    binding_to_dict,
    twoband_oracle_cases,
)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "integration" / "diagram_compiler"))
import dc_lib as dc  # noqa: E402


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def match_row(name: str, expected: dict, ft) -> dict:
    ell_hat_err = None
    ell_r_err = None
    if expected["status"] == 0 and expected["ell_hat"] is not None:
        ell_hat_err = abs(ft.ell_hat - expected["ell_hat"])
    if expected["ell_R"] is not None:
        ell_r_err = abs(ft.ell_R - expected["ell_R"])
    return {
        "name": name,
        "status_match": expected["status"] == ft.status,
        "accepted_match": expected["accepted"] == ft.accepted,
        "reject_stage_match": expected["reject_stage"] == ft.reject_stage,
        "exact_y_match": expected["exact_y_evaluated"] == ft.exact_y_evaluated,
        "ell_hat_abs_err": ell_hat_err,
        "ell_R_abs_err": ell_r_err,
        "py_status": expected["status"],
        "ft_status": ft.status,
        "py_accepted": expected["accepted"],
        "ft_accepted": ft.accepted,
        "py_reject_stage": expected["reject_stage"],
        "ft_reject_stage": ft.reject_stage,
        "py_ell_hat": expected["ell_hat"],
        "ft_ell_hat": ft.ell_hat if expected["status"] == 0 else None,
        "py_ell_R": expected["ell_R"],
        "ft_ell_R": ft.ell_R if ft.ell_R_valid else None,
        "n_exact_graph": ft.n_exact_graph,
        "n_electron_twoband": ft.n_electron_twoband,
        "n_trace": ft.n_trace,
    }


def main(output: Path, fep_dmc: Path, image: str) -> None:
    output.mkdir(parents=True, exist_ok=True)
    baseline = json.loads((ROOT / "research/diagram_compiler/task5/source_provenance.json").read_text())
    kernel = compile_delayed_acceptance(build_twoband_ir(1))
    nir = lower_native_kernel(kernel)
    generated = emit_fortran(nir)
    driver = emit_driver(nir)
    gen_sha = sha256_text(generated)
    if gen_sha != baseline["fortran_source_sha256"]:
        raise SystemExit(f"generated source hash mismatch: {gen_sha}")
    if native_ir_digest(nir) != baseline["native_ir_digest"]:
        raise SystemExit("NativeKernelIR digest mismatch")
    if sha256_path(RUNTIME_FILE) != baseline["runtime_sha256"]:
        raise SystemExit("runtime hash mismatch")
    (output / "generated_twoband_n1.f90").write_text(generated, encoding="utf-8", newline="\n")
    (output / "futureb_dc_validate.f90").write_text(driver, encoding="utf-8", newline="\n")
    makefile = (ROOT / "integration/diagram_compiler/Makefile").read_text(encoding="utf-8")
    (output / "Makefile").write_text(makefile, encoding="utf-8", newline="\n")

    pin = dc.load_json(ROOT / "integration/diagram_compiler/UPSTREAM_FEP_DMC.json")
    state, detail = dc.classify(fep_dmc, pin)
    needles = dc.compiler_kernel_needles_in_tree(fep_dmc)
    write_json(
        output / "fep_dmc_pin.json",
        {
            "detail": detail,
            "head": dc.git_head(fep_dmc),
            "needles": needles,
            "production_hashes": dc.production_hashes(fep_dmc, pin),
            "reference_commit": pin["reference_commit"],
            "state": state,
        },
    )
    if state != dc.STATE_PUBLIC_PRISTINE or needles:
        raise SystemExit(f"FEP-DMC pin not PUBLIC_PRISTINE: {state} {detail} {needles}")

    cases = twoband_oracle_cases(nir, kernel)
    manifest = []
    text_dir = output / "fixtures"
    text_dir.mkdir(exist_ok=True)
    for case in cases:
        path = text_dir / f"{case.name}.txt"
        path.write_text(case.text, encoding="utf-8", newline="\n")
        expected = dict(case.expected)
        for key in ("ell_hat", "ell_R"):
            value = expected[key]
            if isinstance(value, float) and not math.isfinite(value):
                expected[key] = str(value)
        log_q = case.log_q if math.isfinite(case.log_q) else str(case.log_q)
        manifest.append(
            {
                "expected": expected,
                "exact_x_valid": case.exact_x_valid,
                "exact_log_weight_x": case.exact_log_weight_x,
                "log_q": log_q,
                "name": case.name,
                "text_sha256": sha256_path(path),
                "u1": case.u1,
                "u2": case.u2,
                "x": binding_to_dict(case.x, nir.layout),
                "y": binding_to_dict(case.y, nir.layout),
            }
        )
    write_json(output / "fixture_manifest.json", {"cases": manifest, "schema": "diagram_compiler_task6_fixtures_v1"})

    build = Path(tempfile.mkdtemp(prefix="task6_u22_"))
    compile_in_docker(
        runtime=RUNTIME_FILE,
        generated=output / "generated_twoband_n1.f90",
        driver=output / "futureb_dc_validate.f90",
        workdir=build,
        image=image,
    )
    version = gfortran_version(image)
    rows = []
    call_rows = []
    for case in cases:
        ft = run_in_docker("futureb_dc_validate.x", case.text, workdir=build, image=image)
        rows.append(match_row(case.name, case.expected, ft))
        call_rows.append(
            {
                "name": case.name,
                "n_electron_twoband": ft.n_electron_twoband,
                "n_exact_graph": ft.n_exact_graph,
                "n_matmul": ft.n_matmul,
                "n_trace": ft.n_trace,
                "n_vertex_sigmaz": ft.n_vertex_sigmaz,
                "stage1_reject": case.name == "stage1_reject",
            }
        )
    write_csv(output / "native_differential.csv", rows)
    write_csv(output / "native_call_counts.csv", call_rows)

    score = lower_native_score_kernel()
    score_src = emit_fortran(score)
    score_drv = emit_driver(score)
    score_dir = Path(tempfile.mkdtemp(prefix="task6_score_"))
    (score_dir / "generated_score.f90").write_text(score_src, newline="\n")
    (score_dir / "score_driver.f90").write_text(score_drv, newline="\n")
    compile_in_docker(
        runtime=RUNTIME_FILE,
        generated=score_dir / "generated_score.f90",
        driver=score_dir / "score_driver.f90",
        workdir=score_dir,
        image=image,
        exe_name="futureb_dc_score.x",
    )
    pi = np.array([0.5, 0.3, 0.2])
    cheap = np.array([0.1, 0.55, 0.35])
    q = np.array([[0.0, 0.8, 0.2], [0.3, 0.0, 0.7], [0.6, 0.4, 0.0]])
    n = 3
    p = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            log_q = math.log(q[j, i]) - math.log(q[i, j])
            stdin = (
                f"{math.log(cheap[i])} {math.log(cheap[j])} {math.log(pi[i])} {math.log(pi[j])}\n"
                f"{log_q} {1e-16} {1e-16}\n"
            )
            ft = run_in_docker("futureb_dc_score.x", stdin, workdir=score_dir, image=image)
            py = interpret_native_kernel(
                score,
                log_wx=math.log(cheap[i]),
                log_wy=math.log(cheap[j]),
                log_px=math.log(pi[i]),
                log_py=math.log(pi[j]),
                log_q=log_q,
                u1=1e-16,
                u2=1e-16,
            )
            if ft.status != 0 or py.status != 0:
                raise SystemExit("score kernel status")
            a1 = 1.0 if ft.ell_hat >= 0.0 else math.exp(ft.ell_hat)
            delta = ft.ell_R - ft.ell_hat
            a2 = 1.0 if delta >= 0.0 else math.exp(delta)
            p[i, j] = q[i, j] * a1 * a2
        p[i, i] = 1.0 - p[i].sum()
    residual = max(abs(pi[i] * p[i, j] - pi[j] * p[j, i]) for i in range(n) for j in range(n))
    stat = float(np.max(np.abs(pi @ p - pi)))
    write_csv(
        output / "finite_state_native.csv",
        [{"balance_residual": residual, "stationarity_residual": stat, "atol": ATOL, "rtol": RTOL}],
    )

    exe = build / "futureb_dc_validate.x"
    write_json(
        output / "build_environment.json",
        {
            "docker_image": image,
            "fflags": list(FFLAGS),
            "gfortran_version": version,
            "os": "Ubuntu 22.04 aarch64",
            "public_image": "public.ecr.aws/docker/library/ubuntu:22.04",
            "qe_hdf5_mpi_linked": False,
            "private_docker_used": False,
        },
    )
    write_json(
        output / "integration_provenance.json",
        {
            "architecture": "A_separate_validation_executable",
            "binary_sha256": sha256_path(exe),
            "docker_image": image,
            "driver_sha256": sha256_text(driver),
            "fep_dmc_commit": pin["reference_commit"],
            "fortran_source_sha256": gen_sha,
            "gfortran_version": version,
            "level": 2,
            "native_ir_digest": native_ir_digest(nir),
            "production_fep_dmc_modified": False,
            "runtime_sha256": sha256_path(RUNTIME_FILE),
        },
    )
    write_json(
        output / "INTEGRATION_SPEC.json",
        {
            "architecture": "A_separate_validation_executable",
            "backend": "fortran_v1",
            "cache_contract": "A_caller_guarantees_exact_x_valid_belongs_to_x",
            "cheap_policy": "propagator_only_v1",
            "da_design": "B",
            "fep_dmc_commit": pin["reference_commit"],
            "level_reached": 2,
            "level3_attempted": False,
            "level4_attempted": False,
            "p1_equivalence_claimed": False,
            "primitive_set": "native_kernel_v1",
            "target": "positive_real_F_v1",
            "tolerances": {"atol": ATOL, "discrete": "exact", "rtol": RTOL},
        },
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "research/diagram_compiler/task6")
    parser.add_argument(
        "--fep-dmc",
        type=Path,
        default=(Path(os.environ["FUTURE_B_FEP_DMC"])
                 if os.environ.get("FUTURE_B_FEP_DMC") else None),
    )
    parser.add_argument("--image", default=DEFAULT_IMAGE)
    args = parser.parse_args()
    if args.fep_dmc is None:
        parser.error("--fep-dmc or FUTURE_B_FEP_DMC is required; no private default path is used")
    main(args.output, args.fep_dmc, args.image)
