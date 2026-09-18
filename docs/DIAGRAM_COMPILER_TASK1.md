# Task 1: bounded exact diagram compiler

Experimental source-only subsystem on `diagram-compiler/task1`. This is not a Future B release, a new material result, or a reopening of the closed science line.

## 1. Research question

Can the mathematical representation implicit in existing R1 be made explicit, serialized, and lowered into an independently implemented exact evaluator?

Yes, in the tested fixed-order scalar Holstein n=1–4 and Hermitian two-band n=1–3 families. Exact means the same mathematical expression, evaluated in floating point within the fixed tolerance below; it does not mean symbolic arithmetic or bitwise equivalence to every R1 association order. Speed was not an acceptance criterion and was not measured.

## 2. Existing R1 archaeology

| Repository source | Recovered role |
|---|---|
| `src/keldysh4ai/scheme_d/physics_first/contract.py` | Physical object and analytic model contracts |
| `src/keldysh4ai/scheme_d/physics_first/symbolic/plan_spec.py:61` | `scalar_spec`, with separate physics-object and graph-object identifiers |
| `src/keldysh4ai/scheme_d/physics_first/symbolic/plan_spec.py:85` | `twoband_spec`, providers and matrix interface |
| `src/keldysh4ai/scheme_d/physics_first/symbolic/r1.py:29` | Compile-once scalar open-chord DP |
| `src/keldysh4ai/scheme_d/physics_first/symbolic/r1_twoband.py:26` | Matrix DP; retains the untraced operator |
| `src/keldysh4ai/scheme_d/physics_first/symbolic/leaves.py` | Symbolic propagator, vertex and prefactor identities; leaf ABI |
| `src/keldysh4ai/scheme_d/physics_first/symbolic/reference_binder.py` | Runtime leaf values, separate from structural construction |
| `src/keldysh4ai/scheme_d/physics_first/symbolic/guards.py:61` | Time, lattice, provenance and explicit continuous-extension guards |
| `src/keldysh4ai/scheme_d/ir.py` and `exec.py` | Typed graph, hash-consing and Python reference execution |
| `src/keldysh4ai/scheme_d/physics_first/index_oracle.py:94` | Independent explicit scalar diagram sum |
| `src/keldysh4ai/scheme_d/physics_first/index_oracle.py:116` | Independent ordered two-band matrix product |
| `src/future_b/r1_fixed_order/__init__.py` | Public historical evidence surface, not the runtime oracle |
| `benchmarks/r1_fixed_order/frozen_results.json` | Frozen evidence; not recomputed or modified |

The actual physics object is `PF_G_FIXED_TIME_ORDER_G2n`; the graph category is `SHARED_X_GROUP`. They are not interchangeable names. Earlier compiler proposals and numeric-leaf prototypes are not this compile-once symbolic evaluator. Historical z-domain cases are not the runtime `(k,q,tau)` fixtures used here.

Source content hashes and exact oracle routes are in [R1_ORACLE.json](../research/diagram_compiler/task1/R1_ORACLE.json). Many source files were already untracked in this extract; the historical Git HEAD alone cannot pin them. No upstream fetch or source replacement was performed.

## 3. Recovered implicit representation

R1 computes `F_n(x)`, a sum over all perfect chord matchings of vertices `1..2n` at the same sample `x`. There are `(2n-1)!!` diagrams. Chords receive q slots by first-opening rank. Each internal electron segment carries `k - sum(q[open slots])`; no sample value belongs in a structural key.

The hidden representation has three parts:

1. A structural `PlanSpec`, independent of numeric bindings.
2. Semantic leaf descriptors and a deterministic leaf table.
3. A memoized recurrence over `(next vertex, open (slot,opening-vertex) pairs, number opened)`, followed by graph hash-consing.

The represented physical rules are:

- Scalar: `G(p,dtau)=exp(-2*t*(1-cos(p))*dtau)`, `D(a,b)=exp(-omega*(tau[b]-tau[a]))`.
- `F_n=(g/sqrt(L))^(2n) * sum_C product(G segments) * product(D chords)`.
- Every included single-electron bosonic diagram has sign +1 and multiplicity 1.
- Two-band: `H(k)=[[xi_k,delta],[delta,xi_k+gap]]`, `U=exp(-H*dtau)`, `M=(g/sqrt(L))*diag(1,-1)` at every endpoint.
- Traverse vertices forward; prepend both vertices and propagators: `state=M@state`, then `state=U@state`. Multiply the final matrix by all scalar phonon factors. Sum matrices to `Op`; `F=trace(Op)`.
- The two-band vertex already contains g/sqrt(L); there is no extra global prefactor.

