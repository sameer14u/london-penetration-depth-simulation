"""
london_physics.py — Core physics module for London penetration depth simulation.

This module implements the London theory for magnetic-field penetration
into superconducting/diamagnetic materials. It provides:

  - Temperature-dependent London penetration depth (Gorter–Casimir two-fluid model)
  - Analytical field profiles for slab, cylinder, and rectangular geometries
  - 2D field-map generators for visualisation (colour maps + streamplots)
  - Comparison utilities across temperatures, applied fields, and geometries

All internal calculations use SI units (metres, Tesla, Kelvin).
The user interface converts to/from nm for display.

Theory
------
The London brothers (F. & H. London, 1935) proposed a phenomenological
equation governing the magnetic-field distribution inside a superconductor:

    ∇²B = B / λ_L²

where λ_L is the London penetration depth.  The field decays exponentially
from the surface with characteristic length λ_L.  The temperature dependence
is modelled by the Gorter–Casimir two-fluid relation:

    λ(T) = λ₀ / √(1 − (T/Tc)⁴)

where λ₀ is the zero-temperature penetration depth and Tc is the critical
temperature.

References
----------
[1] Tinkham, M. "Introduction to Superconductivity", 2nd ed., Dover (2004).
[2] London, F. & London, H., Proc. Roy. Soc. A149, 71 (1935).
[3] Gorter, C. J. & Casimir, H. B. G., Phys. Z. 35, 963 (1934).
"""

import numpy as np
from scipy.special import i0, i1
from typing import Tuple, List, Dict, Optional

# ═══════════════════════════════════════════════════════════════════════
# Physical constants
# ═══════════════════════════════════════════════════════════════════════
MU_0: float = 4.0 * np.pi * 1e-7       # Vacuum permeability  (T·m/A)
PHI_0: float = 2.0678e-15               # Magnetic flux quantum (Wb)
K_B: float = 1.380649e-23               # Boltzmann constant   (J/K)

# ═══════════════════════════════════════════════════════════════════════
# Predefined superconducting materials
# Tc in Kelvin, lambda_0 in nanometres
# ═══════════════════════════════════════════════════════════════════════
MATERIALS: Dict[str, Dict[str, Optional[float]]] = {
    "Niobium (Nb)":    {"Tc": 9.26,  "lambda_0": 39.0},
    "Lead (Pb)":       {"Tc": 7.19,  "lambda_0": 37.0},
    "Aluminium (Al)":  {"Tc": 1.18,  "lambda_0": 16.0},
    "Tin (Sn)":        {"Tc": 3.72,  "lambda_0": 34.0},
    "Mercury (Hg)":    {"Tc": 4.15,  "lambda_0": 38.0},
    "YBCO":            {"Tc": 92.0,  "lambda_0": 150.0},
    "Custom":          {"Tc": None,  "lambda_0": None},
}


# ═══════════════════════════════════════════════════════════════════════
# Temperature-dependent penetration depth
# ═══════════════════════════════════════════════════════════════════════
def london_penetration_depth(lambda_0: float, T: float, Tc: float) -> float:
    """Compute the temperature-dependent London penetration depth.

    Uses the Gorter–Casimir two-fluid model:

        λ(T) = λ₀ / √(1 − (T/Tc)⁴)

    Parameters
    ----------
    lambda_0 : float
        Zero-temperature penetration depth (metres).
    T : float
        Temperature (K).
    Tc : float
        Critical temperature (K).

    Returns
    -------
    float
        Penetration depth λ(T) in metres.  Returns np.inf if T ≥ Tc
        (material is in the normal state and the Meissner effect vanishes).
    """
    if T >= Tc:
        return np.inf
    t4 = (T / Tc) ** 4
    return lambda_0 / np.sqrt(1.0 - t4)


