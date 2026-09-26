"""Opt-in support fix for FEP-DMC's remove_external_ph (detailed balance).

add_external_ph samples the head-side time only on [0, min(tau_next, tau_max/2)]
and the tail-side time only on [max(tau_prev, tau_max/2), tau_max].
Vertex-time moves let an outermost external vertex drift outside those ranges.
remove_external_ph evaluates the reverse-add densities with exp_sample_omp in
density mode, which has no range check, so such pairs get a nonzero removal
probability although the add can never recreate them. The add/remove pair is
then not in detailed balance.

With FUTUREB_EXTFIX=1 the removal is rejected when either stored time lies
outside the add's proposal range; otherwise the code is unchanged.

Usage: python -m future_b.fepdmc.patches.extfix <perturbo-fep-dmc dir>
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
    start = t.index("subroutine remove_external_ph(diagram, stat)", mod)
    end = t.index("end subroutine", start)
    body = t[start:end]
    body = once(body, "      type(vertex),pointer :: vL,vR, vn1, vn2 \n",
                "      type(vertex),pointer :: vL,vR, vn1, vn2 \n"
                "      logical, save :: extfix_checked = .false., extfix = .false.\n"
                "      character(len=8) :: xfenv\n"
                "      integer :: xfst\n", "declarations")
    body = once(body,
                "      call exp_sample_omp(diagram%seed,tauR, v_tail%tau,decay_exp,vn2%tau,Pt2)\n",
                "      call exp_sample_omp(diagram%seed,tauR, v_tail%tau,decay_exp,vn2%tau,Pt2)\n"
                "      if (.not. extfix_checked) then\n"
                "         call get_environment_variable('FUTUREB_EXTFIX', xfenv, status=xfst)\n"
                "         extfix = (xfst == 0 .and. trim(adjustl(xfenv)) == '1')\n"
                "         extfix_checked = .true.\n"
                "      end if\n"
                "      if (extfix) then\n"
                "         if (vn1%tau > tauL .or. vn2%tau < tauR) return\n"
                "      end if\n", "support check")
    p.write_text(t[:start] + body + t[end:])
    print("external-removal support fix (FUTUREB_EXTFIX) added to", root)


if __name__ == "__main__":
    main(sys.argv[1])
