# =====================================================================
# Search & Matching Model -- Interactive Simulator
# =====================================================================
# Companion to the teaching paper "An Interactive Introduction to
# Search and Matching Models: A Large-Firm Approach for Undergraduate
# Teaching" by Jose Silva.
#
# This script runs as a single cell in Google Colab and produces:
#   - sliders for the seven parameters of the model,
#   - a side-by-side plot of (i) the WC/JC equilibrium, (ii) the
#     Beveridge curve,
#   - a results panel reporting equilibrium values for the benchmark
#     and the counterfactual.
#
# The benchmark calibration is:
#   s     = 0.035   (separation rate)
#   c     = 0.12    (vacancy cost)
#   A     = 1.0     (productivity per worker)
#   b     = 0.41    (flow value of unemployment)
#   beta  = 0.879   (worker bargaining power)
#   phi   = 0.754   (matching efficiency)
#   alpha = 0.5     (vacancy elasticity in matching)
#
# Aggregates and firms: lowercase letters in this script denote
# aggregate quantities (e employment, u unemployment, v vacancies,
# theta = v/u tightness), the same convention used in the body of the
# paper. The matching function M(u, v) takes these aggregates as
# inputs. The firm-level optimization (Appendix A of the paper) uses
# uppercase E, V for the firm's own employment and vacancies, with
# N_f identical firms giving e = N_f * E and v = N_f * V. The
# numerical simulator below works at the aggregate level.
# =====================================================================

import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from scipy.optimize import brentq
from IPython.display import display

# ---------- Benchmark parameters ----------
s0, c0, A0, b0, beta0, phi0, alpha0 = 0.035, 0.12, 1.0, 0.41, 0.879, 0.754, 0.5

# ---------- Model functions ----------
def q(theta, phi, alpha):
    """Vacancy-filling rate."""
    return phi * theta**(-(1 - alpha))

def p(theta, phi, alpha):
    """Job-finding rate."""
    return phi * theta**alpha

def wage_curve(theta, A, b, beta, c):
    """Wage curve from Nash bargaining."""
    return beta*A + beta*c*theta + (1-beta)*b

def job_creation(theta, A, c, s, phi, alpha):
    """Job creation curve from firm optimization."""
    return A - c * (s / q(theta, phi, alpha))

def solve_equilibrium(A, b, beta, c, s, phi, alpha):
    """Find the unique theta* where WC = JC."""
    def diff(theta):
        return wage_curve(theta, A, b, beta, c) - job_creation(theta, A, c, s, phi, alpha)
    theta_star = brentq(diff, 1e-4, 100)
    w_star = wage_curve(theta_star, A, b, beta, c)
    return theta_star, w_star

def bev(theta, s, phi, alpha):
    """Steady-state Beveridge curve point."""
    p_val = p(theta, phi, alpha)
    u = s / (s + p_val)
    v = theta * u
    return u, v

