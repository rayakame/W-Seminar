from __future__ import annotations

import numpy as np
from matplotlib import pyplot as plt

from simulationen import ROOT_DIR
from simulationen.utils import create_absorption_spectrum
from simulationen.utils import read_hitran_par

FILENAME = ROOT_DIR / "data" / "hitran_co2_2025-11-04.par"

df = read_hitran_par(FILENAME)

BIG_FONT = 24
SMALL_FONT = 20
LINEWIDTH = 2
LINEWIDTH_BIG = 2.5

V2_CENTER = 667.38

WN_MIN_FILTER = 630
WN_MAX_FILTER = 710


def main() -> None:
    df_filtered = df[(df["wavenumber"] >= WN_MIN_FILTER) & (df["wavenumber"] <= WN_MAX_FILTER)].copy()

    wn_min = df_filtered["wavenumber"].min()
    wn_max = df_filtered["wavenumber"].max()

    gamma = 0.1
    points_per_linewidth = 20
    delta_wn = gamma / points_per_linewidth
    n_points = int((wn_max - wn_min) / delta_wn)

    wn_grid = np.linspace(wn_min, wn_max, n_points)

    absorbance, _ = create_absorption_spectrum(
        df_filtered["wavenumber"].values,
        df_filtered["intensity"].values,
        wn_grid,
        path_length=1.0,
        pressure=0.1,
        temperature=296,
        concentration=400e-6,
        gamma=gamma,
    )

    absorbance_percent = absorbance * 100
    _, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 15))

    ax1.axvspan(wn_grid.min(), V2_CENTER - 1.5, alpha=0.15, color="orange", label="P-Zweig")
    ax1.axvspan(V2_CENTER - 1.5, V2_CENTER + 2, alpha=0.15, color="yellow", label="Q-Zweig")
    ax1.axvspan(V2_CENTER + 2, wn_grid.max(), alpha=0.15, color="green", label="R-Zweig")

    ax1.plot(wn_grid, absorbance_percent, color="darkblue", linewidth=LINEWIDTH, label=r"$\mathrm{CO_2}$")
    ax1.fill_between(wn_grid, 0, absorbance_percent, color="darkblue", alpha=0.2)

    ax1.axvline(V2_CENTER, color="red", linestyle="--", linewidth=LINEWIDTH_BIG, label=r"$\nu_2$-Bandzentrum")

    ax1.set_xlabel(r"Wellenzahl $\eta$ [$\mathrm{cm}^{-1}$]", fontsize=BIG_FONT)
    ax1.set_ylabel("Absorption [%]", fontsize=BIG_FONT)
    ax1.set_title(r"CO$_2$ Biegeschwingung $\nu_2$ (15 $\mu$m Band)", fontsize=BIG_FONT)
    ax1.grid(True, alpha=0.3, linestyle="--")
    ax1.set_xlim(wn_grid.min(), wn_grid.max())
    ax1.set_ylim(0, max(absorbance_percent) * 1.1)
    ax1.tick_params(axis="both", labelsize=SMALL_FONT)
    ax1.legend(loc="upper left", fontsize=SMALL_FONT)

    q_zweig_min = V2_CENTER - 1
    q_zweig_max = V2_CENTER + 2

    q_mask = (wn_grid >= q_zweig_min) & (wn_grid <= q_zweig_max)

    ax2.axvspan(V2_CENTER - 5, V2_CENTER + 5, alpha=0.15, color="yellow")

    ax2.plot(
        wn_grid[q_mask], absorbance_percent[q_mask], color="darkblue", linewidth=LINEWIDTH, label=r"$\mathrm{CO_2}$"
    )

    ax2.fill_between(wn_grid[q_mask], 0, absorbance_percent[q_mask], color="darkblue", alpha=0.2)

    ax2.axvline(V2_CENTER, color="red", linestyle="--", linewidth=LINEWIDTH_BIG, label=r"$\nu_2$-Bandzentrum")

    ax2.set_xlabel(r"Wellenzahl $\eta$ [$\mathrm{cm}^{-1}$]", fontsize=BIG_FONT)
    ax2.set_ylabel("Absorption [%]", fontsize=BIG_FONT)
    ax2.set_title(r"CO$_2$ Biegeschwingung $\nu_2$ Q-Zweig Detailansicht", fontsize=BIG_FONT)
    ax2.grid(True, alpha=0.3, linestyle="--")
    ax2.set_xlim(q_zweig_min, q_zweig_max)
    ax2.set_ylim(0, max(absorbance_percent[q_mask]) * 1.1)
    ax2.tick_params(axis="both", labelsize=SMALL_FONT)
    ax2.legend(loc="upper right", fontsize=SMALL_FONT)

    ax2.annotate(
        "Überlagerung vieler\nRotationslinien\n(ΔJ = 0)",
        xy=(V2_CENTER, max(absorbance_percent[q_mask]) * 0.5),
        xytext=(V2_CENTER + 1.4, max(absorbance_percent[q_mask]) * 0.6),
        arrowprops={"arrowstyle": "->", "color": "black", "lw": 1.5},
        fontsize=SMALL_FONT,
        ha="center",
        bbox={"boxstyle": "round,pad=0.5", "facecolor": "white", "alpha": 0.8},
    )

    plt.tight_layout()
    plt.savefig(ROOT_DIR / "seminararbeit" / "assets" / "co2_absorption_v2_band.pdf", bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