# ═══════════════════════════════════════════════════════════════════════
# 1-D field profiles
# ═══════════════════════════════════════════════════════════════════════
def field_slab(x: np.ndarray, B0: float, lambda_L: float, d: float) -> np.ndarray:
    """Magnetic-field profile B(x) for an infinite slab of thickness *d*.

    The slab occupies −d/2 ≤ x ≤ d/2.  An external uniform field B₀ is
    applied perpendicular to the slab faces.

    Solution of ∇²B = B/λ² with boundary conditions B(±d/2) = B₀:

        B(x) = B₀ · cosh(x/λ) / cosh(d/(2λ))       (inside)
        B(x) = B₀                                    (outside)

    Parameters
    ----------
    x : ndarray
        Position array (metres), centred at 0.
    B0 : float
        Applied magnetic field (Tesla).
    lambda_L : float
        London penetration depth (metres).
    d : float
        Slab thickness (metres).

    Returns
    -------
    ndarray
        Magnetic field magnitude at each position.
    """
    B = np.full_like(x, B0, dtype=float)
    inside = np.abs(x) <= d / 2.0

    if lambda_L <= 0 or np.isinf(lambda_L):
        # λ → ∞  means full penetration; λ ≤ 0 is unphysical
        if np.isinf(lambda_L):
            B[inside] = B0
        else:
            B[inside] = 0.0
        return B

    # Numerically stable cosh ratio: cosh(a)/cosh(b) = exp(a-b)*(1+exp(-2a))/(1+exp(-2b))
    half_d = d / 2.0
    arg_x = np.abs(x[inside]) / lambda_L
    arg_d = half_d / lambda_L

    if arg_d > 500:
        # Overflow-safe: ratio ≈ exp(|x|/λ − d/(2λ))
        ratio = np.exp(arg_x - arg_d)
    else:
        ratio = np.cosh(arg_x) / np.cosh(arg_d)

    B[inside] = B0 * np.clip(ratio, 0.0, 1.0)
    return B


def field_cylinder(r: np.ndarray, B0: float, lambda_L: float, R: float) -> np.ndarray:
    """Magnetic-field profile B(r) for a long cylinder of radius *R*.

    The cylinder axis is along z.  The external field B₀ is applied along z.

    Solution of the London equation in cylindrical coordinates:

        B(r) = B₀ · I₀(r/λ) / I₀(R/λ)       (r ≤ R)
        B(r) = B₀                              (r > R)

    where I₀ is the modified Bessel function of the first kind, order 0.

    Parameters
    ----------
    r : ndarray
        Radial distance from cylinder axis (metres).
    B0 : float
        Applied magnetic field (Tesla).
    lambda_L : float
        London penetration depth (metres).
    R : float
        Cylinder radius (metres).

    Returns
    -------
    ndarray
        Magnetic field magnitude at each radial position.
    """
    B = np.full_like(r, B0, dtype=float)
    inside = r <= R

    if lambda_L <= 0 or np.isinf(lambda_L):
        if np.isinf(lambda_L):
            B[inside] = B0
        else:
            B[inside] = 0.0
        return B

    r_in = r[inside] / lambda_L
    R_norm = R / lambda_L

    if R_norm > 500:
        # For large arguments, I0(x) ≈ exp(x)/sqrt(2πx)
        # I0(r/λ)/I0(R/λ) ≈ sqrt(R/r)*exp((r-R)/λ)
        r_safe = np.maximum(r[inside], 1e-30)
        ratio = np.sqrt(R / r_safe) * np.exp((r[inside] - R) / lambda_L)
    else:
        i0_r = i0(r_in)
        i0_R = i0(R_norm)
        ratio = i0_r / i0_R

    B[inside] = B0 * np.clip(ratio, 0.0, 1.0)
    return B


