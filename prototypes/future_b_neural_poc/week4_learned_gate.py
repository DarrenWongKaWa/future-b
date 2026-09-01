# SIGNED FORMULA: xi_k=2t*(1-cos k), L=2 k in {0, pi}, tadpole OFF.
"""Week 4 tiny logistic stopping gate. Deployable features only.

Does not edit holstein_ed.py or l2_periodic_pole.py.
Does not retune Week 3 θ_class. No PyTorch, no scikit-learn.
"""

from __future__ import annotations

import ast
import csv
from pathlib import Path
from typing import Any

import numpy as np

from prototypes.future_b_neural_poc.build_week2_table import (
    ACCEPTED_E0,
    G_OVER_T,
    OMEGA_OVER_T,
)
from prototypes.future_b_neural_poc.week3_classical_gate import (
    GATED_CSV,
    MATCH_GRAIN,
    NOT_COMPUTED,
    PREREGISTER_PATH as WEEK3_PREREGISTER,
    SCAN_CSV,
    SCBA_DEPTH,
    TEST_CELLS,
    TRAIN_CELLS,
    matches_ed_grain,
    n_green_gated_total,
    split_of,
    teacher_e0,
)

FEATURE_NAMES = (
    "g",
    "omega",
    "lambda",
    "n_over_64",
    "log10_r_n",
    "abs_sigma_diag",
)
N_FEATURES = len(FEATURE_NAMES)
GD_STEPS = 4000
LEARNING_RATE = 0.1
L2 = 1.0e-2
STOP_P = 0.5
LOG_FLOOR = 1.0e-30
THETA_CLASS = 0.03

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREREGISTER_PATH = ROOT / "notes" / "WEEK4_METRICS_PREREGISTER.md"
STOP_PATH = ROOT / "notes" / "WEEK4_STOP.md"
LEARNED_CSV = HERE / "week4_learned_vs_classical.csv"
WEIGHTS_CSV = HERE / "week4_gate_weights.csv"
VERDICT_CSV = HERE / "week4_verdict.csv"

LEARNED_FIELDS = (
    "g_over_t",
    "omega_over_t",
    "lambda",
    "split",
    "theta_class",
    "depth_classical",
    "depth_learned",
    "depth_oracle",
    "E0_ED",
    "E0_SCBA_fixed",
    "E0_learned",
    "delta_learned",
    "match_grain_ok",
    "n_cost_classical",
    "n_cost_learned",
    "n_infer",
    "note",
)
WEIGHT_FIELDS = ("feature", "train_mean", "train_std", "weight", "note")
VERDICT_FIELDS = (
    "beats_classical",
    "paper1_go",
    "n_train_match",
    "n_test_match",
    "mean_cost_classical_test",
    "mean_cost_learned_test",
    "note",
)
NOTE = (
    "week4_logistic;features=g,omega,lambda,n/64,log10(r_n),|Sigma_diag|;"
    "no_teacher_features;theta_class=0.03;E0_Born_VC=NOT_COMPUTED"
)


def coupling_lambda(g: float, omega: float) -> float:
    return (g * g) / (2.0 * omega)


def raw_features(
    *,
    g: float,
    omega: float,
    depth: int,
    r_n: float,
    abs_sigma: float,
) -> np.ndarray:
    return np.asarray(
        [
            g,
            omega,
            coupling_lambda(g, omega),
            depth / float(SCBA_DEPTH),
            np.log10(max(r_n, LOG_FLOOR)),
            abs_sigma,
        ],
        dtype=np.float64,
    )


def load_scan() -> dict[tuple[float, float], dict[int, dict[str, str]]]:
    with SCAN_CSV.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    out: dict[tuple[float, float], dict[int, dict[str, str]]] = {}
    for row in rows:
        cell = (float(row["g_over_t"]), float(row["omega_over_t"]))
        out.setdefault(cell, {})[int(row["depth"])] = row
    return out


def load_week3_gated() -> dict[tuple[float, float], dict[str, str]]:
    with GATED_CSV.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    return {
        (float(r["g_over_t"]), float(r["omega_over_t"])): r for r in rows
    }


def build_train_xy(
    scan: dict[tuple[float, float], dict[int, dict[str, str]]],
    gated: dict[tuple[float, float], dict[str, str]],
) -> tuple[np.ndarray, np.ndarray]:
    xs: list[np.ndarray] = []
    ys: list[float] = []
    for cell in TRAIN_CELLS:
        n_oracle = int(gated[cell]["depth_oracle"])
        for depth in range(1, n_oracle + 1):
            row = scan[cell][depth]
            r_n = float(row["rel_sigma_diag"])
            abs_sigma = abs(complex(float(row["sigma_diag_re"]), float(row["sigma_diag_im"])))
            xs.append(
                raw_features(
                    g=cell[0],
                    omega=cell[1],
                    depth=depth,
                    r_n=r_n,
                    abs_sigma=abs_sigma,
                )
            )
            ys.append(1.0 if depth == n_oracle else 0.0)
    return np.stack(xs, axis=0), np.asarray(ys, dtype=np.float64)


