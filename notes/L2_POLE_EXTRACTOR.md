# Periodic L=2 pole extractor — fill record

Definition was frozen first in `notes/L2_POLE_DEFINITION.md` (η=10^{-4},
window $[-8.0,0.25]$, $E_0=$ lowest interior $\operatorname{Re}D=0$
of $G(k=0)$, SCBA depth 64, tadpole off, $k\in\{0,\pi\}$).
This file records the fill. It does not start Week 2.

## Checks that must hold

- Geometry: `l2_dispersion()` gives $\xi_0=0$, $\xi_\pi=4t$.
- $g=0$: `E0_ED=0`, `E0_Born=0`, `E0_SCBA=0`.
- Source: `l2_periodic_pole.py` and `build_teacher_map_l2.py` do not
  import `chain_scba` or `crossing_block_poc`.
- `E0_Born_VC` remains `NOT_COMPUTED`.
- Atomic-limit verdict is unchanged: **inconclusive**. Default remains
  **NO** $\Sigma_{\mathrm{VC}}$ on SCBA.

## Counts

CSV: `prototypes/future_b_neural_poc/teacher_map_l2.csv`

| column | real cells | `NOT_COMPUTED` |
|---|---|---|
| `E0_ED` | 12 | 0 |
| `E0_Born` | 12 | 0 |
| `E0_SCBA` | 12 | 0 |
| `E0_Born_VC` | 0 | 12 |

`E0_ED` bits match the previous teacher column, including strong-corner
$(1.05,0.5)$: $M=14$, $E_0=-1.2711554105515426$.

Diagnostics: `prototypes/future_b_neural_poc/l2_pole_diagnostics.json`.
Every Born/SCBA cell has one interior $\operatorname{Re}D$ crossing
in the frozen window; $|D|$ at the root is $\sim\eta$.

## Allowed sentence

On the frozen twelve cells, periodic $L=2$ `E0_ED`, `E0_Born`, and
`E0_SCBA` are real numbers under the signed origin
$\xi_k=2t(1-\cos k)$. `E0_Born_VC` is still `NOT_COMPUTED`.

## Forbidden sentences

- C0 is complete
- Week 2 is open / SCBA should win at weak coupling / fail at strong
- a router may be trained
- $B_{\mathrm{VC}}$ passed the atomic limit
- Physics-for-AI

Looking at who is closer to ED is Week 2. That comparison was not run
as a verdict here.
