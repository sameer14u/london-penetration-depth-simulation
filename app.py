"""
app.py — Interactive Streamlit interface for London Penetration Depth Simulation.

Run with:
    streamlit run app.py

This application provides an interactive simulation of magnetic-field
penetration into superconducting/diamagnetic materials based on the
London equation.  Users can adjust temperature, applied field, material,
geometry, and dimensions to explore the Meissner effect.

Author : SSP Assignment Group
Date   : 2026
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")                 # Non-interactive backend for Streamlit
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.colors import Normalize
import streamlit as st

# ── Import physics engine ──────────────────────────────────────────────
from london_physics import (
    MATERIALS, MU_0,
    london_penetration_depth,
    field_slab, field_cylinder,
    field_rectangle_2d,
    compute_slab_2d, compute_cylinder_2d, compute_rectangle_2d,
    field_vs_distance_slab, field_vs_distance_cylinder,
    compare_temperatures, compare_fields, compare_geometries,
)

# ═══════════════════════════════════════════════════════════════════════
# Page configuration
# ═══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="London Penetration Depth Simulator",
    page_icon="🧲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global matplotlib style ───────────────────────────────────────────
try:
    plt.style.use("seaborn-v0_8-whitegrid")
except OSError:
    plt.style.use("seaborn-whitegrid")
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
})


# ═══════════════════════════════════════════════════════════════════════
# Sidebar — Input Parameters
# ═══════════════════════════════════════════════════════════════════════
st.sidebar.title("🧲 Simulation Parameters")

# ── Material selection ─────────────────────────────────────────────────
material_names = list(MATERIALS.keys())
material = st.sidebar.selectbox("**Material**", material_names, index=0)
mat = MATERIALS[material]

if material == "Custom":
    Tc = st.sidebar.number_input("Critical temperature Tc (K)", 0.5, 200.0, 9.0, 0.1)
    lambda_0_nm = st.sidebar.number_input("lambda_0 (nm)", 1.0, 1000.0, 40.0, 1.0)
else:
    Tc = mat["Tc"]
    lambda_0_nm = mat["lambda_0"]
    st.sidebar.markdown(f"**Tc** = {Tc} K &nbsp;|&nbsp; **lambda_0** = {lambda_0_nm} nm")

lambda_0 = lambda_0_nm * 1e-9  # Convert to metres

# ── Temperature ────────────────────────────────────────────────────────
T = st.sidebar.slider("**Temperature T (K)**", 0.1, float(Tc) * 1.05,
                       float(Tc) * 0.5, 0.01)
normal_state = T >= Tc
if normal_state:
    st.sidebar.warning("⚠️ T ≥ Tc — material is in the **normal state**.  "
                       "The Meissner effect is absent; the field fully penetrates.")

# ── Applied field ──────────────────────────────────────────────────────
B0 = st.sidebar.number_input("**Applied field B_0 (T)**", 0.001, 2.0, 0.1, 0.01,
                              format="%.3f")

# ── Geometry ───────────────────────────────────────────────────────────
geometry = st.sidebar.radio("**Geometry**", ["Slab", "Cylinder", "Rectangular"])

if geometry == "Slab":
    d_nm = st.sidebar.slider("Slab thickness d (nm)", 50, 3000, 500, 10)
    d = d_nm * 1e-9
    dims = {"d": d}
elif geometry == "Cylinder":
    R_nm = st.sidebar.slider("Cylinder radius R (nm)", 50, 3000, 500, 10)
    R = R_nm * 1e-9
    dims = {"R": R}
else:  # Rectangular
    a_nm = st.sidebar.slider("Width a (nm)", 50, 3000, 500, 10)
    b_nm = st.sidebar.slider("Height b (nm)", 50, 3000, 400, 10)
    a, b = a_nm * 1e-9, b_nm * 1e-9
    dims = {"a": a, "b": b}

# ── Resolution ─────────────────────────────────────────────────────────
resolution = st.sidebar.slider("Grid resolution", 100, 500, 200, 25)

# ── Computed parameters ────────────────────────────────────────────────
lambda_T = london_penetration_depth(lambda_0, T, Tc)
lambda_T_nm = lambda_T * 1e9 if not np.isinf(lambda_T) else np.inf

st.sidebar.markdown("---")
st.sidebar.subheader("📐 Computed Values")

if np.isinf(lambda_T):
    st.sidebar.error("lambda(T) → ∞  (normal state)")
else:
    st.sidebar.success(f"**lambda(T) = {lambda_T_nm:.2f} nm**")

    # Screening assessment
    if geometry == "Slab":
        char_dim = d_nm
        dim_label = "d"
    elif geometry == "Cylinder":
        char_dim = R_nm
        dim_label = "R"
    else:
        char_dim = min(a_nm, b_nm)
        dim_label = "min(a,b)"

    ratio = char_dim / lambda_T_nm
    st.sidebar.metric(f"{dim_label} / lambda", f"{ratio:.2f}")
    if ratio > 10:
        st.sidebar.info("🛡️ **Strong screening** — field expelled from bulk")
    elif ratio > 2:
        st.sidebar.info("🔶 **Partial penetration** — field decays but reaches interior")
    else:
        st.sidebar.info("🔴 **Weak screening** — field penetrates throughout")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Formula:**  lambda(T) = lambda_0 / √(1 - (T/Tc)⁴)  \n"
    f"T/Tc = {T/Tc:.3f}"
)


# ═══════════════════════════════════════════════════════════════════════
# Main content — Tabs
# ═══════════════════════════════════════════════════════════════════════
st.title("🧲 London Penetration Depth — Interactive Simulator")
st.markdown(
    "Explore how an external magnetic field penetrates into a "
    "superconducting / diamagnetic material via the **London equation**.  "
    "Adjust parameters in the sidebar to update all visualisations."
)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🗺️ 2D Field Visualisation",
    "📈 Field Profile",
    "🌡️ Temperature Dependence",
    "🔷 Geometry Comparison",
    "🔬 Parameter Study",
    "📖 Theory & Information",
])

# ═══════════════════════════════════════════════════════════════════════
# Tab 1 — 2-D Field Visualisation
# ═══════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("2-D Magnetic-Field Distribution")

    # Compute 2-D field map
    if geometry == "Slab":
        X, Y, Bz, Bx, By = compute_slab_2d(B0, lambda_T, d, resolution, resolution)
    elif geometry == "Cylinder":
        X, Y, Bz, Bx, By = compute_cylinder_2d(B0, lambda_T, R, resolution, resolution)
    else:
        X, Y, Bz, Bx, By = compute_rectangle_2d(B0, lambda_T, a, b, resolution, resolution)

    # Convert to nm for display
    X_nm, Y_nm = X * 1e9, Y * 1e9
    B_norm = Bz / B0  # Normalised field

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # --- Left: Colour map with contours ---
    vmin, vmax = 0.0, np.clip(B_norm.max(), 1.0, 1.5)
    cf = ax1.contourf(X_nm, Y_nm, B_norm, levels=50,
                      cmap="RdBu_r", vmin=vmin, vmax=vmax)
    ax1.contour(X_nm, Y_nm, B_norm, levels=10, colors="k",
                linewidths=0.4, alpha=0.5)
    cbar1 = fig.colorbar(cf, ax=ax1, label="B / B_0", shrink=0.85)

    # Draw material boundary
    if geometry == "Slab":
        for xb in [-d_nm / 2, d_nm / 2]:
            ax1.axvline(xb, color="white", ls="--", lw=1.5, label="Slab boundary" if xb < 0 else "")
    elif geometry == "Cylinder":
        circle = plt.Circle((0, 0), R_nm, fill=False, ec="white", ls="--", lw=1.5)
        ax1.add_patch(circle)
    else:
        rect = Rectangle((-a_nm / 2, -b_nm / 2), a_nm, b_nm,
                         fill=False, ec="white", ls="--", lw=1.5)
        ax1.add_patch(rect)

    ax1.set_xlabel("x (nm)")
    ax1.set_ylabel("y (nm)")
    ax1.set_title(f"Field Magnitude  |B|/B_0  —  {geometry}")
    ax1.set_aspect("equal")

    # --- Right: Streamplot with semi-transparent colour map ---
    ax2.contourf(X_nm, Y_nm, B_norm, levels=50,
                 cmap="RdBu_r", alpha=0.4, vmin=vmin, vmax=vmax)

    # Field-line density: use magnitude to set density
    speed = np.sqrt(Bx**2 + By**2)
    lw = 2.0 * speed / (speed.max() + 1e-30)
    ax2.streamplot(X_nm, Y_nm, Bx, By, color="navy",
                   linewidth=lw, density=1.5, arrowsize=1.0)

    # Draw boundary
    if geometry == "Slab":
        for xb in [-d_nm / 2, d_nm / 2]:
            ax2.axvline(xb, color="red", ls="--", lw=1.5)
    elif geometry == "Cylinder":
        circle2 = plt.Circle((0, 0), R_nm, fill=False, ec="red", ls="--", lw=1.5)
        ax2.add_patch(circle2)
    else:
        rect2 = Rectangle((-a_nm / 2, -b_nm / 2), a_nm, b_nm,
                           fill=False, ec="red", ls="--", lw=1.5)
        ax2.add_patch(rect2)

    ax2.set_xlabel("x (nm)")
    ax2.set_ylabel("y (nm)")
    ax2.set_title(f"Magnetic Field Lines  —  {geometry}")
    ax2.set_aspect("equal")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        f"**Left:** colour map of normalised field magnitude B/B_0.  "
        f"**Right:** field-line streamplot showing how field lines are expelled "
        f"from the superconductor (Meissner effect).  "
        f"Material boundary shown as dashed line."
    )


# ═══════════════════════════════════════════════════════════════════════
# Tab 2 — 1-D Field Profile
# ═══════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Field Intensity vs. Distance from Surface")

    fig2, ax = plt.subplots(figsize=(10, 6))

    if geometry == "Slab":
        x, B = field_vs_distance_slab(B0, lambda_T, d)
        x_nm = x * 1e9
        ax.plot(x_nm, B / B0, "b-", lw=2, label="B(x) / B_0")
        ax.axvline(-d_nm / 2, color="gray", ls="--", lw=1, label="Slab boundary")
        ax.axvline(d_nm / 2, color="gray", ls="--", lw=1)
        ax.set_xlabel("Position x (nm)")
        surface_pos = d_nm / 2  # for annotation

    elif geometry == "Cylinder":
        r, B = field_vs_distance_cylinder(B0, lambda_T, R)
        x_nm = r * 1e9
        ax.plot(x_nm, B / B0, "b-", lw=2, label="B(r) / B_0")
        ax.axvline(R_nm, color="gray", ls="--", lw=1, label="Cylinder surface")
        ax.set_xlabel("Radial distance r (nm)")
        surface_pos = R_nm

    else:  # Rectangular — cut along x at y=0
        x = np.linspace(-2 * a, 2 * a, 500)
        B = field_slab(x, B0, lambda_T, a)  # 1-D cut
        x_nm = x * 1e9
        ax.plot(x_nm, B / B0, "b-", lw=2, label="B(x) / B_0  (y = 0 cut)")
        ax.axvline(-a_nm / 2, color="gray", ls="--", lw=1, label="Boundary")
        ax.axvline(a_nm / 2, color="gray", ls="--", lw=1)
        ax.set_xlabel("Position x (nm)")
        surface_pos = a_nm / 2

    # Reference exponential decay from surface
    if not np.isinf(lambda_T):
        depth = np.linspace(0, surface_pos, 200)
        exp_ref = np.exp(-depth / lambda_T_nm)
        if geometry == "Cylinder":
            ax.plot(surface_pos - depth, exp_ref, "r--", lw=1.5, alpha=0.7,
                    label=f"exp(-x/lambda),  lambda = {lambda_T_nm:.1f} nm")
        else:
            ax.plot(surface_pos - depth, exp_ref, "r--", lw=1.5, alpha=0.7,
                    label=f"exp(-x/lambda),  lambda = {lambda_T_nm:.1f} nm")

        # Annotate lambda
        ax.annotate(f"lambda(T) = {lambda_T_nm:.1f} nm",
                    xy=(surface_pos - lambda_T_nm, np.exp(-1)),
                    xytext=(surface_pos + lambda_T_nm * 0.5, 0.6),
                    fontsize=11, color="red",
                    arrowprops=dict(arrowstyle="->", color="red", lw=1.5))

    ax.set_ylabel("B / B_0")
    ax.set_title(f"Field Profile  —  {geometry}  |  T = {T:.2f} K  |  B_0 = {B0:.3f} T")
    ax.legend(loc="best", fontsize=10)
    ax.set_ylim(-0.05, 1.15)
    ax.grid(True, alpha=0.3)

    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

    if not np.isinf(lambda_T):
        st.info(
            f"The magnetic field decays exponentially from the surface with "
            f"characteristic length **lambda(T) = {lambda_T_nm:.2f} nm** "
            f"(at T = {T:.2f} K).  "
            f"The dashed red curve shows the ideal exponential decay e⁻ˣ/lambda "
            f"for comparison."
        )


# ═══════════════════════════════════════════════════════════════════════
# Tab 3 — Temperature Dependence
# ═══════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Temperature Dependence of Field Penetration")

    col_a, col_b = st.columns(2)

    with col_a:
        # Field profiles at multiple temperatures
        T_fracs = [0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]
        T_values = [f * Tc for f in T_fracs]

        geom_key = geometry.lower()
        if geom_key == "rectangular":
            geom_key = "rectangular"
        results = compare_temperatures(B0, lambda_0, Tc, geom_key, dims, T_values)

        fig3, ax3 = plt.subplots(figsize=(8, 6))
        cmap_t = plt.cm.coolwarm
        for i, (label, x, B) in enumerate(results):
            colour = cmap_t(i / (len(results) - 1))
            ax3.plot(x * 1e9, B / B0, "-", color=colour, lw=1.5, label=label)

        if geometry == "Slab":
            ax3.axvline(-d_nm / 2, color="gray", ls="--", lw=0.8)
            ax3.axvline(d_nm / 2, color="gray", ls="--", lw=0.8)
            ax3.set_xlabel("Position x (nm)")
        elif geometry == "Cylinder":
            ax3.axvline(R_nm, color="gray", ls="--", lw=0.8)
            ax3.set_xlabel("Radial distance r (nm)")
        else:
            ax3.axvline(-a_nm / 2, color="gray", ls="--", lw=0.8)
            ax3.axvline(a_nm / 2, color="gray", ls="--", lw=0.8)
            ax3.set_xlabel("Position x (nm)")

        ax3.set_ylabel("B / B_0")
        ax3.set_title(f"Field Penetration at Various Temperatures — {geometry}")
        ax3.legend(fontsize=8, loc="best")
        ax3.set_ylim(-0.05, 1.15)
        ax3.grid(True, alpha=0.3)
        fig3.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)

    with col_b:
        # lambda(T)/lambda_0 vs T/Tc
        t_ratio = np.linspace(0.01, 0.999, 500)
        lambda_ratio = 1.0 / np.sqrt(1.0 - t_ratio**4)

        fig4, ax4 = plt.subplots(figsize=(8, 6))
        ax4.plot(t_ratio, lambda_ratio, "b-", lw=2)
        ax4.axhline(1.0, color="gray", ls=":", lw=0.8)

        # Mark current temperature
        if T < Tc:
            t_cur = T / Tc
            lam_cur = 1.0 / np.sqrt(1.0 - t_cur**4)
            ax4.plot(t_cur, lam_cur, "ro", ms=10, zorder=5, label=f"Current: T/Tc = {t_cur:.3f}")
            ax4.legend(fontsize=10)

        ax4.set_xlabel("T / Tc")
        ax4.set_ylabel("lambda(T) / lambda_0")
        ax4.set_title("Gorter–Casimir: Penetration Depth vs. Temperature")
        ax4.set_ylim(0.5, 10)
        ax4.set_xlim(0, 1)
        ax4.grid(True, alpha=0.3)
        fig4.tight_layout()
        st.pyplot(fig4)
        plt.close(fig4)

    st.markdown(
        "**Interpretation:**  As temperature approaches Tc, the superfluid "
        "density decreases and the penetration depth diverges.  This means "
        "the material becomes increasingly unable to screen the applied field, "
        "until at T = Tc the superconducting state is destroyed and the "
        "Meissner effect vanishes entirely."
    )


# ═══════════════════════════════════════════════════════════════════════
# Tab 4 — Geometry Comparison
# ═══════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Comparison Across Geometries")

    # Use consistent dimensions for comparison
    comp_dim = st.slider("Characteristic dimension for comparison (nm)",
                         50, 2000, 500, 10, key="comp_dim")
    comp_d = comp_dim * 1e-9

    # Compute 2-D maps for all three geometries
    fig5, axes5 = plt.subplots(1, 3, figsize=(18, 6))

    # Slab
    Xs, Ys, Bzs, _, _ = compute_slab_2d(B0, lambda_T, comp_d,
                                         resolution, resolution)
    im0 = axes5[0].contourf(Xs * 1e9, Ys * 1e9, Bzs / B0, levels=50,
                            cmap="RdBu_r", vmin=0, vmax=1.0)
    for xb in [-comp_dim / 2, comp_dim / 2]:
        axes5[0].axvline(xb, color="white", ls="--", lw=1.2)
    axes5[0].set_title(f"Slab (d = {comp_dim} nm)")
    axes5[0].set_xlabel("x (nm)")
    axes5[0].set_ylabel("y (nm)")
    axes5[0].set_aspect("equal")
    fig5.colorbar(im0, ax=axes5[0], label="B/B_0", shrink=0.8)

    # Cylinder
    Xc, Yc, Bzc, _, _ = compute_cylinder_2d(B0, lambda_T, comp_d / 2,
                                              resolution, resolution)
    im1 = axes5[1].contourf(Xc * 1e9, Yc * 1e9, Bzc / B0, levels=50,
                            cmap="RdBu_r", vmin=0, vmax=1.0)
    circle_c = plt.Circle((0, 0), comp_dim / 2, fill=False, ec="white", ls="--", lw=1.2)
    axes5[1].add_patch(circle_c)
    axes5[1].set_title(f"Cylinder (R = {comp_dim/2:.0f} nm)")
    axes5[1].set_xlabel("x (nm)")
    axes5[1].set_ylabel("y (nm)")
    axes5[1].set_aspect("equal")
    fig5.colorbar(im1, ax=axes5[1], label="B/B_0", shrink=0.8)

    # Rectangular
    Xr, Yr, Bzr, _, _ = compute_rectangle_2d(B0, lambda_T, comp_d, comp_d * 0.8,
                                              resolution, resolution)
    im2 = axes5[2].contourf(Xr * 1e9, Yr * 1e9, Bzr / B0, levels=50,
                            cmap="RdBu_r", vmin=0, vmax=1.0)
    rect_c = Rectangle((-comp_dim / 2, -comp_dim * 0.4),
                        comp_dim, comp_dim * 0.8,
                        fill=False, ec="white", ls="--", lw=1.2)
    axes5[2].add_patch(rect_c)
    axes5[2].set_title(f"Rectangular ({comp_dim}×{comp_dim*0.8:.0f} nm)")
    axes5[2].set_xlabel("x (nm)")
    axes5[2].set_ylabel("y (nm)")
    axes5[2].set_aspect("equal")
    fig5.colorbar(im2, ax=axes5[2], label="B/B_0", shrink=0.8)

    fig5.suptitle(
        f"Geometry Comparison  |  lambda(T) = {lambda_T_nm:.1f} nm  |  B_0 = {B0:.3f} T"
        if not np.isinf(lambda_T) else
        f"Geometry Comparison  |  Normal state  |  B_0 = {B0:.3f} T",
        fontsize=14, y=1.02
    )
    fig5.tight_layout()
    st.pyplot(fig5)
    plt.close(fig5)

    # 1-D overlay comparison
    st.markdown("#### Depth-from-surface comparison")

    geo_results = compare_geometries(B0, lambda_T,
                                     comp_d, comp_d / 2,
                                     comp_d, comp_d * 0.8)
    fig6, ax6 = plt.subplots(figsize=(10, 6))
    colours_g = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    for (label, depth, B_ratio), colour in zip(geo_results, colours_g):
        ax6.plot(depth * 1e9, B_ratio, "-", color=colour, lw=2, label=label)

    if not np.isinf(lambda_T):
        d_ref = np.linspace(0, comp_dim, 200)
        ax6.plot(d_ref, np.exp(-d_ref / lambda_T_nm), "k--", lw=1, alpha=0.5,
                 label=f"exp(-x/lambda), lambda = {lambda_T_nm:.1f} nm")

    ax6.set_xlabel("Depth from surface (nm)")
    ax6.set_ylabel("B / B_0")
    ax6.set_title("Normalised Field vs. Depth — All Geometries")
    ax6.legend(fontsize=10)
    ax6.set_ylim(-0.05, 1.15)
    ax6.grid(True, alpha=0.3)
    fig6.tight_layout()
    st.pyplot(fig6)
    plt.close(fig6)

    st.markdown(
        "**Observation:** The cylinder geometry shows stronger screening "
        "(faster field decay) than the slab for the same penetration depth, "
        "because the curved geometry concentrates the screening currents.  "
        "The rectangular geometry is intermediate."
    )


# ═══════════════════════════════════════════════════════════════════════
# Tab 5 — Parameter Study
# ═══════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("Parameter Study — Multi-value Comparison")

    study_col1, study_col2 = st.columns(2)

    with study_col1:
        st.markdown("#### Vary Applied Field B_0")
        B0_vals = st.multiselect(
            "Select B_0 values (T)",
            [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0],
            default=[0.01, 0.05, 0.1, 0.5],
            key="b0_study"
        )
        if B0_vals:
            results_B = compare_fields(B0_vals, lambda_T, geometry.lower(), dims)
            fig7, ax7 = plt.subplots(figsize=(8, 6))
            for i, (label, x, B) in enumerate(results_B):
                ax7.plot(x * 1e9, B, "-", lw=1.5, label=label)
            ax7.set_xlabel("Position (nm)")
            ax7.set_ylabel("B (T)")
            ax7.set_title(f"Field Profiles for Different B_0 — {geometry}")
            ax7.legend(fontsize=9)
            ax7.grid(True, alpha=0.3)
            fig7.tight_layout()
            st.pyplot(fig7)
            plt.close(fig7)

            st.info(
                "The field profile shape (B/B_0) is **independent** of B_0 in the "
                "London model — the London equation is linear.  The absolute "
                "field values scale proportionally with B_0."
            )

    with study_col2:
        st.markdown("#### Vary Penetration Depth lambda")
        lam_vals_nm = st.multiselect(
            "Select lambda values (nm)",
            [10, 20, 40, 80, 150, 300, 500],
            default=[20, 40, 80, 150],
            key="lam_study"
        )
        if lam_vals_nm:
            fig8, ax8 = plt.subplots(figsize=(8, 6))
            for lam_nm in lam_vals_nm:
                lam_m = lam_nm * 1e-9
                if geometry == "Slab":
                    x, B = field_vs_distance_slab(B0, lam_m, d)
                elif geometry == "Cylinder":
                    x, B = field_vs_distance_cylinder(B0, lam_m, R)
                else:
                    x = np.linspace(-2 * a, 2 * a, 500)
                    B = field_slab(x, B0, lam_m, a)
                ax8.plot(x * 1e9, B / B0, "-", lw=1.5, label=f"lambda = {lam_nm} nm")

            ax8.set_xlabel("Position (nm)")
            ax8.set_ylabel("B / B_0")
            ax8.set_title(f"Effect of Penetration Depth — {geometry}")
            ax8.legend(fontsize=9)
            ax8.set_ylim(-0.05, 1.15)
            ax8.grid(True, alpha=0.3)
            fig8.tight_layout()
            st.pyplot(fig8)
            plt.close(fig8)

            st.info(
                "Larger penetration depth means weaker screening — the field "
                "penetrates deeper into the material.  When lambda ≫ sample dimension, "
                "screening is negligible."
            )


# ═══════════════════════════════════════════════════════════════════════
# Tab 6 — Theory & Information
# ═══════════════════════════════════════════════════════════════════════
with tab6:
    st.subheader("London Theory — Background and Equations")

    st.markdown(r"""
