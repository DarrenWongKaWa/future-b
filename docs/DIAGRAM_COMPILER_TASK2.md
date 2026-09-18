# Task 2: cheap evaluator from the same DiagramIR

Experimental source-only continuation of Task 1 on
`diagram-compiler/task2-cheap-evaluator`. This is not a Future B release,
a delayed-acceptance kernel, a P1 replacement, or a performance result.

## 1. Task-1 baseline

HEAD `1185d81741401e8b3d0729cd315c120a79372f60`. Compiler tests: 281
passed. Differential demonstration: 224/224 exact cases still match
historical R1 and `index_oracle` after Task 2, maximum absolute error
including Op `2.7755575615628914e-17` at the predeclared
`atol=1e-12`, `rtol=1e-10`. Exact compiler modules `ir.py`,
`canonical.py`, `evaluator.py`, `graph.py`, and `r1_import.py` are
byte-identical to that HEAD (hashes in
[baseline.json](../research/diagram_compiler/task2/baseline.json)).

Cheap evaluation was **not** implemented in Task 1.

## 2. Cheap-evaluator research question

Can the same semantic `DiagramIR` that generates the validated exact
evaluator also generate a systematically cheaper evaluator suitable
for a future exact-preserving delayed-acceptance kernel?

Task 2 builds only

```text
DiagramIR -> cheap evaluator
```

It does not generate Stage-1/Stage-2 DA, Fortran, or a native P1
replacement.

## 3. Candidate policies

| Policy | Retained | Discarded | Reciprocity | Scalar n≥2 cheaper? |
|---|---|---|---|---|
| A `propagator_only_v1` | All pairings; scalar `G`,`D`; prefactor; q-dependent `k_form` | Vertices; `matmul`; `trace`; two-band `eigh` (matrix `G` → scalar Gel) | State function, Formulation A | **No** (equals exact) |
| B drop-vertex fail-closed | Scalar `G`,`D` only | Two-band refused unless an explicit matrix approximation exists | State function on scalar | **No** |
| C noncrossing partial sum | Exact leaves on Catalan pairings | Crossing diagrams | State function | Yes, by dropping crossed physics |
| D P1 swap `prop` | Local Gel/Dph/`P_kchange` | The R1 object `F_n` | Transition / occupancy reverse | Not comparable |

Policy D is the public P1 score. It is a different mathematical object
and is **not** implemented.

## 4. Chosen policy

`propagator_only_v1`, schema version 1. Artifact:
[CHEAP_POLICY.json](../research/diagram_compiler/task2/CHEAP_POLICY.json).

| Action | Categories |
|---|---|
| KEEP | `factor.electron_propagator`, `factor.phonon_propagator`, `factor.prefactor`, `diagram.sign`, `diagram.multiplicity`, `family.global_factors`, `diagram_sum.all_pairings`, `momentum.q_terms` |
| DROP | `factor.vertex`, `eval.matmul`, `eval.trace` |
| APPROXIMATE | `electron_interface.matrix2` → scalar Gel of the same `k_form`; empty two-band `global_factors` → `(g/sqrt(L))**(2n)` |
| REFUSE | any unlisted category (fail closed, never treat as 1) |

On Holstein scalar n=1..4 this policy **is** the exact evaluator. That
is a characterization, not a speedup. Two-band cheap equals scalar
exact at the same `Binding` and is not the two-band exact `F`.

## 5. State-weight vs transition-score decision

```text
CHEAP_EVALUATOR_SEMANTICS = STATE_WEIGHT
```

`W_hat(x)` is a function of one `Binding`. The transition score is
derived:

```text
ell_hat_raw(x, y) = log W_hat(y) - log W_hat(x)
```

Historical P1 `prop` is a **transition score** on a Method0 occupancy
swap (`log P_kchange`). That object is not `F_n(x)` and is not
generated here.

## 6. Reverse semantics

Reverse of a legal rebinding is Binding swap: `rev(x,y)=(y,x)`.
Times stay strictly increasing; silent sort is forbidden (`BC01`).
The P1 analog that remains inside this domain is a **q occupancy
swap at fixed ordered tau**, not a vertex-time swap.

`W_hat` is a real positive product-sum of `exp` leaves (and the
scalar prefactor). Complex `log` is refused. `g=0` is fail-closed
for `log_weight`. Reciprocity is by construction. Independent
evaluation of the swapped pair is checked at Task-1 tolerance.
`odd_clip` is supplied and is odd; clipping is **not** applied to
the raw Task-2 score.