def field_rectangle_2d(X: np.ndarray, Y: np.ndarray, B0: float,
                       lambda_L: float, a: float, b: float) -> np.ndarray:
    """2-D field distribution B(x,y) for a rectangular cross-section.

    Uses the product-of-slabs separable approximation:

        B(x,y) = B₀ · [cosh(x/λ)/cosh(a/(2λ))] · [cosh(y/λ)/cosh(b/(2λ))]

    inside the rectangle (|x| ≤ a/2, |y| ≤ b/2), and B₀ outside.

    **Limitation:** This is an approximation valid when the two transverse
    dimensions decouple.  Corner effects and coupling terms are neglected.

    Parameters
    ----------
    X, Y : ndarray
        2-D meshgrid arrays of positions (metres).
    B0 : float
        Applied field (Tesla).
    lambda_L : float
        Penetration depth (metres).
    a : float
        Width of rectangle along x (metres).
    b : float
        Height of rectangle along y (metres).

    Returns
    -------
    ndarray
        2-D array of magnetic field magnitude.
    """
    Bz = np.full_like(X, B0, dtype=float)
    inside = (np.abs(X) <= a / 2.0) & (np.abs(Y) <= b / 2.0)

    if lambda_L <= 0 or np.isinf(lambda_L):
        if np.isinf(lambda_L):
            Bz[inside] = B0
        else:
            Bz[inside] = 0.0
        return Bz

    # x-factor
    arg_x = np.abs(X[inside]) / lambda_L
    arg_a = a / (2.0 * lambda_L)
    if arg_a > 500:
        fx = np.exp(arg_x - arg_a)
    else:
        fx = np.cosh(arg_x) / np.cosh(arg_a)

    # y-factor
    arg_y = np.abs(Y[inside]) / lambda_L
    arg_b = b / (2.0 * lambda_L)
    if arg_b > 500:
        fy = np.exp(arg_y - arg_b)
    else:
        fy = np.cosh(arg_y) / np.cosh(arg_b)

    Bz[inside] = B0 * np.clip(fx * fy, 0.0, 1.0)
    return Bz


# ═══════════════════════════════════════════════════════════════════════
# 2-D field-map generators (for colour maps and streamplots)
# ═══════════════════════════════════════════════════════════════════════

def compute_slab_2d(B0: float, lambda_L: float, d: float,
                    nx: int = 300, ny: int = 300,
                    padding_factor: float = 3.0
                    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray,
                               np.ndarray, np.ndarray]:
    """Compute 2-D field map for an infinite slab.

    The slab extends from −d/2 to d/2 along x (the penetration direction)
    and is infinite along y.  The applied field B₀ is along y (vertical
    in the plot).

    Returns
    -------
    X, Y : ndarray
        Coordinate grids (metres).
    Bz : ndarray
        Magnitude of the magnetic field |B| at each point.
    Bx, By : ndarray
        Vector components for streamplot.  The field is primarily along y,
        deflected around the slab.
    """
    extent = d * padding_factor / 2.0
    x = np.linspace(-extent, extent, nx)
    y = np.linspace(-extent, extent, ny)
    X, Y = np.meshgrid(x, y)

    # Scalar field magnitude
    # For the slab, field penetrates from both faces.  The applied field
    # is along y.  Inside the slab, By decays; outside, By = B0.
    Bz = field_slab(X, B0, lambda_L, d)

    # Vector field for streamplot
    # Applied field is in the y-direction.  Inside slab it is attenuated.
    # Outside slab, field lines squeeze together at the surface.
    By = Bz.copy()
    Bx = np.zeros_like(X)

    return X, Y, Bz, Bx, By


