"""
fig_two_curvatures.py -- the 3D version of the curvature argument.

(a) A small patch of membrane with sides l1 (direction 1) and l2 (direction 2), the normal n0
    at its centre, and the tension on its four edges: sigma*l2 on the two edges of length l2,
    sigma*l1 on the two edges of length l1.
(b) Side view of the patch along direction 1, drawn like the 1D figure: the grid is aligned
    with the tangent and normal at the centre, the membrane has turned by Delta theta_1 at
    each edge, and the tension there has a normal part sigma*l2*sin(Delta theta_1).
    Direction 2 looks the same, with 1 and 2 swapped.

Output: plots/fig_two_curvatures.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

PLOTS = Path(__file__).resolve().parents[1] / "plots"
plt.rcParams.update({"font.size": 11, "mathtext.fontset": "cm"})
BOX = dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.9)
C_MEM, C_REF, C_SIG, C_N, C_P, C_CONT = "#1f6fb4", "0.35", "#7d3c98", "0.1", "#2e86c1", "#c0392b"
C_1, C_2 = "#e07b00", "#1e8449"                  # direction 1 and direction 2
FILL = "#cfe0f1"

fig = plt.figure(figsize=(12, 4.6))
gs = fig.add_gridspec(1, 2, width_ratios=[0.85, 1.15], wspace=0.02)


def arrow(ax, start, vec, color, lw=1.6, ls="-", ms=12):
    ax.annotate("", xy=start + vec, xytext=start,
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=color, ls=ls, mutation_scale=ms,
                                shrinkA=0, shrinkB=0))


# ------------------------------------------------------------------ (a) the patch in 3D
ax = fig.add_subplot(gs[0, 0], projection="3d", computed_zorder=False)
k1, k2, a = 1.0, 0.45, 0.55                      # two curvatures (direction 2 flatter), half-size
surf = lambda x, y: 0.5 * (k1 * x ** 2 + k2 * y ** 2)
px, py = np.meshgrid(np.linspace(-a, a, 15), np.linspace(-a, a, 15))
ax.plot_surface(px, py, surf(px, py), color=FILL, alpha=0.9, lw=0, shade=False, zorder=1)
ax.plot_wireframe(px, py, surf(px, py), color="#a9c6e3", lw=0.4, zorder=2)
s = np.linspace(-a, a, 40)
for xx, yy in [(s, -a + 0 * s), (s, a + 0 * s), (-a + 0 * s, s), (a + 0 * s, s)]:
    ax.plot(xx, yy, surf(xx, yy), color=C_MEM, lw=1.5, zorder=3)
ax.plot(s, 0 * s, surf(s, 0 * s), color=C_1, lw=2.4, zorder=4)          # cut along direction 1
ax.plot(0 * s, s, surf(0 * s, s), color=C_2, lw=2.4, zorder=4)          # cut along direction 2
ax.scatter([0], [0], [0], color="k", s=10, zorder=5)
ax.quiver(0, 0, 0, 0, 0, 0.5, color=C_N, lw=1.8, arrow_length_ratio=0.15, zorder=6)
ax.text(0.04, 0.04, 0.54, "$\\vec n_0$", fontsize=13, color=C_N, zorder=7)
L = 0.36
for sx in (-1, 1):                               # edges of length l2 (x = +-a): sigma l2 along direction 1
    v = np.array([sx, 0, k1 * a]) / np.hypot(1, k1 * a)
    ax.quiver(sx * a, 0, surf(a, 0), *(L * v), color=C_SIG, lw=2.2, arrow_length_ratio=0.25, zorder=6)
for sy in (-1, 1):                               # edges of length l1 (y = +-a): sigma l1 along direction 2
    v = np.array([0, sy, k2 * a]) / np.hypot(1, k2 * a)
    ax.quiver(0, sy * a, surf(0, a), *(L * v), color=C_SIG, lw=2.2, arrow_length_ratio=0.25, zorder=6)
ax.text(a + 0.36, 0, surf(a, 0) + 0.2, "$\\sigma\\ell_2$", color=C_SIG, fontsize=13, zorder=7)
ax.text(0.05, -a - 0.42, surf(0, a) + 0.22, "$\\sigma\\ell_1$", color=C_SIG, fontsize=13, zorder=7)
# side lengths, written next to the edges they measure
ax.text(0.33, -a - 0.03, surf(0.33, a) - 0.1, "$\\ell_1$", color=C_MEM, fontsize=13, ha="center", zorder=7)
ax.text(a + 0.05, -0.33, surf(a, 0.33) - 0.08, "$\\ell_2$", color=C_MEM, fontsize=13, zorder=7)
ax.text(-a - 0.05, 0.05, surf(a, 0) + 0.06, "direction 1", color=C_1, fontsize=11, ha="right", zorder=7)
ax.text(0.08, a + 0.1, surf(0, a) + 0.05, "direction 2", color=C_2, fontsize=11, zorder=7)
ax.view_init(elev=24, azim=-52)
ax.set_xlim(-0.78, 0.78); ax.set_ylim(-0.78, 0.78); ax.set_zlim(0, 0.62)
ax.set_box_aspect((1, 1, 0.55), zoom=1.3)
ax.set_axis_off()


# ------------------------------------------------------------------ (b), (c) side views
def side_view(ax, half_angle_deg, col, i, other):
    """Cut through the centre along direction i, drawn like the 1D figure."""
    lh = 0.8                                     # half-length l_i / 2 (same in both panels)
    pe = np.deg2rad(half_angle_deg)              # Delta theta_i at the edge s_i = l_i / 2
    rc = lh / pe                                 # (only used to draw the arc)
    tm = 0.09                                    # thickness, exaggerated
    P = lambda ph, rr=rc: np.array([rr * np.sin(ph), rc - rr * np.cos(ph)])
    T = lambda ph: np.array([np.cos(ph), np.sin(ph)])
    N = lambda ph: np.array([-np.sin(ph), np.cos(ph)])
    XL, YL = (-1.75, 1.75), (-0.5, 0.9)
    # the cut through the patch (curved rectangle)
    ph = np.linspace(-pe, pe, 80)
    inner = np.array([P(p, rc - tm / 2) for p in ph]); outer = np.array([P(p, rc + tm / 2) for p in ph[::-1]])
    poly = np.vstack([inner, outer])
    ax.fill(poly[:, 0], poly[:, 1], facecolor=FILL, edgecolor=col, lw=1.8, zorder=3)
    # pressures, lightly, as in 1D
    for p in np.linspace(-0.45 * pe, 0.45 * pe, 4):
        arrow(ax, P(p, rc - tm / 2) + 0.26 * N(p), -0.24 * N(p), C_P, lw=1.1, ms=9)
        arrow(ax, P(p, rc + tm / 2) - 0.22 * N(p), 0.2 * N(p), C_CONT, lw=1.1, ms=9)
    # normal at the centre
    arrow(ax, np.array([0, tm / 2]), np.array([0, 0.62]), C_N, lw=1.8)
    ax.text(0.04, 0.6, "$\\vec n_0$", fontsize=13, color=C_N)
    ax.text(0, -0.43, "centre, $s_%d = 0$" % i, fontsize=10, ha="center", bbox=BOX)
    # tension at the two edges and its normal part
    LT = 0.45
    for sgn in (1, -1):
        E = P(sgn * pe)
        d = sgn * T(sgn * pe)                    # tension pulls away from the patch, along the membrane
        arrow(ax, E, LT * d, C_SIG, lw=2.2)
        comp = LT * np.sin(pe)                   # normal part (vertical in this frame)
        arrow(ax, E, np.array([0, comp]), C_SIG, lw=1.3, ls="--", ms=10)
        tip = E + LT * d
        ax.plot([tip[0], E[0]], [tip[1], tip[1]], ls=":", color=C_SIG, lw=0.8)
        ax.plot([E[0], E[0] + sgn * 0.42], [E[1], E[1]], ls="--", color=C_REF, lw=1)   # tangent at centre
        arc = np.linspace(0, pe, 30)
        ax.plot(E[0] + sgn * 0.3 * np.cos(arc), E[1] + 0.3 * np.sin(arc), color=col, lw=1)
        lab = ("$\\Delta\\theta_%d(\\ell_%d/2)$" % (i, i)) if sgn > 0 else ("$-\\Delta\\theta_%d(-\\ell_%d/2)$" % (i, i))
        ax.text(E[0] + sgn * 0.45, E[1], lab, fontsize=10, color=col,
                ha="left" if sgn > 0 else "right", va="center", bbox=BOX)
        ax.text(*(tip + np.array([0.04 * sgn, 0.02])), "$\\sigma\\ell_%d$" % other, color=C_SIG, fontsize=12,
                ha="left" if sgn > 0 else "right", va="bottom")
        ax.text(E[0] + 0.02 * sgn, E[1] - 0.2, "$s_%d = %s\\ell_%d/2$" % (i, "" if sgn > 0 else "-", i),
                fontsize=10, ha="center", va="top", bbox=BOX)
    ax.set_aspect("equal"); ax.set_xlim(*XL); ax.set_ylim(*YL); ax.axis("off")


ax = fig.add_subplot(gs[0, 1]); side_view(ax, 30, C_1, 1, 2)

# panel titles, placed at the same height
fig.text(0.29, 0.93, "(a) A small patch of membrane", ha="center", va="top", fontsize=11)
fig.text(0.68, 0.93, "(b) Side view along direction 1 (orange line);\ndirection 2 is the same, with 1 and 2 swapped",
         ha="center", va="top", fontsize=11)

PLOTS.mkdir(exist_ok=True)
fig.savefig(PLOTS / "fig_two_curvatures.png", dpi=200, bbox_inches="tight")