### 1. The London Equations

The London brothers (Fritz and Heinz London, 1935) proposed two phenomenological equations to describe the electromagnetic behaviour of superconductors:

**First London Equation** (acceleration equation):
$$\frac{\partial \mathbf{J}_s}{\partial t} = \frac{n_s e^2}{m} \mathbf{E}$$

**Second London Equation** (screening equation):
$$\nabla \times \mathbf{J}_s = -\frac{n_s e^2}{m} \mathbf{B}$$

where $n_s$ is the superfluid electron density, $e$ is the electron charge, $m$ is the electron mass, $\mathbf{J}_s$ is the supercurrent density, and $\mathbf{E}$, $\mathbf{B}$ are the electric and magnetic fields.

### 2. The London Penetration Depth

Combining the second London equation with Ampère's law ($\nabla \times \mathbf{B} = \mu_0 \mathbf{J}_s$), we obtain:

$$\nabla^2 \mathbf{B} = \frac{1}{\lambda_L^2} \mathbf{B}$$

where the **London penetration depth** is:

$$\lambda_L = \sqrt{\frac{m}{\mu_0 n_s e^2}}$$

This equation shows that the magnetic field decays exponentially from the surface of a superconductor with characteristic length $\lambda_L$.

### 3. Temperature Dependence — Gorter–Casimir Model

