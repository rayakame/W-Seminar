import numpy as np
import matplotlib.pyplot as plt

from simulationen import ROOT_DIR
from simulationen.formeln import plancks_law, wiens_displacement_law



TEMPERATURE_EARTH = 288.0 # Kelvin
TEMPERATURE_SUN = 5772 # Kelvin

def main():

    max_wavelength_sun = wiens_displacement_law(TEMPERATURE_SUN)  # in Metern
    max_wavelength_earth = wiens_displacement_law(TEMPERATURE_EARTH)  # in Metern
    print(max_wavelength_sun, max_wavelength_earth)

    wavelengths = np.linspace(1e-7, 100e-6, 20000)
    # anything under 1e-7 will just be shown as 0 because its to small and causes an overflow error.

    spectral_radiance_earth, spectral_radiance_sun = [0.0], [0.0]
    # we put 0.0 as the first value here so that in our data there will always be a point P(0 | 0)
    # without having an overflow error as described above
    for wavelength in wavelengths:
        spectral_radiance_sun.append(plancks_law(wavelength, TEMPERATURE_SUN))
        spectral_radiance_earth.append(plancks_law( wavelength, TEMPERATURE_EARTH))

    wavelengths = np.insert(wavelengths, 0, 0.0)
    # we put 0.0 as the first value here so that in our data there will always be a point P(0 | 0)
    # without having an overflow error as described above


    fig = plt.figure(figsize=(14, 10))

    # Obere Plots (1 row, 2 columns für die oberen beiden)
    ax1 = plt.subplot2grid((2, 2), (0, 0))
    ax2 = plt.subplot2grid((2, 2), (0, 1))
    # Unterer Plot (nimmt die ganze Breite ein)
    ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=2)

    # Sonne
    ax1.plot(wavelengths * 1e6, spectral_radiance_sun, linewidth=2.0, color='tab:orange', label=f'Sonne ({TEMPERATURE_SUN} K)')
    ax1.set_xlabel(r'Wellenlänge [$\mu\text{m}$]', fontsize=12)
    ax1.set_ylabel(r"Spektrale Ausstrahlung $E_{b\lambda}$ [$\text{W}\,\text{m}^{-2}\,\mu\text{m}^{-1}$]", fontsize=12)
    ax1.set_title(f'Sonne ({TEMPERATURE_SUN} K)', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 4)  # Fokus auf sichtbaren Bereich
    #ax1.set_ylim(0, 2.6e13)
    ax1.axvspan(0.4, 0.78, alpha=0.1, color='yellow', label='Sichtbares Licht')
    ax1.axvline(x=max_wavelength_sun*1e6, color='orange', linestyle='--', alpha=0.5,
                label=f'Max Sonne: {max_wavelength_sun*1e6:.2f} μm')
    ax1.legend(loc='upper right')

    # Erde
    ax2.plot(wavelengths * 1e6, spectral_radiance_earth, linewidth=2.0, color='tab:blue', label=f'Erde ({TEMPERATURE_EARTH} K)')
    ax2.set_xlabel(r'Wellenlänge [$\mu\text{m}$]', fontsize=12)
    ax2.set_ylabel(r"Spektrale Ausstrahlung $E_{b\lambda}$ [$\text{W}\,\text{m}^{-2}\,\mu\text{m}^{-1}$]", fontsize=12)
    ax2.set_title(f'Erde ({TEMPERATURE_EARTH} K)', fontsize=14)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 40)  # Fokus auf Infrarot
    #ax2.set_ylim(0, 8.5e6)
    ax2.axvspan(0.4, 0.78, alpha=0.1, color='yellow', label='Sichtbares Licht')
    ax2.axvline(x=max_wavelength_sun*1e6, color='orange', linestyle='--', alpha=0.5,
                label=f'Max Sonne: {max_wavelength_sun*1e6:.2f} μm')
    ax2.axvline(x=max_wavelength_earth*1e6, color='blue', linestyle='--', alpha=0.5,
                label=f'Max Erde: {max_wavelength_earth*1e6:.2f} μm')
    ax2.legend(loc='upper right')


    # Kombinierter Plot mit CO2-Absorptionsbanden (unten)
    # Normalisierte Werte für bessere Vergleichbarkeit
    spectral_radiance_sun_norm = np.array(spectral_radiance_sun) / np.max(spectral_radiance_sun)
    spectral_radiance_earth_norm = np.array(spectral_radiance_earth) / np.max(spectral_radiance_earth)

    ax3.semilogx(wavelengths * 1e6, spectral_radiance_sun_norm,
                 linewidth=2.0, color='tab:orange', label=f'Sonne ({TEMPERATURE_SUN} K) - normalisiert')
    ax3.semilogx(wavelengths * 1e6, spectral_radiance_earth_norm,
                 linewidth=2.0, color='tab:blue', label=f'Erde ({TEMPERATURE_EARTH} K) - normalisiert')


    ax3.axvspan(0.4, 0.78, alpha=0.1, color='yellow', label='Sichtbares Licht')
    ax3.axvspan(0.78, 100, alpha=0.1, color='red', label='Infrarot')

    # CO2-Absorptionsbanden markieren
    ax3.axvspan(4.2, 4.4, alpha=0.3, color='green', label='CO₂-Absorption (4.3 μm)')
    ax3.axvspan(14, 16, alpha=0.3, color='green', label='CO₂-Absorption (15 μm)')


    ax3.set_xlabel(r'Wellenlänge [$\mu\text{m}$]', fontsize=12)
    ax3.set_ylabel('Normalisierte spektrale Ausstrahlung', fontsize=12)
    ax3.set_title('Vergleich: Planck-Strahlung und CO₂-Absorptionsbanden', fontsize=14)
    ax3.grid(True, alpha=0.3, which="both")
    ax3.set_xlim(0.1, 100)
    ax3.set_ylim(0, 1.1)
    ax3.legend(loc='upper right')

    # Annotations für wichtige Punkte
    ax3.annotate('Maximum\nSonnenstrahlung', xy=(max_wavelength_sun*1e6, 0.98), xytext=(1.2, 0.8),
                arrowprops=dict(arrowstyle='->', color='orange', alpha=0.7),
                fontsize=10, color='orange')
    ax3.annotate('Maximum\nErdstrahlung', xy=(max_wavelength_earth*1e6, 0.98), xytext=(3.5, 0.7),
                arrowprops=dict(arrowstyle='->', color='blue', alpha=0.7),
                fontsize=10, color='blue')


    plt.savefig(ROOT_DIR / "seminararbeit" / "assets" / "planck_plot.pdf", bbox_inches='tight')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()