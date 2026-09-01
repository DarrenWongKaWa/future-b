# Double-counting memo: do not add \(\Sigma_{\rm VC}\) onto SCBA

Week 1 C0 record. This memo does **not** reopen K4AI-568, K4AI-565, the
crossing-block POC, or archive 11A. It cites existing freeze language
as a record.

## Default (binding)

**NO adding \(\Sigma_{\rm VC}\) onto SCBA.**

Library I = bare Born + bare VC, both on \(G_0\), separate folder
(`prototypes/future_b_neural_poc/crossing_block_poc.py`).

Library II = SCBA on dressed \(G\), separate folder
(`src/keldysh4ai/future_b/hopping/chain_scba.py` and the atomic
`scba_solve` / `scba_constant_cfe` family).

Do not merge the libraries. Do not train a coefficient in front of
either block.

## Which \(O(g^4)\) diagrams SCBA already contains

SCBA is the self-consistent non-crossing rainbow:

\[
\Sigma_{\rm SCBA}(z)=g^2 G(z-\Omega),\qquad G(z)=\frac{1}{z-\Sigma_{\rm SCBA}(z)}
\]

at T=0 with vacuum tadpole off (weighted-shift kernel in
`src/keldysh4ai/future_b_atomic.py`; freeze statement in
`experiments/FUTURE_B/FUTURE_B_C1_BLOCK_LIBRARY_FREEZE.md` FB-C1.4).

Iterating that equation on dressed \(G\) sums the **non-crossing**
rainbow / nested Born diagrams to all orders. Equivalently, T=0 SCBA
is the constant-coefficient continued fraction \(1,1,1,\ldots\).

SCBA does **not** sum crossed phonon lines. Goodvin (intro), as already
recorded in the C1 freeze: SCBA “sums exactly only the non-crossed
diagrams.”

The first crossed / vertex-correction graph is Library I’s
\(\mathcal B_{\rm VC}\), order \(g^4\), three bare propagators, two
internal momenta, combinatorial factor one
(`prototypes/future_b_neural_poc/CROSSING_BLOCK_SOURCE.md`, Appendix
App01). That topology is absent from SCBA.

## Why topological disjointness is not a license to add

1. **Kind split.** SCBA is a *resummation* \(R_{\rm SCBA}\), a complete
   \(\Sigma\). \(\mathcal B_{\rm VC}\) is an *additive diagram block*.
   The freeze forbids placing an additive subset of a class beside the
   resummation of that class, and it forbids
   \(\{R_{\rm SCBA},\mathcal B_{\rm Born}\}\) as a double count of the
   Born skeleton (FB-C1.2, FB-C1.5).
2. **Crossing vs SCBA is still NO in the freeze.**
   \(\{R_{\rm SCBA},\mathcal B_{\rm cross}\}\) is **no** until the
   crossing kernel is source-closed **and** shown not already inside a
   chosen resummation (FB-C1.5). This memo does not close that OPEN
   item and does not treat the POC App01 kernel as that closure for
   Library II.
3. **\(G_0\) versus dressed \(G\).** Library I evaluates \(\mathcal B_{\rm VC}\)
   on bare \(G_0\). Library II dresses \(G\). Adding a bare-\(G_0\)
   \(g^4\) graph onto a self-consistent rainbow is an inconsistent mix,
   not a controlled next order.
4. **Atomic collapse is a numerical trap, not a construction.** At
   hop \(=0\), crossed and non-crossed \(g^4\) graphs take the **same
   value** (Ciuchi Sec. III.3, already retained in FB-C1.4:
   fourth-order non-crossing piece and vertex correction are equal at
   zero density in infinite \(d\); a self-consistent non-crossing /
   Migdal scheme fails because CFE coefficients would all become 1).
   Adding \(\Sigma_{\rm VC}[G_0]\) onto SCBA at \(t=0\) therefore
   *numerically doubles* a piece SCBA already has at \(O(g^4)\), even
   though the Feynman topologies differ. The Week 1 atomic audit
   (`notes/ATOMIC_LIMIT_AUDIT.md`) finds the bare VC coefficient
   \(c=1\), identical to SCBA and half of the exact linear series
   \(c=2\).
5. **Library I internal disjointness is not Library II disjointness.**
   `CROSSING_BLOCK_SOURCE.md` (“Disjointness from `B_BORN`”) only
   states that \(B_{\rm BORN}\) (\(g^2\), one propagator) and
   \(B_{\rm VC}\) (\(g^4\), three propagators) are different blocks
   inside the low-order *bare* grammar, each used once. That record
   does not authorize \(R_{\rm SCBA}+B_{\rm VC}\).

## Verdict

Default NO: do not add \(\Sigma_{\rm VC}\) onto SCBA.

SCBA already contains the non-crossing rainbow / nested Born family to
all orders and does not contain crossed phonon lines. That disjointness
of topology is recorded; it is not used here to stack the libraries.
Week 2, if authorized, compares the two libraries **separately** to
the L=2 teacher, on the same origin.

Cited records (not reopened):

- `experiments/FUTURE_B/FUTURE_B_C1_BLOCK_LIBRARY_FREEZE.md`
  (K4AI-568 freeze; FB-C1.2 kind split; FB-C1.4 SCBA vs crossing;
  FB-C1.5 compatibility matrix)
- `prototypes/future_b_neural_poc/CROSSING_BLOCK_SOURCE.md`
  (App01 kernel; disjointness from `B_BORN` only)
- `notes/SCIENCE_LINE_60DAY.md` human lock: no \(\Sigma_{\rm VC}\) on
  SCBA without a written disjoint-diagram memo; this is that memo,
  and the default it writes is NO.
