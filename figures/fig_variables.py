"""
fig_variables.py -- set-up figure for the problem formulation.

Bubble gripper: rigid housing, constant internal pressure P_i, membrane with tension sigma,
pushed down onto a rigid object, which acts through an outside pressure P_o on the contact
region. Points are labelled by their reference angle theta_0 and move vertically by eta.

The deformed shape is ILLUSTRATIVE (it touches the object, is tangent at the contact edge
and does not penetrate it), not a solution of the model.

Output: plots/fig_variables.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

PLOTS = Path(__file__).resolve().parents[1] / "plots"

plt.rcParams.update({"font.size": 11, "mathtext.fontset": "cm"})

# ---------------- geometry (lengths in units of R; angle th is used only to build curves)
R = 1.0
th_c = np.deg2rad(75)            # where the membrane meets the housing
a, d, th_e = 1.5, 0.25, 0.40     # object radius, push depth past first touch, contact edge
D = R + a - d                    # gripper centre -> object centre


def S(th):
    """distance from gripper centre to object surface along direction th (th = 0 is straight down)"""
    disc = (D * np.cos(th))**2 - (D**2 - a**2)
    return D * np.cos(th) - np.sqrt(np.maximum(disc, 0.0))


h = 1e-6
eta_e = S(th_e) - R
deta_e = (S(th_e + h) - S(th_e - h)) / (2 * h)
Lc = th_c - th_e
c2 = (-eta_e - deta_e * Lc) / Lc**2


def eta_of(th):
    th = np.asarray(th, float)
    out = eta_e + deta_e * (th - th_e) + c2 * (th - th_e)**2
    return np.where(th <= th_e, S(np.minimum(th, th_e)) - R, out)


def xz(r, th):
    return r * np.sin(th), -r * np.cos(th)


th = np.linspace(-th_c, th_c, 600)
ath = np.abs(th)
xR, zR = xz(R, th)                       # reference shape
xA, zA = xz(R + eta_of(ath), th)         # actual shape

# ---------------- colours
BOX = dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85)
C_MEM, C_REF, C_CONT, C_P, C_SIG, C_ETA = "#1f6fb4", "0.35", "#c0392b", "#2e86c1", "#7d3c98", "#1e8449"

fig, ax = plt.subplots(figsize=(7.2, 7.2))

# rigid object (only the top shows)
phi = np.linspace(0, np.pi, 300)
ax.fill_between(a * np.cos(phi), -D + a * np.sin(phi), -2.2, color="0.88", ec="0.45", lw=1.2)
ax.text(0, -1.6, "rigid object", ha="center", fontsize=11, color="0.25")

# housing (rigid, holds the membrane at its rim)
xr, zr = xz(R, th_c)
hb = 0.38
ax.add_patch(plt.Rectangle((-xr - 0.08, zr), 2 * (xr + 0.08), hb, fc="0.55", ec="0.25", lw=1.2,
                           alpha=0.55))
ax.text(-0.5, zr + hb / 2, "rigid housing", ha="center", va="center", color="white", fontsize=11)

# pushing velocity
ax.annotate("", xy=(0, zr + hb + 0.05), xytext=(0, zr + hb + 0.45),
            arrowprops=dict(arrowstyle="-|>", lw=2.2, color="k", mutation_scale=18))
ax.text(0.08, zr + hb + 0.25, "gripper pushed down, $V(t)$", va="center", fontsize=11)

# membrane: reference and actual
ax.plot(xR, zR, ls="--", color=C_REF, lw=1.4)
ax.plot(xA, zA, color=C_MEM, lw=2.8)
m = ath <= th_e
ax.plot(xA[m], zA[m], color=C_CONT, lw=4.5, solid_capstyle="butt")

# internal pressure arrows (normal to membrane, pointing outward)
for t0 in np.deg2rad([-47, -32, 34, 50]):
    rr = R + float(eta_of(abs(t0)))
    x1, z1 = xz(rr - 0.03, t0)
    x0, z0 = xz(rr - 0.25, t0)
    ax.annotate("", xy=(x1, z1), xytext=(x0, z0),
                arrowprops=dict(arrowstyle="-|>", lw=1.3, color=C_P, mutation_scale=11))
ax.text(-0.08, -0.45, "internal pressure\n$P_i$ (constant)",
        ha="right", va="center", color=C_P, fontsize=12)

# contact pressure p (object pushing back on the membrane, along the contact region)
for x0 in np.linspace(-0.32, -0.08, 4):
    t0 = np.arcsin(x0 / (R + eta_e))
    rr = R + float(eta_of(abs(t0)))
    xa, za = xz(rr, t0)
    ax.annotate("", xy=(xa, za + 0.02), xytext=(xa, za - 0.17),
                arrowprops=dict(arrowstyle="-|>", lw=1.2, color=C_CONT, mutation_scale=10))
ax.annotate("outside pressure $P_o$\n(from the object, on the contact region)", xy=(-0.2, -0.95), xytext=(-1.8, -0.98),
            color=C_CONT, fontsize=10.5, va="center", bbox=BOX, arrowprops=dict(arrowstyle="-", lw=0.8, color=C_CONT))

# tension sigma on a small membrane element (tangent, both directions)
t_s = np.deg2rad(-63)
rr = R + float(eta_of(abs(t_s)))
xs, zs = xz(rr, t_s)
tx, tz = np.cos(t_s), np.sin(t_s)        # tangent direction of a circle at angle t_s
for sgn in (1, -1):
    ax.annotate("", xy=(xs + sgn * 0.28 * tx, zs + sgn * 0.28 * tz),
                xytext=(xs + sgn * 0.05 * tx, zs + sgn * 0.05 * tz),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=C_SIG, mutation_scale=12))
ax.plot(xs, zs, "o", color=C_SIG, ms=5)
ax.text(xs - 0.42, zs + 0.02, "tension $\\sigma$", color=C_SIG, fontsize=12, ha="right", va="center")

# eta: deviation between reference and actual shape
t_eta = np.deg2rad(15)
x0, z0 = xz(R, t_eta)                                    # point on the reference sphere
right = th >= 0
z1 = float(np.interp(x0, xA[right], zA[right]))          # same distance from the axis, on the membrane
x1 = x0                                                  # points move vertically
ax.annotate("", xy=(x1, z1), xytext=(x0, z0),
            arrowprops=dict(arrowstyle="<|-|>", lw=1.6, color=C_ETA, mutation_scale=10,
                            shrinkA=0, shrinkB=0))
ax.annotate("$\\eta$ (vertical\ndisplacement)", xy=((x0 + x1) / 2, (z0 + z1) / 2),
            xytext=(0.75, -1.25), color=C_ETA, fontsize=12, bbox=BOX,
            arrowprops=dict(arrowstyle="-", lw=0.8, color=C_ETA))

# centre of the reference sphere and the angle theta_0
C_TH = "k"
ax.plot(0, 0, "o", color=C_TH, ms=5, zorder=5)
ax.text(0.07, -0.02, "centre of the\nreference sphere", fontsize=10, va="center", color="0.1")
ax.plot([0, 0], [0, -R], ls=":", color=C_TH, lw=1.2, zorder=4)          # symmetry axis, theta_0 = 0
xe, ze = xz(R, t_eta)
ax.plot([0, xe], [0, ze], ls=":", color=C_TH, lw=1.2, zorder=4)        # line to the point at theta_0
arc = np.linspace(0, t_eta, 60)
ax.plot(*xz(0.72, arc), color=C_TH, lw=1.2)
ax.text(*xz(0.62, t_eta / 2), "$\\theta_0$", fontsize=14, ha="center", va="center")
ax.annotate("$\\theta_0 = 0$ (pole)", xy=(0, -0.98), xytext=(-0.62, -1.2), fontsize=10, bbox=BOX,
            arrowprops=dict(arrowstyle="-", lw=0.8))
ax.annotate("$\\theta_0 = \\theta_c$ (rim)", xy=(xr, zr), xytext=(1.25, -0.33), fontsize=10,
            arrowprops=dict(arrowstyle="-", lw=0.8))

# labels for the two shapes
xq, zq = xz(R, np.deg2rad(-34))
ax.annotate("reference sphere\n(radius $R$)", xy=(xq, zq), xytext=(-1.8, -1.45),
            fontsize=10.5, color=C_REF, bbox=BOX, arrowprops=dict(arrowstyle="-", lw=0.8, color=C_REF))
xq, zq = xz(R + float(eta_of(np.deg2rad(68))), np.deg2rad(68))
ax.annotate("deformed membrane", xy=(xq, zq), xytext=(1.2, -0.05),
            fontsize=11, color=C_MEM, arrowprops=dict(arrowstyle="-", lw=0.8, color=C_MEM))

# outside pressure
ax.text(-1.7, 0.55, "outside:  $P_{atm} = 0$", fontsize=12)

ax.set_aspect("equal")
ax.set_xlim(-1.85, 1.85)
ax.set_ylim(-1.75, zr + hb + 0.55)
ax.axis("off")
fig.tight_layout()
PLOTS.mkdir(exist_ok=True)
fig.savefig(PLOTS / "fig_variables.png", dpi=220, bbox_inches="tight")
