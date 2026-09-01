# L=2 slice closeout — 切片结项，不是认证

Authority: human closeout 2026-09-01, after
`notes/SCIENCE_LINE_60DAY.md` stop rule 6 (learned gate did not beat
the classical rule after cost).

**This is a slice closeout, not a certification.**
Paper 1 is not GO. It is not Freeze, not CERTIFY, not K4AI-592/593,
not admission to Keldysh4ai `main`, and not a Physics-for-AI result.

Do not merge this record as “Future B succeeded” into Keldysh4ai
`main`. 11A stays archived and unused.

## Allowed sentence (strongest public claim)

On the frozen periodic \(L=2\) Holstein slice: a teacher table exists;
SCBA beats one-shot Born in weak coupling and loses accuracy versus ED
at strong / adiabatic coupling; the classical stop \(\theta=0.03\)
cuts the cost of depth-64 SCBA without exceeding the fixed-maximum
error versus ED; a 7-parameter learned gate matches 5/6 test cells and
does not beat the classical rule. This is not a neural-architecture
result and not Physics-for-AI.

Chinese form (same claim, not stronger):

在冻结的周期 \(L=2\) Holstein 切片上：教师表存在；弱耦合 SCBA 优于
one-shot Born，强/绝热端相对 ED 变差；经典 \(\theta=0.03\) 停机把深度
64 的代价打下来，且相对 ED 不坏过固定满迭代；7 参数学习门在测试集
5/6，没有超过经典规则。这不是神经网络架构结果，也不是
Physics-for-AI。

For an advisor, one paragraph:

> Future B 第一个切片已经按预注册顺序做完。结论是负的、干净的：经典自适应停机有用，小学习门没有超过它，因此不写架构论文。方法笔记在 `notes/METHOD_NOTE.md`。

## Do not say

- Diagrammatic computation grammar is verified or falsified.
- Widen the net, change features, or retune \(\theta\) to flip Week 4.
- Promote the claim because tests passed.
- Put 11A, \(\Phi\), or a device into the contribution.

Week 4 is negative **inside the protocol**: the classical gate is about
one extra rainbow layer versus the ED oracle, on three cells only. The
13-sample logistic stopped early at \((0.75,0.8)\). Apparent cheapness
comes from that illegal early stop and is not an advantage.

## Three claim CSVs

| CSV | What it pins |
|---|---|
| `prototypes/future_b_neural_poc/teacher_map_l2.csv` | 12-cell \(E_0^{\mathrm{ED}}\), \(E_0^{\mathrm{Born}}\), \(E_0^{\mathrm{SCBA}}\) |
| `prototypes/future_b_neural_poc/week2_born_scba_vs_ed.csv` | Born/SCBA regions versus ED |
| `prototypes/future_b_neural_poc/week3_gated_vs_fixed.csv` | classical \(\theta=0.03\) versus depth 64 |

SHA-256:

```
a65dcde29457de0d3935b01f48693d8febb6042749c40fa65e315679d65f836a  teacher_map_l2.csv
73d7ccc625323c6372ea7aba95a850d589c72aaa48f899005cec02d8435303f4  week2_born_scba_vs_ed.csv
19d66c8a0f0c9c931ea02b67cb274f7cbe3cd1b8a78e7d1e996f05164e7d8d20  week3_gated_vs_fixed.csv
```

Negative companion, not a third success table:
`week4_verdict.csv` (`paper1_go=false`; SHA-256
`ed47daaea831e80959870663b91c7e296afbe4809f1dd6395b221d36b778ed8f`).
Per-cell depths: `week4_learned_vs_classical.csv`.

Method note: `notes/METHOD_NOTE.md`.

## Four signed conventions (not reopened)

1. \(\xi_k=2t(1-\cos k)\), so \(E_0(g=0)=0\).
2. Tadpole / Hartree **OFF** in the diagrammatic libraries.
3. Library I and Library II remain separate.
4. Default **NO** \(\Sigma_{\mathrm{VC}}\) on SCBA.

Source map: `notes/SIGNED_CONVENTION_SOURCES.md`. Translator
\(E_{\mathrm{lecture}}=E_{\mathrm{code}}-2t\) and plus-\(g\) in ED stay
with those four; they are not a fifth experiment.

## What stays closed

- Repairing or widening the Week 4 gate.
- Weeks 7–8 typed-block / routing ablations.
- Paper 1.
- New K4AI IDs, Freeze/CERTIFY, 592/593 admission.
- Merge to Keldysh4ai `main` as a success.

If work continues later, it must be a **new question** (spectrum,
\(L=4\), another diagram class) with a **new preregister**. It is not
making this gate larger.