def standardize_fit(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = np.mean(x, axis=0)
    std = np.std(x, axis=0)
    std = np.where(std == 0.0, 1.0, std)
    return mean, std


def apply_standardize(x: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    return (x - mean) / std


def sigmoid(z: np.ndarray) -> np.ndarray:
    clipped = np.clip(z, -40.0, 40.0)
    return 1.0 / (1.0 + np.exp(-clipped))


def train_logistic(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, float]:
    n_samples = x.shape[0]
    weights = np.zeros(N_FEATURES, dtype=np.float64)
    bias = 0.0
    for _ in range(GD_STEPS):
        logits = x @ weights + bias
        pred = sigmoid(logits)
        error = pred - y
        grad_w = (x.T @ error) / n_samples + L2 * weights
        grad_b = float(np.mean(error))
        weights = weights - LEARNING_RATE * grad_w
        bias = bias - LEARNING_RATE * grad_b
    return weights, bias


def predict_proba(phi_raw: np.ndarray, mean: np.ndarray, std: np.ndarray, weights: np.ndarray, bias: float) -> float:
    phi = apply_standardize(phi_raw.reshape(1, -1), mean, std)[0]
    return float(sigmoid(np.asarray([np.dot(phi, weights) + bias]))[0])


def learned_depth(
    cell: tuple[float, float],
    scan: dict[tuple[float, float], dict[int, dict[str, str]]],
    mean: np.ndarray,
    std: np.ndarray,
    weights: np.ndarray,
    bias: float,
) -> int:
    for depth in range(1, SCBA_DEPTH + 1):
        row = scan[cell][depth]
        r_n = float(row["rel_sigma_diag"])
        abs_sigma = abs(complex(float(row["sigma_diag_re"]), float(row["sigma_diag_im"])))
        phi = raw_features(
            g=cell[0],
            omega=cell[1],
            depth=depth,
            r_n=r_n,
            abs_sigma=abs_sigma,
        )
        if predict_proba(phi, mean, std, weights, bias) >= STOP_P:
            return depth
    return SCBA_DEPTH


FORBIDDEN_FEATURE_NAMES = (
    "E0_ED",
    "E0_Born",
    "E0_SCBA",
    "delta",
    "rel_SCBA",
    "rel_Born",
    "depth_oracle",
    "depth_gated",
    "band",
    "split",
    "match_grain_ok",
)


def leakage_source_ok(path: Path) -> bool:
    """AST check: raw_features may only see g, omega, depth, r_n, abs_sigma."""

    if tuple(FEATURE_NAMES) != (
        "g",
        "omega",
        "lambda",
        "n_over_64",
        "log10_r_n",
        "abs_sigma_diag",
    ):
        return False
    source = path.read_text()
    tree = ast.parse(source)
    fn = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "raw_features"
    )
    used: set[str] = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Name):
            used.add(node.id)
    if any(name in used for name in FORBIDDEN_FEATURE_NAMES):
        return False
    allowed = {
        "g",
        "omega",
        "depth",
        "r_n",
        "abs_sigma",
        "coupling_lambda",
        "np",
        "log10",
        "max",
        "float",
        "SCBA_DEPTH",
        "LOG_FLOOR",
    }
    leftover = used - allowed - {"True", "False", "None"}
    # NumPy attribute names (asarray, float64) are not Name loads of teacher fields.
    if any(name in FORBIDDEN_FEATURE_NAMES for name in leftover):
        return False
    return True


