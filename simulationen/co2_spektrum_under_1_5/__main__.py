from __future__ import annotations

import numpy as np
from matplotlib import pyplot as plt

from simulationen import ROOT_DIR
from simulationen.utils import create_absorption_spectrum
from simulationen.utils import read_hitran_par

FILENAME = ROOT_DIR / "data" / "hitran_co2_2025-11-04.par"


WN_MIN_FILTER = 6666
WN_MAX_FILTER = 1000000


def main() -> None:
    df = read_hitran_par(FILENAME)

    df_filtered = df[(df["wavenumber"] >= WN_MIN_FILTER) & (df["wavenumber"] <= WN_MAX_FILTER)].copy()

    wn_min = df_filtered["wavenumber"].min()
    wn_max = df_filtered["wavenumber"].max()
    wn_grid = np.linspace(wn_min, wn_max, 5000)

    absorbance, _ = create_absorption_spectrum(
        df_filtered["wavenumber"].values,
        df_filtered["intensity"].values,
        wn_grid,
        path_length=100.0,
        pressure=1.0,
        temperature=296,
        concentration=400e-6,
        gamma=0.1,
    )

    wl_grid = 10000.0 / wn_grid

    _, ax1 = plt.subplots(figsize=(14, 7))

    absorbance_percent = absorbance * 100

    ax1.plot(wl_grid, absorbance_percent, color="darkblue", linewidth=1.5, label=r"$\mathrm{CO_2}$")
    ax1.set_xlabel(r"Wellenlänge [$\mu\text{m}$]", fontsize=20)
    ax1.set_ylabel("Absorption [%]", fontsize=20)
    ax1.grid(True, alpha=0.3, linestyle="--")
    ax1.set_xlim(wl_grid.min(), wl_grid.max())

    ax1.fill_between(wl_grid, 0, absorbance_percent, color="darkblue", alpha=0.2)

    ax1.tick_params(axis="both", labelsize=18)
    ax1.legend(loc="upper left", fontsize=18)

    plt.tight_layout()
    plt.savefig(ROOT_DIR / "seminararbeit" / "assets" / "co2_absorption_under_1_5.pdf", bbox_inches="tight")

    plt.show()


if __name__ == "__main__":
    main()
