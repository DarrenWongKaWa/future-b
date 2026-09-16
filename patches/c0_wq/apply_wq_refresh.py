"""One-call correctness repair in owned night1/C0/repair_v2 trees only.

The caller copies/builds/runs. This module neither executes a solver nor edits
old evidence. Apply before instrument_c0 so actual frequency writes are traced.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

MARKER = '      ! C0-WQ-REFRESH: define frequency for this newly sampled external q.'
CALL = '      call cal_wq_int(vn1%i_q, vn1%wq)'


def external_body(source: str) -> tuple[int, int, str]:
    matches = list(re.finditer(r'^\s*subroutine\s+add_external_ph\s*\([^\n]*\)\s*$', source, re.M | re.I))
    if len(matches) != 1:
        raise ValueError('expected exactly one add_external_ph implementation')
    start = matches[0].start()
    ending = re.search(r'^\s*end subroutine\b[^\n]*', source[matches[0].end():], re.M | re.I)
    if ending is None:
        raise ValueError('missing add_external_ph ending')
    end = matches[0].end() + ending.end()
    return start, end, source[start:end]


def apply(tree: Path) -> dict:
    tree = Path(tree).resolve()
    if tuple(tree.parts[-5:-1]) != ('night1', 'C0', 'repair_v2', 'trees') or tree.name not in ('baseline', 'candidate'):
        raise ValueError('wq repair is authorized only for owned night1/C0/repair_v2/trees baseline/candidate')
    src = tree / 'pert-src'
    path = src / 'diagMC_JJ_updates.f90'
    manifest = src / 'c0_wq_refresh.json'
    if path.is_symlink():
        raise ValueError('refusing source symlink')
    before = path.read_text()
    if manifest.exists():
        result = json.loads(manifest.read_text())
        if hashlib.sha256(before.encode()).hexdigest() != result['source_sha256_after']:
            raise ValueError('wq-repaired source changed since manifest; do not reapply blindly')
        return result
    if (src / 'c0_instrumentation.json').exists():
        raise ValueError('apply physical refresh before observational instrumentation')
    start, end, body = external_body(before)
    if 'C0-WQ-REFRESH' in body or re.search(r'call\s+cal_wq_int\s*\(', body, re.I):
        raise ValueError('external frequency call already exists without this manifest; audit instead of double insertion')
    sampler = list(re.finditer(r'^\s*call sample_q_omp_int\(diagram%seed,vn1%i_q,vn1%Pq,vn1\); Pq = vn1%Pq[^\n]*\n', body, re.M))
    if len(sampler) != 1:
        raise ValueError('external sampler source anchor changed')
    at = sampler[0].end()
    new_body = body[:at] + MARKER + '\n' + CALL + '\n' + body[at:]
    after = before[:start] + new_body + before[end:]
    result = {
        'patch': 'external_wq_refresh_v1', 'tree': str(tree),
        'file': 'pert-src/diagMC_JJ_updates.f90',
        'source_sha256_before': hashlib.sha256(before.encode()).hexdigest(),
        'source_sha256_after': hashlib.sha256(after.encode()).hexdigest(),
        'inserted_lines': [MARKER, CALL], 'wq_refresh_present': True,
        'physics_change': 'correctness repair: refresh all Nph native eV frequencies after external q sample',
        'rng_change': False, 'units': 'cal_wq_int performs existing Ry-to-eV conversion exactly once',
        'validation': 'NOT_COMPUTED_NATIVE_REPAIR_RUN'
    }
    path.write_text(after)
    manifest.write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tree', type=Path)
    print(json.dumps(apply(parser.parse_args().tree), indent=2))
