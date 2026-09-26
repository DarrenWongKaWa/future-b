"""Opt-in fix for the reference trace in FEP-DMC's remove_external_ph.

When the diagram has internal vertices, remove_external_ph builds the trace of
the configuration *without* the external pair (mat_old) with the wrap segment
propagating at v_head%ekout. At that point the pair is still present, so the head
segment carries momentum k - q. The pair-less wrap segment carries k, whose
energies are vn1%ekout (= vL%ekin). The removal acceptance therefore compares the
with-pair trace with a reference on the wrong band energies. add_external_ph's
identical line is correct (there the pair does not exist yet), and so is the
empty-diagram branch of the removal, which already uses vn1%ekout.

With FUTUREB_EXTRMFIX=1 the reference wrap segment uses vn1%ekout; otherwise the
code is unchanged.

Usage: python -m future_b.fepdmc.patches.extrmfix <perturbo-fep-dmc dir>
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
                "      logical, save :: rmfix_checked = .false., rmfix = .false.\n"
                "      character(len=8) :: rmenv\n"
                "      integer :: rmst\n", "declarations")
    body = once(body,
                "         !old : vR -> v_tail/v_head -> vL\n"
                "         Elist = v_head%ekout - minval(v_head%ekout)\n",
                "         !old : vR -> v_tail/v_head -> vL\n"
                "         if (.not. rmfix_checked) then\n"
                "            call get_environment_variable('FUTUREB_EXTRMFIX', rmenv, status=rmst)\n"
                "            rmfix = (rmst == 0 .and. trim(adjustl(rmenv)) == '1')\n"
                "            rmfix_checked = .true.\n"
                "         end if\n"
                "         if (rmfix) then\n"
                "            Elist = vn1%ekout - minval(vn1%ekout)\n"
                "         else\n"
                "            Elist = v_head%ekout - minval(v_head%ekout)\n"
                "         end if\n", "reference wrap segment")
    p.write_text(t[:start] + body + t[end:])
    print("remove_external_ph reference-trace fix (FUTUREB_EXTRMFIX) added to", root)


if __name__ == "__main__":
    main(sys.argv[1])
