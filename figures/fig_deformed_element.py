"""
fig_deformed_element.py -- figure for the vertical force balance on the deformed membrane.

Free-body diagram of one membrane element (drawn as a curved rectangle, with its thickness
exaggerated, in the same style as fig_curvature.py). Side view of one half of the meridian;
the axis of symmetry is the dotted vertical line. The element lies between the labels
theta_0 and theta_0 + Delta theta_0. Each point moves vertically by eta (positive toward the
centre of the sphere). The forces on the element are the two pressures (normal to the deformed
membrane) and the tension on the two theta-edges (along the tangent of the deformed meridian,
at the tilt angle psi to the horizontal). Forces are summed along the vertical: the grid
lines are the horizontal and vertical directions in which the forces are split, as the grid
of fig_curvature.py shows the tangent and normal directions there.

The deformed shape is ILLUSTRATIVE (a smooth eta that is zero at the rim), not a solution
of the model.

Output: plots/fig_deformed_element.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

PLOTS = Path(__file__).resolve().parents[1] / "plots"

plt.rcParams.update({"font.size": 11, "mathtext.fontset": "cm"})
BOX = dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85)
C_MEM, C_REF, C_CONT, C_P, C_SIG, C_ETA = "#1f6fb4", "0.35", "#c0392b", "#2e86c1", "#7d3c98", "#1e8449"

# ---------------- geometry (lengths in units of R)
R = 1.0
tm = 0.05                                      # membrane thickness (exaggerated)
th_c = np.deg2rad(75)                          # rim
th1, th2 = np.deg2rad(34), np.deg2rad(58)      # the element: theta_0 and theta_0 + Delta theta_0
A = 0.28                                       # size of the illustrative displacement


def eta_zero(th):
    return 0.0 * np.asarray(th, float)


def eta_def(th):
    """illustrative vertical displacement: largest at the pole, zero at the rim"""
    return A * (1 - (np.asarray(th, float) / th_c) ** 2)


def point(th, eta):
    """position in the picture: x = distance from the axis, z = height (centre at z = 0)"""
    return np.array([R * np.sin(th), -(R * np.cos(th) - eta(th))])


def tangent(th, eta, h=1e-6):
    """unit tangent of the meridian, in the direction of increasing theta_0"""
    d = (point(th + h, eta) - point(th - h, eta)) / (2 * h)
    return d / np.hypot(*d)


def normal_out(th, eta):
    """unit normal, away from the centre"""
    t = tangent(th, eta)
    return np.array([t[1], -t[0]])


def tilt(th, eta):
    t = tangent(th, eta)
    return np.arctan2(t[1], t[0])


def arrow(ax, p0, p1, color, lw=1.6, ls="-", ms=12, z=4):
    ax.annotate("", xy=p1, xytext=p0, zorder=z,
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=color, mutation_scale=ms,
                                linestyle=ls, shrinkA=0, shrinkB=0))


def slab(ax, lo, hi, eta, **kw):
    """Curved rectangle along the meridian between the labels lo and hi."""
    a = np.linspace(lo, hi, 80)
    inner = np.array([point(t, eta) - 0.5 * tm * normal_out(t, eta) for t in a])
    outer = np.array([point(t, eta) + 0.5 * tm * normal_out(t, eta) for t in a[::-1]])
    poly = np.vstack([inner, outer])
    ax.fill(poly[:, 0], poly[:, 1], **kw)


fig, ax = plt.subplots(figsize=(7.6, 5.9))
eta = eta_def
tmid = (th1 + th2) / 2
XL, YL = (-0.5, 1.42), (-1.3, 0.22)

# background grid: horizontal and vertical, the directions in which the forces are split
for x in np.arange(-0.5, 1.43, 0.125):
    ax.plot([x, x], YL, color="0.9", lw=0.6, zorder=0)
for y in np.arange(-1.25, 0.23, 0.125):
    ax.plot(XL, [y, y], color="0.9", lw=0.6, zorder=0)
o = np.array([-0.46, -1.26])                    # frame in the corner
arrow(ax, o, o + np.array([0.2, 0.0]), "0.4", lw=1.1, ms=9)
arrow(ax, o, o + np.array([0.0, 0.2]), "0.4", lw=1.1, ms=9)
ax.text(o[0] + 0.23, o[1], "horizontal", color="0.4", va="center", fontsize=9, bbox=BOX)
ax.text(o[0] - 0.01, o[1] + 0.24, "vertical\n(sum forces along it)", color="0.4", ha="left",
        va="bottom", fontsize=9, bbox=BOX)

# centre, axis, radii to the REST positions (theta_0 is a label of the rest position)
ax.plot(0, 0, "o", color="k", ms=5, zorder=5)
ax.text(0.05, 0.02, "centre of the\nreference sphere", fontsize=10, va="bottom", color="0.1", bbox=BOX)
ax.plot([0, 0], [0, -R], ls=":", color="k", lw=1.1)
for t in (th1, th2):
    p = point(t, eta_zero)
    ax.plot([0, p[0]], [0, p[1]], ls=":", color="k", lw=1.0)
arc = np.linspace(0, th1, 40)
ax.plot(0.30 * np.sin(arc), -0.30 * np.cos(arc), color="k", lw=1.1)
ax.text(0.23 * np.sin(th1 / 2) - 0.01, -0.23 * np.cos(th1 / 2), r"$\theta_0$", fontsize=13,
        ha="center", va="center")
arc = np.linspace(th1, th2, 40)
ax.plot(0.43 * np.sin(arc), -0.43 * np.cos(arc), color="k", lw=1.1)
ax.text(0.34 * np.sin(tmid), -0.34 * np.cos(tmid), r"$\Delta\theta_0$", fontsize=11,
        ha="center", va="center")

# reference sphere (dashed) and the rest position of the element (grey)
ths = np.linspace(0, th_c, 300)
ref = np.array([point(t, eta_zero) for t in ths])
ax.plot(ref[:, 0], ref[:, 1], ls="--", color=C_REF, lw=1.3)
slab(ax, th1, th2, eta_zero, color=C_REF, alpha=0.22, lw=0)
ax.annotate("reference sphere\n(radius $R$)", xy=point(np.deg2rad(16), eta_zero), xytext=(0.36, -1.16),
            fontsize=10, color=C_REF, va="center", bbox=BOX,
            arrowprops=dict(arrowstyle="-", lw=0.8, color=C_REF))

# the deformed membrane: the element (solid) and its continuation (faint)
slab(ax, 0.0, th1, eta, color=C_MEM, alpha=0.22, lw=0)
slab(ax, th2, th_c, eta, color=C_MEM, alpha=0.22, lw=0)
slab(ax, th1, th2, eta, facecolor="#cfe0f1", edgecolor=C_MEM, lw=1.6, zorder=3)
ax.text(-0.04, float(point(0.0, eta)[1]), "deformed\nmembrane", fontsize=10, color=C_MEM,
        ha="right", va="center", bbox=BOX)

# vertical displacement of the two ends
for t in (th1, th2):
    arrow(ax, point(t, eta_zero), point(t, eta), C_ETA, lw=1.6, ms=11)
p0 = point(th1, eta_zero)
ax.text(p0[0] - 0.035, p0[1] + 0.07, r"$\eta(\theta_0)$", color=C_ETA, fontsize=11,
        ha="right", va="center", bbox=BOX)
p0 = point(th2, eta_zero)
ax.text(p0[0] + 0.045, p0[1] - 0.03, r"$\eta(\theta_0+\Delta\theta_0)$", color=C_ETA, fontsize=11,
        ha="left", va="center", bbox=BOX)

# pressures: inside pushes the inner face out, outside pushes the outer face in
Lp = 0.17
fracs = (0.20, 0.45, 0.70)
for f in fracs:
    t = th1 + f * (th2 - th1)
    p, n = point(t, eta), normal_out(t, eta)
    arrow(ax, p - (0.5 * tm + Lp) * n, p - (0.5 * tm + 0.01) * n, C_P, lw=1.3, ms=10)
    arrow(ax, p + (0.5 * tm + Lp) * n, p + (0.5 * tm + 0.01) * n, C_CONT, lw=1.3, ms=10)
t = th1 + fracs[0] * (th2 - th1)
ax.text(*(point(t, eta) - (0.5 * tm + Lp + 0.02) * normal_out(t, eta) + np.array([-0.02, 0.0])),
        "inside, $P_i$", color=C_P, fontsize=11, ha="right", va="bottom", bbox=BOX)
t = th1 + fracs[1] * (th2 - th1)
ax.text(*(point(t, eta) + (0.5 * tm + Lp + 0.07) * normal_out(t, eta)), "outside, $P_o$", color=C_CONT,
        fontsize=11, ha="center", va="center", bbox=BOX)

# tension on the two theta-edges, with its vertical part
Ls = 0.34
for t, sgn in ((th2, 1), (th1, -1)):
    p, tg, ps = point(t, eta), tangent(t, eta), tilt(t, eta)
    tip = p + sgn * Ls * tg
    arrow(ax, p, tip, C_SIG, lw=2.2, ms=14, z=5)
    ax.text(*(tip + sgn * 0.05 * tg), r"$\sigma$", color=C_SIG, fontsize=14, ha="center", va="center")
    # horizontal reference line and the tilt angle (kept small: it is not the subject of the figure)
    ax.plot([p[0], p[0] + sgn * 0.36], [p[1], p[1]], ls="--", color=C_REF, lw=1.0)
    a = np.linspace(0, ps, 30)
    if sgn == 1:
        # outer edge: vertical part drawn from the edge point
        vert = p + np.array([0.0, Ls * np.sin(ps)])
        arrow(ax, p, vert, C_SIG, lw=1.4, ls="--", ms=10, z=5)
        ax.plot([tip[0], vert[0]], [tip[1], vert[1]], ls=":", color=C_SIG, lw=0.9)
        ax.plot(p[0] + 0.17 * np.cos(a), p[1] + 0.17 * np.sin(a), color=C_SIG, lw=0.9)
        ax.text(p[0] + 0.19, p[1] + 0.05, r"$\psi(\theta_0+\Delta\theta_0)$", color=C_SIG, fontsize=10,
                ha="left", va="center", bbox=BOX)
        ax.text(vert[0] - 0.02, vert[1] + 0.035, r"vertical part $\sigma\sin\psi(\theta_0+\Delta\theta_0)$",
                color=C_SIG, fontsize=10.5, ha="center", va="bottom", bbox=BOX)
    else:
        # inner edge: vertical part drawn at the tip, so the reference line closes the triangle
        foot = np.array([tip[0], p[1]])
        arrow(ax, foot, tip, C_SIG, lw=1.4, ls="--", ms=10, z=5)
        ax.plot(p[0] - 0.14 * np.cos(a), p[1] - 0.14 * np.sin(a), color=C_SIG, lw=0.9)
        ax.text(p[0] - 0.15, p[1] + 0.02, r"$\psi(\theta_0)$", color=C_SIG, fontsize=10,
                ha="center", va="bottom", bbox=BOX)
        ax.text(tip[0] - 0.03, (p[1] + tip[1]) / 2 + 0.01, r"$\sigma\sin\psi(\theta_0)$", color=C_SIG,
                fontsize=10.5, ha="right", va="center", bbox=BOX)

ax.set_aspect("equal")
ax.set_xlim(*XL)
ax.set_ylim(*YL)
ax.axis("off")
fig.tight_layout()
PLOTS.mkdir(exist_ok=True)
fig.savefig(PLOTS / "fig_deformed_element.png", dpi=220, bbox_inches="tight")
