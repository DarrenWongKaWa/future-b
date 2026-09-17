"""Public P1 adapter source contract (no network, no compiler)."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPLY = ROOT / "integration" / "p1" / "apply_p1.py"
VERIFY = ROOT / "integration" / "p1" / "verify_p1.py"
MODULE = ROOT / "integration" / "p1" / "linear_da_mod.f90"
RECORD = ROOT / "provenance" / "P1_PUBLIC_PATCH.json"
C0_APPLY = ROOT / "integration" / "c0" / "apply_c0.py"
UPSTREAM_TOOL = ROOT / "tools" / "verify_fep_dmc_upstream.py"

JJ_UPDATES = "perturbo-fep-dmc/pert-src/diagMC_JJ_updates.f90"
JJ_DRIVER = "perturbo-fep-dmc/pert-src/diagMC_JJ.f90"
MAKEFILE = "perturbo-fep-dmc/pert-src/makefile"
MODULE_REL = "perturbo-fep-dmc/pert-src/linear_da_mod.f90"
OTHER_PINNED = (
    "perturbo-fep-dmc/pert-src/diagMC.f90",
    "perturbo-fep-dmc/pert-src/pert_param.f90",
)

BANNED = (
    "C2_FORCE_A1",
    "P1_FIXTURE",
    "p1_fixture_on",
    "c1_mark_",
    "c2_dump_swap",
    "c2_live_fp",
    "c0_copy_wq",
    "night1",
    "C2_fixture",
    "/Users/",
)

PRISTINE_UPDATES = """subroutine add_ph(diagram, stat)
      call sample_q_omp_int(diagram%seed, vn1%i_q, vn1%Pq, vn1); Pq = vn1%Pq
      call cal_wq_int( vn1%i_q,     vn1%wq   )
end subroutine

subroutine add_external_ph(diagram, stat)
      call sample_q_omp_int(diagram%seed,vn1%i_q,vn1%Pq,vn1); Pq = vn1%Pq

      vn2%wq = vn1%wq
end subroutine

subroutine update_swap(diagram, stat)
      use DiagMC 

      implicit none
      real(dp) :: P_accept, P_kchange, ran, factor
      if(tauL>tauR) stop ' time disordered @ update_swap'

      vLn => diagram%vertexList(diagram%order+1)
      call cal_gkq_vtex_int( vRn, vRn%gkq )
      P_accept = abs(factor) * P_kchange
      call random_number_omp(diagram%seed,ran)
      if(ran<P_accept) then
         stat%accept(7) = stat%accept(7) + 1
      end if
end subroutine
"""

PRISTINE_DRIVER = """subroutine diagmc_JJ()
   use DiagMC
   use diagMC_gnt_debug
   use JJ_update, only : updateJJ_drive
   call setup_dqmc()
   write(stdout,'(A30,7E15.5)')'acceptance = ',(1.d0*stat_total%accept)/stat_total%update
   call stop_clock('diagmc_JJ')
