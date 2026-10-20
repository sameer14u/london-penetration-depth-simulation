"""
generate_figures.py — Generate all figures for the report and screenshots.

This script produces publication-quality figures showing:
1. 2D field visualisation for each geometry
2. 1D field profiles
3. Temperature dependence
4. Geometry comparison
5. Parameter studies

All figures are saved to the figures/ directory.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import os

from london_physics import (
    MATERIALS, london_penetration_depth,
    field_slab, field_cylinder, field_rectangle_2d,
    compute_slab_2d, compute_cylinder_2d, compute_rectangle_2d,
    field_vs_distance_slab, field_vs_distance_cylinder,
    compare_temperatures, compare_fields, compare_geometries,
)

# Setup
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

FIG_DIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# Material: Niobium
Tc = 9.26
lambda_0 = 39e-9  # metres
T = 4.0  # K
B0 = 0.1  # T
lambda_T = london_penetration_depth(lambda_0, T, Tc)
lambda_T_nm = lambda_T * 1e9

d = 500e-9       # slab thickness
R = 250e-9       # cylinder radius
a = 500e-9       # rectangle width
b = 400e-9       # rectangle height

print(f"Niobium: Tc={Tc} K, lambda_0={lambda_0*1e9:.0f} nm")
print(f"T={T} K → lambda(T)={lambda_T_nm:.2f} nm")
print(f"Slab d={d*1e9:.0f} nm, Cylinder R={R*1e9:.0f} nm, Rect {a*1e9:.0f}×{b*1e9:.0f} nm")
print()

# ═══════════════════════════════════════════════════════════════════════
# Figure 1: 2D Field Visualisation — Slab
# ═══════════════════════════════════════════════════════════════════════
print("Generating Figure 1: 2D Slab...")
X, Y, Bz, Bx, By = compute_slab_2d(B0, lambda_T, d, 300, 300)
X_nm, Y_nm = X * 1e9, Y * 1e9
B_norm = Bz / B0

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

cf = ax1.contourf(X_nm, Y_nm, B_norm, levels=50, cmap="RdBu_r", vmin=0, vmax=1.0)
ax1.contour(X_nm, Y_nm, B_norm, levels=10, colors="k", linewidths=0.4, alpha=0.5)
fig.colorbar(cf, ax=ax1, label="B / B_0", shrink=0.85)
for xb in [-d*1e9/2, d*1e9/2]:
    ax1.axvline(xb, color="white", ls="--", lw=1.5)
ax1.set_xlabel("x (nm)")
ax1.set_ylabel("y (nm)")
ax1.set_title("Field Magnitude |B|/B_0 — Slab")
ax1.set_aspect("equal")

ax2.contourf(X_nm, Y_nm, B_norm, levels=50, cmap="RdBu_r", alpha=0.4, vmin=0, vmax=1.0)
speed = np.sqrt(Bx**2 + By**2)
lw = 2.0 * speed / (speed.max() + 1e-30)
ax2.streamplot(X_nm, Y_nm, Bx, By, color="navy", linewidth=lw, density=1.5, arrowsize=1.0)
for xb in [-d*1e9/2, d*1e9/2]:
    ax2.axvline(xb, color="red", ls="--", lw=1.5)
ax2.set_xlabel("x (nm)")
ax2.set_ylabel("y (nm)")
ax2.set_title("Magnetic Field Lines — Slab")
ax2.set_aspect("equal")

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig1_2d_slab.png"), bbox_inches="tight")
plt.close(fig)
print("  Saved fig1_2d_slab.png")

# ═══════════════════════════════════════════════════════════════════════
# Figure 2: 2D Field Visualisation — Cylinder
# ═══════════════════════════════════════════════════════════════════════
print("Generating Figure 2: 2D Cylinder...")
X, Y, Bz, Bx, By = compute_cylinder_2d(B0, lambda_T, R, 300, 300)
X_nm, Y_nm = X * 1e9, Y * 1e9
B_norm = Bz / B0

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

cf = ax1.contourf(X_nm, Y_nm, B_norm, levels=50, cmap="RdBu_r", vmin=0, vmax=1.5)
ax1.contour(X_nm, Y_nm, B_norm, levels=10, colors="k", linewidths=0.4, alpha=0.5)
fig.colorbar(cf, ax=ax1, label="B / B_0", shrink=0.85)
circle = plt.Circle((0, 0), R*1e9, fill=False, ec="white", ls="--", lw=1.5)
ax1.add_patch(circle)
ax1.set_xlabel("x (nm)")
ax1.set_ylabel("y (nm)")
ax1.set_title("Field Magnitude |B|/B_0 — Cylinder")
ax1.set_aspect("equal")

ax2.contourf(X_nm, Y_nm, B_norm, levels=50, cmap="RdBu_r", alpha=0.4, vmin=0, vmax=1.5)
speed = np.sqrt(Bx**2 + By**2)
lw = 2.0 * speed / (speed.max() + 1e-30)
ax2.streamplot(X_nm, Y_nm, Bx, By, color="navy", linewidth=lw, density=1.5, arrowsize=1.0)
circle2 = plt.Circle((0, 0), R*1e9, fill=False, ec="red", ls="--", lw=1.5)
ax2.add_patch(circle2)
ax2.set_xlabel("x (nm)")
ax2.set_ylabel("y (nm)")
ax2.set_title("Magnetic Field Lines — Cylinder (Meissner Effect)")
ax2.set_aspect("equal")

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig2_2d_cylinder.png"), bbox_inches="tight")
plt.close(fig)
print("  Saved fig2_2d_cylinder.png")

# ═══════════════════════════════════════════════════════════════════════
# Figure 3: 2D Field Visualisation — Rectangle
# ═══════════════════════════════════════════════════════════════════════
print("Generating Figure 3: 2D Rectangle...")
X, Y, Bz, Bx, By = compute_rectangle_2d(B0, lambda_T, a, b, 300, 300)
X_nm, Y_nm = X * 1e9, Y * 1e9
B_norm = Bz / B0

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

cf = ax1.contourf(X_nm, Y_nm, B_norm, levels=50, cmap="RdBu_r", vmin=0, vmax=1.0)
ax1.contour(X_nm, Y_nm, B_norm, levels=10, colors="k", linewidths=0.4, alpha=0.5)
fig.colorbar(cf, ax=ax1, label="B / B_0", shrink=0.85)
rect = Rectangle((-a*1e9/2, -b*1e9/2), a*1e9, b*1e9, fill=False, ec="white", ls="--", lw=1.5)
ax1.add_patch(rect)
ax1.set_xlabel("x (nm)")
ax1.set_ylabel("y (nm)")
ax1.set_title("Field Magnitude |B|/B_0 — Rectangular")
ax1.set_aspect("equal")

ax2.contourf(X_nm, Y_nm, B_norm, levels=50, cmap="RdBu_r", alpha=0.4, vmin=0, vmax=1.0)
speed = np.sqrt(Bx**2 + By**2)
lw = 2.0 * speed / (speed.max() + 1e-30)
ax2.streamplot(X_nm, Y_nm, Bx, By, color="navy", linewidth=lw, density=1.5, arrowsize=1.0)
rect2 = Rectangle((-a*1e9/2, -b*1e9/2), a*1e9, b*1e9, fill=False, ec="red", ls="--", lw=1.5)
ax2.add_patch(rect2)
ax2.set_xlabel("x (nm)")
ax2.set_ylabel("y (nm)")
ax2.set_title("Magnetic Field Lines — Rectangular")
ax2.set_aspect("equal")

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig3_2d_rectangle.png"), bbox_inches="tight")
plt.close(fig)
print("  Saved fig3_2d_rectangle.png")

# ═══════════════════════════════════════════════════════════════════════
# Figure 4: 1D Field Profiles
# ═══════════════════════════════════════════════════════════════════════
print("Generating Figure 4: 1D Profiles...")
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Slab
x, B = field_vs_distance_slab(B0, lambda_T, d)
axes[0].plot(x*1e9, B/B0, "b-", lw=2, label="B(x)/B_0")
axes[0].axvline(-d*1e9/2, color="gray", ls="--", lw=1)
axes[0].axvline(d*1e9/2, color="gray", ls="--", lw=1)
depth_ref = np.linspace(0, d*1e9/2, 200)
axes[0].plot(d*1e9/2 - depth_ref, np.exp(-depth_ref/lambda_T_nm), "r--", lw=1.5, alpha=0.7, label=f"exp(-x/lambda)")
axes[0].set_xlabel("Position x (nm)")
axes[0].set_ylabel("B / B_0")
axes[0].set_title(f"Slab (d = {d*1e9:.0f} nm)")
axes[0].legend(fontsize=9)
axes[0].set_ylim(-0.05, 1.15)
axes[0].grid(True, alpha=0.3)

# Cylinder
r, B = field_vs_distance_cylinder(B0, lambda_T, R)
axes[1].plot(r*1e9, B/B0, "b-", lw=2, label="B(r)/B_0")
axes[1].axvline(R*1e9, color="gray", ls="--", lw=1)
depth_ref = np.linspace(0, R*1e9, 200)
axes[1].plot(R*1e9 - depth_ref, np.exp(-depth_ref/lambda_T_nm), "r--", lw=1.5, alpha=0.7, label=f"exp(-x/lambda)")
axes[1].set_xlabel("Radial distance r (nm)")
axes[1].set_ylabel("B / B_0")
axes[1].set_title(f"Cylinder (R = {R*1e9:.0f} nm)")
axes[1].legend(fontsize=9)
axes[1].set_ylim(-0.05, 1.15)
axes[1].grid(True, alpha=0.3)

# Rectangular (x-cut)
x = np.linspace(-2*a, 2*a, 500)
B = field_slab(x, B0, lambda_T, a)
axes[2].plot(x*1e9, B/B0, "b-", lw=2, label="B(x)/B_0 (y=0)")
axes[2].axvline(-a*1e9/2, color="gray", ls="--", lw=1)
axes[2].axvline(a*1e9/2, color="gray", ls="--", lw=1)
axes[2].set_xlabel("Position x (nm)")
axes[2].set_ylabel("B / B_0")
axes[2].set_title(f"Rectangular (a = {a*1e9:.0f} nm, b = {b*1e9:.0f} nm)")
axes[2].legend(fontsize=9)
axes[2].set_ylim(-0.05, 1.15)
axes[2].grid(True, alpha=0.3)

fig.suptitle(f"1D Field Profiles — Niobium, T = {T} K, lambda(T) = {lambda_T_nm:.1f} nm, B_0 = {B0} T", fontsize=14, y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig4_1d_profiles.png"), bbox_inches="tight")
plt.close(fig)
print("  Saved fig4_1d_profiles.png")

# ═══════════════════════════════════════════════════════════════════════
# Figure 5: Temperature Dependence
# ═══════════════════════════════════════════════════════════════════════
print("Generating Figure 5: Temperature dependence...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

T_fracs = [0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]
T_values = [f * Tc for f in T_fracs]
results = compare_temperatures(B0, lambda_0, Tc, "slab", {"d": d}, T_values)

cmap_t = plt.cm.coolwarm
for i, (label, x, B) in enumerate(results):
    colour = cmap_t(i / (len(results) - 1))
    ax1.plot(x * 1e9, B / B0, "-", color=colour, lw=1.5, label=label)

ax1.axvline(-d*1e9/2, color="gray", ls="--", lw=0.8)
ax1.axvline(d*1e9/2, color="gray", ls="--", lw=0.8)
ax1.set_xlabel("Position x (nm)")
ax1.set_ylabel("B / B_0")
ax1.set_title("Field Penetration at Various Temperatures — Slab")
ax1.legend(fontsize=7, loc="upper right")
ax1.set_ylim(-0.05, 1.15)
ax1.grid(True, alpha=0.3)

# lambda(T)/lambda_0 vs T/Tc
t_ratio = np.linspace(0.01, 0.999, 500)
lambda_ratio = 1.0 / np.sqrt(1.0 - t_ratio**4)
ax2.plot(t_ratio, lambda_ratio, "b-", lw=2)
ax2.axhline(1.0, color="gray", ls=":", lw=0.8)
t_cur = T / Tc
lam_cur = 1.0 / np.sqrt(1.0 - t_cur**4)
ax2.plot(t_cur, lam_cur, "ro", ms=10, zorder=5, label=f"T = {T} K (T/Tc = {t_cur:.2f})")
ax2.set_xlabel("T / Tc")
ax2.set_ylabel("lambda(T) / lambda_0")
ax2.set_title("Gorter–Casimir: Penetration Depth vs. Temperature")
ax2.set_ylim(0.5, 10)
ax2.set_xlim(0, 1)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig5_temperature_dependence.png"), bbox_inches="tight")
plt.close(fig)
print("  Saved fig5_temperature_dependence.png")

# ═══════════════════════════════════════════════════════════════════════
# Figure 6: Geometry Comparison
# ═══════════════════════════════════════════════════════════════════════
print("Generating Figure 6: Geometry comparison...")

# 2D maps side by side
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

Xs, Ys, Bzs, _, _ = compute_slab_2d(B0, lambda_T, d, 200, 200)
im0 = axes[0].contourf(Xs*1e9, Ys*1e9, Bzs/B0, levels=50, cmap="RdBu_r", vmin=0, vmax=1.0)
for xb in [-d*1e9/2, d*1e9/2]:
    axes[0].axvline(xb, color="white", ls="--", lw=1.2)
axes[0].set_title(f"Slab (d = {d*1e9:.0f} nm)")
axes[0].set_xlabel("x (nm)")
axes[0].set_ylabel("y (nm)")
axes[0].set_aspect("equal")
fig.colorbar(im0, ax=axes[0], label="B/B_0", shrink=0.8)

Xc, Yc, Bzc, _, _ = compute_cylinder_2d(B0, lambda_T, R, 200, 200)
im1 = axes[1].contourf(Xc*1e9, Yc*1e9, Bzc/B0, levels=50, cmap="RdBu_r", vmin=0, vmax=1.5)
circle_c = plt.Circle((0, 0), R*1e9, fill=False, ec="white", ls="--", lw=1.2)
axes[1].add_patch(circle_c)
axes[1].set_title(f"Cylinder (R = {R*1e9:.0f} nm)")
axes[1].set_xlabel("x (nm)")
axes[1].set_ylabel("y (nm)")
axes[1].set_aspect("equal")
fig.colorbar(im1, ax=axes[1], label="B/B_0", shrink=0.8)

Xr, Yr, Bzr, _, _ = compute_rectangle_2d(B0, lambda_T, a, b, 200, 200)
im2 = axes[2].contourf(Xr*1e9, Yr*1e9, Bzr/B0, levels=50, cmap="RdBu_r", vmin=0, vmax=1.0)
rect_c = Rectangle((-a*1e9/2, -b*1e9/2), a*1e9, b*1e9, fill=False, ec="white", ls="--", lw=1.2)
axes[2].add_patch(rect_c)
axes[2].set_title(f"Rectangular ({a*1e9:.0f}×{b*1e9:.0f} nm)")
axes[2].set_xlabel("x (nm)")
axes[2].set_ylabel("y (nm)")
axes[2].set_aspect("equal")
fig.colorbar(im2, ax=axes[2], label="B/B_0", shrink=0.8)

fig.suptitle(f"Geometry Comparison — lambda(T) = {lambda_T_nm:.1f} nm, B_0 = {B0} T", fontsize=14, y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig6_geometry_comparison_2d.png"), bbox_inches="tight")
plt.close(fig)
print("  Saved fig6_geometry_comparison_2d.png")

# 1D depth comparison
geo_results = compare_geometries(B0, lambda_T, d, R, a, b)
fig, ax = plt.subplots(figsize=(10, 6))
colours_g = ["#1f77b4", "#ff7f0e", "#2ca02c"]
for (label, depth, B_ratio), colour in zip(geo_results, colours_g):
    ax.plot(depth * 1e9, B_ratio, "-", color=colour, lw=2, label=label)
d_ref = np.linspace(0, max(d, 2*R, a)*1e9/2, 200)
ax.plot(d_ref, np.exp(-d_ref / lambda_T_nm), "k--", lw=1, alpha=0.5,
         label=f"exp(-x/lambda), lambda = {lambda_T_nm:.1f} nm")
ax.set_xlabel("Depth from surface (nm)")
ax.set_ylabel("B / B_0")
ax.set_title("Normalised Field vs. Depth — All Geometries")
ax.legend(fontsize=10)
ax.set_ylim(-0.05, 1.15)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig7_geometry_comparison_1d.png"), bbox_inches="tight")
plt.close(fig)
print("  Saved fig7_geometry_comparison_1d.png")

# ═══════════════════════════════════════════════════════════════════════
# Figure 7: Parameter Study — Varying lambda
# ═══════════════════════════════════════════════════════════════════════
print("Generating Figure 7: lambda parameter study...")
fig, ax = plt.subplots(figsize=(10, 6))
for lam_nm in [20, 40, 80, 150, 300]:
    lam_m = lam_nm * 1e-9
    x, B = field_vs_distance_slab(B0, lam_m, d)
    ax.plot(x * 1e9, B / B0, "-", lw=1.5, label=f"lambda = {lam_nm} nm")
ax.axvline(-d*1e9/2, color="gray", ls="--", lw=0.8)
ax.axvline(d*1e9/2, color="gray", ls="--", lw=0.8)
ax.set_xlabel("Position x (nm)")
ax.set_ylabel("B / B_0")
ax.set_title(f"Effect of Penetration Depth — Slab (d = {d*1e9:.0f} nm)")
ax.legend(fontsize=10)
ax.set_ylim(-0.05, 1.15)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig8_lambda_study.png"), bbox_inches="tight")
plt.close(fig)
print("  Saved fig8_lambda_study.png")

# ═══════════════════════════════════════════════════════════════════════
# Figure 8: Parameter Study — Varying B_0
# ═══════════════════════════════════════════════════════════════════════
print("Generating Figure 8: B_0 parameter study...")
fig, ax = plt.subplots(figsize=(10, 6))
for B0_val in [0.01, 0.05, 0.1, 0.5]:
    x, B = field_vs_distance_slab(B0_val, lambda_T, d)
    ax.plot(x * 1e9, B, "-", lw=1.5, label=f"B_0 = {B0_val} T")
ax.axvline(-d*1e9/2, color="gray", ls="--", lw=0.8)
ax.axvline(d*1e9/2, color="gray", ls="--", lw=0.8)
ax.set_xlabel("Position x (nm)")
ax.set_ylabel("B (T)")
ax.set_title(f"Field Profiles for Different B_0 — Slab")
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig9_B0_study.png"), bbox_inches="tight")
plt.close(fig)
print("  Saved fig9_B0_study.png")

# ═══════════════════════════════════════════════════════════════════════
# Figure 9: Temperature Dependence — Cylinder
# ═══════════════════════════════════════════════════════════════════════
print("Generating Figure 9: Temperature dependence (cylinder)...")
fig, ax = plt.subplots(figsize=(10, 6))
T_values_cyl = [f * Tc for f in [0.1, 0.3, 0.5, 0.7, 0.9, 0.95]]
results_cyl = compare_temperatures(B0, lambda_0, Tc, "cylinder", {"R": R}, T_values_cyl)
cmap_t = plt.cm.coolwarm
for i, (label, r_arr, B) in enumerate(results_cyl):
    colour = cmap_t(i / (len(results_cyl) - 1))
    ax.plot(r_arr * 1e9, B / B0, "-", color=colour, lw=1.5, label=label)
ax.axvline(R*1e9, color="gray", ls="--", lw=0.8, label="Cylinder surface")
ax.set_xlabel("Radial distance r (nm)")
ax.set_ylabel("B / B_0")
ax.set_title(f"Temperature Dependence — Cylinder (R = {R*1e9:.0f} nm)")
ax.legend(fontsize=7, loc="upper left")
ax.set_ylim(-0.05, 1.15)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig10_temp_cylinder.png"), bbox_inches="tight")
plt.close(fig)
print("  Saved fig10_temp_cylinder.png")

# ═══════════════════════════════════════════════════════════════════════
# Figure 10: Multiple Materials Comparison
# ═══════════════════════════════════════════════════════════════════════
print("Generating Figure 10: Materials comparison...")
fig, ax = plt.subplots(figsize=(10, 6))
materials_to_compare = ["Niobium (Nb)", "Lead (Pb)", "Aluminium (Al)", "YBCO"]
T_compare = 1.0  # K — all materials are superconducting at 1K except check

for mat_name in materials_to_compare:
    mat_data = MATERIALS[mat_name]
    Tc_mat = mat_data["Tc"]
    lam0_mat = mat_data["lambda_0"] * 1e-9
    if T_compare < Tc_mat:
        lam_T = london_penetration_depth(lam0_mat, T_compare, Tc_mat)
        x, B = field_vs_distance_slab(B0, lam_T, d)
        ax.plot(x * 1e9, B / B0, "-", lw=1.5,
                label=f"{mat_name}: lambda(T)={lam_T*1e9:.1f} nm")

ax.axvline(-d*1e9/2, color="gray", ls="--", lw=0.8)
ax.axvline(d*1e9/2, color="gray", ls="--", lw=0.8)
ax.set_xlabel("Position x (nm)")
ax.set_ylabel("B / B_0")
ax.set_title(f"Material Comparison at T = {T_compare} K — Slab (d = {d*1e9:.0f} nm)")
ax.legend(fontsize=9)
ax.set_ylim(-0.05, 1.15)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig11_materials_comparison.png"), bbox_inches="tight")
plt.close(fig)
print("  Saved fig11_materials_comparison.png")

print()
print(f"All figures saved to {FIG_DIR}/")
print("Done.")
