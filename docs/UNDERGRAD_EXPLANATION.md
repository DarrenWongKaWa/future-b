# Oral explanation (undergraduate level)

We simulate one extra electron in lithium fluoride. The electron
distorts the surrounding lattice; that combined object is a polaron.
The formation energy is how much lower the energy is than a bare
electron in a frozen lattice. On the grid we actually used, that number
is about **minus a quarter of an electron-volt**. A previous plot of
**+9 eV** was the electron’s absolute energy before subtracting the
empty-crystal reference. Those are different questions.

The computer builds Feynman diagrams (pictures of the electron emitting
and reabsorbing lattice vibrations) and averages them with Monte Carlo.
Some proposed changes to a diagram are expensive: they need the full
electron–phonon vertex and a contraction of the rest of the diagram.

We tried a cheap filter called delayed acceptance (P1). First guess,
using only easy energy and time information, whether a swap of two
vibrations is worth the expensive calculation. If the guess says “no”,
skip the expensive work. If it says “yes”, still do the expensive exact
check so the simulation remains statistically exact. That is not
replacing physics with a neural network.

The filter rejected about one third of those expensive swap attempts.
The whole program got a bit faster in the final test, but not clearly
by 5% once we used the statistical rule we had written down in advance.
We stopped instead of rerunning until the number looked nicer.

We also built a way to reuse arithmetic across families of diagrams
(R1). On the tests we finished, it was correct but not faster than an
ordinary optimized formula. Grouping diagrams in the real LiF code, and
training small residual models, are written up as future work and were
not done here.
