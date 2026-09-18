# Task 2 — consolidated research report

Result: **bounded cheap evaluator established** from the same
`DiagramIR` as Task 1, with explicit policy `propagator_only_v1` and
`CHEAP_EVALUATOR_SEMANTICS = STATE_WEIGHT`. Not a delayed-acceptance
compiler, not a P1 replacement, not a wall-clock claim.

The requested eight chronological milestone commits were grouped after
a genuine red collection (imports missing) rather than reconstructed
as eight git snapshots. That process limit is recorded here.

## 1. Task-1 baseline preservation

Isolated worktree from `1185d81`. Task-1 compiler tests: 281 passed.
Exact 224/224 recheck: passed, max error `2.7755575615628914e-17`.
Exact modules `ir.py`, `canonical.py`, `evaluator.py`, `graph.py`,
`r1_import.py` unchanged (see `baseline.json`). Original dirty
checkout `/Users/kawawong/Research/future-b` was not edited.

## 2. Candidate cheap policies

See `docs/DIAGRAM_COMPILER_TASK2.md` §3. Four named candidates:
propagator-only full sum (A), drop-vertex fail-closed (B), noncrossing
subseries (C), P1 swap prop (D). A was chosen for reciprocity,
derivability, and removal of two-band matrix primitives. C is the
only candidate that cheapens scalar pairing count; it drops crossed
diagrams this extract treats as physically large. D is the wrong
object.

## 3. Semantic decision

`CHEAP_EVALUATOR_SEMANTICS = STATE_WEIGHT`

## 4. DiagramIR sufficiency

Yes, for Formulation A on the admitted R1 family. Reverse is a pair of
`Binding`s. `TransitionIR` is necessary for a P1 occupancy-swap score
and was **not** introduced.

## 5. Chosen CheapPolicy

`propagator_only_v1`. KEEP G, D, prefactor, signs, multiplicities, all
pairings, q-terms. DROP vertex, matmul, trace. APPROXIMATE two-band
matrix G as scalar Gel. REFUSE uncovered kinds. File:
`CHEAP_POLICY.json`.

## 6. Compiler architecture

```text
DiagramIR -> lower_diagramwise -> Exact DAG -> compile_evaluator
         -> lower_cheap        -> Cheap DAG -> compile_cheap
```

## 7. Reverse / reciprocity

`ell(x,y)=log W_hat(y)-log W_hat(x)`, `W_hat>0` real.
`ell(y,x)=-ell(x,y)` by construction. Residuals in
`differential_results.csv` are 0.0. Unsorted tau reverse raises
`BC01`. `odd_clip(-x)=-odd_clip(x)`; clip is not applied to the raw
score.

## 8. P1 correspondence

`P1_CORRESPONDENCE["verdict"]=="NOT_IDENTICAL"`. Classes:
representation mismatch, proposal metadata missing, compiler policy
different. A local Gel ratio on a q-swap is required to differ from
the grouped cheap log-ratio.

## 9. Exact vs cheap graph

Two-band n=3: exact 194 unique nodes / 110 expensive primitives;
cheap 124 / 0. Scalar n=4: 803 / 0 on both. `graph_costs.csv`.

## 10. Differential validation

7 family/order rows, cheap = scalar exact, reciprocity residual 0.
Two-band family exact differs (n=1 `|Δ|=0.053`). Task-1 224/224
unchanged.

## 11. Independence

`tests/test_cheap_independence.py`. Cheap primitives live in
`cheap_evaluator.py` and do not call `electron_value` / `evaluate_dag`
/ R1.

## 12. Repository changes

| Path | Purpose |
|---|---|
| `src/keldysh4ai/diagram_compiler/cheap_policy.py` | Versioned KEEP/DROP/APPROXIMATE/REFUSE |
| `cheap_evaluator.py` | Cheap lowering, interpreter, compile_cheap/compile_exact |
| `cheap_cost.py` | Static node/expensive-primitive counts |
| `tests/test_cheap_*.py` | Policy, lowering, reciprocity, independence, cost, P1, protection |
| `scripts/diagram_compiler_task2.py` | Evidence regeneration |
| `docs/DIAGRAM_COMPILER_TASK2.md` | Technical document |
| `research/diagram_compiler/task2/` | JSON/CSV artifacts and this report |

No C0/P1 adapter, frozen benchmark, or v1.2.0 release file is
modified.

## 13. Verification

Task-1 compiler tests 281 passed. Task-2 tests 52 passed. 224/224
exact recheck passed. Policy and cheap-IR JSON round-trip. Reverse
mutation (identity reverse, illegal tau swap, dropped prefactor) fail
where intended. Static two-band expensive count drops to 0.
`git diff --check` is required at commit.

## 14. Current compiler maturity

| Capability | Status |
|---|---|
| Diagram representation | ESTABLISHED, bounded family scope |
| Exact evaluator generation | ESTABLISHED |
| DAG/CSE optimization | ESTABLISHED, ordered structural CSE only |
| Cheap evaluator generation | ESTABLISHED for `propagator_only_v1` |
| Cheap reverse reciprocity | ESTABLISHED by construction |
| Delayed-acceptance generation | NOT IMPLEMENTED |
| Native code generation | NOT IMPLEMENTED |
| Variable-order compilation | NOT IMPLEMENTED |

## 15. Biggest remaining abstraction gap

**A delayed-acceptance kernel object that pairs the exact DAG with
this cheap state-weight score under an explicit reversible proposal,
without becoming a general Monte Carlo IR.**

## 16. Exactly one next task

Task 3 — generate an exact-preserving delayed-acceptance kernel from
the exact and cheap evaluator representations. Not implemented.