def build_learned_rows(
    scan: dict[tuple[float, float], dict[int, dict[str, str]]],
    gated: dict[tuple[float, float], dict[str, str]],
    teacher: dict[tuple[float, float], dict[str, float]],
    mean: np.ndarray,
    std: np.ndarray,
    weights: np.ndarray,
    bias: float,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for g in G_OVER_T:
        for omega in OMEGA_OVER_T:
            cell = (g, omega)
            w3 = gated[cell]
            e0_ed = teacher[cell]["E0_ED"]
            e0_fixed = teacher[cell]["E0_SCBA"]
            depth_c = int(w3["depth_gated"])
            depth_o = int(w3["depth_oracle"])
            depth_l = learned_depth(cell, scan, mean, std, weights, bias)
            e0_learned_token = scan[cell][depth_l]["E0"]
            e0_learned = None if e0_learned_token == NOT_COMPUTED else float(e0_learned_token)
            match = matches_ed_grain(e0_learned, e0_fixed, e0_ed)
            delta = None if e0_learned is None else e0_learned - e0_ed
            n_infer = depth_l
            rows.append(
                {
                    "g_over_t": repr(g),
                    "omega_over_t": repr(omega),
                    "lambda": repr(coupling_lambda(g, omega)),
                    "split": split_of(cell),
                    "theta_class": repr(THETA_CLASS),
                    "depth_classical": str(depth_c),
                    "depth_learned": str(depth_l),
                    "depth_oracle": str(depth_o),
                    "E0_ED": repr(e0_ed),
                    "E0_SCBA_fixed": repr(e0_fixed),
                    "E0_learned": NOT_COMPUTED if e0_learned is None else repr(e0_learned),
                    "delta_learned": NOT_COMPUTED if delta is None else repr(delta),
                    "match_grain_ok": "true" if match else "false",
                    "n_cost_classical": str(int(w3["n_green_gated_total"])),
                    "n_cost_learned": str(n_green_gated_total(depth_l) + n_infer),
                    "n_infer": str(n_infer),
                    "note": NOTE,
                }
            )
    return rows


def evaluate(
    rows: list[dict[str, str]],
    leakage_ok: bool,
) -> dict[str, Any]:
    train = [r for r in rows if r["split"] == "train"]
    test = [r for r in rows if r["split"] == "test"]
    n_train_match = sum(1 for r in train if r["match_grain_ok"] == "true")
    n_test_match = sum(1 for r in test if r["match_grain_ok"] == "true")
    mean_c = sum(int(r["n_cost_classical"]) for r in test) / 6.0
    mean_l = sum(int(r["n_cost_learned"]) for r in test) / 6.0
    t1 = leakage_ok
    t2 = n_train_match == 6
    t3 = n_test_match == 6
    t4 = mean_l < mean_c
    t5 = all(
        float(r["E0_SCBA_fixed"]) == ACCEPTED_E0[(float(r["g_over_t"]), float(r["omega_over_t"]))]["E0_SCBA"]
        and r["theta_class"] == repr(THETA_CLASS)
        for r in rows
    )
    beats = t1 and t2 and t3 and t4 and t5
    return {
        "T1": t1,
        "T2": t2,
        "T3": t3,
        "T4": t4,
        "T5": t5,
        "n_train_match": n_train_match,
        "n_test_match": n_test_match,
        "mean_cost_classical_test": mean_c,
        "mean_cost_learned_test": mean_l,
        "beats_classical": beats,
        "paper1_go": beats,
        "stop_required": not t1,
    }


def write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fields})


def main() -> None:
    if not PREREGISTER_PATH.is_file():
        raise RuntimeError("CONFLICT: Week 4 preregister must exist before training")
    if not WEEK3_PREREGISTER.is_file():
        raise RuntimeError("CONFLICT: Week 3 preregister missing")
    teacher = teacher_e0()
    scan = load_scan()
    gated = load_week3_gated()
    x_raw, y = build_train_xy(scan, gated)
    mean, std = standardize_fit(x_raw)
    x = apply_standardize(x_raw, mean, std)
    weights, bias = train_logistic(x, y)
    leakage_ok = leakage_source_ok(Path(__file__))
    rows = build_learned_rows(scan, gated, teacher, mean, std, weights, bias)
    write_csv(LEARNED_CSV, LEARNED_FIELDS, rows)
    weight_rows = [
        {
            "feature": name,
            "train_mean": repr(float(mean[i])),
            "train_std": repr(float(std[i])),
            "weight": repr(float(weights[i])),
            "note": NOTE,
        }
        for i, name in enumerate(FEATURE_NAMES)
    ]
    weight_rows.append(
        {
            "feature": "bias",
            "train_mean": "0.0",
            "train_std": "1.0",
            "weight": repr(float(bias)),
            "note": NOTE,
        }
    )
    write_csv(WEIGHTS_CSV, WEIGHT_FIELDS, weight_rows)
    verdict = evaluate(rows, leakage_ok)
    write_csv(
        VERDICT_CSV,
        VERDICT_FIELDS,
        [
            {
                "beats_classical": "true" if verdict["beats_classical"] else "false",
                "paper1_go": "true" if verdict["paper1_go"] else "false",
                "n_train_match": str(verdict["n_train_match"]),
                "n_test_match": str(verdict["n_test_match"]),
                "mean_cost_classical_test": repr(float(verdict["mean_cost_classical_test"])),
                "mean_cost_learned_test": repr(float(verdict["mean_cost_learned_test"])),
                "note": NOTE,
            }
        ],
    )
    if verdict["stop_required"]:
        STOP_PATH.write_text(
            "# Week 4 stop\n\nTeacher-feature leakage. Neural result is not admitted.\n"
        )
    elif STOP_PATH.is_file():
        STOP_PATH.unlink()
    print(f"wrote {LEARNED_CSV}")
    print(f"wrote {WEIGHTS_CSV}")
    print(f"wrote {VERDICT_CSV}")
    print(f"n_train_samples={x_raw.shape[0]}")
    print(f"T1 leakage_ok={verdict['T1']}")
    print(f"T2 train_match={verdict['n_train_match']}/6 pass={verdict['T2']}")
    print(f"T3 test_match={verdict['n_test_match']}/6 pass={verdict['T3']}")
    print(
        f"T4 cost mean_classical={verdict['mean_cost_classical_test']!r} "
        f"mean_learned={verdict['mean_cost_learned_test']!r} pass={verdict['T4']}"
    )
    print(f"T5 teacher_lock={verdict['T5']}")
    print(f"beats_classical={verdict['beats_classical']}")
    print(f"paper1_go={verdict['paper1_go']}")


if __name__ == "__main__":
    main()
