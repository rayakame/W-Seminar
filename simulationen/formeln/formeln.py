from scipy import constants
import numpy as np

def plancks_law(wavelength: float, temperature: float) -> float:
    """Planck's radiation law

    Returns spectral radiance in W/(m²·sr·m)
    """
    first = (2 * constants.h * (constants.c ** 2)) / (wavelength ** 5)
    second = 1 / (np.exp((constants.h * constants.c) / (wavelength * constants.k * temperature)) - 1)
    return first * second


def wien_max_wavelength(temperature: float) -> float:
    """Wien's displacement law

    Returns the peak wavelength of a body's radiation
    """
    b_wien = constants.value("Wien wavelength displacement law constant")
    return b_wien / temperature