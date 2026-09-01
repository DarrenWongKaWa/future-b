# Future B

Periodic \(L=2\) Holstein teacher map. Extracted from Keldysh4ai
`prototype/future-b-neural-poc`. Inverse/11A/K4AI task machinery is
**not** in this tree.

Start here: [FUTURE_B.md](FUTURE_B.md), then
[notes/CONSTRAINTS_FUTURE_B.md](notes/CONSTRAINTS_FUTURE_B.md).

Parent (read-only archive):
`/Users/kawawong/Research/Keldysh4ai-worktrees/future-b-neural-poc`

Pins: [notes/SOURCE_PINS.md](notes/SOURCE_PINS.md)

## Setup

```bash
cd /Users/kawawong/Research/future-b
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

Or, without install:

```bash
PYTHONPATH=src python -m pytest tests -q
```

## Live tables

- `prototypes/future_b_neural_poc/teacher_map_l2.csv`
- `prototypes/future_b_neural_poc/week2_born_scba_vs_ed.csv`

Week 3 is not started. Do not train a router. Do not add
\(\Sigma_{\mathrm{VC}}\) onto SCBA. Do not merge this extract back
into Keldysh4ai `main`.