def compute_cylinder_2d(B0: float, lambda_L: float, R: float,
                        nx: int = 300, ny: int = 300,
                        padding_factor: float = 3.0
                        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray,
                                   np.ndarray, np.ndarray]:
    """Compute 2-D field map for a long cylinder (cross-section).

    The cylinder axis is along z (out of the page).  The applied field B₀ is
    along y (vertical).  We compute the (x,y) cross-section.

    Outside the cylinder the field is the superposition of the uniform
    applied field and the diamagnetic (dipole) response:

        Bx_ext = −B₀ R² · 2xy / r⁴
        By_ext = B₀ (1 + R²(y²−x²)/r⁴ )          (exact 2-D dipole)

    Inside the cylinder the longitudinal field (along the applied direction)
    follows the Bessel-function solution.

    Returns
    -------
    X, Y, Bz, Bx, By : ndarray
    """
    extent = R * padding_factor
    x = np.linspace(-extent, extent, nx)
    y = np.linspace(-extent, extent, ny)
    X, Y = np.meshgrid(x, y)

    r2 = X**2 + Y**2
    r2_safe = np.where(r2 < 1e-30, 1e-30, r2)
    r = np.sqrt(r2_safe)

    inside = r <= R
    outside = ~inside

    # ----- Interior (Bessel solution) ----- #
    Bz = np.full_like(X, B0, dtype=float)
    if not np.isinf(lambda_L) and lambda_L > 0:
        r_in = r[inside] / lambda_L
        R_norm = R / lambda_L
        if R_norm > 500:
            r_safe = np.maximum(r[inside], 1e-30)
            ratio = np.sqrt(R / r_safe) * np.exp((r[inside] - R) / lambda_L)
        else:
            ratio = i0(r_in) / i0(R_norm)
        Bz[inside] = B0 * np.clip(ratio, 0.0, 1.0)
    elif np.isinf(lambda_L):
        Bz[inside] = B0  # full penetration
    else:
        Bz[inside] = 0.0

    # ----- Exterior (uniform + diamagnetic dipole) ----- #
    # Perfect diamagnet in a uniform field B₀ ŷ produces a 2-D dipole
    # distortion.  The total exterior field in Cartesian:
    #   Bx = -B0 * R² * 2*x*y / r⁴
    #   By = B0 * (1 + R² * (y²-x²) / r⁴ )
    Bx = np.zeros_like(X)
    By = np.zeros_like(Y)

    r4 = r2_safe**2
    Bx[outside] = -B0 * R**2 * 2.0 * X[outside] * Y[outside] / r4[outside]
    By[outside] = B0 * (1.0 + R**2 * (Y[outside]**2 - X[outside]**2) / r4[outside])

    # Inside: field is along applied direction (y), magnitude from Bessel
    By[inside] = Bz[inside]
    Bx[inside] = 0.0

    # Update Bz as total magnitude for colour map
    Bz[outside] = np.sqrt(Bx[outside]**2 + By[outside]**2)

    return X, Y, Bz, Bx, By


def compute_rectangle_2d(B0: float, lambda_L: float, a: float, b: float,
                         nx: int = 300, ny: int = 300,
                         padding_factor: float = 3.0
                         ) -> Tuple[np.ndarray, np.ndarray, np.ndarray,
                                    np.ndarray, np.ndarray]:
    """Compute 2-D field map for a rectangular cross-section.

    The applied field is along y.  Inside the rectangle, the field
    magnitude follows the product-of-slabs approximation.  Outside,
    the field is taken as the uniform applied field (the exterior
    distortion for a rectangle has no simple closed form; we use B₀
    as the far-field value, smoothly transitioning at the boundary).

    Returns
    -------
    X, Y, Bz, Bx, By : ndarray
    """
    extent_x = a * padding_factor / 2.0
    extent_y = b * padding_factor / 2.0
    extent = max(extent_x, extent_y)
    x = np.linspace(-extent, extent, nx)
    y = np.linspace(-extent, extent, ny)
    X, Y = np.meshgrid(x, y)

    Bz = field_rectangle_2d(X, Y, B0, lambda_L, a, b)

    # Vector field: applied field along y
    By = Bz.copy()
    Bx = np.zeros_like(X)

    return X, Y, Bz, Bx, By


# ═══════════════════════════════════════════════════════════════════════
# 1-D field-vs-distance profiles (for line plots)
# ═══════════════════════════════════════════════════════════════════════

def field_vs_distance_slab(B0: float, lambda_L: float, d: float,
                           n_points: int = 500
                           ) -> Tuple[np.ndarray, np.ndarray]:
    """Compute B(x) across a slab from −2d to +2d.

    Returns
    -------
    x : ndarray  — position (metres)
    B : ndarray  — magnetic field (Tesla)
    """
    x = np.linspace(-2.0 * d, 2.0 * d, n_points)
    B = field_slab(x, B0, lambda_L, d)
    return x, B


def field_vs_distance_cylinder(B0: float, lambda_L: float, R: float,
                               n_points: int = 500
                               ) -> Tuple[np.ndarray, np.ndarray]:
    """Compute B(r) from r = 0 to r = 3R for a cylinder.

    Returns
    -------
    r : ndarray  — radial distance (metres)
    B : ndarray  — magnetic field (Tesla)
    """
    r = np.linspace(0, 3.0 * R, n_points)
    B = field_cylinder(r, B0, lambda_L, R)
    return r, B


# ═══════════════════════════════════════════════════════════════════════
# Comparison utilities
# ═══════════════════════════════════════════════════════════════════════

