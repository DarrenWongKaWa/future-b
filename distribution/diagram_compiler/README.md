# Future B Diagram Compiler 0.2.0

An experimental, fixed-order physics-aware diagram compiler. This package
contains the Python compiler, exact and cheap evaluators, Design-B delayed
acceptance, typed NativeKernelIR, deterministic Fortran emission, and a
versioned Fortran primitive runtime.

Install the wheel with Python 3.11 or newer:

```sh
python -m pip install future_b_diagram_compiler-0.2.0-py3-none-any.whl
python -c "from keldysh4ai.diagram_compiler import build_scalar_ir; print(build_scalar_ir(1).family.family_id)"
```

The source distribution adds the Task 1–7 evidence, scientific tests,
public FEP-DMC pin checker and Docker build recipe. From an unpacked sdist:

```sh
python -m pip install -e '.[dev]'
python examples/quickstart.py
python -m pytest -q tests
python scripts/diagram_compiler_task1.py --output /tmp/task1-evidence
```

The Fortran path requires `gfortran`. The Task 6 native validation additionally
requires Docker and a separately cloned public FEP-DMC checkout at commit
`05d08449cffdbd0dfbbbf5009add5cc887bc754b`. See
`integration/diagram_compiler/README.md`.

Scope: fixed-order scalar Holstein and Hermitian two-band families tested in
Tasks 1–6. The compiler does not replace production `update_swap` or public
P1. No performance acceleration, real-material end-to-end result, arbitrary
diagram topology, or generic QFT support is claimed. See
`docs/DIAGRAM_COMPILER_RELEASE_NOTES.md` and the evidence CSVs.
