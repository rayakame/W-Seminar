import numpy as np

from simulationen import ROOT_DIR
from simulationen.formeln.formeln import effective_pressure
from simulationen.utils import read_hitran_par, create_absorption_spectrum, calculate_total_emissivity

FILENAME = ROOT_DIR / "data" / "hitran_co2_2025-11-04.par"

df = read_hitran_par(FILENAME)

wn_min = df['wavenumber'].min()
wn_max = df['wavenumber'].max()


gamma = 0.1
points_per_linewidth = 0.08
delta_wn = gamma / points_per_linewidth
n_points = int((wn_max - wn_min) / delta_wn)
wn_grid = np.linspace(wn_min, wn_max, n_points)

PATH_LENGTH = 8000
# Die Atmosphäre ist ca. 8km hoch, deswegen nehmen wir an das sich auf 8km eine konstante CO2-Konzentration ergibt.

CONCENTRATION = 425e-6
# 425 ppm wurden durch Messungen 2025 gezeigt
# https://gml.noaa.gov/ccgg/trends/

TEMPERATURE = 255
# Emissionstemperatur der Erde

TEMPERATURE_SURFACE = 288
# Oberflächentemperatur

absorbance, optical_depth = create_absorption_spectrum(
    df['wavenumber'], df['intensity'], wn_grid,
    path_length=8000,
    concentration=420e-6,
    pressure=effective_pressure(PATH_LENGTH),
    temperature=TEMPERATURE
)

epsilon = calculate_total_emissivity(wn_grid, absorbance, temperature=TEMPERATURE_SURFACE)
print(epsilon)
