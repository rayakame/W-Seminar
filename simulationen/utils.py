from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd
from scipy import constants


def read_hitran_par(filename: str | pathlib.Path) -> pd.DataFrame:
    """
    Liest HITRAN .par Format ein
    """
    data = []

    if isinstance(filename, str):
        filename = pathlib.Path(filename)

    with filename.open() as f:
        for line in f:
            molecule_id = int(line[0:2])
            isotopologue = int(line[2:3])
            wavenumber = float(line[3:15])
            intensity = float(line[15:25])

            data.append(
                {
                    "molecule": molecule_id,
                    "isotopologue": isotopologue,
                    "wavenumber": wavenumber,
                    "intensity": intensity,
                }
            )

    return pd.DataFrame(data)


def create_absorption_spectrum(
    wavenumbers: np.ndarray,
    intensities: np.ndarray,
    wn_grid: np.ndarray,
    path_length: float = 1.0,
    concentration: float = 400e-6,
    pressure: float = 1.0,
    temperature: int = 296,
    gamma: float = 0.1,
) -> tuple[np.ndarray, np.ndarray]:
    number_density = 2.69e19 * (pressure * 1.0) * (273.15 / temperature) * concentration

    optical_depth = np.zeros_like(wn_grid)

    gamma_l = gamma * pressure

    path_length_cm = path_length * 100

    for wn, intensity in zip(wavenumbers, intensities, strict=True):
        lorentz = (gamma_l / np.pi) / ((wn_grid - wn) ** 2 + gamma_l**2)
        alpha = intensity * number_density * lorentz
        optical_depth += alpha * path_length_cm

    transmission = np.exp(-optical_depth)

    absorbance = 1 - transmission

    return absorbance, optical_depth


def calculate_total_emissivity(wn_grid: np.ndarray, absorbance: np.ndarray, temperature: float = 288.0) -> float:
    """
    Berechnet die totale Emissivität durch Integration über das Planck-Spektrum
    """

    c1 = 2 * constants.pi * constants.h * constants.c**2
    c2 = constants.h * constants.c / constants.k

    wavelength = 1e-2 / wn_grid

    planck = c1 / (wavelength**5 * (np.exp(c2 / (wavelength * temperature)) - 1))

    planck_wn = planck * (1e-2 / wn_grid**2)

    numerator = np.trapezoid(absorbance * planck_wn, wn_grid)
    denominator = constants.sigma * temperature**4

    return numerator / denominator
