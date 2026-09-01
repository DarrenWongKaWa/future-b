# SIGNED FORMULA: xi_k=2t*(1-cos k), L=2 k in {0, pi}, tadpole OFF.
"""Same-origin periodic L=2 Born / SCBA ground-energy pole extractor.

E0 is the lowest real-frequency root of Re D(omega)=0 for G(k=0),
with frozen eta, window, and SCBA depth. See notes/L2_POLE_DEFINITION.md.

This module must not import chain_scba or crossing_block_poc.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


# Frozen locks. Do not retune after seeing the twelve-cell table.
T = 1.0
ETA = 1.0e-4
OMEGA_MIN = -8.0
OMEGA_MAX = 0.25
COARSE_N = 16501
SCBA_DEPTH = 64
BISECTION_ITERS = 80
RE_D_ZERO_TOL = 1.0e-14
K_POINTS = (0.0, float(np.pi))

NOT_COMPUTED = "NOT_COMPUTED"


def xi_k(k: NDArray[np.float64] | tuple[float, ...] | float, *, t: float = T) -> NDArray[np.float64]:
    """xi_k = 2t(1-cos k). L=2 lock: xi(0)=0, xi(pi)=4t."""

    values = np.asarray(2.0 * t * (1.0 - np.cos(np.asarray(k, dtype=np.float64))), dtype=np.float64)
    return values


def l2_dispersion(*, t: float = T) -> NDArray[np.float64]:
    xi = xi_k(np.asarray(K_POINTS, dtype=np.float64), t=t)
    if xi.shape != (2,):
        raise RuntimeError("L=2 extractor admits exactly two momenta")
    if abs(float(xi[0])) > 1.0e-15 or abs(float(xi[1]) - 4.0 * t) > 1.0e-15:
        raise RuntimeError("xi_0=0, xi_pi=4t lock failed")
    return xi


def _as_z(z: complex | NDArray[np.complex128]) -> NDArray[np.complex128]:
    array = np.asarray(z, dtype=np.complex128)
    return array


def rainbow_sigma(
    z: complex | NDArray[np.complex128],
    *,
    g: float,
    omega0: float,
    t: float = T,
    depth: int,
) -> NDArray[np.complex128]:
    """Local Holstein rainbow on periodic L=2.

    depth=0 is one-shot Born on G0.
    depth=SCBA_DEPTH is the frozen SCBA truncation.
    Tail: Sigma(z-(depth+1)*Omega)=0.
    """

    if depth < 0:
        raise ValueError("depth must be nonnegative")
    if not np.isfinite(g) or g < 0.0 or not np.isfinite(omega0) or omega0 <= 0.0:
        raise ValueError("invalid g or omega0")
    sample = _as_z(z)
    xi = l2_dispersion(t=t)
    coupling = (g * g) / 2.0
    sigma = np.zeros(sample.shape, dtype=np.complex128)
    for step in range(depth, -1, -1):
        z_emit = sample - (step + 1) * omega0
        green_sum = np.zeros(sample.shape, dtype=np.complex128)
        for band in xi:
            green_sum += 1.0 / (z_emit - band - sigma)
        sigma = coupling * green_sum
    return sigma


def born_sigma(z: complex | NDArray[np.complex128], *, g: float, omega0: float, t: float = T) -> NDArray[np.complex128]:
    return rainbow_sigma(z, g=g, omega0=omega0, t=t, depth=0)


def scba_sigma(
    z: complex | NDArray[np.complex128],
    *,
    g: float,
    omega0: float,
    t: float = T,
    depth: int = SCBA_DEPTH,
) -> NDArray[np.complex128]:
    return rainbow_sigma(z, g=g, omega0=omega0, t=t, depth=depth)


def denominator(
    omega: NDArray[np.float64] | float,
    *,
    g: float,
    omega0: float,
    depth: int,
    t: float = T,
    eta: float = ETA,
) -> NDArray[np.complex128]:
    """D(omega) = omega + i eta - Sigma(omega + i eta), xi_0=0."""

    sample = np.asarray(omega, dtype=np.float64)
    z = sample.astype(np.complex128) + 1.0j * eta
    return z - rainbow_sigma(z, g=g, omega0=omega0, t=t, depth=depth)


def _bisection_root(
    *,
    g: float,
    omega0: float,
    depth: int,
    left: float,
    right: float,
    f_left: float,
) -> float:
    a = float(left)
    b = float(right)
    fa = float(f_left)
    for _ in range(BISECTION_ITERS):
        mid = 0.5 * (a + b)
        fmid = float(np.real(denominator(mid, g=g, omega0=omega0, depth=depth)))
        if abs(fmid) <= RE_D_ZERO_TOL:
            return float(mid)
        if fa * fmid <= 0.0:
            b = mid
        else:
            a = mid
            fa = fmid
    return float(0.5 * (a + b))


def lowest_real_pole(
    *,
    g: float,
    omega0: float,
    depth: int,
    t: float = T,
    eta: float = ETA,
) -> tuple[float | None, float | None, int]:
    """Lowest interior Re D=0 root, or (None, None, n_crossings)."""

    omega = np.linspace(OMEGA_MIN, OMEGA_MAX, COARSE_N, dtype=np.float64)
    real_d = np.real(denominator(omega, g=g, omega0=omega0, depth=depth, t=t, eta=eta))
    n_crossings = 0
    root: float | None = None
    for index in range(COARSE_N - 1):
        left = float(real_d[index])
        right = float(real_d[index + 1])
        if not np.isfinite(left) or not np.isfinite(right):
            continue
        hit = False
        if abs(left) <= RE_D_ZERO_TOL:
            candidate = float(omega[index])
            hit = True
        elif left * right < 0.0:
            candidate = _bisection_root(
                g=g,
                omega0=omega0,
                depth=depth,
                left=float(omega[index]),
                right=float(omega[index + 1]),
                f_left=left,
            )
            hit = True
        if not hit:
            continue
        if candidate <= OMEGA_MIN or candidate >= OMEGA_MAX:
            continue
        n_crossings += 1
        if root is None:
            root = candidate
    if root is None:
        return None, None, n_crossings
    abs_d = float(np.abs(denominator(root, g=g, omega0=omega0, depth=depth, t=t, eta=eta)))
    return float(root), abs_d, n_crossings


@dataclass(frozen=True)
class PoleResult:
    kind: str
    g: float
    omega0: float
    depth: int
    E0: float | None
    abs_D: float | None
    n_crossings: int
    eta: float = ETA

    @property
    def csv_value(self) -> str:
        if self.E0 is None:
            return NOT_COMPUTED
        return repr(float(self.E0))


def e0_born(*, g: float, omega0: float, t: float = T) -> PoleResult:
    energy, abs_d, n_crossings = lowest_real_pole(g=g, omega0=omega0, depth=0, t=t)
    return PoleResult("born", float(g), float(omega0), 0, energy, abs_d, n_crossings)


def e0_scba(*, g: float, omega0: float, t: float = T, depth: int = SCBA_DEPTH) -> PoleResult:
    energy, abs_d, n_crossings = lowest_real_pole(g=g, omega0=omega0, depth=depth, t=t)
    return PoleResult("scba", float(g), float(omega0), int(depth), energy, abs_d, n_crossings)


def g0_poles(*, omega0: float = 0.8) -> tuple[PoleResult, PoleResult]:
    """g=0 sanity (not a CSV row): both poles must sit at 0."""

    return e0_born(g=0.0, omega0=omega0), e0_scba(g=0.0, omega0=omega0)
