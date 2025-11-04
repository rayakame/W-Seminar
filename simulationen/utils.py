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
                               path_length=100, concentration=400e-6):
    number_density = 2.69e19 * concentration

    optical_depth = np.zeros_like(wn_grid)

    gamma = 0.1

    for wn, intensity in zip(wavenumbers, intensities):
        lorentz = gamma / (np.pi * ((wn_grid - wn) ** 2 + gamma ** 2))
        optical_depth += intensity * number_density * path_length * 100 * lorentz

    absorbance = 1 - np.exp(-optical_depth)

    return absorbance
