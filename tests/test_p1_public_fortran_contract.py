"""Public P1 Fortran module and patched-source falsifiers (no compiler)."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from future_b.p1_da import (
    delayed_acceptance_prob,
    native_re_ratio,
    native_re_target,
    stage2_exact_accept,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "integration" / "p1" / "linear_da_mod.f90"
RECORD = ROOT / "provenance" / "P1_PUBLIC_PATCH.json"
HIST = ROOT / "src" / "future_b" / "fortran" / "linear_da_mod.f90"

BANNED = (
    "C2_FORCE_A1",
    "P1_FIXTURE",
    "p1_fixture_on",
    "c1_mark_",
    "c2_dump_swap",
    "c2_live_fp",
    "c0_copy_wq",
    "night1",
    "shadow",
)


def test_public_module_is_not_the_historical_archive():
    assert MODULE.is_file()
    assert HIST.is_file()
    pub = MODULE.read_bytes()
    hist = HIST.read_bytes()
    assert hashlib.sha256(pub).hexdigest() != hashlib.sha256(hist).hexdigest()
    text = pub.decode()
    for b in BANNED:
        assert b not in text, b
    assert "error stop" in text or "stop '" in text
    assert "DMC_Method" in text
    assert "dmc_band" in text
    assert "zeroTMC" in text
    assert "sample_gt" in text
    assert "Gel(" in text and "Dph(" in text
    assert "cal_ek_int" in text
    # exact ell_R must come from P_accept, not a re-sum of Gel/Dph in stage2
    stage2 = text.split("subroutine linear_da_stage2", 1)[1].split("end subroutine", 1)[0]
    assert "P_accept" in stage2
    assert "log(" in stage2
    assert "ell_hat" in stage2
    assert "Gel(" not in stage2
    assert "Dph(" not in stage2


def test_p1_record_schema_and_not_donor():
    rec = json.loads(RECORD.read_text())
    assert rec["adapter"] == "p1_delayed_acceptance"
    assert rec["architecture"] == "C"
    assert rec["historical_donor_equivalence"] == "not_established"
    assert rec["upstream_commit"] == json.loads(
        (ROOT / "provenance" / "UPSTREAM_FEP_DMC.json").read_text()
    )["reference_commit"]
    assert rec["module_sha256"] == hashlib.sha256(MODULE.read_bytes()).hexdigest()
    for name in (
        "PUBLIC_PRISTINE",
        "PUBLIC_C0_APPLIED",
        "PUBLIC_P1_APPLIED",
        "PUBLIC_C0_P1_APPLIED",
    ):
        st = rec["states"][name]
        for key in (
            "perturbo-fep-dmc/pert-src/diagMC_JJ_updates.f90",
            "perturbo-fep-dmc/pert-src/makefile",
            "perturbo-fep-dmc/pert-src/diagMC_JJ.f90",
        ):
            assert len(st[key]) == 64, key


def test_da_reciprocal_identity_with_clipped_score():
    clip = math.log(10.0)
    for r in (0.01, 0.2, 0.9, 1.0, 1.7, 12.0, 40.0):
        ell = math.log(r)
        eh = max(-clip, min(clip, ell))
        rhat = math.exp(eh)
        a_xy = delayed_acceptance_prob(1.0, r, rhat)
        a_yx = delayed_acceptance_prob(r, 1.0, 1.0 / rhat)
        assert abs(a_xy / a_yx - r) <= 1e-12 * max(1.0, r)


def test_dropping_ell_hat_correction_is_a_different_kernel():
    ell_r, ell_hat, ran = 0.3, 0.5, 0.9
    ok = stage2_exact_accept(ran, ell_r, ell_hat)
    wrong = math.log(max(ran, 1.0e-300)) < min(0.0, ell_r)
    assert ok is False
    assert wrong is True


def test_abs_complex_is_not_r_native():
    mx, my = 1.0 + 0.8j, 0.5 - 0.9j
    r = native_re_ratio(my, mx)
    wrong = abs(my) / abs(mx)
    assert abs(wrong - r) > 1e-8
    assert abs(native_re_target(mx)) == abs(mx.real)


def test_zero_new_real_part_rejects():
    assert delayed_acceptance_prob(2.0, 0.0, 1.5) == 0.0
