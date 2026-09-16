"""Copy C2_fixture tree and gate dump/reverse behind P1_FIXTURE (default off)."""
from __future__ import annotations
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'research/mainline/CLOSURE/2026-09-14/runs/night1/C2_fixture/trees/adapter'
DST = ROOT / 'closure/2026-09-16-final/trees/p1_clean'


def replace_once(s, old, new, label):
    if s.count(old) != 1:
        raise ValueError(f'{label}: {s.count(old)}')
    return s.replace(old, new, 1)


def main():
    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns('*.o', '*.mod', 'perturbo.x'))
    src = DST / 'pert-src'
    da = (src / 'linear_da_mod.f90').read_text()
    da = replace_once(
        da,
        '  logical function linear_da_hook()\n',
        '  logical function p1_fixture_on()\n'
        '    character(len=8) :: env\n'
        '    integer :: st\n'
        '    p1_fixture_on = .false.\n'
        '    call get_environment_variable(\'P1_FIXTURE\', env, status=st)\n'
        '    if (st==0) then\n'
        '      if (trim(adjustl(env))==\'1\' .or. trim(adjustl(env))==\'on\') p1_fixture_on = .true.\n'
        '    endif\n'
        '  end function p1_fixture_on\n\n'
        '  logical function linear_da_hook()\n',
        'fixture gate')
    (src / 'linear_da_mod.f90').write_text(da)
    jj = (src / 'diagMC_JJ_updates.f90').read_text()
    jj = replace_once(
        jj,
        '           linear_da_eval, linear_da_aux_uniform, linear_ld, c2_dump_swap, p1_prop_ell\n',
        '           linear_da_eval, linear_da_aux_uniform, linear_ld, c2_dump_swap, p1_prop_ell, p1_fixture_on, &\n'
        '           n_stage1_rej, n_stage2, n_accept\n',
        'use fixture')
    jj = replace_once(
        jj,
        '      call c2_dump_swap(10, iv1, iv2, diagram, 0.d0, 0.d0, 0_8, 0_8, 0.d0, 0.d0, 0.d0, 0.d0)\n',
        '      if (p1_fixture_on()) call c2_dump_swap(10, iv1, iv2, diagram, 0.d0, 0.d0, 0_8, 0_8, 0.d0, 0.d0, 0.d0, 0.d0)\n',
        'dump10')
    jj = replace_once(
        jj,
        '            call c2_dump_swap(1, iv1, iv2, diagram, ell_hat, 0.d0, &\n'
        '              c1_ncall(c1_g_prod)+c1_ncall(c1_g_full)+c1_ncall(c1_epc)-ng_enter, &\n'
        '              c1_ncall(c1_env_left)+c1_ncall(c1_env_right)+c1_ncall(c1_env_mid)-ne_enter, &\n'
        '              minval(vL%ekout), 0.d0, 0.d0, 0.d0)\n'
        '            return\n',
        '            n_stage1_rej = n_stage1_rej + 1\n'
        '            if (p1_fixture_on()) call c2_dump_swap(1, iv1, iv2, diagram, ell_hat, 0.d0, &\n'
        '              c1_ncall(c1_g_prod)+c1_ncall(c1_g_full)+c1_ncall(c1_epc)-ng_enter, &\n'
        '              c1_ncall(c1_env_left)+c1_ncall(c1_env_right)+c1_ncall(c1_env_mid)-ne_enter, &\n'
        '              minval(vL%ekout), 0.d0, 0.d0, 0.d0)\n'
        '            return\n',
        'a1 counter')
    # dump subroutine also increments n_stage1_rej; skip double count when fixture on
    dump = (src / 'linear_da_mod.f90').read_text()
    dump = dump.replace('    if (stage == 1) n_stage1_rej = n_stage1_rej + 1\n',
                        '    ! stage-1 count is in update_swap, independent of dump\n')
    (src / 'linear_da_mod.f90').write_text(dump)
    jj = replace_once(
        jj,
        '         call c2_dump_swap(3, iv1, iv2, diagram, ell_hat, ellR, &\n'
        '           c1_ncall(c1_g_prod)+c1_ncall(c1_g_full)+c1_ncall(c1_epc)-ng_enter, &\n'
        '           c1_ncall(c1_env_left)+c1_ncall(c1_env_right)+c1_ncall(c1_env_mid)-ne_enter, &\n'
        '           minval(vL%ekout), minval(vRn%ekout), real(mat_old), real(mat_new))\n',
        '         if (p1_fixture_on()) call c2_dump_swap(3, iv1, iv2, diagram, ell_hat, ellR, &\n'
        '           c1_ncall(c1_g_prod)+c1_ncall(c1_g_full)+c1_ncall(c1_epc)-ng_enter, &\n'
        '           c1_ncall(c1_env_left)+c1_ncall(c1_env_right)+c1_ncall(c1_env_mid)-ne_enter, &\n'
        '           minval(vL%ekout), minval(vRn%ekout), real(mat_old), real(mat_new))\n',
        'dump3')
    jj = replace_once(
        jj,
        '         stat%accept(7) = stat%accept(7) + 1; call c1_mark_commit(7)\n'
        '         if (diagram%vertexList(iv1)%tau <= diagram%vertexList(iv2)%tau) then\n',
        '         stat%accept(7) = stat%accept(7) + 1; call c1_mark_commit(7)\n'
        '         n_accept = n_accept + 1\n'
        '         if (p1_fixture_on() .and. diagram%vertexList(iv1)%tau <= diagram%vertexList(iv2)%tau) then\n',
        'accept gate 1')
    # the else branch of tau still runs reverse without gate — fix the else if
    jj = jj.replace(
        '         else\n'
        '            call p1_prop_ell(diagram, iv2, iv1, ell_rev)\n',
        '         else if (p1_fixture_on()) then\n'
        '            call p1_prop_ell(diagram, iv2, iv1, ell_rev)\n')
    jj = replace_once(
        jj,
        '      else\n'
        '         call c2_dump_swap(12, iv1, iv2, diagram, ell_hat, ellR, &\n',
        '      else\n'
        '         n_stage2 = n_stage2 + 1\n'
        '         if (p1_fixture_on()) call c2_dump_swap(12, iv1, iv2, diagram, ell_hat, ellR, &\n',
        'a2 counter')
    (src / 'diagMC_JJ_updates.f90').write_text(jj)
    (src / 'p1_clean.json').write_text(json.dumps({
        'schema': 'p1-clean-v1',
        'fixture_default': 'off',
        'source': str(SRC),
        'note': 'dump and after-commit reverse only if P1_FIXTURE=1; DA counters independent',
    }, indent=2) + '\n')
    print('patched', DST)


if __name__ == '__main__':
    main()
