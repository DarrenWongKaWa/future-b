# Diagram Compiler native validation

This directory contains the validation-only bridge for Task 6. It does not
patch `update_swap`, replace public P1, or modify the pinned FEP-DMC tree.

The native image is reproducible from the tracked Dockerfile:

```sh
docker build -f integration/diagram_compiler/Dockerfile.u22 \
  -t futureb-u22-env:local .
```

The FEP-DMC source is an external witness. Clone it into a user-selected
directory and check out the pinned commit before running validation:

```sh
git clone https://github.com/yaoluo/FEP-DMC /tmp/fep-dmc
git -C /tmp/fep-dmc checkout 05d08449cffdbd0dfbbbf5009add5cc887bc754b
FUTURE_B_FEP_DMC=/tmp/fep-dmc \
  FUTURE_B_DC_DOCKER=futureb-u22-env:local \
  python scripts/diagram_compiler_task6.py \
  --fep-dmc /tmp/fep-dmc --image futureb-u22-env:local
```

There is deliberately no private machine path default. The validator refuses
to run without an explicit `--fep-dmc` path or `FUTURE_B_FEP_DMC`.
