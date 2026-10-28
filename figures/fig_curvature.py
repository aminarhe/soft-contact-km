"""
fig_curvature.py -- figure for the "Pressure and curvature" section.

Free-body diagram of a small curved piece of membrane (drawn as a curved rectangle, with its
thickness exaggerated) used to show that the pressure difference equals tension times
curvature. Tension acts on the two end faces, the inside pressure P_i on the face towards the
centre of curvature, the outside pressure P_o on the other face. Forces are summed along the
normal at s = 0, so the picture is turned so that the tangent at s = 0 is horizontal: the grid
lines are then exactly the tangent and normal directions in which the forces are split.

Output: plots/fig_curvature.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

PLOTS = Path(__file__).resolve().parents[1] / "plots"
plt.rcParams.update({"font.size": 11, "mathtext.fontset": "cm"})
BOX = dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.9)
C_MEM, C_REF, C_CONT, C_P, C_SIG, C_N = "#1f6fb4", "0.35", "#c0392b", "#2e86c1", "#7d3c98", "0.1"

# Midline of the piece: arc of radius rc about the centre of curvature C = (0, 0).
# phi is the angle of the tangent with the horizontal: point = rc (sin phi, -cos phi).
rc = 2.0
tm = 0.16                                       # membrane thickness (exaggerated)
ph0, ph1 = 0.0, np.deg2rad(40)                  # tangent angle at s = 0 (horizontal) and s = L
dth = ph1 - ph0                                 # Delta theta(L), exaggerated for clarity


def pt(ph, rad=rc):
    return np.array([rad * np.sin(ph), -rad * np.cos(ph)])


def tan(ph):                                    # unit tangent, direction of increasing s
    return np.array([np.cos(ph), np.sin(ph)])


def nrm(ph):                                    # unit normal towards the centre of curvature
    return np.array([-np.sin(ph), np.cos(ph)])


def arrow(ax, start, vec, color, lw=1.6, ls="-", ms=12, z=4):
    ax.annotate("", xy=start + vec, xytext=start, zorder=z,
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=color, ls=ls, mutation_scale=ms,
                                shrinkA=0, shrinkB=0))


def slab(ax, lo, hi, **kw):
    """Curved rectangle between tangent angles lo and hi."""
    a = np.linspace(lo, hi, 80)
    inner = np.array([pt(x, rc - tm / 2) for x in a])
    outer = np.array([pt(x, rc + tm / 2) for x in a[::-1]])
    poly = np.vstack([inner, outer])
    ax.fill(poly[:, 0], poly[:, 1], **kw)


fig, ax = plt.subplots(figsize=(7.4, 6.2))
XL, YL = (-1.6, 2.75), (-2.65, 0.35)

# background grid, aligned with the tangent (horizontal) and normal (vertical) at s = 0
for x in np.arange(-1.5, 2.8, 0.25):
    ax.plot([x, x], YL, color="0.9", lw=0.6, zorder=0)
for y in np.arange(-2.5, 0.4, 0.25):
    ax.plot(XL, [y, y], color="0.9", lw=0.6, zorder=0)
o = np.array([-1.45, -2.5])                     # frame in the corner
arrow(ax, o, np.array([0.4, 0]), "0.4", lw=1.1, ms=9)
arrow(ax, o, np.array([0, 0.4]), "0.4", lw=1.1, ms=9)
ax.text(o[0] + 0.46, o[1], "tangent at $s = 0$", color="0.4", va="center", fontsize=9, bbox=BOX)
ax.text(o[0] - 0.02, o[1] + 0.48, "normal at $s = 0$", color="0.4", ha="left", fontsize=9, bbox=BOX)

# centre of curvature and radii to the two ends (radius = 1/kappa)
ax.plot(0, 0, "o", color=C_REF, ms=4)
ax.text(0.08, 0.07, "centre of curvature", fontsize=9.5, color=C_REF, ha="left", bbox=BOX)
for ph in (ph0, ph1):
    P = pt(ph, rc - tm / 2)
    ax.plot([0, P[0]], [0, P[1]], ls=":", color=C_REF, lw=1)
ax.text(-0.09, -0.55, "radius $1/\\kappa$", fontsize=10, color=C_REF, ha="center", va="center",
        rotation=90, bbox=BOX)

# the membrane: the piece (solid) and its continuation (faint)
slab(ax, np.deg2rad(-16), ph0, color=C_MEM, alpha=0.12, lw=0)
slab(ax, ph1, np.deg2rad(56), color=C_MEM, alpha=0.12, lw=0)
slab(ax, ph0, ph1, facecolor="#cfe0f1", edgecolor=C_MEM, lw=1.6, zorder=3)
A, B = pt(ph0), pt(ph1)                          # midpoints of the two end faces
ax.text(*(A + np.array([-0.05, -0.33])), "$s = 0$", fontsize=11, ha="center", bbox=BOX)
ax.text(*(B + np.array([0.2, -0.12])), "$s = L$", fontsize=11, ha="left", bbox=BOX)
mid = 0.5 * (ph0 + ph1)
ax.annotate("piece of length $L$", xy=pt(np.deg2rad(4), rc + tm / 2), xytext=(0.35, -2.58), fontsize=11,
            color=C_MEM, bbox=BOX, arrowprops=dict(arrowstyle="-", lw=0.8, color=C_MEM))

# pressures: inside pushes the inner face out, outside pushes the outer face in
for ph in np.deg2rad([8, 16, 24, 32]):
    arrow(ax, pt(ph, rc - tm / 2) + 0.36 * nrm(ph), -0.34 * nrm(ph), C_P, lw=1.3, ms=10)
for ph in np.deg2rad([10, 18, 26, 34]):
    arrow(ax, pt(ph, rc + tm / 2) - 0.28 * nrm(ph), 0.26 * nrm(ph), C_CONT, lw=1.3, ms=10)
ax.text(*(pt(np.deg2rad(20)) + 0.62 * nrm(np.deg2rad(20))), "inside, $P_i$", fontsize=11,
        color=C_P, ha="center", bbox=BOX)
ax.text(*(pt(np.deg2rad(40)) - 0.36 * nrm(np.deg2rad(40))), "outside, $P_o$", fontsize=11,
        color=C_CONT, ha="left", va="top", bbox=BOX)

# tilt of one pressure arrow away from the normal at s = 0: the angle Delta theta(s)
phs = np.deg2rad(26)
tail = pt(phs, rc + tm / 2) - 0.28 * nrm(phs)
ax.plot([tail[0], tail[0]], [tail[1], tail[1] + 0.3], ls=":", color=C_CONT, lw=1)
arc = np.linspace(np.pi / 2, np.pi / 2 + phs, 20)
ax.plot(tail[0] + 0.17 * np.cos(arc), tail[1] + 0.17 * np.sin(arc), color=C_CONT, lw=0.9)
ax.text(tail[0] + 0.06, tail[1] + 0.06, "$\\Delta\\theta(s)$", fontsize=10, color=C_CONT, va="bottom", ha="left")

# tension on the two end faces, along the membrane
LT = 0.62
arrow(ax, A, -LT * tan(ph0), C_SIG, lw=2.2, z=5)
ax.text(*(A - LT * tan(ph0) + np.array([-0.04, 0.0])), "$\\sigma$", color=C_SIG, fontsize=14,
        ha="right", va="center")
arrow(ax, B, LT * tan(ph1), C_SIG, lw=2.2, z=5)
ax.text(*(B + LT * tan(ph1) + np.array([0.05, 0.03])), "$\\sigma$", color=C_SIG, fontsize=14)

# normal at s = 0: the direction in which forces are summed
arrow(ax, A + 0.5 * tm * nrm(ph0), 0.75 * nrm(ph0), C_N, lw=1.8, z=5)
ax.annotate("normal at $s = 0$\n(sum forces along it)", xy=A + 0.6 * nrm(ph0), xytext=(-1.5, -1.25),
            fontsize=10, bbox=BOX, arrowprops=dict(arrowstyle="-", lw=0.8))

# at s = L: tangent at s = 0 (a grid line), the angle Delta theta(L), and the two parts of sigma
ax.plot([B[0], B[0] + 0.8], [B[1], B[1]], ls="--", color=C_REF, lw=1.1)
arc = np.linspace(ph0, ph1, 40)
ax.plot(B[0] + 0.33 * np.cos(arc), B[1] + 0.33 * np.sin(arc), color=C_SIG, lw=1)
ax.text(B[0] + 0.4 * np.cos(mid), B[1] + 0.4 * np.sin(mid) - 0.02, "$\\Delta\\theta(L)$",
        fontsize=11, color=C_SIG, ha="left", va="center", bbox=BOX)
tip = B + LT * tan(ph1)
comp_n, comp_t = LT * np.sin(dth), LT * np.cos(dth)
arrow(ax, B, np.array([0, comp_n]), C_SIG, lw=1.4, ls="--", ms=10, z=5)
ax.plot([tip[0], B[0]], [tip[1], tip[1]], ls=":", color=C_SIG, lw=0.9)
ax.plot([tip[0], tip[0]], [tip[1], B[1]], ls=":", color=C_SIG, lw=0.9)
ax.annotate("normal part $\\sigma \\sin\\Delta\\theta(L)$", xy=B + np.array([0, 0.6 * comp_n]),
            xytext=(1.2, -0.7), fontsize=10.5, color=C_SIG, bbox=BOX,
            arrowprops=dict(arrowstyle="-", lw=0.8, color=C_SIG))

# curvature definition
ax.text(-1.5, -1.75, "curvature  $\\kappa = \\dfrac{d\\,\\Delta\\theta}{ds}$", fontsize=12, ha="left", bbox=BOX)

ax.set_aspect("equal")
ax.set_xlim(*XL)
ax.set_ylim(*YL)
ax.axis("off")
fig.tight_layout()
PLOTS.mkdir(exist_ok=True)
fig.savefig(PLOTS / "fig_curvature.png", dpi=220, bbox_inches="tight")
