# Task 1 — consolidated research report

Result: **bounded exact compiler established**, not a general diagram compiler or a performance result. The requested chronological test-first/milestone-commit process was not fully followed; this limitation is recorded rather than reconstructed retrospectively.

## 1. R1 archaeology

The implementation of interest is the compile-once symbolic R1 family under `src/keldysh4ai/scheme_d/physics_first/symbolic/`, not the frozen public report adapter or an earlier numeric-leaf prototype. `plan_spec.py` fixes the supported families; `r1.py` and `r1_twoband.py` build recursive graphs; `leaves.py` describes symbolic dependencies; `reference_binder.py` supplies current numeric values; `scheme_d/exec.py` executes the original graph.

Physical conventions were recovered from `physics_first/contract.py`, `index_oracle.py`, and those actual builders. [R1_ORACLE.json](R1_ORACLE.json) pins 18 local source/evidence files by content hash. Many were untracked before Task 1, so the historical Git commit alone is not a complete source pin.

## 2. Mathematical object recovered

`PF_G_FIXED_TIME_ORDER_G2n` is the physical object; `SHARED_X_GROUP` is its graph category. The output is `F_n(x)`, the fixed-time sum over all `(2n-1)!!` perfect chord matchings at shared `(k,q,tau)`.

Scalar weights use `xi_k=2t(1-cos k)`, `G=exp(-xi*dtau)`, Einstein-vacuum `D=exp(-omega*dtau)`, and global `(g/sqrt(L))^(2n)`. Signs and multiplicities are +1/1. Two-band weights use `U=exp(-[[xi,delta],[delta,xi+gap]]*dtau)` and endpoint vertices `(g/sqrt(L))*diag(1,-1)`, with both U and M left-multiplied in forward vertex order. `Op` is preserved and `F=trace(Op)`.

No external segments, time/momentum integration, Jacobian, factorial, dressed propagator, tadpole or SCBA addition is included. The object is not native `D(C)`, an integrated kernel, or an energy observable.

## 3. Implicit IR

R1 already contained a structural plan, symbolic leaf identities, and a DP state `(v, open (slot,start) chords, n_opened)`. Open/close branches encode diagram enumeration; memoized suffixes and graph hash-consing provide sharing. Opening-rank q slots and ordered matrix dependencies are essential physical information, not incidental names.

## 4. Explicit DiagramIR

`DiagramIR` contains schema/object IDs, a `Family`, a `Variables` contract and explicit `Diagram` records. Each diagram stores pairing, canonical ID, sign, multiplicity and ordered `Factor` records. `MomentumForm` stores immutable integer coefficients, not evaluated momenta.

Actual complete serialized example: [r1_scalar_n2.json](r1_scalar_n2.json), containing all three n2 diagrams. Its crossing-diagram middle electron factor is:

```json
{"interval": [1, 2], "k_form": {"k_coeff": 1, "q_terms": [[0, -1], [1, -1]]}, "kind": "electron_propagator", "open_chord_slots": [0, 1]}
```

Physical semantics live in IR/schema rules; executable operations live in the DAG; hash-consing/fanout information is optimization metadata. Unknown schema fields, changed model conventions, illegal factors, fractional/boolean indices and noncanonical diagram order are rejected. General physical rule composition is not yet expressible.

## 5. Compiler architecture

```text
R1 PlanSpec -> structural adapter -> DiagramIR -> exact evaluation DAG -> callable evaluator
```

The main path is `compile_evaluator` in `src/keldysh4ai/diagram_compiler/evaluator.py:223`, using explicit-factor lowering in `graph.py:161`. It snapshots the IR once, lowers it once, and executes fresh numeric bindings without old R1 imports or retained old runtime state. Generated output is a DAG program with a Python closure/interpreter, not native source or machine code.

A direct diagramwise evaluator provides the unfactored implementation. A separate `lower_grouped` manually reproduces the recovered R1 recurrence after validating the admitted family. That comparison lowering is not automatic rediscovery of DP by generic CSE.

## 6. Canonicalization and CSE

Canonical identities retain time interval, integer momentum form, chord slot, phonon endpoints, vertex direction/incoming scope and normalization rule. Arithmetic identities retain ordered children. Numerical equality of q values, time differences or primitive results never merges structurally distinct leaves.

