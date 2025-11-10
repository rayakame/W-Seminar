import numpy as np
from matplotlib import pyplot as plt

from simulationen import ROOT_DIR
from simulationen.utils import read_hitran_par, create_absorption_spectrum

FILENAME = ROOT_DIR / "data" / "hitran_co2_2025-11-04.par"


V3_CENTER = 2349.16
V2_CENTER = 667.38

df = read_hitran_par(FILENAME)

#wn_min_filter = 1
#wn_max_filter = 1000000
#
#df_filtered = df[(df['wavenumber'] >= wn_min_filter) &
#                 (df['wavenumber'] <= wn_max_filter)].copy()

wn_min = df['wavenumber'].min()
wn_max = df['wavenumber'].max()

gamma = 0.1
points_per_linewidth = 0.12
delta_wn = gamma / points_per_linewidth
n_points = int((wn_max - wn_min) / delta_wn)

print(n_points)
wn_grid = np.linspace(wn_min, wn_max, n_points)

absorbance, optical_depth = create_absorption_spectrum(
    df_filtered['wavenumber'].values,
    df_filtered['intensity'].values,
    wn_grid,
    path_length=100.0,
    pressure=1.0,
    temperature=296,
    concentration=400e-6,
    gamma=gamma
)

wl_grid = 10000.0 / wn_grid
V2_CENTER = 10000.0 / V2_CENTER
V3_CENTER = 10000.0 / V3_CENTER



fig, ax1 = plt.subplots(figsize=(14, 7))


ax1.plot(wl_grid, absorbance * 100, color='darkblue', linewidth=1.2, label=r"$\mathrm{CO_2}$")
ax1.set_xlabel(r'Wellenlänge [$\mu\text{m}$]', fontsize=20)
ax1.set_ylabel('Absorption [%]', fontsize=20)
#ax1.set_title('CO2 Absorptionsspektrum',fontsize=14)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_ylim(0, 100)
ax1.set_xlim(wl_grid.min(),wl_grid.max())


ax1.fill_between(wl_grid, 0, absorbance * 100, color='darkblue', alpha=0.2)

ax1.axvline(V3_CENTER, color='red', linestyle='--', linewidth=2.5,
            label=r'$\nu_3$-Bandzentrum')

ax1.axvline(V2_CENTER, color='orange', linestyle='--', linewidth=2.5,
            label=r'$\nu_2$-Bandzentrum')

ax1.tick_params(axis='both', labelsize=18)
ax1.legend(loc='upper center', fontsize=18)

plt.tight_layout()
plt.savefig(ROOT_DIR / "seminararbeit" / "assets" / "co2_absorption.pdf", bbox_inches='tight')

plt.show()