# ---------- Plot ----------
def plot_model(s, c, A, b, beta, phi, alpha):

    # Benchmark
    theta0, w0 = solve_equilibrium(A0, b0, beta0, c0, s0, phi0, alpha0)

    # Counterfactual
    theta1, w1 = solve_equilibrium(A, b, beta, c, s, phi, alpha)

    theta_grid = np.linspace(0.01, max(theta0, theta1)*2, 400)

    # Curves
    wc0 = wage_curve(theta_grid, A0, b0, beta0, c0)
    jc0 = job_creation(theta_grid, A0, c0, s0, phi0, alpha0)

    wc1 = wage_curve(theta_grid, A, b, beta, c)
    jc1 = job_creation(theta_grid, A, c, s, phi, alpha)

    # Beveridge curves
    u_b0, v_b0 = bev(theta_grid, s0, phi0, alpha0)
    u_b1, v_b1 = bev(theta_grid, s, phi, alpha)

    # Equilibrium values
    u0, v0 = bev(theta0, s0, phi0, alpha0)
    u1, v1 = bev(theta1, s, phi, alpha)

    p0, q0 = p(theta0, phi0, alpha0), q(theta0, phi0, alpha0)
    p1, q1 = p(theta1, phi, alpha), q(theta1, phi, alpha)

    # ---------- Plot ----------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # WC & JC
    ax1.plot(theta_grid, wc0, 'b-', label="WC (benchmark)")
    ax1.plot(theta_grid, jc0, 'r-', label="JC (benchmark)")
    ax1.plot(theta_grid, wc1, 'b--', label="WC (new)")
    ax1.plot(theta_grid, jc1, 'r--', label="JC (new)")

    ax1.scatter(theta0, w0, color='black', s=80)
    ax1.scatter(theta1, w1, color='green', s=80)

    ax1.set_xlabel("θ (tightness)")
    ax1.set_ylabel("w (wage)")
    ax1.set_title("Labor Market Equilibrium")
    ax1.legend()
    ax1.grid(alpha=0.3)

    # Beveridge
    ax2.plot(u_b0, v_b0, 'k-', label="Benchmark")
    ax2.plot(u_b1, v_b1, 'k--', label="New")

    ax2.scatter(u0, v0, color='black', s=80)
    ax2.scatter(u1, v1, color='green', s=80)

    ax2.set_xlabel("u (unemployment)")
    ax2.set_ylabel("v (vacancies)")
    ax2.set_title("Beveridge Curve")
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.show()

    # ---------- Results panel ----------
    display(widgets.HTML(f"""
    <div style='border:1px solid #ccc; padding:12px; border-radius:8px; background:#f9f9f9'>
    <b>Equilibrium Comparison</b><br><br>

    <b>Benchmark</b><br>
    θ = {theta0:.3f} <br>
    w = {w0:.3f} <br>
    p = {p0:.3f} <br>
    q = {q0:.3f} <br>
    u = {u0:.3f} <br>
    v = {v0:.3f} <br><br>

    <b>Counterfactual</b><br>
    θ = {theta1:.3f} <br>
    w = {w1:.3f} <br>
    p = {p1:.3f} <br>
    q = {q1:.3f} <br>
    u = {u1:.3f} <br>
    v = {v1:.3f}
    </div>
    """))

# ---------- Widgets ----------
style = {"description_width": "110px"}

s_w     = widgets.FloatSlider(value=s0,     min=0.01, max=0.20, step=0.005, description="s",     style=style)
c_w     = widgets.FloatSlider(value=c0,     min=0.05, max=1.00, step=0.01,  description="c",     style=style)
A_w     = widgets.FloatSlider(value=A0,     min=0.50, max=2.00, step=0.05,  description="A",     style=style)
b_w     = widgets.FloatSlider(value=b0,     min=0.10, max=1.00, step=0.05,  description="b",     style=style)
beta_w  = widgets.FloatSlider(value=beta0,  min=0.10, max=0.99, step=0.01,  description="β",     style=style)
phi_w   = widgets.FloatSlider(value=phi0,   min=0.20, max=2.00, step=0.05,  description="φ",     style=style)
alpha_w = widgets.FloatSlider(value=alpha0, min=0.10, max=0.90, step=0.05,  description="α",     style=style)

# Reset button
reset_btn = widgets.Button(description="Reset to benchmark", button_style='warning')

def reset_params(_):
    s_w.value = s0
    c_w.value = c0
    A_w.value = A0
    b_w.value = b0
    beta_w.value = beta0
    phi_w.value = phi0
    alpha_w.value = alpha0

reset_btn.on_click(reset_params)

# Layout
ui = widgets.VBox([
    widgets.HTML("<b>Counterfactual parameters</b>"),
    widgets.HBox([s_w, c_w, A_w]),
    widgets.HBox([b_w, beta_w, phi_w]),
    widgets.HBox([alpha_w]),
    reset_btn
])

out = widgets.interactive_output(
    plot_model,
    {"s": s_w, "c": c_w, "A": A_w, "b": b_w, "beta": beta_w, "phi": phi_w, "alpha": alpha_w}
)

display(ui, out)