The two-fluid model (Gorter & Casimir, 1934) gives the temperature dependence:

$$\lambda(T) = \frac{\lambda_0}{\sqrt{1 - \left(\frac{T}{T_c}\right)^4}}$$

where $\lambda_0 = \lambda(T=0)$ is the zero-temperature penetration depth and $T_c$ is the critical temperature.  As $T \to T_c$, $\lambda \to \infty$ and the Meissner effect vanishes.

### 4. Solutions for Different Geometries

#### Infinite Slab (thickness $d$)

For a slab occupying $-d/2 \le x \le d/2$ with applied field $B_0$:

$$B(x) = B_0 \frac{\cosh(x/\lambda)}{\cosh(d/2\lambda)}$$

#### Long Cylinder (radius $R$)

For a cylinder with axial field $B_0$:

$$B(r) = B_0 \frac{I_0(r/\lambda)}{I_0(R/\lambda)}$$

where $I_0$ is the modified Bessel function of the first kind, order 0.

#### Rectangular Cross-section ($a \times b$)

Using the product-of-slabs (separable) approximation:

$$B(x,y) \approx B_0 \frac{\cosh(x/\lambda)}{\cosh(a/2\lambda)} \cdot \frac{\cosh(y/\lambda)}{\cosh(b/2\lambda)}$$