No external electron segments, integration Jacobian, momentum-volume factor, factorial, tadpole, dressed propagator, or SCBA correction is silently supplied. This is neither a bound native `D(C)` nor an integrated `SUMMED_KERNEL`, full `G(T)`, or ground-state energy.

## 4. Minimal explicit DiagramIR

`src/keldysh4ai/diagram_compiler/ir.py` separates physical semantics from execution and optimization:

| Type | Physical information |
|---|---|
| `DiagramIR` | Schema version `1.0.0`, graph object, family, variables and diagram list |
| `Family` | Model, order, bands/interface, dispersion, phonon/normalization convention, rule version, global factors |
| `Variables` | External k, q/time slots, first-opening rule, strict time ordering, dynamic parameter names |
| `Diagram` | Canonical chord pairing, identity, sign, multiplicity and ordered explicit factors |
| `Factor` | Electron interval/momentum, phonon endpoints, vertex endpoint/direction, or prefactor |
| `MomentumForm` | Immutable integer k coefficient and `(q slot, coefficient)` terms |

The model and `diagram-compiler-v1` rule identifiers select the precise formulas in section 3. This is a bounded family schema, not a generic tensor-contraction or open-boundary diagram language.

Dynamic values are `(k,q,tau,t,omega,g,L)` plus `(delta,gap)` for two bands. The order, topology, index dependencies, model conventions, signs and multiplicities are structural. Synthetic material/default gauge/analytic data identity and finite-versus-continuous mode are checked at binding/import boundaries. No numeric leaf cache or old evaluator object is serialized.

The actual complete serialized example is [r1_scalar_n2.json](../research/diagram_compiler/task1/r1_scalar_n2.json). One exact factor from its crossing diagram is:

```json
{"interval": [1, 2], "k_form": {"k_coeff": 1, "q_terms": [[0, -1], [1, -1]]}, "kind": "electron_propagator", "open_chord_slots": [0, 1]}
```

JSON field ordering is deterministic. Deserialization rejects foreign schema/object/model contracts, unknown fields, fractional or boolean structural indices, incomplete/duplicate diagrams, wrong factors and changed binding rules. Mutable IR containers are unhashable; momentum forms used in graph keys are immutable. Compilation snapshots the IR, so later edits cannot alter a compiled evaluator.

## 5. Exact evaluator architecture

```text
actual R1 PlanSpec
  -> import_r1_spec (bounded structural frontend)
  -> explicit DiagramIR
  -> serialize / deserialize / validate
  -> lower_diagramwise(share=True)
  -> EvalDag
  -> compile_evaluator callable
  -> fresh Binding -> F, and Op for two bands
```

The adapter reconstructs the admitted family from `PlanSpec`; it does not reverse-engineer arbitrary R1 Graphs. Backend/ABI details are not inherited by the Python evaluator. Unknown physical/provider/rule/provenance contracts are rejected rather than guessed.

`evaluate_diagramwise` is the unfactored diagram sum. `lower_diagramwise` consumes the explicit factors and emits ordered input/constant/add/mul/matmul/trace nodes. `compile_evaluator` lowers once, retains an isolated snapshot, and computes each DAG node once per new binding. This is generation of an executable DAG program with a Python closure/interpreter, not emitted native source or JIT machine code.

`lower_grouped` is a separate, manually transcribed R1-family recurrence. Its admission validator checks the entire explicit family first. It is useful for representation comparison but does **not** demonstrate that general CSE automatically discovers R1's DP. Validation itself enumerates diagrams; the overall grouped-lowering call is not enumeration-free.

Public naive/DAG entry points validate supported IR/bindings; DAG execution rejects a different object/model/order. Low-level `EvalDag` is an internal, trusted lowering product, not a serialized arbitrary-program input format. `check=False` is reserved for internally prevalidated execution and intentional numerical mutation controls.

## 6. Canonicalization rules

