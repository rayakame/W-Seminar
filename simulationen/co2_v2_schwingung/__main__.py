from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from simulationen import ROOT_DIR

PERIODS = 3
A = 1.0
OMEGA = 1


def main() -> None:
    t = np.linspace(0, PERIODS * 2 * np.pi, 500)

    x = t
    y = A * np.cos(OMEGA * t)  # Auslenkung in y-Richtung
    z = A * np.sin(OMEGA * t)  # Auslenkung in z-Richtung

    # Plotting
    fig, ax = plt.subplots(figsize=(18, 7), subplot_kw={"projection": "3d"})

    # Haupttrajektorie in kräftigem Rot
    ax.plot(x, y, z, color="darkred", linewidth=2.5, label="Atombahn", zorder=10)

    # Endpunkt markieren (blau)
    ax.scatter(x[-1], y[-1], z[-1], color="red", s=100, label=r"C-Atom", zorder=15, linewidth=2)

    ax.quiver(0, 0, 0, max(x) + 2, 0, 0, color="black", arrow_length_ratio=0.015, linewidth=2, alpha=0.7, label="Zeit")
    ax.quiver(
        0,
        0,
        -A * 1.55,
        0,
        0,
        2 * A * 1.55,
        color="green",
        arrow_length_ratio=0.07,
        linewidth=2,
        alpha=0.7,
        label=r"${\upsilon_2}^x$-Schwingung",
    )
    ax.quiver(
        0,
        A * 1.55,
        0,
        0,
        -2 * A * 1.55,
        0,
        color="blue",
        arrow_length_ratio=0.07,
        linewidth=2,
        alpha=0.7,
        label=r"${\upsilon_2}^y$-Schwingung",
    )

    ax.plot(x, y, 0, color="blue", alpha=0.3, linewidth=1.5)

    ax.plot(x, 0, z, color="green", alpha=0.3, linewidth=1.5)

    for x_pos in [0, max(x) / 2, max(x)]:
        circle_theta = np.linspace(0, 2 * np.pi, 50)
        circle_y = A * np.cos(circle_theta)
        circle_z = A * np.sin(circle_theta)
        circle_x = np.full_like(circle_y, x_pos)
        ax.plot(circle_x, circle_y, circle_z, color="gray", alpha=0.2, linewidth=1, linestyle=":")

    ax.legend(loc="lower center", fontsize=14, bbox_to_anchor=(0.5, 0.2), ncol=3)

    ax.set_box_aspect([3, 1, 1])

    ax.grid(False)
    ax.set_axis_off()

    ax.view_init(elev=10, azim=-53, roll=0)

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    bbox = fig.bbox_inches.from_bounds(5, 1, 8, 4.5)

    plt.savefig(
        ROOT_DIR / "seminararbeit" / "assets" / "co2_absorption_v2_schwingung.pdf", bbox_inches=bbox, pad_inches=0
    )
    plt.show()


if __name__ == "__main__":
    main()
