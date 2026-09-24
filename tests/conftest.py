"""Collection boundary for the GitHub-only Diagram Compiler evidence suite.

The frozen v1.2.0 sdist intentionally omits the compiler's research evidence,
generated Fortran fixture, and FEP-DMC validation bridge.  Source-tree and CI
runs include those artifacts and collect the full compiler suite.  An unpacked
sdist therefore skips only the tests whose declared inputs are absent.
"""

from __future__ import annotations

from pathlib import Path


_COMPILER_TESTS = frozenset(
    {
        "test_cheap_cost.py",
        "test_cheap_evaluator.py",
        "test_cheap_independence.py",
        "test_cheap_p1.py",
        "test_cheap_policy.py",
        "test_cheap_protection.py",
        "test_cheap_reciprocity.py",
        "test_da_algebra.py",
        "test_da_finite_state.py",
        "test_da_independence.py",
        "test_da_kernel.py",
        "test_da_protection.py",
        "test_dag_sharing.py",
        "test_dc_fep_dmc_validate.py",
        "test_dc_distribution.py",
        "test_diagram_ir.py",
        "test_evaluator_vs_r1.py",
        "test_fortran_backend.py",
        "test_fortran_primitives.py",
        "test_fortran_protection.py",
        "test_native_kernel.py",
        "test_proposal_spec.py",
        "test_r1_import.py",
        "test_target_policy.py",
    }
)


def pytest_ignore_collect(collection_path: Path, config) -> bool:
    """Skip the evidence-dependent compiler suite only when it is absent."""
    root = Path(__file__).resolve().parents[1]
    return (
        not (root / "research" / "diagram_compiler").is_dir()
        and collection_path.name in _COMPILER_TESTS
    )