- Vertices retain physical time order; no time sorting is performed on behalf of callers.
- Each chord is earlier-to-later; sorted chords define opening-rank q slots.
- Diagrams and factors must occur in the prescribed canonical order.
- A diagram ID such as `C_(1,3)_(2,4)` is local to its enclosing family, not a globally model-independent physical identity.
- Electron keys contain interval, open-slot set and integer momentum form.
- Phonon keys contain slot and both endpoint indices.
- Vertex keys retain direction, incoming open slots and chord slot, matching recovered R1 dependency scope even where this constant vertex happens to be numerically equal.
- Prefactor keys contain the normalization rule and symbolic exponent, never g or L values.
- Arithmetic keys preserve operation and ordered child identities. Matrix products are never sorted, reversed or commuted.

There is no floating-value equality merging, approximate simplification, sample-dependent constant folding, cross-family cache, or global graph-equivalence proof.

## 7. DAG sharing rules

The primary optimization is ordered structural hash-consing. It reuses leaves and identical factor-chain prefixes; scalar phonon products can also recur. A node with multiple incoming uses is evaluated once per binding. Rebinding invalidates all numeric values by creating a fresh execution cache.

Measured graph counts from [graph_stats.csv](../research/diagram_compiler/task1/graph_stats.csv):

| Family/order | Diagrams | Naive nodes | Unique DAG nodes | Shared nodes | Arithmetic operations | Recovered DP / R1 nodes |
|---|---:|---:|---:|---:|---:|---:|
| Scalar 1 | 1 | 7 | 7 | 0 | 3 | 7 / 7 |
| Scalar 2 | 3 | 35 | 28 | 3 | 15 | 28 / 28 |
| Scalar 3 | 15 | 257 | 124 | 34 | 91 | 95 / 95 |
| Scalar 4 | 105 | 2417 | 803 | 144 | 732 | 315 / 315 |
| Two-band 1 | 1 | 12 | 12 | 0 | 6 | 11 / 11 |
| Two-band 2 | 3 | 62 | 47 | 6 | 27 | 43 / 43 |
| Two-band 3 | 15 | 452 | 194 | 46 | 142 | 142 / 142 |

“Shared nodes” counts graph nodes with fanout >1, including constants. “Arithmetic operations” counts non-input/non-constant operation nodes, not FLOPs or leaf-evaluation costs. Even the naive lowering retains shared identity constants. Shared arithmetic nodes, separately recorded in CSV, are scalar n2/n3/n4: 2/12/83; two-band n2/n3: 2/17.

The primary DAG does not recover all of the DP's distributive suffix sharing. Equal recovered-DP/R1 node and leaf counts are counts only, **not graph isomorphism**, and no count is a speedup measurement.

## 8. R1 differential validation

Tolerance was fixed before the broad comparisons and never loosened:

`abs(value-reference) <= 1e-12 + 1e-10*abs(reference)` elementwise, with nonfinite results rejected.

Historical reference: `r1_symbolic_build` or `r1_twoband_build`, `ReferenceBinder`, then `scheme_d.exec.interpret`; the two-band environment additionally receives `structural_eye()`. Independent reference: explicit `index_oracle` diagram enumeration/products. Neither is implemented through the new primitive functions.

Evidence:

- 224 reproducible demo bindings: scalar n1–4 and two-band n1–3, two named fixture splits, 16 scenarios each. “RESERVED_CONFIRMATION” is an existing fixture label, not an unseen statistical holdout or performance campaign.
- All naive, unshared DAG, shared DAG, recovered DP and compiled-closure outputs agree with both reference routes.
- The CSV maximum absolute difference from R1, including every two-band `Op` entry, is `2.7755575615628914e-17`.
- Seven seeded randomized model/order tests, 12 finite-grid bindings each, vary L, k, q, times and physical parameters.
- Asymmetric controls detect sign, momentum sign, phonon endpoint, wrong leaf sharing, q-slot and noncommutative multiplication faults. Unsupported prefactors are rejected. The numerical fault tests deliberately bypass structural validation to prove oracle sensitivity.
- A→B→A rebinding and source-IR mutation tests verify no stale numeric cache or recompilation.
- Isolated subprocesses execute only JSON IR plus numeric bindings while imports of `scheme_d` and `future_b` are blocked; both scalar and full two-band outputs agree with the parent R1 reference.
- Structural mutation tests cover family metadata, variable scopes, unknown factors, duplicate phonons, malformed types and DAG/IR mismatch.