The primary DAG shares identical leaves and ordered factor prefixes. It does not perform distributive refactoring or general tensor algebra. Matrix order is preserved and tested before trace. Each node executes once per binding; the cache is not reused across bindings.

## 7. Differential validation

Fixed rule: `abs(v-r) <= 1e-12 + 1e-10*abs(r)`, elementwise, rejecting nonfinite values. It was not loosened.

References are the original R1 graph plus `ReferenceBinder`/`exec.interpret`, and independent explicit `index_oracle` enumeration. Both scalar F and every untraced two-band Op entry are checked. The 224-case reproducible demonstration passes, as do 84 seeded randomized bindings in tests.

Representative DEV/base rows, all real (imaginary part zero):

| Case | R1 result | Naive generated result | DAG result | Max error including Op |
|---|---:|---:|---:|---:|
| Scalar n1 | 0.05054715936426681 | 0.05054715936426681 | 0.05054715936426681 | 0 |
| Scalar n2 | 0.003835721205083103 | 0.003835721205083103 | 0.003835721205083103 | 0 |
| Scalar n3 | 0.00023812627788467457 | 0.00023812627788467454 | 0.00023812627788467454 | 2.71e-20 |
| Scalar n4 | 0.00021651527667647456 | 0.00021651527667647467 | 0.00021651527667647467 | 1.08e-19 |
| Two-band n1 | 0.10104575201940723 | 0.10104575201940723 | 0.10104575201940723 | 6.78e-21 |
| Two-band n2 | 0.00644400418112769 | 0.006444004181127689 | 0.006444004181127689 | 1.30e-18 |
| Two-band n3 | 0.00040932218041703244 | 0.00040932218041703244 | 0.00040932218041703244 | 2.71e-20 |

The maximum over the full demonstration is `2.7755575615628914e-17`. [differential.csv](differential.csv) contains all rows. Existing fixture split names do not establish an unseen statistical holdout.

The saved standalone example produces exactly `(0.0024401634116377456+0j)` in both evaluators; [binding.json](binding.json) and [demo_result.json](demo_result.json) preserve the inputs and outputs.

## 8. Graph statistics

| Family/order | Naive nodes | Unique DAG nodes | Shared nodes | Estimated operations |
|---|---:|---:|---:|---:|
| Scalar n1 | 7 | 7 | 0 | 3 |
| Scalar n2 | 35 | 28 | 3 | 15 |
| Scalar n3 | 257 | 124 | 34 | 91 |
| Scalar n4 | 2417 | 803 | 144 | 732 |
| Two-band n1 | 12 | 12 | 0 | 6 |
| Two-band n2 | 62 | 47 | 6 | 27 |
| Two-band n3 | 452 | 194 | 46 | 142 |

Shared nodes have fanout >1; operation counts exclude input/constant nodes and are neither FLOPs nor total cost. Even the naive graph retains shared structural identity constants. [graph_stats.csv](graph_stats.csv) additionally records shared arithmetic nodes and recovered-DP/R1 counts. Primary CSE is smaller than the naive graph but does not recover all DP suffix factorization. Equal DP/R1 counts are not graph isomorphism. No timings or speedup claims are supplied.

## 9. Higher-order extension analysis

Pairings grow as 1, 3, 15, 105, 945, 10395 for n1–6. Explicit frontend construction and validation retain factorial pairing growth; DAG sharing does not remove it. The implemented resource bound n≤6 is not evidence for every admitted order: campaign-validated orders are scalar n1–4 and two-band n1–3 only.

Another fixed order needs numerical/matrix tests and construction-resource checks. New material or diagram families require independently specified propagator/vertex/gauge, band/mode, sign/multiplicity and boundary contracts before admission. Variable-order sampling requires a separate measure and reversible proposal contract. None was implemented here.

## 10. Repository changes

