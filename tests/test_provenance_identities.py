"""Provenance identities: public source vs timed historical source.

These tests exist to stop a reader (or a later edit) from treating
v1.0.0 checksums, the timed confirm-tree Fortran, and the current
public tree as the same object.

Science numbers are locked by hash. Documentation must distinguish
historical vs current files.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Timed confirm-tree excerpt, frozen in v1.0.0 / the 0.956 binary source.
# Immutable. v1.0.1 F03 changed the public file; the hashes must differ.
TIMED_LINEAR_DA_MOD_SHA256 = (
    "004b23b66e00f4ca20e2cc683c8e99124f12713549fcc02363e0e0afc37854df"
)
P1_CLEAN_BINARY_SHA256 = (
    "f9518a21fc2b8750fb3b7ed6f6e065db398cb2f425969cd718d1dcdef2b2c25c"
)
V101_COMMIT = "e418d88153c31f767486a016014cf71c0d091dce"
V100_COMMIT = "77835ca15e5846863aeab8ad32ebfbb46f66353c"
V101_ARCHIVE_SHA256 = (
    "e35c17f7afad2e3fe80ccbf63b115c6a184a4455d00c0e93ee9cac882fff51f8"
)
# Private live-extract wrap-up commit recorded in FINAL_PROVENANCE.json.
# Not a public GitHub commit.
HISTORICAL_WRAPUP_EXTRACT_COMMIT = (
    "6e5529f481bf0751d6b619bd427aff250c712d55"
)

HISTORICAL_SUMS = ROOT / "release/2026-09-16/SHA256SUMS.txt"
V102_SUMS = ROOT / "release/v1.0.2/SHA256SUMS.txt"
V102_PROVENANCE = ROOT / "release/v1.0.2/PROVENANCE.json"
# v1.0.2 SHA256SUMS.txt is immutable. Do not rewrite it when README/docs move on.
V102_SUMS_FILE_SHA256 = (
    "ea84202aaecf84e03bd3b7eaf65ebc8875a2458920f218208a7eaf8042dff47f"
)
V103_SUMS = ROOT / "release/v1.0.3/SHA256SUMS.txt"
V103_PROVENANCE = ROOT / "release/v1.0.3/PROVENANCE.json"
# v1.0.3 SHA256SUMS.txt is immutable. Do not rewrite it for v1.1.0.
V103_SUMS_FILE_SHA256 = (
    "f2bb278dee11f5ae1002a9420f0e095b14cd54cffef904f13d7d81935032f418"
)
V103_CANDIDATE_COMMIT = "e2735a1603ad4351e3b84d1ec9109adb20d0d426"
V111_SUMS = ROOT / "release/v1.1.0/SHA256SUMS.txt"
V111_PROVENANCE = ROOT / "release/v1.1.0/PROVENANCE.json"
V111_SUMS_FILE_SHA256 = (
    "8b5752fb65c1feb82308a3d63452fe76504f45e39dc8d5ffaf5a2a20ba4ff158"
)
V111_CANDIDATE_COMMIT = "3bc9098888cafc8c88eaa19ad63009fcae56f6a6"
V120_SUMS = ROOT / "release/v1.2.0/SHA256SUMS.txt"
V120_PROVENANCE = ROOT / "release/v1.2.0/PROVENANCE.json"
# v1.2.0 SHA256SUMS.txt is immutable. Do not rewrite it for v1.3.0.
V120_SUMS_FILE_SHA256 = (
    "829f3d0533783c6a0952c80b7874fe60adbd22c9da8c3ea0f42f2b862fd862f8"
)
V130_SUMS = ROOT / "release/v1.3.0/SHA256SUMS.txt"
V130_PROVENANCE = ROOT / "release/v1.3.0/PROVENANCE.json"
# v1.3.0 SHA256SUMS.txt is immutable. Do not rewrite it for v1.3.1.
V130_SUMS_FILE_SHA256 = (
    "3d50ac8dc2bc771c6b263355005208a8f27bc337a6c27861c8b1ab235fa4c059"
)
FROZEN_P1 = ROOT / "benchmarks/p1_vs_bbest/frozen_results.json"
LINEAR_DA = ROOT / "src/future_b/fortran/linear_da_mod.f90"


def _version() -> str:
    return (ROOT / "VERSION").read_text().strip()


def _current_sums() -> Path:
    return ROOT / "release" / f"v{_version()}" / "SHA256SUMS.txt"


def _current_provenance() -> Path:
    return ROOT / "release" / f"v{_version()}" / "PROVENANCE.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _parse_sums(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, name = line.split(None, 1)
        out[name] = digest
    return out


def test_timed_linear_da_mod_hash_is_the_frozen_v100_pin():
    frozen = json.loads(FROZEN_P1.read_text())
    assert frozen["timed_path_provenance"]["linear_da_mod_sha256"] == TIMED_LINEAR_DA_MOD_SHA256
    assert frozen["binaries"]["P1_clean"] == P1_CLEAN_BINARY_SHA256
    assert frozen["classification"] == "P1_UNRESOLVED_WITHIN_BUDGET"


def test_current_linear_da_mod_is_not_the_timed_file():
    current = _sha256(LINEAR_DA)
    assert current != TIMED_LINEAR_DA_MOD_SHA256
    assert len(current) == 64
    assert re.fullmatch(r"[0-9a-f]{64}", current)


def test_historical_v100_sums_do_not_match_current_readme_or_scientific_result():
    hist = _parse_sums(HISTORICAL_SUMS)
    assert hist["README.md"] != _sha256(ROOT / "README.md")
    assert hist["docs/SCIENTIFIC_RESULT.md"] != _sha256(ROOT / "docs/SCIENTIFIC_RESULT.md")
    # Frozen science files in that list must still match (result not rewritten).
    assert hist["benchmarks/p1_vs_bbest/frozen_results.json"] == _sha256(FROZEN_P1)
    assert hist["benchmarks/c5_dev/frozen_results.json"] == _sha256(
        ROOT / "benchmarks/c5_dev/frozen_results.json"
    )


def test_public_manifest_does_not_claim_historical_lists_match_current_tree():
    text = (ROOT / "docs/PUBLIC_MANIFEST.md").read_text()
    assert "still match those historical" not in text
    assert "Existing hashed files that are in the tree still match" not in text


def test_provenance_md_does_not_claim_github_excerpt_is_byte_identical_to_timed_source():
    text = (ROOT / "docs/PROVENANCE.md").read_text()
    assert "byte-identical copy of the confirm-tree source" not in text
    current = _sha256(LINEAR_DA)
    assert TIMED_LINEAR_DA_MOD_SHA256 in text
    assert current in text


def test_readme_does_not_claim_excerpts_match_timed_clean_source():
    text = (ROOT / "README.md").read_text()
    assert "still match the timed clean source" not in text


def test_v102_provenance_records_both_fortran_identities():
    assert V102_PROVENANCE.is_file(), "release/v1.0.2/PROVENANCE.json is required"
    rec = json.loads(V102_PROVENANCE.read_text())
    timed = rec["timed_historical_source"]["timed_linear_da_mod_sha256"]
    current_doc = rec["current_public_source"]["linear_da_mod_sha256"]
    assert timed == TIMED_LINEAR_DA_MOD_SHA256
    assert current_doc == _sha256(LINEAR_DA)
    assert rec["current_public_source"]["linear_da_mod_differs_from_timed"] is True
    assert timed != current_doc
    assert rec["public_version"] == "1.0.2"


def test_v102_checksum_file_is_immutable():
    assert _sha256(V102_SUMS) == V102_SUMS_FILE_SHA256


def test_v103_checksum_file_is_immutable():
    assert V103_SUMS.is_file()
    assert _sha256(V103_SUMS) == V103_SUMS_FILE_SHA256
    rec = json.loads(V103_PROVENANCE.read_text())
    assert rec["public_version"] == "1.0.3"


def test_v111_checksum_file_is_immutable():
    assert V111_SUMS.is_file()
    assert _sha256(V111_SUMS) == V111_SUMS_FILE_SHA256
    rec = json.loads(V111_PROVENANCE.read_text())
    assert rec["public_version"] == "1.1.0"


def test_v120_checksum_file_is_immutable():
    assert V120_SUMS.is_file()
    assert _sha256(V120_SUMS) == V120_SUMS_FILE_SHA256
    rec = json.loads(V120_PROVENANCE.read_text())
    assert rec["public_version"] == "1.2.0"


def test_v130_checksum_file_is_immutable():
    assert V130_SUMS.is_file()
    assert _sha256(V130_SUMS) == V130_SUMS_FILE_SHA256
    rec = json.loads(V130_PROVENANCE.read_text())
    assert rec["public_version"] == "1.3.0"


def test_v130_patched_fortran_and_frozen_science_still_match_v130_sums():
    # v1.3.1 corrects documentation only; the patched Fortran is unchanged.
    sums = _parse_sums(V130_SUMS)
    for rel in (
        "benchmarks/p1_vs_bbest/frozen_results.json",
        "src/future_b/fepdmc/data/bchain.f90",
        "src/future_b/fepdmc/data/rb_window.f90",
        "src/future_b/fepdmc/data/mkl_vsl.f90",
        "src/future_b/fepdmc/data/make.sys",
        "src/future_b/fepdmc/patches/extfix.py",
        "src/future_b/fepdmc/patches/extrmfix.py",
    ):
        assert _sha256(ROOT / rel) == sums[rel], rel


def test_v120_science_production_fortran_and_adapters_still_match_v120_sums():
    sums = _parse_sums(V120_SUMS)
    for rel in (
        "benchmarks/p1_vs_bbest/frozen_results.json",
        "benchmarks/c5_dev/frozen_results.json",
        "src/future_b/fortran/linear_da_mod.f90",
        "src/future_b/fortran/update_swap_p1_excerpt.f90",
        "integration/c0/apply_c0.py",
        "integration/p1/apply_p1.py",
        "integration/p1/linear_da_mod.f90",
        "provenance/UPSTREAM_FEP_DMC.json",
    ):
        assert _sha256(ROOT / rel) == sums[rel], rel


def test_v102_science_and_production_fortran_still_match_v102_sums():
    sums = _parse_sums(V102_SUMS)
    for rel in (
        "benchmarks/p1_vs_bbest/frozen_results.json",
        "benchmarks/c5_dev/frozen_results.json",
        "src/future_b/fortran/linear_da_mod.f90",
        "src/future_b/fortran/update_swap_p1_excerpt.f90",
    ):
        assert _sha256(ROOT / rel) == sums[rel], rel


def test_v103_science_and_production_fortran_still_match_v103_sums():
    sums = _parse_sums(V103_SUMS)
    for rel in (
        "benchmarks/p1_vs_bbest/frozen_results.json",
        "benchmarks/c5_dev/frozen_results.json",
        "src/future_b/fortran/linear_da_mod.f90",
        "src/future_b/fortran/update_swap_p1_excerpt.f90",
    ):
        assert _sha256(ROOT / rel) == sums[rel], rel


def test_v111_science_and_production_fortran_still_match_v111_sums():
    sums = _parse_sums(V111_SUMS)
    for rel in (
        "benchmarks/p1_vs_bbest/frozen_results.json",
        "benchmarks/c5_dev/frozen_results.json",
        "src/future_b/fortran/linear_da_mod.f90",
        "src/future_b/fortran/update_swap_p1_excerpt.f90",
    ):
        assert _sha256(ROOT / rel) == sums[rel], rel


def test_current_sha256sums_validate_claimed_files():
    version = _version()
    if version == "1.0.2":
        # v1.0.2 SHA256SUMS is a frozen tree snapshot, not a live lock.
        return
    path = _current_sums()
    assert path.is_file(), f"missing {path} for VERSION={version}"
    sums = _parse_sums(path)
    assert "release/2026-09-16/SHA256SUMS.txt" not in sums
    assert sums, "current checksum file is empty"
    for name, digest in sums.items():
        fpath = ROOT / name
        assert fpath.is_file(), name
        assert _sha256(fpath) == digest, name


def test_historical_sha256sums_file_bytes_are_unchanged():
    # Pin the historical list itself so it cannot be "cleaned up".
    assert _sha256(HISTORICAL_SUMS) == (
        "ec5af757820392029baf5c35042acce11c658889faf27fe9594fbd08fc741fd9"
    )


def test_historical_wrapup_commit_is_documented_as_not_public_v101():
    rec = json.loads(V102_PROVENANCE.read_text())
    wrap = rec["historical_wrapup_git_commit_in_FINAL_PROVENANCE"]
    assert wrap["git_commit"] == HISTORICAL_WRAPUP_EXTRACT_COMMIT
    assert wrap["git_commit"] != V101_COMMIT
    assert wrap["git_commit"] != V100_COMMIT
    hist = json.loads((ROOT / "release/2026-09-16/FINAL_PROVENANCE.json").read_text())
    assert hist["git_commit"] == HISTORICAL_WRAPUP_EXTRACT_COMMIT


def test_public_version_files_agree():
    version = _version()
    pyproject = (ROOT / "pyproject.toml").read_text()
    init = (ROOT / "src/future_b/__init__.py").read_text()
    citation = (ROOT / "CITATION.cff").read_text()
    assert f'version = "{version}"' in pyproject
    assert f'__version__ = "{version}"' in init
    assert f'version: "{version}"' in citation
    rec_path = _current_provenance()
    if rec_path.is_file():
        rec = json.loads(rec_path.read_text())
        assert rec["public_version"] == version


def test_v102_tag_is_the_commit_binding_when_present():
    import subprocess

    rec = json.loads(V102_PROVENANCE.read_text())
    tag = rec["public_git_tag"]
    assert tag == "v1.0.2"
    assert rec["public_git_commit_binding"] == "git_tag"
    assert rec["public_git_commit"] is None
    proc = subprocess.run(
        ["git", "rev-parse", "--verify", f"{tag}^{{commit}}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return
    peel = proc.stdout.strip()
    assert peel == "05eab61108cae7e512a89f26530996c1591851b8"
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    anc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", peel, head], cwd=ROOT
    )
    assert anc.returncode == 0
