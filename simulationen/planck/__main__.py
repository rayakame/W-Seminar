from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from simulationen import ROOT_DIR
from simulationen.formeln import plancks_law
from simulationen.formeln import wiens_displacement_law

TEMPERATURE_EARTH = 288.0
TEMPERATURE_SUN = 5772

TITLE_FONT_SIZE = 20
BIG_FONT_SIZE = 18
SMALL_FONT_SIZE = 15


def main() -> None:
    max_wavelength_sun = wiens_displacement_law(TEMPERATURE_SUN)
    max_wavelength_earth = wiens_displacement_law(TEMPERATURE_EARTH)

    wavelengths = np.linspace(1e-7, 100e-6, 20000)
    # anything under 1e-7 will just be shown as 0 because its to small and causes an overflow error.

    spectral_radiance_earth, spectral_radiance_sun = [0.0], [0.0]
    # we put 0.0 as the first value here so that in our data there will always be a point P(0 | 0)
    # without having an overflow error as described above
    for wavelength in wavelengths:
        spectral_radiance_sun.append(plancks_law(wavelength, TEMPERATURE_SUN))
        spectral_radiance_earth.append(plancks_law(wavelength, TEMPERATURE_EARTH))

    wavelengths = np.insert(wavelengths, 0, 0.0)
    # we put 0.0 as described above

    plt.figure(figsize=(14, 10))

    ax1 = plt.subplot2grid((2, 2), (0, 0))
    ax2 = plt.subplot2grid((2, 2), (0, 1))
    ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=2)

    ax1.plot(
        wavelengths * 1e6,
        spectral_radiance_sun,
        linewidth=2.0,
        color="tab:orange",
        label=f"Sonne ({TEMPERATURE_SUN} K)",
    )
    ax1.set_xlabel(r"Wellenlänge [$\mu\text{m}$]", fontsize=BIG_FONT_SIZE)
    ax1.set_ylabel(r"$E_{b\lambda}$ [$\text{W}\,\text{m}^{-2}\,\mu\text{m}^{-1}$]", fontsize=BIG_FONT_SIZE)
    ax1.set_title(f"Sonne ({TEMPERATURE_SUN} K)", fontsize=TITLE_FONT_SIZE)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 4)
    ax1.axvspan(0.4, 0.78, alpha=0.1, color="yellow", label="Sichtbares Licht")
    ax1.axvline(
        x=max_wavelength_sun * 1e6,
        color="orange",
        linestyle="--",
        alpha=0.5,
        label=f"Max Sonne: {max_wavelength_sun * 1e6:.2f} " + r"$\mu\text{m}$",
    )
    ax1.tick_params(axis="both", labelsize=SMALL_FONT_SIZE)
    ax1.legend(loc="upper right", fontsize=SMALL_FONT_SIZE)

    ax2.plot(
        wavelengths * 1e6,
        spectral_radiance_earth,
        linewidth=2.0,
        color="tab:blue",
        label=f"Erde ({TEMPERATURE_EARTH} K)",
    )
    ax2.set_xlabel(r"Wellenlänge [$\mu\text{m}$]", fontsize=BIG_FONT_SIZE)
    ax2.set_ylabel(r"$E_{b\lambda}$ [$\text{W}\,\text{m}^{-2}\,\mu\text{m}^{-1}$]", fontsize=BIG_FONT_SIZE)
    ax2.set_title(f"Erde ({TEMPERATURE_EARTH} K)", fontsize=TITLE_FONT_SIZE)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 40)
    ax2.axvspan(0.4, 0.78, alpha=0.1, color="yellow", label="Sichtbares Licht")
    ax2.axvline(
        x=max_wavelength_sun * 1e6,
        color="orange",
        linestyle="--",
        alpha=0.5,
        label=f"Max Sonne: {max_wavelength_sun * 1e6:.2f} " + r"$\mu\text{m}$",
    )
    ax2.axvline(
        x=max_wavelength_earth * 1e6,
        color="blue",
        linestyle="--",
        alpha=0.5,
        label=f"Max Erde: {max_wavelength_earth * 1e6:.2f} " + r"$\mu\text{m}$",
    )
    ax2.tick_params(axis="both", labelsize=SMALL_FONT_SIZE)
    ax2.legend(loc="upper right", fontsize=SMALL_FONT_SIZE)

    spectral_radiance_sun_norm = np.array(spectral_radiance_sun) / np.max(spectral_radiance_sun)
    spectral_radiance_earth_norm = np.array(spectral_radiance_earth) / np.max(spectral_radiance_earth)

    ax3.semilogx(
        wavelengths * 1e6,
        spectral_radiance_sun_norm,
        linewidth=2.0,
        color="tab:orange",
        label=f"Sonne ({TEMPERATURE_SUN} K) - normalisiert",
    )
    ax3.semilogx(
        wavelengths * 1e6,
        spectral_radiance_earth_norm,
        linewidth=2.0,
        color="tab:blue",
        label=f"Erde ({TEMPERATURE_EARTH} K) - normalisiert",
    )

    ax3.axvspan(0.4, 0.78, alpha=0.1, color="yellow", label="Sichtbares Licht")
    ax3.axvspan(0.78, 100, alpha=0.1, color="red", label="Infrarot")

    ax3.axvspan(4.2, 4.4, alpha=0.3, color="green", label=r"$\mathrm{CO_2}\text{-Absorption} (4.3 \mu\text{m})$")
    ax3.axvspan(14, 16, alpha=0.3, color="green", label=r"$\mathrm{CO_2}\text{-Absorption} (15 \mu\text{m})$")

    ax3.set_xlabel(r"Wellenlänge [$\mu\text{m}$]", fontsize=BIG_FONT_SIZE)
    ax3.set_ylabel("Normalisierte spektrale Ausstrahlung", fontsize=BIG_FONT_SIZE)
    ax3.set_title(r"Vergleich: Planck-Strahlung und $\mathrm{CO_2}$-Absorptionsbanden", fontsize=TITLE_FONT_SIZE)
    ax3.grid(True, alpha=0.3, which="both")
    ax3.set_xlim(0.1, 100)
    ax3.set_ylim(0, 1.1)
    ax3.tick_params(axis="both", labelsize=SMALL_FONT_SIZE)
    ax3.legend(loc="lower left", fontsize=SMALL_FONT_SIZE)

    ax3.annotate(
        "Maximum\nSonnenstrahlung",
        xy=(max_wavelength_sun * 1e6, 0.98),
        xytext=(1.2, 0.8),
        arrowprops={"arrowstyle": "->", "color": "orange", "alpha": 0.7},
        fontsize=10,
        color="orange",
    )
    ax3.annotate(
        "Maximum\nErdstrahlung",
        xy=(max_wavelength_earth * 1e6, 0.98),
        xytext=(3.5, 0.7),
        arrowprops={"arrowstyle": "->", "color": "blue", "alpha": 0.7},
        fontsize=10,
        color="blue",
    )

    plt.savefig(ROOT_DIR / "seminararbeit" / "assets" / "planck_plot.pdf", bbox_inches="tight")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
