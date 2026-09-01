"""Atomic Future-B C0 addition resolvent.

This module deliberately keeps the physical objects used by the calculation
small and explicit.  A :class:`GreenState` is not interchangeable with a
``SigmaOperator``; both carry the grid signature on which they were created.
The SCBA block is the project weighted-shift, fixed-``D0`` ansatz.  It is not
an exact identity or a claim about an infinite coupling/domain limit.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, expm1, isfinite
from typing import Any, Iterable, Mapping

import numpy as np


CRITERION_VERSION = "future-b-c0-atomic-addition-resolvent-v2"
DEFAULT_N_NU = 128
DEFAULT_NU_MIN = 0.1
DEFAULT_NU_MAX = 20.0
DEFAULT_MIXING = 0.5
DEFAULT_TOLERANCE = 1.0e-12


def _readonly(array: np.ndarray, dtype: Any | None = None) -> np.ndarray:
    """Return a private, immutable NumPy array."""
    result = np.array(array, dtype=dtype, copy=True)
    result.setflags(write=False)
    return result


def _as_float(value: Any, name: str) -> float:
    if isinstance(value, (bool, np.bool_)):
        raise ValueError(f"{name} must be a finite scalar")
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a finite scalar") from exc
    if not isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _strict_int(value: Any, name: str, *, minimum: int | None = None) -> int:
    if isinstance(value, (bool, np.bool_)):
        raise ValueError(f"{name} must be an integer")
    try:
        result = int(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if isinstance(value, (float, np.floating)) and (not np.isfinite(value) or float(value) != result):
        raise ValueError(f"{name} must be an integer")
    if minimum is not None and result < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return result


@dataclass(frozen=True, slots=True)
class AtomicModel:
    """Frozen parameters for species-A, one-site vacuum addition."""

    g: float
    omega0: float
    temperature: float = 0.0
    epsilon0: float = 0.0
    t: float = 1.0
    n_sites: int = 1
    n_electrons_initial: int = 0
    n_electrons_final: int = 1
    thermal_m_max: int = 31

    def __post_init__(self) -> None:
        for name in ("g", "omega0", "temperature", "epsilon0", "t"):
            raw = getattr(self, name)
            if isinstance(raw, (bool, np.bool_)) or not isinstance(raw, (int, float, np.integer, np.floating)):
                raise ValueError(f"{name} must be a scalar number")
            value = _as_float(getattr(self, name), name)
            if name == "omega0" and value <= 0:
                raise ValueError("omega0 must be positive")
            if name == "temperature" and value < 0:
                raise ValueError("temperature must be non-negative")
            object.__setattr__(self, name, value)
        if self.g < 0:
            raise ValueError("g must be non-negative")
        if self.epsilon0 != 0.0 or self.t != 1.0:
            raise ValueError("frozen atomic scope requires epsilon0=0 and t=1")
        for name, minimum in (("n_sites", 1), ("n_electrons_initial", 0), ("n_electrons_final", 0), ("thermal_m_max", 0)):
            object.__setattr__(self, name, _strict_int(getattr(self, name), name, minimum=minimum))
        if self.n_sites != 1 or self.n_electrons_initial != 0 or self.n_electrons_final != 1:
            raise ValueError("only the one-site vacuum-addition model is supported")

    @classmethod
    def from_config(cls, config: Mapping[str, Any], g: float, omega0: float, temperature: float) -> "AtomicModel":
        """Construct a model using immutable project fields from a config."""
        return cls(
            g=_as_float(g, "g"),
            omega0=_as_float(omega0, "omega0"),
            temperature=_as_float(temperature, "temperature"),
            epsilon0=_as_float(config.get("epsilon0", 0.0), "epsilon0"),
            t=_as_float(config.get("t", 1.0), "t"),
            n_sites=_strict_int(config.get("N_sites", 1), "n_sites", minimum=1),
            n_electrons_initial=_strict_int(config.get("N_el_initial", 0), "n_electrons_initial", minimum=0),
            n_electrons_final=_strict_int(config.get("N_el_final", 1), "n_electrons_final", minimum=0),
            thermal_m_max=_strict_int(config.get("thermal_initial_m_max", 31), "thermal_m_max", minimum=0),
        )

    @property
    def signature(self) -> tuple[float, float, float, float]:
        return (self.g, self.omega0, self.temperature, self.epsilon0)

    @property
    def T(self) -> float:
        """Frozen-config spelling for temperature."""
        return self.temperature

    @property
    def omega(self) -> float:
        return self.omega0

    @property
    def species(self) -> str:
        return "A_vacuum_addition"

    @property
    def initial_ensemble(self) -> str:
        return "zero_electron_thermal_phonon_addition"

    @property
    def frequency_observable(self) -> str:
        return "analytic_upper_half_plane_resolvent"

    @property
    def not_grandcanonical_matsubara(self) -> bool:
        return True


def bose_occupation(omega0: float, temperature: float) -> float:
    """Return ``nB`` with the prescribed exact zero-temperature limit."""
    if any(isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, float, np.integer, np.floating)) for value in (omega0, temperature)):
        raise ValueError("omega0 and temperature must be scalar numbers")
    omega0 = _as_float(omega0, "omega0")
    temperature = _as_float(temperature, "temperature")
    if omega0 <= 0 or temperature < 0:
        raise ValueError("omega0 must be positive and temperature non-negative")
    if temperature == 0:
        return 0.0
    ratio = omega0 / temperature
    # Avoid overflow in expm1 for the exact Boltzmann tail at tiny T.
    if ratio > 700.0:
        return 0.0
    return float(1.0 / expm1(ratio))


n_bose = bose_occupation


@dataclass(frozen=True, slots=True, eq=False)
class ResolventGrid:
    """Analytic upper-half-plane samples and their finite shift lattice."""

    nu: np.ndarray
    z: np.ndarray
    shifts: np.ndarray
    omega0: float
    half_width: int

    def __post_init__(self) -> None:
        if not isinstance(self.half_width, (int, np.integer)) or isinstance(self.half_width, (bool, np.bool_)):
            raise ValueError("half_width must be an integer")
        if isinstance(self.omega0, (bool, np.bool_)) or not isinstance(self.omega0, (int, float, np.integer, np.floating)):
            raise ValueError("grid omega0 must be a scalar number")
        omega0 = _as_float(self.omega0, "omega0")
        if omega0 <= 0:
            raise ValueError("grid omega0 must be positive")
        nu = _readonly(self.nu, np.float64)
        z = _readonly(self.z, np.complex128)
        raw_shifts = np.asarray(self.shifts)
        if raw_shifts.ndim != 1 or not np.all(np.isfinite(raw_shifts)) or not np.all(raw_shifts == np.floor(raw_shifts)):
            raise ValueError("grid shifts must be finite integers")
        shifts = _readonly(raw_shifts, np.int64)
        if nu.ndim != 1 or z.ndim != 2 or z.shape != (shifts.size, nu.size):
            raise ValueError("grid arrays have inconsistent shapes")
        if np.any(~np.isfinite(nu)) or np.any(nu <= 0) or self.half_width < 0:
            raise ValueError("grid requires positive nu and non-negative half_width")
        if nu.size > 1 and not np.allclose(np.diff(np.log(nu)), np.diff(np.log(nu))[0], rtol=1e-12, atol=1e-15):
            raise ValueError("grid nu samples must be geometric")
        expected_shifts = np.arange(-int(self.half_width), int(self.half_width) + 1, dtype=np.int64)
        if not np.array_equal(shifts, expected_shifts):
            raise ValueError("grid shifts must be exactly -J..J")
        expected_z = shifts[:, None] * omega0 + 1j * nu[None, :]
        if np.any(~np.isfinite(z)) or not np.array_equal(z, expected_z):
            raise ValueError("grid z must equal i*nu+j*omega0")
        object.__setattr__(self, "omega0", omega0)
        object.__setattr__(self, "nu", nu)
        object.__setattr__(self, "z", z)
        object.__setattr__(self, "shifts", shifts)

    @property
    def n_nu(self) -> int:
        return int(self.nu.size)

    @property
    def signature(self) -> tuple[int, float, bytes, bytes, bytes]:
        return (self.half_width, self.omega0, self.nu.tobytes(), self.shifts.tobytes(), self.z.tobytes())

    @property
    def central_index(self) -> int:
        return self.half_width

    @property
    def central_z(self) -> np.ndarray:
        return self.z[self.central_index]

    @property
    def j(self) -> np.ndarray:
        """Alias exposing the integer shift index explicitly."""
        return self.shifts

    @property
    def metadata(self) -> dict[str, Any]:
        return {
            "species": "A_vacuum_addition",
            "observable": "analytic_upper_half_plane_resolvent",
            "not_grandcanonical_matsubara": True,
            "nu_min": float(self.nu[0]),
            "nu_max": float(self.nu[-1]),
            "nu_count": self.n_nu,
            "nu_spacing": "geometric",
            "half_width": self.half_width,
        }


def analytic_resolvent_grid(
    omega0: float,
    half_width: int,
    *,
    nu_min: float = DEFAULT_NU_MIN,
    nu_max: float = DEFAULT_NU_MAX,
    n_nu: int = DEFAULT_N_NU,
) -> ResolventGrid:
    """Build ``nu=geomspace(.1,20,128)``, ``z=i*nu+j*Omega`` samples."""
    if isinstance(omega0, (bool, np.bool_)) or not isinstance(omega0, (int, float, np.integer, np.floating)):
        raise ValueError("omega0 must be a scalar number")
    omega0 = _as_float(omega0, "omega0")
    half_width = _strict_int(half_width, "half_width", minimum=0)
    n_nu = _strict_int(n_nu, "n_nu", minimum=1)
    if any(isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, float, np.integer, np.floating)) for value in (nu_min, nu_max)):
        raise ValueError("nu bounds must be scalar numbers")
    nu_min = _as_float(nu_min, "nu_min")
    nu_max = _as_float(nu_max, "nu_max")
    if omega0 <= 0 or nu_min <= 0 or nu_max <= nu_min:
        raise ValueError("invalid grid parameters")
    nu = np.geomspace(nu_min, nu_max, n_nu)
    shifts = np.arange(-half_width, half_width + 1, dtype=np.int64)
    z = shifts[:, None] * omega0 + 1j * nu[None, :]
    return ResolventGrid(nu=nu, z=z, shifts=shifts, omega0=omega0, half_width=int(half_width))


# Short aliases used by callers and tests.
build_grid = analytic_resolvent_grid
make_grid = analytic_resolvent_grid


@dataclass(frozen=True, slots=True, eq=False)
class GreenState:
    """Typed dressed or bare Green-function state on one resolvent grid."""

    values: np.ndarray
    grid: ResolventGrid
    model_signature: tuple[float, float, float, float]
    iteration: int = 0

    def __post_init__(self) -> None:
        values = _readonly(self.values, np.complex128)
        if values.shape != self.grid.z.shape:
            raise ValueError("GreenState shape does not match its grid")
        if np.any(~np.isfinite(values)):
            raise ValueError("GreenState values must be finite")
        object.__setattr__(self, "values", values)

    @property
    def central(self) -> np.ndarray:
        return self.values[self.grid.central_index]


@dataclass(frozen=True, slots=True, eq=False)
class SigmaOperator:
    """Typed Born self-energy operator evaluated on a resolvent grid."""

    values: np.ndarray
    grid: ResolventGrid
    model_signature: tuple[float, float, float, float]

    def __post_init__(self) -> None:
        values = _readonly(self.values, np.complex128)
        if values.shape != self.grid.z.shape:
            raise ValueError("SigmaOperator shape does not match its grid")
        if np.any(~np.isfinite(values)):
            raise ValueError("SigmaOperator values must be finite")
        object.__setattr__(self, "values", values)

    @property
    def central(self) -> np.ndarray:
        return self.values[self.grid.central_index]


def bare_green(model: AtomicModel, grid: ResolventGrid) -> GreenState:
    _check_model_grid(model, grid)
    return GreenState(1.0 / grid.z, grid, model.signature)


def _check_model_grid(model: AtomicModel, grid: ResolventGrid) -> None:
    if not isinstance(grid, ResolventGrid):
        raise TypeError("grid must be a ResolventGrid")
    if not np.isclose(model.omega0, grid.omega0, rtol=0, atol=0):
        raise ValueError("model and grid omega0 mismatch")


def _check_state_grid(state: GreenState, model: AtomicModel, grid: ResolventGrid) -> None:
    if not isinstance(state, GreenState):
        raise TypeError("Born input must be a GreenState")
    _check_model_grid(model, grid)
    if state.grid.signature != grid.signature or state.model_signature != model.signature:
        raise ValueError("GreenState model/grid does not match requested Born operator")


def born_self_energy(state: GreenState, model: AtomicModel, grid: ResolventGrid | None = None) -> SigmaOperator:
    """Evaluate ``g²[(1+nB)G(z-Omega)+nB G(z+Omega)]``.

    At either finite-lattice boundary the shifted value is the fixed analytic
    outside-tail ``1/z``.  The returned object is deliberately a
    :class:`SigmaOperator`, never a ``GreenState``.
    """
    if not isinstance(state, GreenState):
        raise TypeError("Born input must be a GreenState")
    grid = state.grid if grid is None else grid
    _check_state_grid(state, model, grid)
    n_b = bose_occupation(model.omega0, model.temperature)
    shifted_minus = np.empty_like(state.values)
    shifted_plus = np.empty_like(state.values)
    shifted_minus[1:] = state.values[:-1]
    shifted_plus[:-1] = state.values[1:]
    shifted_minus[0] = 1.0 / (grid.z[0] - model.omega0)
    shifted_plus[-1] = 1.0 / (grid.z[-1] + model.omega0)
    sigma = model.g**2 * ((1.0 + n_b) * shifted_minus + n_b * shifted_plus)
    return SigmaOperator(sigma, grid, model.signature)


born_sigma = born_self_energy
evaluate_born_sigma = born_self_energy


def dyson_green(sigma: SigmaOperator, model: AtomicModel, grid: ResolventGrid | None = None) -> GreenState:
    """Apply ``G=1/(z-Sigma)`` while rejecting model/grid mismatches."""
    if not isinstance(sigma, SigmaOperator):
        raise TypeError("Dyson input must be a SigmaOperator")
    grid = sigma.grid if grid is None else grid
    _check_model_grid(model, grid)
    if sigma.grid.signature != grid.signature or sigma.model_signature != model.signature:
        raise ValueError("SigmaOperator model/grid mismatch in Dyson update")
    return GreenState(1.0 / (grid.z - sigma.values), grid, model.signature)


dyson_update = dyson_green


@dataclass(frozen=True, slots=True)
class SCBAResult:
    state: GreenState
    sigma: SigmaOperator
    iterations: int
    converged: bool
    update_norm: float
    closure_residual: float


def scba_solve(
    model: AtomicModel,
    grid: ResolventGrid,
    *,
    mixing: float = DEFAULT_MIXING,
    max_iterations: int = 10000,
    tolerance: float = DEFAULT_TOLERANCE,
) -> SCBAResult:
    """Solve fixed-``D0`` weighted-shift SCBA with damped Dyson updates."""
    _check_model_grid(model, grid)
    max_iterations = _strict_int(max_iterations, "max_iterations", minimum=1)
    if isinstance(mixing, (bool, np.bool_)) or not isinstance(mixing, (int, float, np.integer, np.floating)):
        raise ValueError("invalid SCBA iteration settings")
    if isinstance(tolerance, (bool, np.bool_)) or not isinstance(tolerance, (int, float, np.integer, np.floating)):
        raise ValueError("invalid SCBA iteration settings")
    mixing = _as_float(mixing, "mixing")
    tolerance = _as_float(tolerance, "tolerance")
    if not 0 < mixing <= 1 or tolerance <= 0:
        raise ValueError("invalid SCBA iteration settings")
    state = bare_green(model, grid)
    update_norm = float("inf")
    converged = False
    iterations = 0
    for iterations in range(1, max_iterations + 1):
        sigma = born_self_energy(state, model, grid)
        updated = dyson_green(sigma, model, grid)
        values = (1.0 - mixing) * state.values + mixing * updated.values
        update_norm = float(np.max(np.abs(values - state.values)))
        state = GreenState(values, grid, model.signature, iterations)
        # Re-evaluate Born on the NEW state before declaring convergence.
        new_sigma = born_self_energy(state, model, grid)
        new_residual = relative_closure_residual(state, new_sigma, model)
        if update_norm <= tolerance and new_residual <= tolerance:
            converged = True
            break
    sigma = born_self_energy(state, model, grid)
    dyson = dyson_green(sigma, model, grid)
    residual = relative_closure_residual(state, sigma, model)
    return SCBAResult(state, sigma, iterations, converged, update_norm, residual)


solve_scba = scba_solve


def relative_closure_residual(state: GreenState, sigma: SigmaOperator, model: AtomicModel) -> float:
    """Recomputed full-grid ``G-Dyson[Born(G)]`` infinity residual.

    ``sigma`` is accepted for API compatibility but must be a fresh operator
    on the same state/grid; the Born operator is always recomputed here so a
    stale self-energy can never be mistaken for a closure check.
    """
    if not isinstance(state, GreenState):
        raise TypeError("closure state must be a GreenState")
    if not isinstance(sigma, SigmaOperator):
        raise TypeError("closure self-energy must be a SigmaOperator")
    if state.grid.signature != sigma.grid.signature or state.model_signature != sigma.model_signature:
        raise ValueError("state and SigmaOperator grid/model mismatch")
    fresh_sigma = born_self_energy(state, model, state.grid)
    if not np.array_equal(fresh_sigma.values, sigma.values):
        raise ValueError("stale SigmaOperator supplied for closure residual")
    dyson = dyson_green(fresh_sigma, model, state.grid)
    numerator = float(np.max(np.abs(state.values - dyson.values)))
    denominator = max(1.0, float(np.max(np.abs(state.values))))
    return numerator / denominator


def thermal_probabilities(model: AtomicModel) -> tuple[np.ndarray, float]:
    """Return ``p_m`` for ``m=0..m_max`` and its omitted thermal mass."""
    if model.temperature == 0:
        p = np.zeros(model.thermal_m_max + 1, dtype=np.float64)
        p[0] = 1.0
        return _readonly(p), 0.0
    q = exp(-model.omega0 / model.temperature)
    p = (1.0 - q) * q ** np.arange(model.thermal_m_max + 1, dtype=np.float64)
    missing = float(q ** (model.thermal_m_max + 1))
    return _readonly(p), missing


def _flatten_z(z: np.ndarray | Iterable[complex]) -> tuple[np.ndarray, tuple[int, ...]]:
    try:
        arr = np.asarray(z, dtype=np.complex128)
    except (TypeError, ValueError) as exc:
        raise ValueError("z must be a finite complex sample array") from exc
    if np.any(~np.isfinite(arr)) or np.any(np.imag(arr) <= 0.0):
        raise ValueError("z must lie strictly in the finite upper half-plane")
    return arr.reshape(-1), arr.shape


def ed_green(model: AtomicModel, z: np.ndarray | Iterable[complex], cutoff: int) -> tuple[np.ndarray, float]:
    """Independent truncated final-sector ED thermal addition resolvent."""
    cutoff = _strict_int(cutoff, "cutoff", minimum=1)
    zz, shape = _flatten_z(z)
    n = np.arange(cutoff, dtype=np.float64)
    h = np.diag(model.omega0 * n)
    if cutoff > 1:
        hop = model.g * np.sqrt(np.arange(1, cutoff, dtype=np.float64))
        h += np.diag(hop, 1) + np.diag(hop, -1)
    energies, vectors = np.linalg.eigh(h)
    probabilities, missing = thermal_probabilities(model)
    result = np.zeros(zz.size, dtype=np.complex128)
    for m, probability in enumerate(probabilities):
        if probability == 0.0:
            continue
        if m >= cutoff:
            raise ValueError("ED cutoff is smaller than a nonzero thermal initial state")
        weights = np.abs(vectors[m, :]) ** 2
        denominators = zz[:, None] + m * model.omega0 - energies[None, :]
        result += probability * np.sum(weights[None, :] / denominators, axis=1)
    return result.reshape(shape), missing


ed_reference = ed_green


def poisson_pmf(mean: float, cutoff: int) -> np.ndarray:
    cutoff = _strict_int(cutoff, "cutoff", minimum=1)
    if mean < 0 or not isfinite(mean):
        raise ValueError("invalid Poisson parameters")
    pmf = np.empty(cutoff, dtype=np.float64)
    pmf[0] = exp(-mean)
    for n in range(1, cutoff):
        pmf[n] = pmf[n - 1] * mean / n
    return _readonly(pmf)


def lf_green(model: AtomicModel, z: np.ndarray | Iterable[complex], count_cutoff: int) -> tuple[np.ndarray, float]:
    """Independent thermal Lang--Firsov (Poisson-difference) resolvent."""
    count_cutoff = _strict_int(count_cutoff, "count_cutoff", minimum=1)
    zz, shape = _flatten_z(z)
    n_b = bose_occupation(model.omega0, model.temperature)
    s = (model.g / model.omega0) ** 2
    plus = poisson_pmf(s * (1.0 + n_b), count_cutoff)
    minus = poisson_pmf(s * n_b, count_cutoff)
    difference_weights = np.convolve(plus, minus[::-1])
    l_values = np.arange(-(count_cutoff - 1), count_cutoff, dtype=np.float64)
    poles = l_values * model.omega0 - model.g**2 / model.omega0
    result = np.sum(
        difference_weights[None, :] / (zz[:, None] - poles[None, :]),
        axis=1,
    )
    missing = float(max(0.0, 1.0 - float(np.sum(plus) * np.sum(minus))))
    return result.reshape(shape), missing


lf_reference = lf_green


def scba_constant_cfe(z: np.ndarray | Iterable[complex], g: float, omega0: float, depth: int) -> np.ndarray:
    """T=0 fixed-D0 constant-coefficient continued fraction (finite depth)."""
    depth = _strict_int(depth, "depth", minimum=0)
    if g < 0 or omega0 <= 0:
        raise ValueError("invalid CFE parameters")
    zz, shape = _flatten_z(z)
    # The lower shift boundary is z-(depth+1)*Omega because Born uses
    # G(z-Omega) at T=0.
    result = 1.0 / (zz - (depth + 1) * omega0)
    for j in range(depth, -1, -1):
        result = 1.0 / (zz - j * omega0 - g**2 * result)
    return result.reshape(shape)


def exact_t0_linear_cfe(z: np.ndarray | Iterable[complex], g: float, omega0: float, depth: int) -> np.ndarray:
    """T=0 ``n*g²`` continued fraction, retained as an independent negative control."""
    depth = _strict_int(depth, "depth", minimum=0)
    if g < 0 or omega0 <= 0:
        raise ValueError("invalid CFE parameters")
    zz, shape = _flatten_z(z)
    result = 1.0 / (zz - (depth + 1) * omega0)
    for j in range(depth, -1, -1):
        result = 1.0 / (zz - j * omega0 - (j + 1) * g**2 * result)
    return result.reshape(shape)


def exact_moments(model: AtomicModel) -> dict[str, float]:
    """Analytic LF moments through fourth order."""
    n_b = bose_occupation(model.omega0, model.temperature)
    c = model.g**2 * (2.0 * n_b + 1.0)
    return {"M0": 1.0, "M1": 0.0, "M2": c, "M3": model.g**2 * model.omega0, "M4": c * model.omega0**2 + 3.0 * c**2}


def scba_moments(model: AtomicModel) -> dict[str, float]:
    """Analytic fixed-D0 SCBA negative-control moments through fourth order."""
    moments = exact_moments(model)
    c = moments["M2"]
    result = dict(moments)
    result["M4"] = c * model.omega0**2 + 2.0 * c**2
    return result


def moment_negative_control(model: AtomicModel) -> dict[str, float]:
    exact = exact_moments(model)
    scba = scba_moments(model)
    return {"exact_M4": exact["M4"], "scba_M4": scba["M4"], "M4_gap": exact["M4"] - scba["M4"]}


def relative_l2(a: np.ndarray, b: np.ndarray, *, denominator: np.ndarray | None = None) -> float:
    """Relative L2 difference, optionally using a common reference norm."""
    a_grid = a.grid if isinstance(a, GreenState) else None
    b_grid = b.grid if isinstance(b, GreenState) else None
    if a_grid is not None and b_grid is not None and a_grid.signature != b_grid.signature:
        raise ValueError("relative_l2 states must use the same resolvent grid")
    aa = np.asarray(a.values if isinstance(a, GreenState) else a, dtype=np.complex128)
    bb = np.asarray(b.values if isinstance(b, GreenState) else b, dtype=np.complex128)
    if aa.shape != bb.shape:
        raise ValueError("relative_l2 operands must have identical sample shape")
    if isinstance(denominator, GreenState):
        if a_grid is not None and denominator.grid.signature != a_grid.signature:
            raise ValueError("relative_l2 denominator state uses a different resolvent grid")
        norm_source = np.asarray(denominator.values, dtype=np.complex128)
    else:
        norm_source = bb if denominator is None else np.asarray(denominator, dtype=np.complex128)
    if norm_source.shape != aa.shape:
        raise ValueError("relative_l2 denominator must match sample shape")
    norm = float(np.linalg.norm(norm_source.ravel()))
    if norm == 0:
        raise ValueError("relative_l2 denominator has zero norm")
    return float(np.linalg.norm((aa - bb).ravel()) / norm)


__all__ = [
    "AtomicModel", "ResolventGrid", "GreenState", "SigmaOperator", "SCBAResult",
    "analytic_resolvent_grid", "build_grid", "make_grid", "bose_occupation", "n_bose",
    "bare_green", "born_self_energy", "born_sigma", "evaluate_born_sigma", "dyson_green", "dyson_update", "scba_solve", "solve_scba",
    "relative_closure_residual", "thermal_probabilities", "ed_green", "poisson_pmf",
    "ed_reference", "lf_green", "lf_reference", "scba_constant_cfe", "exact_t0_linear_cfe", "exact_moments",
    "scba_moments", "moment_negative_control", "relative_l2", "CRITERION_VERSION",
]
