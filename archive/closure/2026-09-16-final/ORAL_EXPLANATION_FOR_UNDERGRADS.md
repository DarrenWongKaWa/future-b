# Oral explanation (undergrad level)

We simulate an electron dragging a crystal distortion in LiF. The
computer builds Feynman diagrams and averages them. Some diagram moves
are expensive (electron-phonon vertices and environments).

We tried a cheap filter (P1): guess whether a swap of two phonons is
worth the expensive calculation, then always do the expensive exact
check if the guess says yes. That is delayed acceptance, not replacing
physics with a neural net.

On the grid we actually used, the formation energy is about **minus a
quarter of an electron-volt**, not +9 eV (that +9 was the electron
energy before subtracting the empty-crystal reference).

The filter did reject about a third of the expensive swap attempts. The
whole program did **not** get a clearly proven 5% wall-clock win in the
final test we had budget for. We stopped instead of hunting a nicer
number.
