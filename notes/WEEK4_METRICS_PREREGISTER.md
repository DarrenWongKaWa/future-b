# Week 4 metrics — preregistered before any learned-gate table

Authority: HUMAN LOCK 2026-08-31 plus Week 3 leftover_decision=true.
Binding constraints: `notes/CONSTRAINTS_FUTURE_B.md`.
`notes/SCIENCE_LINE_60DAY.md` remains in force.

This file is written **before**
`prototypes/future_b_neural_poc/week4_learned_vs_classical.csv`,
`prototypes/future_b_neural_poc/week4_gate_weights.csv`, and
**before** `notes/WEEK4_REPORT.md`. Features, model, hyperparameters,
win rule, and leakage ban are frozen here. They are not fitted to test
depths or to which cells differ by one rainbow layer.

Week 4 trains **one tiny CPU logistic gate**. It does not edit
`holstein_ed.py` or `l2_periodic_pole.py`, does not change \(\eta\),
\(L\), \(\xi_k\), tadpole, `SCBA_DEPTH`, or \(\theta_{\mathrm{class}}=0.03\),
does not mix libraries, does not invent \(E_0^{\mathrm{Born+VC}}\),
and does not use 11A numbers.

Immutable inputs: `teacher_map_l2.csv`, `week3_depth_scan.csv`,
`week3_gated_vs_fixed.csv`, `week3_theta_selection.csv`.

## Split (unchanged)

Train and test cells are the Week 3 split. No reshuffle.

## Deployable features (frozen)

At rainbow depth \(n\in\{1,\ldots,64\}\), the feature vector is

```
φ = (
  g,
  Ω,
  λ,                          # λ = g² / (2 t Ω), t=1; function of (g,Ω) only
  n / 64,
  log10(max(r_n, 1e-30)),     # same r_n as the classical gate
  |Σ^{(n)}(z_diag)|           # z_diag = 0 + iη
)
```

Six numbers. No other coordinates.

**Forbidden as features** (leakage → immediate stop):

- \(E_0^{\mathrm{ED}}\), \(E_0^{\mathrm{Born}}\), \(E_0^{\mathrm{SCBA}}\)
- \(\Delta_X\), \(\mathrm{rel}_X\), `match_grain_ok`
- `depth_oracle`, `depth_gated` of any other cell
- Week-1/Week-2 band strings (`weak` / `intermediate` / `strong`)
- train/test split flags
- any 11A or proxy-POC number

\(\lambda\) is allowed because it is a function of the physical input
\(x=(g,\Omega)\) and is available at deploy time. Band strings are
forbidden so a cut declared for reporting cannot be smuggled in as a
categorical teacher-style label.

## Labels (train only; not features)

The deployable loop stops at the first accepted \(n\) and never
evaluates later depths. Train samples are therefore only

```
n = 1, 2, …, depth_oracle(cell)   (inclusive)
y_n = 1  if n == depth_oracle(cell)
y_n = 0  if n < depth_oracle(cell)
```

Do **not** include \(n>\mathrm{depth\_oracle}\) (those steps are not
on the stopped trajectory). `depth_oracle` uses \(E_0^{\mathrm{ED}}\)
and is a **supervision target**, not an input. Test labels are not
used to update weights.

## Model and hyperparameters (frozen)

Binary logistic regression, NumPy only (no PyTorch, no scikit-learn):

```
p = 1 / (1 + exp(−(w·φ̃ + b)))
```

\(\varphi\) is standardized with **train-sample** mean and standard
deviation (population std, ddof=0). If a coordinate has std 0, replace
that std by 1.

| knob | value |
|------|-------|
| weights init | 0 |
| bias init | 0 |
| optimizer | full-batch gradient descent on binary cross-entropy |
| steps | 4000 |
| learning rate | 0.1 |
| L2 on \(w\) only (not \(b\)) | \(10^{-2}\) |
| seed | 0 (unused if init is identically zero; recorded anyway) |
| stop threshold | \(p \ge 0.5\) |

Do not retune after seeing test cost or test matching.

