# SIGNED FORMULA: H=2t*n-t*sum_PBC(c^dag c+h.c.)+Omega*b^dag*b+g*n*(b+b^dag), xi_k=2t*(1-cos k).
"""Minimal dense L=2 periodic Holstein ED with total-phonon cutoff M."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from functools import cached_property
from math import sqrt
from pathlib import Path
from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray


FloatArray = NDArray[np.float64]
ComplexArray = NDArray[np.complex128]
Configuration = tuple[int, int]
BasisState = tuple[int, Configuration]


def code_dispersion(k: ArrayLike, *, t: float = 1.0) -> FloatArray:
    """Frozen code-origin band: xi_k=2t(1-cos k)."""

    return np.asarray(2.0 * t * (1.0 - np.cos(np.asarray(k))), dtype=np.float64)


def periodic_l2_electronic_hamiltonian(*, t: float = 1.0) -> FloatArray:
    """L=2 PBC block with both directed links, hence eigenvalues 0 and 4t."""

    if not np.isfinite(t) or t < 0.0:
        raise ValueError("t must be finite and nonnegative")
    return np.asarray([[2.0 * t, -2.0 * t], [-2.0 * t, 2.0 * t]])


def phonon_configurations(total_cutoff: int) -> tuple[Configuration, ...]:
    if not isinstance(total_cutoff, int) or isinstance(total_cutoff, bool):
        raise ValueError("total_cutoff must be an integer")
    if total_cutoff < 0:
        raise ValueError("total_cutoff must be nonnegative")
    return tuple(
        (n0, n1)
        for n0 in range(total_cutoff + 1)
        for n1 in range(total_cutoff - n0 + 1)
    )


@dataclass(frozen=True)
class LehmannSpectrum:
    k: float
    eta: float
    omega: FloatArray
    green: ComplexArray
    spectral: FloatArray
    weights: FloatArray


@dataclass(frozen=True)
class CutoffRow:
    L: int
    t: float
    g: float
    omega0: float
    cutoff_kind: str
    M: int
    dimension: int
    E0: float
    delta_E0_vs_M_minus_2: float | None
    passes_1e_minus_4: bool


@dataclass(frozen=True)
class HolsteinL2ED:
    """One electron on two periodic sites times local phonon Fock states."""

    t: float
    g: float
    omega0: float
    total_cutoff: int

    def __post_init__(self) -> None:
        if not np.isfinite(self.t) or self.t < 0.0:
            raise ValueError("t must be finite and nonnegative")
        if not np.isfinite(self.g) or self.g < 0.0:
            raise ValueError("g must be finite and nonnegative")
        if not np.isfinite(self.omega0) or self.omega0 <= 0.0:
            raise ValueError("omega0 must be finite and positive")
        phonon_configurations(self.total_cutoff)

    @cached_property
    def configurations(self) -> tuple[Configuration, ...]:
        return phonon_configurations(self.total_cutoff)

    @cached_property
    def basis(self) -> tuple[BasisState, ...]:
        return tuple(
            (electron_site, configuration)
            for configuration in self.configurations
            for electron_site in (0, 1)
        )

    @cached_property
    def basis_index(self) -> dict[BasisState, int]:
        return {state: index for index, state in enumerate(self.basis)}

    @property
    def dimension(self) -> int:
        return (self.total_cutoff + 1) * (self.total_cutoff + 2)

    def index_of(self, electron_site: int, phonons: Configuration) -> int:
        try:
            return self.basis_index[(electron_site, phonons)]
        except KeyError as error:
            raise ValueError("state is outside the L=2 total-M basis") from error

    @cached_property
    def hamiltonian(self) -> FloatArray:
        """Full Hermitian +g*n*(b+b^dag) Hamiltonian; no Hartree shift."""

        matrix = np.zeros((self.dimension, self.dimension), dtype=np.float64)
        electronic = periodic_l2_electronic_hamiltonian(t=self.t)
        for column, (electron_site, phonons) in enumerate(self.basis):
            for target_site in (0, 1):
                row = self.basis_index[(target_site, phonons)]
                matrix[row, column] += electronic[target_site, electron_site]

            matrix[column, column] += self.omega0 * sum(phonons)

            if sum(phonons) < self.total_cutoff:
                raised = list(phonons)
                raised[electron_site] += 1
                row = self.basis_index[(electron_site, tuple(raised))]
                element = self.g * sqrt(phonons[electron_site] + 1)
                matrix[row, column] += element
                matrix[column, row] += element
        return matrix

    @cached_property
    def eigensystem(self) -> tuple[FloatArray, FloatArray]:
        values, vectors = np.linalg.eigh(self.hamiltonian)
        return values, vectors

    def ground_energy(self) -> float:
        return float(self.eigensystem[0][0])

    def lehmann_spectrum(
        self,
        *,
        k: float,
        omega: ArrayLike,
        eta: float = 0.05,
    ) -> LehmannSpectrum:
        frequencies = np.asarray(omega, dtype=np.float64)
        if frequencies.ndim != 1 or frequencies.size == 0:
            raise ValueError("omega must be a nonempty 1D grid")
        if not np.isfinite(eta) or eta <= 0.0:
            raise ValueError("eta must be positive")
        source = np.zeros(self.dimension, dtype=np.complex128)
        source[self.index_of(0, (0, 0))] = 1.0 / sqrt(2.0)
        source[self.index_of(1, (0, 0))] = np.exp(1j * k) / sqrt(2.0)
        eigenvalues, eigenvectors = self.eigensystem
        weights = np.asarray(np.abs(eigenvectors.conj().T @ source) ** 2)
        green = np.sum(
            weights[np.newaxis, :]
            / (frequencies[:, np.newaxis] + 1j * eta - eigenvalues[np.newaxis, :]),
            axis=1,
        )
        spectral = -2.0 * np.imag(green)
        return LehmannSpectrum(
            k=float(k),
            eta=float(eta),
            omega=frequencies,
            green=np.asarray(green, dtype=np.complex128),
            spectral=np.asarray(spectral, dtype=np.float64),
            weights=np.asarray(weights, dtype=np.float64),
        )


def cutoff_scan(
    *,
    t: float = 1.0,
    g: float = 1.05,
    omega0: float = 0.5,
    cutoffs: Iterable[int] = range(0, 21, 2),
    threshold: float = 1.0e-4,
) -> tuple[CutoffRow, ...]:
    rows: list[CutoffRow] = []
    previous: float | None = None
    for total_cutoff in cutoffs:
        model = HolsteinL2ED(t=t, g=g, omega0=omega0, total_cutoff=total_cutoff)
        energy = model.ground_energy()
        delta = None if previous is None else abs(energy - previous)
        rows.append(
            CutoffRow(
                L=2,
                t=t,
                g=g,
                omega0=omega0,
                cutoff_kind="total_phonon_M",
                M=total_cutoff,
                dimension=model.dimension,
                E0=energy,
                delta_E0_vs_M_minus_2=delta,
                passes_1e_minus_4=delta is not None and delta < threshold,
            )
        )
        previous = energy
    return tuple(rows)


def first_converged_cutoff(rows: Iterable[CutoffRow]) -> int | None:
    return next((row.M for row in rows if row.passes_1e_minus_4), None)


def write_cutoff_table(path: Path) -> tuple[CutoffRow, ...]:
    """Write the frozen strong-corner M=0,2,...,20 cutoff table."""

    rows = cutoff_scan()
    fieldnames = tuple(CutoffRow.__dataclass_fields__)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            payload = dict(row.__dict__)
            if row.delta_E0_vs_M_minus_2 is None:
                payload["delta_E0_vs_M_minus_2"] = ""
            writer.writerow(payload)
    return rows