| Path | Purpose |
|---|---|
| `src/keldysh4ai/diagram_compiler/ir.py` | Explicit versioned physical representation and JSON |
| `src/keldysh4ai/diagram_compiler/canonical.py` | Independent pairing/factor construction and strict family validation |
| `src/keldysh4ai/diagram_compiler/graph.py` | Ordered DAG/CSE and separately recovered DP |
| `src/keldysh4ai/diagram_compiler/evaluator.py` | Independent primitives, binding guards and compile-once evaluator |
| `src/keldysh4ai/diagram_compiler/r1_import.py` | Bounded structural/value adapters |
| `src/keldysh4ai/diagram_compiler/__init__.py` | Experimental source API |
| `tests/test_diagram_ir.py` | Hand construction, serialization and structural faults |
| `tests/test_r1_import.py` | Actual R1 specs, binding/provenance rejection |
| `tests/test_evaluator_vs_r1.py` | Independent differential, random and physics mutation tests |
| `tests/test_dag_sharing.py` | Ordered sharing, snapshot/rebinding and isolated runtime tests |
| `scripts/diagram_compiler_task1.py` | Reproducible evidence generation, without benchmarks |
| `docs/DIAGRAM_COMPILER_TASK1.md` | Twelve-section technical documentation |
| `research/diagram_compiler/task1/` | Small JSON/CSV example, provenance, verification and this report |
| `AGENT_LOG.md` | Short appended Task 1 record; left uncommitted because the file already carries other sessions' uncommitted edits |

No production adapter, release configuration, version, tag, historical source/evidence, benchmark or C0/P1 implementation is changed by this subsystem. Pre-existing dirty work is excluded from Task 1 commits.

## 11. Verification

- Compiler-specific tests: **281 passed**, no failures or skips.
- Final full suite: **1291 passed, 11 skipped, 17 failed, 45 errors**.
- Baseline: 1010 passed, 11 skipped, 17 failed, 45 errors. Exact failure/error IDs are unchanged: no additions or removals among 62 IDs.
- Existing failures include missing toolchain artifacts, external LiF/FEP files and historical R5 assertions. They were not all attributed to one missing compiler and were not repaired by modifying frozen science.
- Round-trip, all lowerings, zero coupling, repeated-then-separated dynamic inputs, A→B→A reuse, matrix noncommutativity, unsupported prefactors and asymmetric numerical faults are covered.
- Two isolated subprocess tests block old R1/public runtime imports and execute serialized IR/bindings against independent parent-process references.
- Final independent post-hardening review found no canonical-family numerical blocker but identified a mutable structural-number type gap. Four new tests failed before the correction and passed afterward.
- Hash comparison found **0 changed/missing files among 2893** protected files under `src/future_b`, `src/keldysh4ai/scheme_d`, `benchmarks`, and `release`. The snapshot was taken after initial Task 1 implementation, so it proves subsequent immutability, not pristine pre-task state.
- No remote release validation is claimed: this checkout has no configured remote or local release tags. No release/tag/version operation was performed.

Details: [verification.json](verification.json) and [baseline_failures.txt](baseline_failures.txt). Reproduction commands are in the technical document.

Process caveats: most initial code preceded its tests; seven chronological milestone commits were not made. Later closure/guard fixes did have observed red→green tests. Earlier background reports not returned to this session are not represented as completed independent approvals. These limitations do not change the measured numerical result, but prevent claiming full compliance with the originally requested process.

## 12. Current compiler maturity

| Capability | Status |
|---|---|
| Diagram representation | ESTABLISHED, bounded family scope |
| Exact evaluator generation | ESTABLISHED, executable DAG/Python closure |
| DAG/CSE optimization | ESTABLISHED, ordered structural CSE only |
| Cheap evaluator generation | NOT IMPLEMENTED |
| Delayed-acceptance generation | NOT IMPLEMENTED |
| Native code generation | NOT IMPLEMENTED |
| Variable-order compilation | NOT IMPLEMENTED |

This is a source-only experimental exact compiler baseline, not an arbitrary-diagram compiler, new release, material solution, paper GO, or demonstrated acceleration.

## 13. Biggest remaining abstraction gap

**A compositional typed physical rule/interface layer independent of the two hard-coded family templates.** The explicit representation is adequate for the admitted R1 objects, but changing physical families still requires implementation changes rather than supplying a general diagram specification.

## 14. Exactly one next task

**Task 2 — derive a cheap evaluator from the same DiagramIR**.

Recommended only; not implemented. No delayed-acceptance, P1 generation or performance campaign is included in this delivery.
