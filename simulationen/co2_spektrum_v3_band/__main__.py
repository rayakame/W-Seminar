from __future__ import annotations

import numpy as np
from matplotlib import pyplot as plt

from simulationen import ROOT_DIR
from simulationen.utils import create_absorption_spectrum
from simulationen.utils import read_hitran_par

FILENAME = ROOT_DIR / "data" / "hitran_co2_2025-11-04.par"


WN_MIN_FILTER = 2300
WN_MAX_FILTER = 2390
V3_CENTER = 2349.16


def main() -> None:
    df = read_hitran_par(FILENAME)
    df_filtered = df[(df["wavenumber"] >= WN_MIN_FILTER) & (df["wavenumber"] <= WN_MAX_FILTER)].copy()

    wn_min = df_filtered["wavenumber"].min()
    wn_max = df_filtered["wavenumber"].max()

    gamma = 0.4
    points_per_linewidth = 20
    delta_wn = gamma / points_per_linewidth
    n_points = int((wn_max - wn_min) / delta_wn)

    wn_grid = np.linspace(wn_min, wn_max, n_points)

    absorbance, _ = create_absorption_spectrum(
        df_filtered["wavenumber"].values,
        df_filtered["intensity"].values,
        wn_grid,
        path_length=0.4,
        pressure=0.1,
        temperature=296,
        concentration=400e-6,
        gamma=gamma,
    )

    _, ax1 = plt.subplots(figsize=(14, 7))

    absorbance_percent = absorbance * 100

    ax1.axvspan(wn_grid.min(), V3_CENTER, alpha=0.15, color="orange", label="P-Zweig")
    ax1.axvspan(V3_CENTER, wn_grid.max(), alpha=0.15, color="green", label="R-Zweig")

    ax1.plot(wn_grid, absorbance_percent, color="darkblue", linewidth=1.5, label=r"$\mathrm{CO_2}$")
    ax1.fill_between(wn_grid, 0, absorbance_percent, color="darkblue", alpha=0.2)

    ax1.axvline(V3_CENTER, color="red", linestyle="--", linewidth=2, label=r"$\nu_3$-Bandzentrum")

    ax1.set_xlabel(r"Wellenzahl $\eta$ [$\mathrm{cm}^{-1}$]", fontsize=20)
    ax1.set_ylabel("Absorption [%]", fontsize=20)
    ax1.grid(True, alpha=0.3, linestyle="--")
    ax1.set_xlim(wn_grid.min(), wn_grid.max())
    ax1.set_ylim(0, 75)

    ax1.tick_params(axis="both", labelsize=18)
    ax1.legend(loc="upper left", fontsize=18)

    plt.tight_layout()
    plt.savefig(ROOT_DIR / "seminararbeit" / "assets" / "co2_absorption_v3_band.pdf", bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