### 5. Physical Significance

- **Meissner Effect:** A superconductor expels magnetic flux from its interior.  The London equation quantifies this screening.
- **Penetration Depth:** Typical values are 20–200 nm for conventional superconductors, meaning screening currents flow in a thin surface layer.
- **Type-I vs Type-II:** This simulation applies to the Meissner state of Type-I superconductors (and Type-II below $H_{c1}$).  Vortex states are not modelled.

### 6. Assumptions and Limitations

| Assumption | Implication |
|---|---|
| **Local electrodynamics** | The London equation is local — the current at a point depends only on the field at that point.  Non-local (Piper–Casimir) effects are neglected. |
| **Isotropic material** | $\lambda$ is assumed scalar.  Anisotropic superconductors (e.g., HTSC) have direction-dependent $\lambda$. |
| **Uniform $n_s$** | The superfluid density is assumed constant throughout the bulk. |
| **Below $H_c$** | The London equation is valid only in the Meissner state, below the critical field. |
| **Gorter–Casimir model** | The $(T/T_c)^4$ law is approximate; BCS theory gives a more accurate temperature dependence. |
| **Separable approximation (rectangle)** | The product-of-slabs formula neglects corner coupling; it is exact only for infinite slabs. |

### 7. References

1. Tinkham, M. *Introduction to Superconductivity*, 2nd ed., Dover (2004).
2. London, F. & London, H., "The Electromagnetic Equations of the Supraconductor", *Proc. Roy. Soc. A* **149**, 71–88 (1935).
3. Gorter, C. J. & Casimir, H. B. G., *Phys. Z.* **35**, 963 (1934).
4. Ashcroft, N. W. & Mermin, N. D., *Solid State Physics*, Harcourt (1976), Ch. 34.
5. Kittel, C., *Introduction to Solid State Physics*, 8th ed., Wiley (2005), Ch. 12.
    """)


# ═══════════════════════════════════════════════════════════════════════
# Footer
# ═══════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.9em;'>"
    "London Penetration Depth Simulator &nbsp;|&nbsp; "
    "Solid State Physics Assignment &nbsp;|&nbsp; "
    "Built with Python, Streamlit & Matplotlib"
    "</div>",
    unsafe_allow_html=True,
)
