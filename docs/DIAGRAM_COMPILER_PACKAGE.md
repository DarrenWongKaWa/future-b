# Installable Diagram Compiler package

`future-b-diagram-compiler` is a separate experimental Python distribution.
Its import path is `keldysh4ai.diagram_compiler`. Use a clean Python 3.11+
environment so another distribution named `keldysh4ai` cannot shadow it.
The wheel includes the Python compiler, R1 oracle modules, the Fortran
primitive runtime and the tracked rebind fixture. The sdist additionally
includes Tasks 1–7 reports, CSV/JSON evidence, tests, a deterministic
quickstart and the public FEP-DMC validation recipe.

## Build from the GitHub source tree

```sh
python scripts/build_diagram_compiler_package.py --stage /tmp/diagram-compiler-source
python -m pip install build
python -m build /tmp/diagram-compiler-source --outdir /tmp/diagram-compiler-dist
```

The staging command refuses an existing destination. `SOURCE_MANIFEST.json`
in the staged source records every copied file's SHA256 and the source commit.
Use a clean tagged checkout for a release build.

## Install and run

```sh
python3.12 -m venv /tmp/dc-env
/tmp/dc-env/bin/python -m pip install /tmp/diagram-compiler-dist/future_b_diagram_compiler-0.2.0-py3-none-any.whl
/tmp/dc-env/bin/python /tmp/diagram-compiler-source/examples/quickstart.py
```

The quickstart compiles a scalar n=1 DiagramIR and evaluates one binding.
The generated example should print `exact_F=0.05137576466738666` and the
same value for `cheap_F_hat`. Scalar cheapness is not a cost reduction in
this policy.

## Reproduce the research checks

Unpack the source tarball, install its `dev` extra, then run `python -m pytest
-q tests` and `python scripts/diagram_compiler_task1.py --output /tmp/task1`.
Task 1 checks 224 fixed bindings against R1 and an independent diagram
index oracle. The optional Task 6 validation also needs Docker, the
tracked `Dockerfile.u22`, and a separately cloned public FEP-DMC tree at
`05d08449cffdbd0dfbbbf5009add5cc887bc754b`. Follow
[`integration/diagram_compiler/README.md`](../integration/diagram_compiler/README.md).

The four editable draw.io pages are in
[`diagram-compiler-workflows.drawio`](diagrams/diagram-compiler-workflows.drawio).

The package does not produce a real-material observable, replace production
FEP-DMC `update_swap` or public P1, or establish a Monte Carlo speedup.
