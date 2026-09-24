# Diagram Compiler integration onto public main

The original Diagram Compiler preview was developed on the Future B live
extract history and released as `diagram-compiler-v0.1.0`. That history
has no Git merge base with the public `main` line containing Future B
v1.2.0. This integration copies the bounded compiler source, tests,
evidence, native validation bridge and CI into a branch based on public
`main`; it does not merge the two unrelated histories.

The public v1.2.0 tag, its P1 adapter, frozen science records and release
assets remain unchanged. The integrated subsystem remains experimental:

- it handles the documented fixed-order scalar and two-band families;
- Task 6 validates a separate generated kernel at LEVEL 2;
- it does not replace `update_swap` or public P1;
- it does not establish a speedup, real-material end-to-end result, or
  generic diagram/QFT compiler.

The original `diagram-compiler-v0.1.0` tag remains immutable. Future
commits on public `main` can now have ordinary Git ancestry with the
integrated source.

The frozen v1.2.0 sdist retains its existing manifest and checksum record.
It does not include the compiler evidence directory, generated native fixture
or FEP-DMC bridge. The compiler evidence suite runs from the GitHub source
tree and its dedicated CI workflow; an unpacked v1.2.0 sdist skips only those
evidence-dependent tests.

An independent `future-b-diagram-compiler` 0.2.0 wheel/sdist is built
from the tracked compiler source using
[`build_diagram_compiler_package.py`](../scripts/build_diagram_compiler_package.py).
Its sdist carries the Task 1–7 evidence and four editable draw.io pages;
its wheel carries the Python compiler and Fortran primitive runtime. See
[`DIAGRAM_COMPILER_PACKAGE.md`](DIAGRAM_COMPILER_PACKAGE.md) for install
and reproduction commands.