Deployable rule: scan \(n=1,2,\ldots,64\); stop at the smallest \(n\)
with \(p_n\ge 0.5\); if none, use 64. Features at step \(n\) use only
quantities available from \(\Sigma^{(n)}\) and \(\Sigma^{(n-1)}\) at
\(z_{\mathrm{diag}}\) plus the known \((g,\Omega)\).

## Cost, including inference

```
n_green_learned_total = n_green_pole(depth) + n_green_discover(depth)
n_infer               = depth          # one logistic eval per scanned n ≥ 1
n_cost_learned        = n_green_learned_total + n_infer
n_cost_classical      = n_green_gated_total(depth_classical)
```

One logistic evaluation is counted as 1 against one Green evaluation.
That overcharges the gate. It is intentional.

Classical comparator is the frozen Week 3 gate \(\theta=0.03\), not
a newly tuned \(\theta\).

## Win rule (all required)

The learned gate **beats** the classical gate iff all of the following
hold on the frozen test split:

1. Source/feature leakage check passes (no forbidden feature in \(\varphi\)).
2. Train matching 6/6 at the Week 3 grain
   \(|\Delta_{\mathrm{learned}}|\le|\Delta_{\mathrm{fixed}}|+10^{-4}t\).
3. Test matching 6/6 at the same grain; \(\theta_{\mathrm{class}}\) and
   learned weights are not retuned on test.
4. Mean `n_cost_learned` on test is **strictly less** than mean
   `n_cost_classical` on test.
5. No test cell has larger `depth_learned` than `depth_classical`
   unless that cell still matches and the mean in (4) still falls
   (mean cost is the criterion; this bullet is a recording rule, not
   an extra fail). Recording only: count how many test cells are
   strictly cheaper / equal / more expensive.

If (1) fails: write `notes/WEEK4_STOP.md`, do not claim a win.
If (2) or (3) or (4) fails: **negative result**, skip Paper 1, do not
widen the network, do not add features, do not retune. Continue to the
method note.

Paper 1 is **GO** only if the learned gate beats the classical gate
under this win rule. Diagram-block architecture remains untested until
Weeks 7–8, which run only if Paper 1 is GO.

## Tests T1–T5 (rules only; not evaluated here)

T1 Leakage: feature builder does not read teacher energies, teacher
errors, oracle depth, or band strings. Fail and stop if it does.

T2 Train matching 6/6 for the learned gate.

T3 Test matching 6/6.

T4 Cost: mean test `n_cost_learned` < mean test `n_cost_classical`.

T5 Classical \(\theta\) and Week 3 depths are unchanged; learned table
`E0_SCBA_fixed` equals teacher `E0_SCBA`.

## CSV schema (not written yet)

`prototypes/future_b_neural_poc/week4_learned_vs_classical.csv`

```
g_over_t,omega_over_t,lambda,split,theta_class,
depth_classical,depth_learned,depth_oracle,
E0_ED,E0_SCBA_fixed,E0_learned,
delta_learned,match_grain_ok,
n_cost_classical,n_cost_learned,n_infer,note
```

`prototypes/future_b_neural_poc/week4_gate_weights.csv`

```
feature,train_mean,train_std,weight,note
```

plus a final row `bias`. Six feature rows in the order of \(\varphi\).

`prototypes/future_b_neural_poc/week4_verdict.csv`

```
beats_classical,paper1_go,n_train_match,n_test_match,
mean_cost_classical_test,mean_cost_learned_test,note
```

`beats_classical` and `paper1_go` are lowercase `true`/`false` and
must be equal under this week’s rule.

## What this preregister does not authorize

- widening the logistic net or switching to an MLP after a loss
- adding forbidden features
- retuning lr, L2, steps, or the 0.5 threshold after test
- L=4 ED (remains `NOT_COMPUTED`)
- typed-block / generic architecture ablations (Weeks 7–8 only if GO)
- \(\Phi\)-learning, Keldysh, Anderson–Holstein, devices, DiagMC
- claiming Physics-for-AI from a stopping-gate comparison
