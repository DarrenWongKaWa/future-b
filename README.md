# Future B

Periodic \(L=2\) Holstein teacher map. Extracted from Keldysh4ai
`prototype/future-b-neural-poc`. Inverse/11A/K4AI task machinery is
**not** in this tree.

Start here: [FUTURE_B.md](FUTURE_B.md), then
[notes/CONSTRAINTS_FUTURE_B.md](notes/CONSTRAINTS_FUTURE_B.md).

Signed-convention papers: [notes/SIGNED_CONVENTION_SOURCES.md](notes/SIGNED_CONVENTION_SOURCES.md),
PDFs in [references/](references/).
Motive: [notes/MOTIVATION.md](notes/MOTIVATION.md).

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
- `prototypes/future_b_neural_poc/week3_gated_vs_fixed.csv`
- `prototypes/future_b_neural_poc/week4_verdict.csv` (`paper1_go=false`)

Closeout: [notes/SLICE_CLOSEOUT.md](notes/SLICE_CLOSEOUT.md)
(**切片结项，不是认证**), method note
[notes/METHOD_NOTE.md](notes/METHOD_NOTE.md). Do not widen the learned
gate. Do not add \(\Sigma_{\mathrm{VC}}\) onto SCBA. Do not merge this
extract into Keldysh4ai `main` as “Future B succeeded”.
