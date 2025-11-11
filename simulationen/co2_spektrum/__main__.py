from __future__ import annotations

import numpy as np
from matplotlib import pyplot as plt

from simulationen import ROOT_DIR
from simulationen.utils import create_absorption_spectrum
from simulationen.utils import read_hitran_par

FILENAME = ROOT_DIR / "data" / "hitran_co2_2025-11-04.par"


V3_CENTER = 2349.16
V2_CENTER = 667.38

BIG_FONT_SIZE = 20
SMALL_FONT_SIZE = 18

WN_MIN_FILTER = 555
WN_MAX_FILTER = 100000


def main() -> None:
    df = read_hitran_par(FILENAME)

    df_filtered = df[(df["wavenumber"] >= WN_MIN_FILTER) & (df["wavenumber"] <= WN_MAX_FILTER)].copy()

    wn_min = df_filtered["wavenumber"].min()
    wn_max = df_filtered["wavenumber"].max()

    gamma = 0.1
    points_per_linewidth = 0.12
    delta_wn = gamma / points_per_linewidth
    n_points = int((wn_max - wn_min) / delta_wn)

    wn_grid = np.linspace(wn_min, wn_max, n_points)

    absorbance, _ = create_absorption_spectrum(
        df_filtered["wavenumber"].values,
        df_filtered["intensity"].values,
        wn_grid,
        path_length=100.0,
        pressure=1.0,
        temperature=296,
        concentration=400e-6,
        gamma=gamma,
    )

    wl_grid = 10000.0 / wn_grid
    v2_center = 10000.0 / V2_CENTER
    v3_center = 10000.0 / V3_CENTER

    _, ax1 = plt.subplots(figsize=(14, 7))

    ax1.plot(wl_grid, absorbance * 100, color="darkblue", linewidth=1.2, label=r"$\mathrm{CO_2}$")
    ax1.set_xlabel(r"Wellenlänge [$\mu\text{m}$]", fontsize=BIG_FONT_SIZE)
    ax1.set_ylabel("Absorption [%]", fontsize=BIG_FONT_SIZE)
    ax1.grid(True, alpha=0.3, linestyle="--")
    ax1.set_ylim(0, 100)
    ax1.set_xlim(wl_grid.min(), wl_grid.max())

    ax1.fill_between(wl_grid, 0, absorbance * 100, color="darkblue", alpha=0.2)

    ax1.axvline(v3_center, color="red", linestyle="--", linewidth=2.5, label=r"$\nu_3$-Bandzentrum")

    ax1.axvline(v2_center, color="orange", linestyle="--", linewidth=2.5, label=r"$\nu_2$-Bandzentrum")

    ax1.tick_params(axis="both", labelsize=SMALL_FONT_SIZE)
    ax1.legend(loc="upper center", fontsize=SMALL_FONT_SIZE)

    plt.tight_layout()
    plt.savefig(ROOT_DIR / "seminararbeit" / "assets" / "co2_absorption.pdf", bbox_inches="tight")

    plt.show()


if __name__ == "__main__":
    main()
