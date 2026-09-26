"""future_b.fepdmc: pooled ratio estimator, exactness validator, patch registry and CLI."""

from __future__ import annotations

import sys

from pathlib import Path

import numpy as np
import pytest

from future_b.fepdmc import pooled as compare_pooled
from future_b.fepdmc import validate as validate_exactness


def _chain(root: Path, i: int, etrue: float, sign: float, cpu: float) -> None:
    c = root / "lif_hole" / f"chain{i:02d}"
    c.mkdir(parents=True)
    (c / "stdout.log").write_text(f"            Etrue =    {etrue:.10E}    0.0E+00\n"
                                  f"            <g/Z> =     {sign:.10E}    0.0E+00\n")
    (c / "stderr.log").write_text(f"real\t1m0.0s\nuser\t0m{cpu:.3f}s\nsys\t0m0.1s\n")


def test_pooled_is_sign_weighted_not_mean_of_ratios(tmp_path):
    # Two chains: a high-sign chain at E=-1 and a low-sign chain at E=-3.
    _chain(tmp_path, 0, -1.0, 0.20, 10.0)
    _chain(tmp_path, 1, -3.0, 0.02, 10.0)
    tau, e_bare = 2.0, 0.0
    side = compare_pooled.side(str(tmp_path), "lif_hole", tau, e_bare)
    expected = (-1.0 * 0.20 + -3.0 * 0.02) / (0.20 + 0.02)
    assert side["Q_pooled"] == pytest.approx(expected)
    assert side["Q_mean_of_chain_ratios"] == pytest.approx(-2.0)
    assert side["cpu_s"] == pytest.approx(10.0)


def test_validator_pooled_matches_compare_pooled(tmp_path):
    rng = np.random.default_rng(0)
    for i in range(6):
        _chain(tmp_path, i, -0.87 + 0.001 * rng.standard_normal(), 0.999, 5.0)
    q, se, n = validate_exactness.pooled(tmp_path, "lif_hole")
    side = compare_pooled.side(str(tmp_path), "lif_hole", 1.0, 0.0)
    assert n == 6
    assert q == pytest.approx(side["Q_pooled"])
    assert se == pytest.approx(side["se_delta"])


def test_validator_needs_two_chains(tmp_path):
    _chain(tmp_path, 0, -0.87, 1.0, 1.0)
    q, se, n = validate_exactness.pooled(tmp_path, "lif_hole")
    assert n == 1 and np.isnan(q) and np.isnan(se)


def test_patch_registry_and_data_files():
    from future_b.fepdmc import FEP_DMC_PIN, patches
    from future_b.fepdmc.patches import base, bchain

    assert patches.ORDER == ("base", "bchain", "wqfix", "extfix", "extrmfix")
    assert set(patches.PROFILES["fixes"]) == {"base", "wqfix", "extfix", "extrmfix"}
    for name in ("bchain.f90", "rb_window.f90", "mkl_vsl.f90", "make.sys"):
        assert (base.DATA / name).is_file(), name
    assert bchain.DATA == base.DATA
    assert len(FEP_DMC_PIN) == 40
    with pytest.raises(ValueError):
        patches.apply(Path("."), "not-a-patch")


def test_pin_matches_provenance_record():
    import json

    from future_b.fepdmc import FEP_DMC_PIN

    rec = json.loads((Path(__file__).resolve().parents[1] / "provenance" / "UPSTREAM_FEP_DMC.json").read_text())
    assert rec["reference_commit"] == FEP_DMC_PIN


def test_prepare_refuses_tree_without_pert_src(tmp_path):
    from future_b.fepdmc.prepare import main, prepare_tree

    with pytest.raises(FileNotFoundError):
        prepare_tree(tmp_path)
    assert main([str(tmp_path)]) == 2


def test_prepare_dry_run_lists_profile(tmp_path):
    from future_b.fepdmc.prepare import prepare_tree

    (tmp_path / "pert-src").mkdir()
    assert prepare_tree(tmp_path, "fixes", dry_run=True) == ["base", "wqfix", "extfix", "extrmfix"]


def test_runner_switch_env_maps_flags():
    from future_b.fepdmc import runner

    a = runner.parser().parse_args(["ez", "lif_hole", "2", "--wqfix", "--extfix", "--extrmfix",
                                    "--extar", "0.02", "--data", "/d"])
    env, rb = runner.switch_env(a, "lif_hole")
    assert (env["FUTUREB_WQFIX"], env["FUTUREB_EXTFIX"], env["FUTUREB_EXTRMFIX"]) == ("1", "1", "1")
    assert (env["FUTUREB_EXTAR"], env["FUTUREB_EXTAR_P"]) == ("1", "0.02")
    assert env["FUTUREB_ANY"] == "0" and "FUTUREB_MV_UNTIL" not in env
    assert rb == "0"  # three-band hole: no single-band RB
    assert runner.binary("perturbo-fep-dmc-pkg").endswith("perturbo-fep-dmc-pkg/pert-src/perturbo.x")


def test_runner_requires_dataset(monkeypatch):
    from future_b.fepdmc import runner

    monkeypatch.delenv("FUTUREB_FEPDMC_DATA", raising=False)
    assert runner.main(["ez", "lif_hole", "1"]) == 2


def test_cli_dispatch_and_help():
    from future_b.fepdmc import cli

    assert cli.main(["--help"]) == 0
    assert cli.main(["unknown"]) == 2
    assert cli.main([]) == 2
    assert set(cli.COMMANDS) == {"prepare", "run", "compare", "validate"}


ANALYSIS_MODULES = ("analyze_mode_rb", "analyze_modes", "analyze_q", "analyze_rb", "analyze_svd",
                    "collect_sign", "compare_bchain", "compare_between", "decompose_native",
                    "estimate_groups", "summarize_materials", "summarize_sign")


def test_analysis_modules_import_without_scipy(monkeypatch):
    # scipy is optional (future-b[analysis]); importing a module must not need it.
    import importlib

    for mod in list(sys.modules):
        if mod.startswith(("future_b.fepdmc.analysis.", "scipy.")) or mod == "scipy":
            monkeypatch.delitem(sys.modules, mod)
    monkeypatch.setitem(sys.modules, "scipy", None)
    for name in ANALYSIS_MODULES:
        importlib.import_module(f"future_b.fepdmc.analysis.{name}")


def test_analysis_modules_import_without_side_effects():
    import importlib

    for name in ANALYSIS_MODULES:
        mod = importlib.import_module(f"future_b.fepdmc.analysis.{name}")
        assert callable(getattr(mod, "main", None)), name
