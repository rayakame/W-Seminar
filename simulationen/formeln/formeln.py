from scipy import constants
import numpy as np

def plancks_law(wavelength: float, temperature: float, *, refractive_index: float = 1.0) -> float:
    """Planck's radiation law

    Returns spectral radiance in W/(m^3)
    """
    first = (2 * constants.pi * constants.h * (constants.c ** 2)) / ((refractive_index**2) * (wavelength ** 5))
    second = 1 / (np.exp((constants.h * constants.c) / (wavelength * constants.k * temperature)) - 1)
    return first * second


def wiens_displacement_law(temperature: float, *, refractive_index: float = 1.0) -> float:
    """Wien's displacement law

    Returns the peak wavelength of a body's radiation
    """
    b_wien = constants.value("Wien wavelength displacement law constant")
    return b_wien / temperature * refractive_index


def wiens_displacement_law_temperature(wavelength: float) -> float:
    """Wien's displacement law temperature
    Returns the peak temperature of a body's radiation
    """

    b_wien = constants.value("Wien wavelength displacement law constant")
    return b_wien / wavelength