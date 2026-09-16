# Application project summary (defensible)

I worked on first-principles diagrammatic Monte Carlo for the LiF
electron polaron. I audited native Fortran updates, found and repaired a
phonon-frequency refresh bug, and implemented exclusive timers that
located swap and environment/EPC costs.

I derived and implemented an exact-corrected analytic delayed-acceptance
score (P1) for legal swaps, validated stage-1 rejections against native
g/environment call counts, and ran free-running real-material chains.
After subtracting the documented bare-band energy, the formation energy
on the frozen 20³/rank20 setting is about −0.25 eV.

A protocol-frozen confirmation of a **clean** P1 binary versus B-best
gave a wall-time ratio whose 95% bootstrap interval still crossed the
predeclared 5% threshold, with some chains failing a predeclared HAC
stability test. I therefore did **not** claim a practical speedup.

I did not train the frozen P4/P5 models because the 64-d packet/label
contract was not met, and I did not claim R1 accelerates the material
code: the native grouped measure was not closed. I documented these as
unverified rather than as universal negatives.
