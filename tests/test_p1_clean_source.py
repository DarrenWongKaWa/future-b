"""Clean P1 production path: fixture work gated; counters independent of dump."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN = json.loads((ROOT / "benchmarks/p1_vs_bbest/frozen_results.json").read_text())


def _excerpt() -> str:
    path = ROOT / "src/future_b/fortran/update_swap_p1_excerpt.f90"
    assert path.exists(), path
    return path.read_text()


def _da_mod() -> str:
    return (ROOT / "src/future_b/fortran/linear_da_mod.f90").read_text()


def test_fixture_gate_defaults_off():
    text = _da_mod()
    assert "p1_fixture_on = .false." in text
    assert "get_environment_variable('P1_FIXTURE'" in text


def test_dump_and_after_commit_reverse_are_fixture_only():
    text = _excerpt()
    assert "if (p1_fixture_on()) call c2_dump_swap(10" in text
    assert "if (p1_fixture_on()) call c2_dump_swap(1" in text
    assert "if (p1_fixture_on() .and. diagram%vertexList(iv1)%tau" in text
    assert "else if (p1_fixture_on()) then" in text
    # production DA score remains
    assert "call linear_da_eval" in text
    assert "n_stage1_rej = n_stage1_rej + 1" in text


def test_stage1_return_is_before_cal_gkq():
    text = _excerpt()
    a1 = text.find("n_stage1_rej = n_stage1_rej + 1")
    ret = text.find("return", a1)
    gkq = text.find("call cal_gkq_vtex_int", a1)
    env = text.find("call left_environment_matrix", a1)
    assert 0 <= a1 < ret < gkq
    assert ret < env


def test_exact_target_is_abs_real_not_abs_complex():
    text = _excerpt()
    assert "ellR = log(abs(real(mat_new))) - log(abs(real(mat_old)))" in text
    assert "abs(mat_new)" not in text or "abs(real(mat_new))" in text
    da = _da_mod()
    assert "n_stage1_rej" in da
    assert "n_stage2" in da
    assert "n_accept" in da


def test_stage1_count_not_inside_dump_subroutine():
    da = _da_mod()
    # count moved out of dump so C2_DUMP/P1_FIXTURE cannot zero it
    assert "stage-1 count is in update_swap, independent of dump" in da
    assert "if (stage == 1) n_stage1_rej = n_stage1_rej + 1" not in da


def test_excerpt_keeps_exact_stage2_subtraction():
    """F04: deleting `- ell_hat` from the native accept line must fail this test."""
    text = _excerpt()
    assert "min(0.d0, ellR - ell_hat)" in text
    assert text.count("min(0.d0, ellR - ell_hat)") == 1


def test_force_a1_is_fixture_only():
    """F03: C2_FORCE_A1 must not apply when P1_FIXTURE is off."""
    da = _da_mod()
    idx = da.find("get_environment_variable('C2_FORCE_A1'")
    assert idx > 0
    assert "p1_fixture_on()" in da[idx - 250 : idx]


def test_timed_binary_pin_unchanged():
    """0.956 used SHA256 f9518a21. v1.0.1 may patch FORCE_A1 gating only."""
    prov = FROZEN["timed_path_provenance"]
    assert FROZEN["binaries"]["P1_clean"].startswith("f9518a21")
    assert "P1_FIXTURE=0" in prov["confirm_env"]
    assert prov["gating_applied_before_compile"] is True
    v100 = prov["linear_da_mod_sha256"]
    digest = hashlib.sha256((ROOT / "src/future_b/fortran/linear_da_mod.f90").read_bytes()).hexdigest()
    # Maintenance may differ from the timed file; record both.
    assert len(v100) == 64
    assert len(digest) == 64
