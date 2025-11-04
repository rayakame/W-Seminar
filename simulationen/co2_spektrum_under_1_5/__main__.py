import numpy as np
from matplotlib import pyplot as plt

from simulationen import ROOT_DIR
from simulationen.utils import read_hitran_par, create_absorption_spectrum

FILENAME = ROOT_DIR / "data" / "hitran_co2_2025-11-04.par"

df = read_hitran_par(FILENAME)

print(f"Geladene Linien: {len(df)}")
print(f"Wellenzahlbereich: {df['wavenumber'].min():.1f} - {df['wavenumber'].max():.1f}")
wn_min_filter = 6666
wn_max_filter = 1000000

df_filtered = df[(df['wavenumber'] >= wn_min_filter) &
                 (df['wavenumber'] <= wn_max_filter)].copy()

print(f"\nNach Filter: {len(df_filtered)} Linien")
print(f"Gefilterte Wellenzahl: {df_filtered['wavenumber'].min():.1f} - {df_filtered['wavenumber'].max():.1f}")
print(f"Entspricht Wellenlänge: {10000/df_filtered['wavenumber'].max():.2f} - {10000/df_filtered['wavenumber'].min():.2f} micrometer")

wn_min = df_filtered['wavenumber'].min()
wn_max = df_filtered['wavenumber'].max()
wn_grid = np.linspace(wn_min, wn_max, 5000)

absorbance = create_absorption_spectrum(
    df_filtered['wavenumber'].values,
    df_filtered['intensity'].values,
    wn_grid,
    path_length=100,
    concentration=400e-6
)

wl_grid = 10000.0 / wn_grid


fig, ax1 = plt.subplots(figsize=(14, 7))

absorbance_percent = absorbance * 100

ax1.plot(wl_grid, absorbance_percent, color='darkblue', linewidth=1.5, label=r"$\mathrm{CO_2}$")
ax1.set_xlabel(r'Wellenlänge [$\mu\text{m}$]', fontsize=12)
ax1.set_ylabel('Absorption [%]', fontsize=12)
ax1.set_title('CO2 Absorptionsspektrum',
              fontsize=20)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim(wl_grid.min(),wl_grid.max())
#\ax1.set_ylim(0.1)
#ax1.set_yscale('log')

ax1.fill_between(wl_grid, 0, absorbance_percent, color='darkblue', alpha=0.2)


ax1.legend(loc='upper right')

plt.tight_layout()
plt.savefig(ROOT_DIR / "seminararbeit" / "assets" / "co2_absorption_under_1_5.pdf", bbox_inches='tight')

plt.show()