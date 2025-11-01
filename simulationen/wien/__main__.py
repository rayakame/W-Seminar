import numpy as np
from simulationen.formeln import plancks_law, wiens_displacement_law_temperature
import matplotlib.pyplot as plt
from simulationen import ROOT_DIR


def main():
    wavelengths = np.linspace(1e-7, 100e-6, 20000)
    temperature_range = np.linspace(500, 5000, 5)

    # Plancksche Strahlung für mehrere Temperaturen (vektoriell)
    spectral_radiances = [plancks_law(wavelengths, T) for T in temperature_range]

    # Wiensche Verschiebungslinie
    radiances = plancks_law(wavelengths, wiens_displacement_law_temperature(wavelengths))

    fig, ax = plt.subplots()

    for i, s in enumerate(spectral_radiances):
        ax.loglog(wavelengths * 1e6, s, label=fr"$T={temperature_range[i]:.0f}\,\text{{K}}$")

    ax.plot(wavelengths * 1e6, radiances, 'k--', label=r"$E_{b\lambda}(T = b/\lambda)$")

    ax.set_xlabel(r'Wellenlänge [$\mu\text{m}$]', fontsize=12)
    ax.set_ylabel(r"Spektrale Ausstrahlung $E_{b\lambda}$ [$\text{W}\,\text{m}^{-2}\,\mu\text{m}^{-1}$]", fontsize=12)

    ax.set_ylim(1e2, 1e15)
    ax.set_xlim(1e-1, 1e2)
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(ROOT_DIR / "seminararbeit" / "assets" / "wien_plot.pdf", bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    main()
