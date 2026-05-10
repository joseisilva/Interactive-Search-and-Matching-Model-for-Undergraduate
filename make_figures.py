"""
Generate figures for the search-and-matching teaching paper.
Produces five PDFs in /home/claude/figures/:
  - fig_equilibrium.pdf       : WC/JC intersection diagram (the main figure)
  - fig_beveridge.pdf         : Beveridge curve with equilibrium dot
  - fig_productivity_shock.pdf: WC/JC shifts after a productivity shock
  - fig_ui_shock.pdf          : WC/JC shifts after higher unemployment benefits
  - fig_interface.pdf         : Mockup of the Colab interactive interface
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from scipy.optimize import brentq

os.makedirs("/home/claude/figures", exist_ok=True)

# ---------- Benchmark parameters (matches the Colab notebook) ----------
s0, c0, A0, b0, beta0, phi0, alpha0 = 0.035, 0.12, 1.0, 0.41, 0.879, 0.754, 0.5

def q(theta, phi, alpha):
    return phi * theta**(-(1 - alpha))

def p(theta, phi, alpha):
    return phi * theta**alpha

def wage_curve(theta, A, b, beta, c):
    return beta*A + beta*c*theta + (1-beta)*b

def job_creation(theta, A, c, s, phi, alpha):
    return A - c * (s / q(theta, phi, alpha))

def solve_eq(A, b, beta, c, s, phi, alpha):
    f = lambda t: wage_curve(t, A, b, beta, c) - job_creation(t, A, c, s, phi, alpha)
    th = brentq(f, 1e-4, 100)
    return th, wage_curve(th, A, b, beta, c)

def bev(theta, s, phi, alpha):
    pv = p(theta, phi, alpha)
    u = s / (s + pv)
    v = theta * u
    return u, v

# Style
plt.rcParams.update({
    "font.size": 12,
    "axes.labelsize": 13,
    "axes.titlesize": 14,
    "legend.fontsize": 11,
    "figure.dpi": 120,
    "savefig.bbox": "tight",
})

# ============================================================
# FIGURE 1: Labor-market equilibrium (WC and JC intersect)
# ============================================================
theta_star, w_star = solve_eq(A0, b0, beta0, c0, s0, phi0, alpha0)
theta_grid = np.linspace(0.05, 1.6, 400)
wc_vals = wage_curve(theta_grid, A0, b0, beta0, c0)
jc_vals = job_creation(theta_grid, A0, c0, s0, phi0, alpha0)

fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(theta_grid, wc_vals, "b-", lw=2.2, label=r"Wage curve $w^{WC}(\theta)$ (upward-sloping)")
ax.plot(theta_grid, jc_vals, "r-", lw=2.2, label=r"Job creation curve $w^{JC}(\theta)$ (downward-sloping)")

ax.scatter([theta_star], [w_star], color="black", s=110, zorder=5)
ax.annotate(rf"Equilibrium $(\theta^*, w^*) = ({theta_star:.2f}, {w_star:.3f})$",
            xy=(theta_star, w_star),
            xytext=(theta_star + 0.30, w_star - 0.025),
            fontsize=11,
            arrowprops=dict(arrowstyle="->", color="black", lw=1))

# Dashed guide lines to axes
ax.plot([theta_star, theta_star], [0.93, w_star], "k:", lw=0.8)
ax.plot([0, theta_star], [w_star, w_star], "k:", lw=0.8)

# Use a clean tick set without overlap
ax.set_xticks([0.0, 0.3, theta_star, 1.0, 1.3, 1.6])
ax.set_xticklabels(["0.0", "0.3", r"$\theta^*$", "1.0", "1.3", "1.6"])

ax.set_xlabel(r"Labor-market tightness $\theta = v/u$")
ax.set_ylabel(r"Wage $w$")
ax.set_title("Labor-market equilibrium: WC meets JC")
ax.set_xlim(0, 1.6)
ax.set_ylim(0.93, 1.005)  # zoom in to make the slopes visible
ax.legend(loc="lower left", framealpha=0.95)
ax.grid(alpha=0.3)
plt.savefig("/home/claude/figures/fig_equilibrium.pdf")
plt.savefig("/home/claude/figures/fig_equilibrium.png", dpi=150)
plt.close()
print("fig_equilibrium done.")

# ============================================================
# FIGURE 2: Beveridge curve
# ============================================================
theta_grid_b = np.linspace(0.02, 3.0, 400)
u_b, v_b = bev(theta_grid_b, s0, phi0, alpha0)
u_eq, v_eq = bev(theta_star, s0, phi0, alpha0)

fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(u_b, v_b, "k-", lw=2.2, label="Beveridge curve")
ax.scatter([u_eq], [v_eq], color="black", s=110, zorder=5)
ax.annotate(rf"$(u^*, v^*) = ({u_eq:.3f}, {v_eq:.3f})$",
            xy=(u_eq, v_eq),
            xytext=(u_eq + 0.02, v_eq + 0.02),
            fontsize=11,
            arrowprops=dict(arrowstyle="->", color="black", lw=1))

# Add a 45-degree ray of constant tightness through the origin to illustrate theta
theta_ray = theta_star
u_ray = np.linspace(0, 0.12, 50)
v_ray = theta_ray * u_ray
ax.plot(u_ray, v_ray, "g--", lw=1, alpha=0.7, label=rf"Ray $v = \theta^* u$")

ax.set_xlabel(r"Unemployment rate $u$")
ax.set_ylabel(r"Vacancy rate $v$")
ax.set_title("The Beveridge curve")
ax.set_xlim(0, 0.12)
ax.set_ylim(0, 0.16)
ax.legend(loc="upper right", framealpha=0.95)
ax.grid(alpha=0.3)
plt.savefig("/home/claude/figures/fig_beveridge.pdf")
plt.savefig("/home/claude/figures/fig_beveridge.png", dpi=150)
plt.close()
print("fig_beveridge done.")

# ============================================================
# FIGURE 3: Productivity shock — WC/JC shift
# ============================================================
A_new = 1.15
th_n, w_n = solve_eq(A_new, b0, beta0, c0, s0, phi0, alpha0)

# Use a wider grid so dashed lines extend across the plot
theta_grid_wide = np.linspace(0.05, 2.4, 400)
wc_vals_wide = wage_curve(theta_grid_wide, A0, b0, beta0, c0)
jc_vals_wide = job_creation(theta_grid_wide, A0, c0, s0, phi0, alpha0)
wc_n = wage_curve(theta_grid_wide, A_new, b0, beta0, c0)
jc_n = job_creation(theta_grid_wide, A_new, c0, s0, phi0, alpha0)

fig, ax = plt.subplots(figsize=(7.5, 5))
ax.plot(theta_grid_wide, wc_vals_wide, "b-", lw=2, label=r"WC (benchmark)")
ax.plot(theta_grid_wide, jc_vals_wide, "r-", lw=2, label=r"JC (benchmark)")
ax.plot(theta_grid_wide, wc_n, "b--", lw=2, label=r"WC (high $A$)")
ax.plot(theta_grid_wide, jc_n, "r--", lw=2, label=r"JC (high $A$)")

ax.scatter([theta_star], [w_star], color="black", s=110, zorder=5, label="Old equilibrium")
ax.scatter([th_n], [w_n], color="green", s=110, zorder=5, label="New equilibrium")

ax.annotate("", xy=(th_n, w_n), xytext=(theta_star, w_star),
            arrowprops=dict(arrowstyle="->", color="purple", lw=1.5))

ax.set_xlabel(r"Labor-market tightness $\theta$")
ax.set_ylabel(r"Wage $w$")
ax.set_title(rf"Productivity shock: $A$ from {A0:.2f} to {A_new:.2f}")
ax.set_xlim(0, 2.4)
ax.set_ylim(0.93, 1.18)
ax.legend(loc="lower right", framealpha=0.95, ncol=1, fontsize=10)
ax.grid(alpha=0.3)
plt.savefig("/home/claude/figures/fig_productivity_shock.pdf")
plt.savefig("/home/claude/figures/fig_productivity_shock.png", dpi=150)
plt.close()
print("fig_productivity_shock done.")

# ============================================================
# FIGURE 4: Higher unemployment benefits — WC/JC shift
# ============================================================
b_new = 0.65
th_b, w_b = solve_eq(A0, b_new, beta0, c0, s0, phi0, alpha0)
wc_b = wage_curve(theta_grid, A0, b_new, beta0, c0)
jc_b = job_creation(theta_grid, A0, c0, s0, phi0, alpha0)  # JC unchanged

fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(theta_grid, wc_vals, "b-", lw=2, label=r"WC (benchmark)")
ax.plot(theta_grid, jc_vals, "r-", lw=2, label=r"JC (unchanged)")
ax.plot(theta_grid, wc_b, "b--", lw=2, label=r"WC (high $b$)")

ax.scatter([theta_star], [w_star], color="black", s=90, zorder=5, label="Old equilibrium")
ax.scatter([th_b], [w_b], color="green", s=90, zorder=5, label="New equilibrium")

ax.annotate("", xy=(th_b, w_b), xytext=(theta_star, w_star),
            arrowprops=dict(arrowstyle="->", color="purple", lw=1.5))

ax.set_xlabel(r"Labor-market tightness $\theta$")
ax.set_ylabel(r"Wage $w$")
ax.set_title(rf"Higher unemployment benefits: $b$ from {b0:.2f} to {b_new:.2f}")
ax.set_xlim(0, 1.6)
ax.set_ylim(0.93, 1.005)
ax.legend(loc="lower left", framealpha=0.95, fontsize=10)
ax.grid(alpha=0.3)
plt.savefig("/home/claude/figures/fig_ui_shock.pdf")
plt.savefig("/home/claude/figures/fig_ui_shock.png", dpi=150)
plt.close()
print("fig_ui_shock done.")

# ============================================================
# FIGURE 5: Mockup of the Colab interactive interface
# ============================================================
# Reproduce the side-by-side WC/JC + Beveridge layout with the slider panel above.

fig = plt.figure(figsize=(12, 9))

# Top row: slider panel mockup
ax_sliders = fig.add_axes([0.05, 0.74, 0.90, 0.22])
ax_sliders.axis("off")

# Title
ax_sliders.text(0.5, 0.95, "Counterfactual parameters", fontsize=14,
                ha="center", va="top", weight="bold",
                transform=ax_sliders.transAxes)

# Draw 7 slider mockups in a grid: 3-3-1
labels = [("s", s0, 0.01, 0.20), ("c", c0, 0.05, 1.00),
          ("A", A0, 0.50, 2.00), ("b", b0, 0.10, 1.00),
          ("β", beta0, 0.10, 0.99), ("φ", phi0, 0.20, 2.00),
          ("α", alpha0, 0.10, 0.90)]

slider_positions = [(0.03, 0.65), (0.36, 0.65), (0.69, 0.65),
                    (0.03, 0.40), (0.36, 0.40), (0.69, 0.40),
                    (0.03, 0.15)]

for (lab, val, lo, hi), (x, y) in zip(labels, slider_positions):
    # Label
    ax_sliders.text(x, y + 0.08, lab, fontsize=12, weight="bold",
                    transform=ax_sliders.transAxes)
    # Track
    ax_sliders.add_patch(Rectangle((x + 0.04, y + 0.07), 0.20, 0.015,
                                   facecolor="#cccccc", edgecolor="none",
                                   transform=ax_sliders.transAxes))
    # Filled portion
    frac = (val - lo) / (hi - lo)
    ax_sliders.add_patch(Rectangle((x + 0.04, y + 0.07), 0.20*frac, 0.015,
                                   facecolor="#1f77b4", edgecolor="none",
                                   transform=ax_sliders.transAxes))
    # Knob
    ax_sliders.add_patch(plt.Circle((x + 0.04 + 0.20*frac, y + 0.0775),
                                    0.012, color="#1f77b4",
                                    transform=ax_sliders.transAxes))
    # Value
    ax_sliders.text(x + 0.27, y + 0.075, f"{val:.3f}",
                    fontsize=11, family="monospace",
                    transform=ax_sliders.transAxes)

# Reset button (next to alpha, on the right side)
ax_sliders.add_patch(Rectangle((0.69, 0.18), 0.22, 0.10,
                               facecolor="#ff7f0e", edgecolor="none",
                               transform=ax_sliders.transAxes))
ax_sliders.text(0.80, 0.23, "Reset to benchmark",
                fontsize=11, color="white", weight="bold",
                ha="center", va="center",
                transform=ax_sliders.transAxes)

# Border around sliders panel
ax_sliders.add_patch(Rectangle((0, 0), 1, 1, fill=False,
                               edgecolor="#888888", lw=1,
                               transform=ax_sliders.transAxes))

# ----- Bottom row: two plots -----
# Left: WC/JC
ax1 = fig.add_axes([0.07, 0.08, 0.40, 0.55])
A_cf, b_cf = 1.10, 0.55
th_cf, w_cf = solve_eq(A_cf, b_cf, beta0, c0, s0, phi0, alpha0)
wc_cf = wage_curve(theta_grid, A_cf, b_cf, beta0, c0)
jc_cf = job_creation(theta_grid, A_cf, c0, s0, phi0, alpha0)

ax1.plot(theta_grid, wc_vals, "b-", lw=1.8, label="WC (benchmark)")
ax1.plot(theta_grid, jc_vals, "r-", lw=1.8, label="JC (benchmark)")
ax1.plot(theta_grid, wc_cf, "b--", lw=1.8, label="WC (new)")
ax1.plot(theta_grid, jc_cf, "r--", lw=1.8, label="JC (new)")
ax1.scatter([theta_star], [w_star], color="black", s=70, zorder=5)
ax1.scatter([th_cf], [w_cf], color="green", s=70, zorder=5)
ax1.set_xlabel(r"$\theta$ (tightness)")
ax1.set_ylabel(r"$w$ (wage)")
ax1.set_title("Labor Market Equilibrium")
ax1.set_xlim(0, 2.0)
ax1.set_ylim(0.92, 1.13)
ax1.legend(fontsize=9, framealpha=0.95)
ax1.grid(alpha=0.3)

# Right: Beveridge
ax2 = fig.add_axes([0.55, 0.08, 0.40, 0.55])
ub_cf, vb_cf = bev(theta_grid_b, s0, phi0, alpha0)  # benchmark s, phi
u_eq_cf, v_eq_cf = bev(th_cf, s0, phi0, alpha0)
ax2.plot(u_b, v_b, "k-", lw=1.8, label="Benchmark")
ax2.plot(ub_cf, vb_cf, "k--", lw=1.8, label="New")
ax2.scatter([u_eq], [v_eq], color="black", s=70, zorder=5)
ax2.scatter([u_eq_cf], [v_eq_cf], color="green", s=70, zorder=5)
ax2.set_xlabel(r"$u$ (unemployment)")
ax2.set_ylabel(r"$v$ (vacancies)")
ax2.set_title("Beveridge Curve")
ax2.set_xlim(0, 0.12)
ax2.set_ylim(0, 0.16)
ax2.legend(fontsize=9, framealpha=0.95)
ax2.grid(alpha=0.3)

plt.savefig("/home/claude/figures/fig_interface.pdf")
plt.savefig("/home/claude/figures/fig_interface.png", dpi=150)
plt.close()
print("fig_interface done.")

print("\nAll figures generated.")
