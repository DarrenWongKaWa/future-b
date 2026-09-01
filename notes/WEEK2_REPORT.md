# Week 2 report — Born/SCBA vs ED on the frozen L=2 map

Worker S (Science). Branch `prototype/future-b-neural-poc`.
HEAD: `e6a14f652467f28bf67976b9334d5db822111449` (teacher-map commit
`e6a14f6`). No new K4AI number. No merge to `main`. No commit from
this worker. No L=2 ED rerun. No training. No change to $\eta$,
$L$, $\xi_k$, tadpole, `holstein_ed.py`, or
`l2_periodic_pole.py`. `chain_scba.py` was not called.

Preregister `notes/WEEK2_METRICS_PREREGISTER.md` was written to disk
**before** `prototypes/future_b_neural_poc/week2_born_scba_vs_ed.csv`
and before this report. Metrics use only that file's formulas and the
immutable teacher-map $E_0$ columns. Week-2 bands replace Week-1
label cuts for this week only; `notes/WEEK1_LABELS_PREREGISTER.md` was
not edited.

Corrected questions (not the older sentence in
`notes/SCIENCE_LINE_60DAY.md`): (1) at weak $\lambda$, is SCBA
closer to ED than one-shot Born? (2) at strong / adiabatic
$\lambda$, does SCBA lose accuracy versus ED (not versus Born)?

## 1. Tests T1–T4: pass/fail and the counts

Source:
`prototypes/future_b_neural_poc/week2_born_scba_vs_ed.csv`
(12 rows; $E_0$ columns equal
`prototypes/future_b_neural_poc/teacher_map_l2.csv`). Bands from
Week-2 cuts: 4 weak ($\lambda<0.08$), 7 intermediate, 1 strong.

| test | verdict | counts |
|------|---------|--------|
| T1 weak-coupling sanity | **PASS** | 4/4 weak cells have $\lvert\Delta_{\mathrm{SCBA}}\rvert < \lvert\Delta_{\mathrm{Born}}\rvert$; 0 violations |
| T2 strong-coupling accuracy vs ED | **PASS** | 1/1 strong cell $(1.05,0.5)$: $\mathrm{rel}_{\mathrm{SCBA}}=0.37357276423723235 \ge 0.20$ |
| T3 monotone structure | **PASS** | 17/17 comparisons; 0 exceptions |
| T4 physical signs | **PASS** | 12/12 cells satisfy $E0_{\mathrm{ED}} < E0_{\mathrm{SCBA}} < E0_{\mathrm{Born}} < 0$; no pole-search miss |

T1 cells ($\lambda<0.08$): $(0.15,0.5)$, $(0.15,0.8)$,
$(0.15,2.0)$, $(0.45,2.0)$. These are **not** the six Week-1
“weak” labels. Descriptive column `scba_beats_born` is `true` on
**12/12** cells, including the strong cell; that 12/12 count is **not**
a T1–T4 success criterion except as T1 on the four weak cells.

T3: $\mathrm{rel}_{\mathrm{SCBA}}$ increases with $g$ at each
fixed $\Omega$, and increases as $\Omega$ decreases at each fixed
$g$. Grid $\mathrm{rel}_{\mathrm{SCBA}}(g,\Omega)$:

| $g/t$ | $\Omega/t=0.5$ | $0.8$ | $2.0$ |
|---------|------------------|---------|---------|
| 0.15 | 0.02036247 | 0.00829575 | 0.00151864 |
| 0.45 | 0.13591526 | 0.06508419 | 0.01333597 |
| 0.75 | 0.26301949 | 0.14709219 | 0.03538076 |
| 1.05 | 0.37357276 | 0.23172885 | 0.06516381 |

No minor exception was recorded. No rescue sweep.

`notes/WEEK2_STOP.md` was **not** written: T1 and T4 both passed, so
thresholds were not softened and the stop file is not required. T2 and
T3 also passed.

## 2. What “SCBA loses at strong coupling” means here

On this slice that phrase is T2, not a Born-versus-SCBA ranking: at
the unique strong cell $(g/t,\Omega/t)=(1.05,0.5)$,
$\lambda=1.1025$, SCBA underbinds relative to ED by
$\Delta_{\mathrm{SCBA}}=0.4748690404948537$ and
$\mathrm{rel}_{\mathrm{SCBA}}=0.37357276423723235$, which is above
the preregistered 0.20 threshold, so more than a fifth of the teacher
binding is missing ($E0_{\mathrm{SCBA}}=-0.7962863700566889$ versus
$E0_{\mathrm{ED}}=-1.2711554105515426$). Born is worse still
($\mathrm{rel}_{\mathrm{Born}}=0.523065801830631$), so SCBA remains
closer to ED than one-shot Born on that cell; the collapse is versus
the teacher at large $\lambda$ / small $\Omega$. Spectra were not
opened because T4 passed.

## 3. Claim ceiling

On the frozen periodic L=2 slice, one-shot Born and SCBA have structured, physically credible regions of use versus ED. SCBA is closer to ED than Born in every cell computed. Accuracy versus ED collapses at large λ / small Ω. This is not adaptivity, not a learned gate, and not Physics-for-AI.

## 4. What remains NOT_COMPUTED

- $E0_{\mathrm{Born+VC}}$: still `NOT_COMPUTED` in all 12 teacher-map
  cells; not invented; not a Week-2 column.
- Spectra: not opened (T4 did not fail).
- Week 3 classical gate: $\theta_{\mathrm{class}}$, gated versus
  fixed-maximum SCBA, and error–cost accounting.
- Any learned gate, router, MLP, or GRU.
- $L\neq 2$, $n_k\neq 2$, open-chain `chain_scba.py` energies.
- $\Sigma_{\mathrm{VC}}$ on SCBA (forbidden; default **NO**).
- Architecture, conservation, or Physics-for-AI evidence.
- Archive 11A, K4AI-592, and K4AI-593 as live Future B proof.

## 5. Do not start Week 3

Week 3 is not started. This worker does not implement
$\lVert\Delta\Sigma\rVert/\lVert\Sigma\rVert<\theta_{\mathrm{class}}$,
does not choose $\theta_{\mathrm{class}}$, and does not train. A
later week cannot rescue a failed earlier week; Week 2 here is a
teacher-backed comparison on the frozen twelve-cell slice, not a
license to open adaptive stopping.