`TransitionIR` is not required for this reverse.

## 7. Cheap lowering architecture

```text
                    DiagramIR
                   /         \
             exact lower    cheap lower
                 ↓              ↓
            Exact DAG       Cheap DAG
         compile_evaluator  compile_cheap
```

`compile_cheap` snapshots the IR, consults the versioned policy, and
emits a scalar DAG (`input`/`const`/`add`/`mul` only). It does not
mutate `DiagramIR`, call `lower_diagramwise` / `lower_grouped`, call
`electron_value` / `vertex_value`, or import historical R1.

API:

```python
exact = compile_exact(ir)
cheap = compile_cheap(ir, policy="propagator_only_v1")
exact.evaluate(binding)   # {"F": ...}
cheap.evaluate(binding)   # {"F_hat", "log_W_hat"}
cheap.transition_score(x, y)
```

Unsupported semantic nodes fail closed. A policy that DROPs a
category the lowering does not actually implement (`momentum.q_terms`,
`diagram_sum.all_pairings`) is refused rather than silently kept.

## 8. Exact/cheap independence

Monkeypatch tests replace `evaluate_diagramwise`, `evaluate_dag`,
`compile_evaluator`, `electron_value`, `vertex_value`,
`lower_diagramwise`, and `lower_grouped` with failures. Cheap
evaluation still runs. An isolated subprocess blocks `scheme_d` /
`future_b` imports and the same exact backends.

Cheap leaf formulas copy frozen `xi_k=2t(1-cos k)` locally so a
change to exact CSE does not silently rewrite the cheap score.

## 9. P1 correspondence

Not identical. Classification:

- representation mismatch (`SHARED_X_GROUP` `F_n` vs `BOUND_C` swap)
- proposal metadata missing (`iv1`,`iv2`, occupancy reverse, `P_kchange`)
- compiler policy intentionally different (full pairing sum of G,D vs
  local mid-segment Gel/Dph, no clip)

Leaf-level `G~exp(-e Δτ)` and `D~exp(-ω Δτ)` overlap. A grouped
log-ratio is not the P1 local Gel ratio; a test requires them to
differ on a q occupancy swap.

## 10. Cost model

Declared **before** timings: count unique DAG nodes and expensive
primitives `n_eigh + n_vertex + n_matmul + n_trace`.

From [graph_costs.csv](../research/diagram_compiler/task2/graph_costs.csv):

| Family | n | exact unique | cheap unique | exact expensive | cheap expensive |
|---|---:|---:|---:|---:|---:|
| scalar | 1–4 | 7, 28, 124, 803 | 7, 28, 124, 803 | 0 | 0 |
| two-band | 1–3 | 12, 47, 194 | 7, 28, 124 | 7, 28, 110 | 0 |

Two-band cheap DAGs contain no vertex, `eigh`, `matmul`, or `trace`.
Scalar graphs are unchanged. Microbenchmark point estimates exist in
[microbenchmarks.csv](../research/diagram_compiler/task2/microbenchmarks.csv)
and are **not** a speedup claim.

## 11. Differential validation

Seven representative family/order rows: cheap matches scalar exact
with residual 0; two-band family exact differs (n=1 abs err
`5.30e-2`). Reciprocity residual 0 on those rows. Full Task-1 224/224
exact cases still pass at max error `2.78e-17`.

## 12. Limitations

- Scalar cheapness is not a reduction under this policy.
- Two-band cheap is blind to `delta`, `gap`, `σ_z` vertices, and
  `trace(Op)`.
- Pairing enumeration remains factorial; this is not variable-order
  compilation.
- Public P1 numerical scores are not reproduced.
- Protection hashes prove Task-1 exact modules were not edited in
  Task 2; they do not re-prove the original dirty-tree 62-ID full
  suite, which is not present in this isolated worktree.
- Milestone commits were grouped after a red collection of missing
  modules, not eight separate red-green git commits.

## 13. Implications for Task 3

Exact and cheap evaluators now exist on one `DiagramIR`. A future
exact-preserving delayed-acceptance kernel can use
`ell_hat = log W_hat(y)-log W_hat(x)` as Stage 1 and the unchanged
exact `F` ratio as Stage 2 **for rebinding moves**. Occupancy-swap
P1-like moves still need an explicit, small move record; that is not
a general Monte Carlo IR and is not implemented here.
