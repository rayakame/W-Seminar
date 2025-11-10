import numpy as np
import pandas as pd


def read_hitran_par(filename: str) -> pd.DataFrame:
    """
    Liest HITRAN .par Format ein
    """
    data = []

    with open(filename, 'r') as f:
        for line in f:
            molecule_id = int(line[0:2])
            isotopologue = int(line[2:3])
            wavenumber = float(line[3:15])
            intensity = float(line[15:25])

            data.append({
                'molecule': molecule_id,
                'isotopologue': isotopologue,
                'wavenumber': wavenumber,
                'intensity': intensity
            })

    return pd.DataFrame(data)


def create_absorption_spectrum(wavenumbers, intensities, wn_grid,
                               path_length=1.0, concentration=400e-6, pressure=1.0, temperature=296, gamma=0.1):
    number_density = 2.69e19 * (pressure * 1.0) * (273.15 / temperature) * concentration

    optical_depth = np.zeros_like(wn_grid)

    gamma_L = gamma * pressure

    path_length_cm = path_length * 100

    for wn, intensity in zip(wavenumbers, intensities):
        lorentz = (gamma_L / np.pi) / ((wn_grid - wn) ** 2 + gamma_L ** 2)
        alpha = intensity * number_density * lorentz
        optical_depth += alpha * path_length_cm



    transmission = np.exp(-optical_depth)

    absorbance = 1 - transmission

    return absorbance, optical_depth


def calculate_total_emissivity(wn_grid, absorbance, temperature=288.0):
    """
    Berechnet die totale Emissivität durch Integration über das Planck-Spektrum
    """
    from scipy import constants

    c1 = 2 * constants.pi * constants.h * constants.c ** 2
    c2 = constants.h * constants.c / constants.k 

    wavelength = 1e-2 / wn_grid

    planck = c1 / (wavelength ** 5 * (np.exp(c2 / (wavelength * temperature)) - 1))

    planck_wn = planck * (1e-2 / wn_grid ** 2)

    numerator = np.trapz(absorbance * planck_wn, wn_grid)
    denominator = constants.sigma * temperature**4

    epsilon = numerator / denominator

    return epsilon