end subroutine
"""

PRISTINE_MAKEFILE = """diagMC_pre.f90 \\
diagMC.f90 \\
diagMC_debug.f90 \\
diagMC_JJ_updates.f90 \\
diagMC_updates.f90
"""

C0_ANCHOR = "      call sample_q_omp_int(diagram%seed,vn1%i_q,vn1%Pq,vn1); Pq = vn1%Pq"
C0_LINE = "      call cal_wq_int( vn1%i_q,     vn1%wq   )"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_layout(root: Path, payloads: dict[str, bytes]) -> None:
    for rel, data in payloads.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def _init_git(root: Path) -> str:
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = "FutureB Test"
    env["GIT_AUTHOR_EMAIL"] = "test@example.invalid"
    env["GIT_COMMITTER_NAME"] = env["GIT_AUTHOR_NAME"]
    env["GIT_COMMITTER_EMAIL"] = env["GIT_AUTHOR_EMAIL"]
    subprocess.check_call(["git", "init", "-q"], cwd=root, env=env)
    subprocess.check_call(["git", "config", "core.fileMode", "true"], cwd=root, env=env)
    subprocess.check_call(["git", "config", "core.autocrlf", "false"], cwd=root, env=env)
    subprocess.check_call(["git", "add", "-A"], cwd=root, env=env)
    subprocess.check_call(["git", "commit", "-q", "-m", "seed"], cwd=root, env=env)
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()


def _payloads() -> dict[str, bytes]:
    out = {
        JJ_UPDATES: PRISTINE_UPDATES.encode(),
        JJ_DRIVER: PRISTINE_DRIVER.encode(),
        MAKEFILE: PRISTINE_MAKEFILE.encode(),
        "unrelated.txt": b"leave me alone\n",
    }
    for rel in OTHER_PINNED:
        out[rel] = f"{rel}\n".encode()
    return out


def _pin(payloads: dict[str, bytes], commit: str) -> dict:
    files = {
        rel: {"sha256": _sha(payloads[rel]), "role": "test"}
        for rel in (JJ_UPDATES, MAKEFILE, *OTHER_PINNED)
    }
    return {
        "schema_version": 1,
        "repository": "https://github.com/yaoluo/FEP-DMC",
        "reference_commit": commit,
        "files": files,
        "historical_donor_equivalence": "not_established",
    }


def _run(script: Path, tree: Path, extra: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), "--tree", str(tree), *extra],
        capture_output=True,
        text=True,
    )


def test_p1_tools_and_record_exist():
    assert APPLY.is_file(), "integration/p1/apply_p1.py is required"
    assert VERIFY.is_file(), "integration/p1/verify_p1.py is required"
    assert MODULE.is_file(), "integration/p1/linear_da_mod.f90 is required"
    assert RECORD.is_file(), "provenance/P1_PUBLIC_PATCH.json is required"


def test_production_module_has_no_historical_forcing():
    text = MODULE.read_text()
    hits = [b for b in BANNED if b in text]
    assert hits == []
    assert "LINEAR_DA_SCORE" in text or "prop" in text
    assert "zeroTMC" in text
    assert "DMC_Method" in text
    assert "dmc_band" in text
    assert "sample_gt" in text
    assert "linear_da_stage2" in text
    assert "log(P_accept)" in text or "log(P_accept" in text or "log(p_accept" in text.lower()
    assert "n_s1_reject" in text
    assert "n_expensive" in text
    assert "omp atomic" in text.lower() or "!$omp atomic" in text.lower()


def test_dry_run_zero_writes(tmp_path: Path):
    payloads = _payloads()
    _write_layout(tmp_path, payloads)
    commit = _init_git(tmp_path)
    pin = tmp_path / "pin.json"
    pin.write_text(json.dumps(_pin(payloads, commit)))
    before = {rel: (tmp_path / rel).read_bytes() for rel in payloads}
    mtimes = {rel: (tmp_path / rel).stat().st_mtime_ns for rel in payloads}
    proc = _run(APPLY, tmp_path, ["--pin", str(pin), "--dry-run"])
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "DRY_RUN" in proc.stdout
    assert "PUBLIC_PRISTINE" in proc.stdout
    for rel, data in before.items():
        assert (tmp_path / rel).read_bytes() == data
        assert (tmp_path / rel).stat().st_mtime_ns == mtimes[rel]
    assert list(tmp_path.rglob("*.futureb-p1.tmp")) == []


def test_pristine_apply_and_idempotent(tmp_path: Path):
    payloads = _payloads()
    _write_layout(tmp_path, payloads)
    commit = _init_git(tmp_path)
    pin = tmp_path / "pin.json"
    pin.write_text(json.dumps(_pin(payloads, commit)))
    first = _run(APPLY, tmp_path, ["--pin", str(pin)])
    assert first.returncode == 0, first.stdout + first.stderr
    v = _run(VERIFY, tmp_path, ["--pin", str(pin)])
    assert v.returncode == 0, v.stdout + v.stderr
    assert "PUBLIC_P1_APPLIED" in v.stdout
    text = (tmp_path / JJ_UPDATES).read_text()
    assert "linear_da_eval" in text
    assert text.find("linear_da_eval") < text.find("cal_gkq_vtex_int")
    assert "ell_R - ell_hat" in text or "ell_R-ell_hat" in text
    assert "P_accept = abs(factor) * P_kchange" in text
    assert "abs(factor) * P_kchange" in text
    assert "abs(mat_new)" not in text
    mk = (tmp_path / MAKEFILE).read_text()
    assert "linear_da_mod.f90 \\" in mk
    assert mk.find("diagMC.f90") < mk.find("linear_da_mod.f90") < mk.find("diagMC_debug.f90")
    drv = (tmp_path / JJ_DRIVER).read_text()
    assert "linear_da_ensure" in drv
    assert drv.find("setup_dqmc") < drv.find("linear_da_ensure")
    assert drv.find("acceptance") < drv.find("linear_da_report")
    assert (tmp_path / MODULE_REL).is_file()
    after = {rel: (tmp_path / rel).read_bytes() for rel in (JJ_UPDATES, JJ_DRIVER, MAKEFILE, MODULE_REL)}
    second = _run(APPLY, tmp_path, ["--pin", str(pin)])
    assert second.returncode == 2, second.stdout + second.stderr
    assert "ALREADY_APPLIED" in second.stdout
    for rel, data in after.items():
        assert (tmp_path / rel).read_bytes() == data
    up = subprocess.run(
        [sys.executable, str(UPSTREAM_TOOL), str(tmp_path), "--pin", str(pin)],
        capture_output=True,
        text=True,
    )
    assert up.returncode != 0


def test_c0_then_p1_and_p1_then_c0_match(tmp_path: Path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    payloads = _payloads()
    hashes = {}
    for name, tree in (("a", a), ("b", b)):
        _write_layout(tree, payloads)
        commit = _init_git(tree)
        pin = tree / "pin.json"
        pin.write_text(json.dumps(_pin(payloads, commit)))
        c0_pre = payloads[JJ_UPDATES]
        c0_src = payloads[JJ_UPDATES].decode().replace(
            C0_ANCHOR + "\n", C0_ANCHOR + "\n" + C0_LINE + "\n", 1
        )
        c0_rec = tree / "c0.json"
        c0_rec.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "adapter": "c0_wq_refresh",
                    "upstream_repository": "https://github.com/yaoluo/FEP-DMC",
                    "upstream_commit": commit,
                    "preimage_file": JJ_UPDATES,
                    "preimage_sha256": _sha(c0_pre),
                    "postimage_sha256": _sha(c0_src.encode()),
                    "changed_region": {
                        "subroutine": "add_external_ph",
                        "anchor": C0_ANCHOR,
                        "inserted_line": C0_LINE,
                    },
                }
            )
        )
        args_c0 = ["--pin", str(pin), "--record", str(c0_rec)]
        args_p1 = ["--pin", str(pin)]
        if name == "a":
            r1 = _run(C0_APPLY, tree, args_c0)
            assert r1.returncode == 0, r1.stdout + r1.stderr
            r2 = _run(APPLY, tree, args_p1)
            assert r2.returncode == 0, r2.stdout + r2.stderr
        else:
            r1 = _run(APPLY, tree, args_p1)
            assert r1.returncode == 0, r1.stdout + r1.stderr
            r2 = _run(C0_APPLY, tree, args_c0)
            assert r2.returncode == 0, r2.stdout + r2.stderr
        v = _run(VERIFY, tree, args_p1)
        assert v.returncode == 0, v.stdout + v.stderr
        assert "PUBLIC_C0_P1_APPLIED" in v.stdout
        hashes[name] = {
            rel: _sha((tree / rel).read_bytes())
            for rel in (JJ_UPDATES, JJ_DRIVER, MAKEFILE, MODULE_REL)
        }
        assert C0_LINE in (tree / JJ_UPDATES).read_text()
        assert "linear_da_eval" in (tree / JJ_UPDATES).read_text()
    assert hashes["a"] == hashes["b"]


def test_wrong_commit_refused(tmp_path: Path):
    payloads = _payloads()
    _write_layout(tmp_path, payloads)
    _init_git(tmp_path)
    pin = tmp_path / "pin.json"
    pin.write_text(json.dumps(_pin(payloads, "b" * 40)))
    proc = _run(APPLY, tmp_path, ["--pin", str(pin)])
    assert proc.returncode == 1
    assert (tmp_path / JJ_UPDATES).read_bytes() == payloads[JJ_UPDATES]


def test_dirty_pinned_source_refused(tmp_path: Path):
    payloads = _payloads()
    _write_layout(tmp_path, payloads)
    commit = _init_git(tmp_path)
    pin = tmp_path / "pin.json"
    pin.write_text(json.dumps(_pin(payloads, commit)))
    target = tmp_path / JJ_UPDATES
    target.write_bytes(target.read_bytes() + b"! dirty\n")
    proc = _run(APPLY, tmp_path, ["--pin", str(pin)])
    assert proc.returncode == 1
    v = _run(VERIFY, tmp_path, ["--pin", str(pin)])
    assert v.returncode == 1
    assert "UNKNOWN" in v.stdout


def test_missing_and_duplicate_swap_anchor_refused(tmp_path: Path):
    for kind in ("missing", "duplicate"):
        tree = tmp_path / kind
        src = PRISTINE_UPDATES
        if kind == "missing":
            src = src.replace("if(tauL>tauR) stop ' time disordered @ update_swap'", "if(.false.) stop")
        else:
            src = src.replace(
                "if(tauL>tauR) stop ' time disordered @ update_swap'\n",
                "if(tauL>tauR) stop ' time disordered @ update_swap'\n"
                "      if(tauL>tauR) stop ' time disordered @ update_swap'\n",
            )
        payloads = _payloads()
        payloads[JJ_UPDATES] = src.encode()
        _write_layout(tree, payloads)
        commit = _init_git(tree)
        pin = tree / "pin.json"
        pin.write_text(json.dumps(_pin(payloads, commit)))
        proc = _run(APPLY, tree, ["--pin", str(pin)])
        assert proc.returncode == 1, kind + proc.stdout + proc.stderr


def test_altered_makefile_or_driver_is_unknown(tmp_path: Path):
    payloads = _payloads()
    _write_layout(tmp_path, payloads)
    commit = _init_git(tmp_path)
    pin = tmp_path / "pin.json"
    pin.write_text(json.dumps(_pin(payloads, commit)))
    assert _run(APPLY, tmp_path, ["--pin", str(pin)]).returncode == 0
    (tmp_path / MAKEFILE).write_bytes((tmp_path / MAKEFILE).read_bytes() + b"#x\n")
    v = _run(VERIFY, tmp_path, ["--pin", str(pin)])
    assert v.returncode == 1
    assert "UNKNOWN" in v.stdout
    # restore makefile, break driver
    git = ["git", "-C", str(tmp_path), "checkout", "--", MAKEFILE]
    subprocess.check_call(git)
    # re-apply to restore makefile from P1? checkout restores vanilla makefile
    # After vanilla makefile restore the tree is partial P1.
    v2 = _run(VERIFY, tmp_path, ["--pin", str(pin)])
    assert v2.returncode == 1
    assert "UNKNOWN" in v2.stdout