def compare_temperatures(B0: float, lambda_0: float, Tc: float,
                         geometry: str, dimensions: dict,
                         temperatures: List[float]
                         ) -> List[Tuple[str, np.ndarray, np.ndarray]]:
    """Compute field profiles at multiple temperatures for comparison.

    Parameters
    ----------
    B0 : float
        Applied field (T).
    lambda_0 : float
        Zero-temperature penetration depth (m).
    Tc : float
        Critical temperature (K).
    geometry : str
        'slab', 'cylinder', or 'rectangular'.
    dimensions : dict
        Geometry-specific dimensions in metres:
        {'d': ...} for slab, {'R': ...} for cylinder,
        {'a': ..., 'b': ...} for rectangular.
    temperatures : list of float
        Temperatures (K) at which to evaluate.

    Returns
    -------
    list of (label, x_or_r, B) tuples
    """
    results = []
    for T in temperatures:
        lam = london_penetration_depth(lambda_0, T, Tc)
        label = f"T = {T:.2f} K  (λ = {lam*1e9:.1f} nm)" if not np.isinf(lam) else f"T = {T:.2f} K  (normal)"

        if geometry == "slab":
            x, B = field_vs_distance_slab(B0, lam, dimensions["d"])
        elif geometry == "cylinder":
            x, B = field_vs_distance_cylinder(B0, lam, dimensions["R"])
        else:  # rectangular — use a 1-D cut along x at y=0
            d_eff = dimensions["a"]
            x, B = field_vs_distance_slab(B0, lam, d_eff)

        results.append((label, x, B))
    return results


def compare_fields(B0_values: List[float], lambda_L: float,
                   geometry: str, dimensions: dict
                   ) -> List[Tuple[str, np.ndarray, np.ndarray]]:
    """Compute field profiles for multiple applied-field strengths.

    Parameters
    ----------
    B0_values : list of float
        Applied field values (T).
    lambda_L : float
        Penetration depth (m).
    geometry : str
        'slab', 'cylinder', or 'rectangular'.
    dimensions : dict
        Geometry-specific dimensions (m).

    Returns
    -------
    list of (label, x_or_r, B) tuples
    """
    results = []
    for B0 in B0_values:
        label = f"B₀ = {B0:.3f} T"
        if geometry == "slab":
            x, B = field_vs_distance_slab(B0, lambda_L, dimensions["d"])
        elif geometry == "cylinder":
            x, B = field_vs_distance_cylinder(B0, lambda_L, dimensions["R"])
        else:
            x, B = field_vs_distance_slab(B0, lambda_L, dimensions["a"])
        results.append((label, x, B))
    return results


def compare_geometries(B0: float, lambda_L: float,
                       slab_d: float, cyl_R: float,
                       rect_a: float, rect_b: float
                       ) -> List[Tuple[str, np.ndarray, np.ndarray]]:
    """Compare field penetration across geometries.

    For a fair comparison the distance is normalised from the surface
    inward.  We return (label, depth_from_surface, B/B0).

    Parameters
    ----------
    B0 : float
        Applied field (T).
    lambda_L : float
        Penetration depth (m).
    slab_d, cyl_R, rect_a, rect_b : float
        Dimensions (m).

    Returns
    -------
    list of (label, depth, B/B0)
    """
    n = 500
    results = []

    # Slab: distance from surface = d/2 - |x|
    x_slab = np.linspace(0, slab_d / 2.0, n)
    B_slab = field_slab(x_slab, B0, lambda_L, slab_d)
    depth_slab = slab_d / 2.0 - x_slab  # depth from surface
    results.append(("Slab", depth_slab, B_slab / B0))

    # Cylinder: depth from surface = R - r
    r_cyl = np.linspace(0, cyl_R, n)
    B_cyl = field_cylinder(r_cyl, B0, lambda_L, cyl_R)
    depth_cyl = cyl_R - r_cyl
    results.append(("Cylinder", depth_cyl, B_cyl / B0))

    # Rectangle: 1-D cut along x at y=0
    x_rect = np.linspace(0, rect_a / 2.0, n)
    B_rect = field_slab(x_rect, B0, lambda_L, rect_a)
    depth_rect = rect_a / 2.0 - x_rect
    results.append(("Rectangular", depth_rect, B_rect / B0))

    return results
