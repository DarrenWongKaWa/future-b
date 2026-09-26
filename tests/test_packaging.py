"""Packaging gates: wheel/sdist boundaries and no private-path runtime.

These tests inspect the *source tree* that setuptools will package.
They do not build a wheel (that is a release-job check).
"""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "future_b"

# Canonical files tests open. Keep this list in sync with MANIFEST.in.
SDIST_TEST_DATA = (
    "benchmarks/p1_vs_bbest/frozen_results.json",
    "benchmarks/c5_dev/frozen_results.json",
    "benchmarks/c5_dev/c5_per_chain_diagnostics.csv",
    "benchmarks/r1_fixed_order/frozen_results.json",
    "patches/p1_clean/apply_p1_clean.py",
    "docs/PROVENANCE.md",
    "docs/PUBLIC_MANIFEST.md",
    "docs/SCIENTIFIC_RESULT.md",
    "VERSION",
    "CITATION.cff",
    "release/2026-09-16/SHA256SUMS.txt",
    "release/2026-09-16/FINAL_PROVENANCE.json",
    "release/v1.0.2/SHA256SUMS.txt",
    "release/v1.0.2/PROVENANCE.json",
    "release/v1.0.3/SHA256SUMS.txt",
    "release/v1.0.3/PROVENANCE.json",
    "provenance/UPSTREAM_FEP_DMC.json",
    "provenance/C0_PUBLIC_PATCH.json",
    "tools/verify_fep_dmc_upstream.py",
    "integration/c0/apply_c0.py",
    "integration/c0/verify_c0.py",
    "integration/c0/c0_lib.py",
    "docs/UPSTREAM_FEP_DMC.md",
    "docs/C0_PUBLIC_ADAPTER.md",
    "docs/SOURCE_ATTRIBUTION.md",
    "docs/LIMITATIONS.md",
    "release/v1.1.0/SHA256SUMS.txt",
    "release/v1.1.0/PROVENANCE.json",
    "provenance/P1_PUBLIC_PATCH.json",
    "integration/p1/apply_p1.py",
    "integration/p1/verify_p1.py",
    "integration/p1/p1_lib.py",
    "integration/p1/linear_da_mod.f90",
    "docs/P1_PUBLIC_ADAPTER.md",
    "docs/METHOD_P1.md",
    "release/v1.2.0/SHA256SUMS.txt",
    "release/v1.2.0/PROVENANCE.json",
    "release/v1.2.0/NATIVE_VALIDATION.json",
    "release/v1.3.0/SHA256SUMS.txt",
    "release/v1.3.0/PROVENANCE.json",
    "release/v1.3.1/SHA256SUMS.txt",
    "release/v1.3.1/PROVENANCE.json",
    "release/v1.3.2/SHA256SUMS.txt",
    "release/v1.3.2/PROVENANCE.json",
    "docs/FEP_DMC_TOOLKIT.md",
    "docs/CONTRIBUTIONS.md",
)

PRIVATE_PATH_NEEDLES = (
    "research/luo_energy_1pct",
    "C2_fixture",
    "night1/C0/repair_v2",
    "/Users/",
)


def test_c2_oracle_is_not_under_runtime_package():
    assert not (SRC / "fortran" / "c2_oracle.py").exists()


def test_c2_oracle_is_not_importable_as_future_b_module():
    with pytest.raises((ModuleNotFoundError, ImportError)):
        importlib.import_module("future_b.fortran.c2_oracle")


def test_runtime_python_has_no_private_research_paths():
    hits = []
    for path in SRC.rglob("*.py"):
        text = path.read_text()
        for needle in PRIVATE_PATH_NEEDLES:
            if needle in text:
                hits.append(f"{path.relative_to(ROOT)}: {needle}")
    assert hits == []


def test_manifest_declares_sdist_test_data():
    manifest = ROOT / "MANIFEST.in"
    assert manifest.is_file(), "MANIFEST.in is required so sdist tests are not accidental"
    body = manifest.read_text()
    missing = [rel for rel in SDIST_TEST_DATA if rel not in body]
    assert missing == []
