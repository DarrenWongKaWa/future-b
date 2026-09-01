# Candidate 1 stop — T1 structure failed on A(ω)

Authority: `notes/C1_METRICS_PREREGISTER.md`. Artifact:
`prototypes/future_b_neural_poc/c1_spectral_vs_ed.csv`.

C1-T1 required error_A(SCBA64) to increase with g at each fixed Ω and
to increase as Ω decreases at each fixed g, with at most one of 17
comparisons allowed to fail. The CSV gives **15/17** strict increases
and **2** exceptions, both at the strong/adiabatic cell (1.05, 0.5):

- fixed Ω=0.5: error_A_SCBA64(0.75)=1.2736098120802806
  !< error_A_SCBA64(1.05)=0.9863172923173602
- fixed g=1.05: error_A_SCBA64(Ω=0.8)=1.4156798290239707
  !< error_A_SCBA64(Ω=0.5)=0.9863172923173602

T1 verdict: **FAIL**. Thresholds were not softened. The metric was not
moved onto Z or error_M1 after seeing the table. No learned gate, no
θ retune, no Week-4 repair, no Weeks 7–8.

Candidate 1 stops. `paper1_go` stays false.