The first symmetric mutation fixture was insensitive to some errors; it was replaced by an explicitly asymmetric fixture, not by a looser tolerance. The final independent review found a remaining mutable-index type gap; four new tests reproduced it before the fix. The compiler-specific suite has 281 passing tests.

Full repository testing is not green: the baseline already had 17 failures, 45 errors and 11 skips (compiler availability, external LiF/FEP data, and historical R5 assertions). See [verification.json](../research/diagram_compiler/task1/verification.json) for final counts and exact baseline-ID comparison. No pre-existing scientific test was weakened.

Process limitation: initial implementation preceded most milestone tests; seven chronological test-first milestone commits were not produced. Later compile-closure and validation repairs had observed red→green tests. Delivery must not be described as complete compliance with the requested TDD/commit history. Earlier background review reports not returned to this session are not treated as approvals; the final post-hardening independent review and executable evidence are the relied-on checks.

## 9. Demonstration

Run from the repository root with its existing NumPy/test environment:

```sh
PYTHONPATH=src .venv/bin/python scripts/diagram_compiler_task1.py
.venv/bin/python -m pytest -q tests/test_diagram_ir.py tests/test_r1_import.py tests/test_evaluator_vs_r1.py tests/test_dag_sharing.py
```

Execute the saved example without constructing an R1 plan:

```python
import json
from pathlib import Path
from keldysh4ai.diagram_compiler import Binding, DiagramIR, compile_evaluator

folder = Path("research/diagram_compiler/task1")
ir = DiagramIR.from_json((folder / "r1_scalar_n2.json").read_text())
binding = Binding(**json.loads((folder / "binding.json").read_text()))
evaluate = compile_evaluator(ir)
print(evaluate(binding)["F"])
```

Observed result: `(0.0024401634116377456+0j)`, identical to R1 for this example; see [demo_result.json](../research/diagram_compiler/task1/demo_result.json). The script regenerates the serialized example, binding, differential CSV, graph counts and source provenance. It does not benchmark or run native chains.

## 10. What is NOT yet a compiler capability

| Capability | Status |
|---|---|
| Diagram representation | ESTABLISHED within the admitted fixed-order families |
| Exact evaluator generation | ESTABLISHED as an independently implemented DAG program and Python closure |
| DAG/CSE optimization | ESTABLISHED for ordered structural sharing; general algebraic optimization remains absent |
| Cheap evaluator generation | NOT IMPLEMENTED |
| Delayed-acceptance generation | NOT IMPLEMENTED |
| Native code generation | NOT IMPLEMENTED |
| Variable-order compilation | NOT IMPLEMENTED |

No arbitrary topology/subset frontend, automatic DP discovery, general multi-band material provider, open-boundary composition, frequency integration, stochastic proposal generator, GPU/LLVM/Fortran backend, P1 generation, or performance result is claimed. The source-only research package is not added to the public release surface. C0/P1, native evidence, frozen benchmarks, the historical 0.956 result, versions and releases are not rewritten.

## 11. Higher-order extension analysis

Pairing growth is 1, 3, 15, 105, 945, 10395 for n=1..6. Explicit construction and validation scale with the number of diagrams times their factors; DAG CSE reduces execution redundancy but does not remove frontend enumeration. The code admits only integer n≤6 as a resource bound; scalar n5/6 and two-band n4–6 are **not** validated by this campaign. There is no arbitrary-order claim.

Within the current fixed family, another order needs new differential/matrix tests and construction-memory checks. A genuinely different family needs explicit external-leg/band/mode structure, provider and gauge contracts, symmetry/sign/multiplicity rules, and its own independent oracle before admission. A variable-order sampler additionally needs a measure, proposal/reverse mapping and normalization contract; it does not follow from having several fixed-order compilers.

The primary remaining abstraction gap is a **compositional typed physical rule/interface layer independent of the two hard-coded family templates**. Without it, importing a new family requires code changes rather than lowering a general diagram description. The recovered DP comparison is not a substitute for that layer.

## 12. Next research milestone

Exactly one proposed next task: **Task 2 — derive a cheap evaluator from the same DiagramIR**.

Task 2 is not implemented or implicitly authorized by this result. Task 1 establishes only the bounded exact representation/evaluation baseline; it supplies no acceptance-ratio, approximation-quality, material-observable or efficiency claim.
