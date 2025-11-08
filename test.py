import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.proj3d import proj_transform

from simulationen import ROOT_DIR

# Parameters
periods = 3  # Anzahl der Schwingungsperioden
t = np.linspace(0, periods * 2 * np.pi, 500)
A = 1.0  # Amplitude der Biegeschwingung in Angström
omega = 1  # Kreisfrequenz (normiert)

# Helikale Trajektorie des C-Atoms
x = t  # Fortschreiten entlang der Molekülachse (könnte auch konstant sein)
y = A * np.cos(omega * t)  # Auslenkung in y-Richtung
z = A * np.sin(omega * t)  # Auslenkung in z-Richtung

# Plotting
fig, ax = plt.subplots(figsize=(18, 7),subplot_kw=dict(projection='3d'))


# Haupttrajektorie in kräftigem Rot
ax.plot(x, y, z, color='darkred', linewidth=2.5, label='Atombahn', zorder=10)


# Endpunkt markieren (blau)
ax.scatter(x[-1], y[-1], z[-1], color='red', s=100,
           label=r'C-Atom', zorder=15, linewidth=2)


ax.quiver(0, 0, 0,  # Startpunkt (x, y, z)
          max(x)+ 2, 0, 0,  # Richtungsvektor (dx, dy, dz)
          color='black',
          arrow_length_ratio=0.015,  # Größe der Pfeilspitze
          linewidth=2,
          alpha=0.7,
          label='Molekülachse')
ax.quiver(0, 0, -A*1.55,  # Startpunkt (x, y, z)
          0, 0, 2*A*1.55,  # Richtungsvektor (dx, dy, dz)
          color='green',
          arrow_length_ratio=0.07,  # Größe der Pfeilspitze
          linewidth=2,
          alpha=0.7,
          label=r'${\upsilon_2}^x$-Schwingung')
ax.quiver(0, A*1.55, 0,  # Startpunkt (x, y, z)
          0, -2*A*1.55, 0,  # Richtungsvektor (dx, dy, dz)
          color='blue',
          arrow_length_ratio=0.07,  # Größe der Pfeilspitze
          linewidth=2,
          alpha=0.7,
          label=r'${\upsilon_2}^y$-Schwingung')

# Projektionen auf die Ebenen (mit besserer Sichtbarkeit)
# xy-Ebene (Sicht von oben)
ax.plot(x, y, 0, color='blue', alpha=0.3, linewidth=1.5)

# xz-Ebene (Sicht von der Seite)
ax.plot(x, 0, z, color='green', alpha=0.3, linewidth=1.5)

# Kreisförmige Bahnen an verschiedenen Positionen zeigen
for x_pos in [0, max(x)/2, max(x)]:
    circle_theta = np.linspace(0, 2*np.pi, 50)
    circle_y = A * np.cos(circle_theta)
    circle_z = A * np.sin(circle_theta)
    circle_x = np.full_like(circle_y, x_pos)
    ax.plot(circle_x, circle_y, circle_z, color='gray',
            alpha=0.2, linewidth=1, linestyle=':')

# Achsenbeschriftungen

# Titel
#ax.set_title(r'$\upsilon_2$-Biegeschwingung: Rotation des C-Atoms um die Molekülachse',
#             fontsize=20, fontweight='bold', pad=20)

# Legende
ax.legend(loc='lower center',
          fontsize=18)

# Gleichmäßige Skalierung für alle Achsen
ax.set_box_aspect([3, 1, 1])  # x-Achse länger, da Fortschreiten

# Grid für bessere Orientierung
ax.grid(False)
ax.set_axis_off()

ax.view_init(elev=10, azim=-53, roll=0)

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

bbox = fig.bbox_inches.from_bounds(5, 0, 8, 5.5)

plt.savefig(ROOT_DIR / "seminararbeit" / "assets" / "co2_absorption_v2_schwingung.pdf",
            bbox_inches=bbox)
plt.show()