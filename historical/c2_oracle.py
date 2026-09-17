"""Independent log P_kchange from dumped swap fields + LiF wq/ek tables."""
from __future__ import annotations
import math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CLIP = math.log(10.0)
LOGDPH = math.log(1e-15)
CUT = 1e-3
RYD2EV = 13.605698066
NGRID = 20


def ld(w, d):
    w = float(w)
    if (not math.isfinite(w)) or w < CUT:
        return LOGDPH
    return -w * abs(float(d))


def logp_from_row(row, ek_old, ek_new):
    tau12 = float(row['tauR']) - float(row['tauL'])
    ell = -(float(ek_new) - float(ek_old)) * tau12
    ell += ld(row['w1'], float(row['tauR']) - float(row['tpl'])) - ld(row['w1'], float(row['tauL']) - float(row['tpl']))
    ell += ld(row['w2'], float(row['tauL']) - float(row['tpr'])) - ld(row['w2'], float(row['tauR']) - float(row['tpr']))
    return float(np.clip(ell, -CLIP, CLIP))


def reverse_logp(row, ek_old, ek_new):
    """Occupancy reverse at fixed time order. Do not flip both dt and dE."""
    rev = dict(row)
    rev['w1'], rev['w2'] = row['w2'], row['w1']
    rev['tpl'], rev['tpr'] = row['tpr'], row['tpl']
    return logp_from_row(rev, ek_new, ek_old)


def grid_index(q):
    p = tuple(int(x) % NGRID for x in q)
    return p[0] * NGRID * NGRID + p[1] * NGRID + p[2]


def open_ek_table():
    path = ROOT / 'research/luo_energy_1pct/2026-09-11/runs/prep/htable/gkq-20/enk.dat'
    return np.memmap(path, dtype='<f8', mode='r', offset=4, shape=(4, NGRID**3), order='F')


def min_ek_eV(table, k):
    return float(table[0, grid_index(k)]) * RYD2EV


def load_dump(path):
    rows = []
    with Path(path).open() as handle:
        header = handle.readline().split()
        for line in handle:
            if not line.strip() or line.startswith('#'):
                continue
            tok = line.split()
            if len(tok) != len(header):
                continue
            rec = dict(zip(header, tok))
            for k in rec:
                if k in ('stage', 'attempt', 'iv1', 'iv2', 'kinx', 'kiny', 'kinz',
                         'qrx', 'qry', 'qrz', 'nu1', 'nu2', 'ng_delta', 'nenv_delta',
                         'order', 'nph_ext'):
                    rec[k] = int(float(rec[k]))
                else:
                    rec[k] = float(rec[k])
            rows.append(rec)
    return rows
