"""Opt-in fix for a stale phonon frequency in FEP-DMC's add_external_ph.

At the pinned commit, multiphonon_update_matrix::add_external_ph samples a new
momentum for the external (boundary-wrapping) pair but never calls cal_wq_int.
vn1%wq, and through vn2%wq = vn1%wq the partner's, keep the frequencies left in
the recycled vertex slot (or uninitialized memory on first use). They then enter
the pair's Dph factors, its imaginary-time decay and the energy estimator.
add_ph calls cal_wq_int at the same point.

With FUTUREB_WQFIX=1 the missing call is made; otherwise the code is unchanged.

This is the defect the C0 source adapter (integration/c0, v1.1.0) fixes
unconditionally on the same line; this patch is its run-time-switchable form,
for A/B runs against unfixed native. On a C0 tree the switch is redundant.

Usage: python -m future_b.fepdmc.patches.wqfix <perturbo-fep-dmc dir>
"""

from __future__ import annotations

import sys
from pathlib import Path


def once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"anchor for {label!r} found {n} times")
    return text.replace(old, new)


def main(root: str) -> None:
    p = Path(root) / "pert-src" / "diagMC_JJ_updates.f90"
    t = p.read_text()
    mod = t.index("module multiphonon_update_matrix")
    start = t.index("subroutine add_external_ph(diagram, stat)", mod)
    end = t.index("end subroutine", start)
    body = t[start:end]
    body = once(body, "      type(vertex),pointer :: vL,vR, vn1, vn2 \n",
                "      type(vertex),pointer :: vL,vR, vn1, vn2 \n"
                "      logical, save :: wqfix_checked = .false., wqfix = .false.\n"
                "      character(len=8) :: wqenv\n"
                "      integer :: wqst\n", "declarations")
    body = once(body, "      call sample_q_omp_int(diagram%seed,vn1%i_q,vn1%Pq,vn1); Pq = vn1%Pq\n",
                "      call sample_q_omp_int(diagram%seed,vn1%i_q,vn1%Pq,vn1); Pq = vn1%Pq\n"
                "      if (.not. wqfix_checked) then\n"
                "         call get_environment_variable('FUTUREB_WQFIX', wqenv, status=wqst)\n"
                "         wqfix = (wqst == 0 .and. trim(adjustl(wqenv)) == '1')\n"
                "         wqfix_checked = .true.\n"
                "      end if\n"
                "      if (wqfix) call cal_wq_int( vn1%i_q, vn1%wq )\n", "q sample")
    p.write_text(t[:start] + body + t[end:])
    print("wq fix (FUTUREB_WQFIX) added to", root)


if __name__ == "__main__":
    main(sys.argv[1])
