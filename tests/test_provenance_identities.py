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
CURRENT_SUMS = ROOT / "release/v1.0.2/SHA256SUMS.txt"
CURRENT_PROVENANCE = ROOT / "release/v1.0.2/PROVENANCE.json"
FROZEN_P1 = ROOT / "benchmarks/p1_vs_bbest/frozen_results.json"
LINEAR_DA = ROOT / "src/future_b/fortran/linear_da_mod.f90"


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


def test_current_maintenance_provenance_records_both_fortran_identities():
    assert CURRENT_PROVENANCE.is_file(), "release/v1.0.2/PROVENANCE.json is required"
    rec = json.loads(CURRENT_PROVENANCE.read_text())
    timed = rec["timed_historical_source"]["timed_linear_da_mod_sha256"]
    current_doc = rec["current_public_source"]["linear_da_mod_sha256"]
    assert timed == TIMED_LINEAR_DA_MOD_SHA256
    assert current_doc == _sha256(LINEAR_DA)
    assert rec["current_public_source"]["linear_da_mod_differs_from_timed"] is True
    assert timed != current_doc


def test_current_sha256sums_validate_claimed_files():
    assert CURRENT_SUMS.is_file(), "release/v1.0.2/SHA256SUMS.txt is required"
    sums = _parse_sums(CURRENT_SUMS)
    assert "release/2026-09-16/SHA256SUMS.txt" not in sums
    assert sums, "current checksum file is empty"
    for name, digest in sums.items():
        path = ROOT / name
        assert path.is_file(), name
        assert _sha256(path) == digest, name


def test_historical_sha256sums_file_bytes_are_unchanged():
    # Pin the historical list itself so it cannot be "cleaned up".
    assert _sha256(HISTORICAL_SUMS) == (
        "ec5af757820392029baf5c35042acce11c658889faf27fe9594fbd08fc741fd9"
    )


def test_historical_wrapup_commit_is_documented_as_not_public_v101():
    rec = json.loads(CURRENT_PROVENANCE.read_text())
    wrap = rec["historical_wrapup_git_commit_in_FINAL_PROVENANCE"]
    assert wrap["git_commit"] == HISTORICAL_WRAPUP_EXTRACT_COMMIT
    assert wrap["git_commit"] != V101_COMMIT
    assert wrap["git_commit"] != V100_COMMIT
    hist = json.loads((ROOT / "release/2026-09-16/FINAL_PROVENANCE.json").read_text())
    assert hist["git_commit"] == HISTORICAL_WRAPUP_EXTRACT_COMMIT


def test_public_version_files_agree():
    version = (ROOT / "VERSION").read_text().strip()
    pyproject = (ROOT / "pyproject.toml").read_text()
    init = (ROOT / "src/future_b/__init__.py").read_text()
    citation = (ROOT / "CITATION.cff").read_text()
    rec = json.loads(CURRENT_PROVENANCE.read_text())
    assert rec["public_version"] == version
    assert f'version = "{version}"' in pyproject
    assert f'__version__ = "{version}"' in init
    assert f'version: "{version}"' in citation
