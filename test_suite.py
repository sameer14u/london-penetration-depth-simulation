"""
test_suite.py — Comprehensive unit and physics test suite for London model simulation.
"""
import pytest
import numpy as np
from london_physics import (
    MU_0, PHI_0, MATERIALS,
    london_penetration_depth,
    field_slab, field_cylinder, field_rectangle_2d,
    compute_slab_2d, compute_cylinder_2d, compute_rectangle_2d,
    compare_temperatures, compare_geometries
)

def test_london_penetration_depth_at_zero():
    lam0 = 40e-9
    Tc = 10.0
    # At T=0, lambda = lambda_0
    lam_0 = london_penetration_depth(lam0, 0.0, Tc)
    assert np.isclose(lam_0, lam0)

def test_london_penetration_depth_divergence():
    lam0 = 40e-9
    Tc = 10.0
    # At T = Tc, lambda -> inf
    assert np.isinf(london_penetration_depth(lam0, Tc, Tc))
    assert np.isinf(london_penetration_depth(lam0, 11.0, Tc))

def test_slab_boundary_condition():
    d = 500e-9
    lam = 50e-9
    B0 = 0.2
    # At x = ±d/2, B must equal B0 exactly
    x_b = np.array([-d/2.0, d/2.0])
    B_b = field_slab(x_b, B0, lam, d)
    assert np.allclose(B_b, B0)

def test_slab_screening():
    d = 1000e-9
    lam = 50e-9  # d/lam = 20 (strong screening)
    B0 = 0.5
    x = np.array([0.0])
    B_c = field_slab(x, B0, lam, d)
    # Inside centre should be exponentially small
    assert B_c[0] < 1e-4

def test_cylinder_boundary_condition():
    R = 250e-9
    lam = 40e-9
    B0 = 0.1
    # At r = R, B = B0
    r_b = np.array([R])
    B_b = field_cylinder(r_b, B0, lam, R)
    assert np.isclose(B_b[0], B0)

def test_cylinder_screening():
    R = 500e-9
    lam = 30e-9
    B0 = 0.1
    r_0 = np.array([0.0])
    B_0 = field_cylinder(r_0, B0, lam, R)
    assert B_0[0] < 1e-5

def test_rectangle_symmetry():
    a = 400e-9
    b = 300e-9
    lam = 40e-9
    B0 = 0.1
    X = np.array([[-a/4, a/4], [-a/4, a/4]])
    Y = np.array([[-b/4, -b/4], [b/4, b/4]])
    Bz = field_rectangle_2d(X, Y, B0, lam, a, b)
    assert np.isclose(Bz[0, 0], Bz[0, 1])
    assert np.isclose(Bz[0, 0], Bz[1, 0])

def test_2d_mesh_shapes():
    nx, ny = 50, 60
    X, Y, Bz, Bx, By = compute_slab_2d(0.1, 40e-9, 400e-9, nx=nx, ny=ny)
    assert Bz.shape == (ny, nx)
    assert Bx.shape == (ny, nx)
    assert By.shape == (ny, nx)

if __name__ == '__main__':
    print("Running automated test suite...")
    test_london_penetration_depth_at_zero()
    test_london_penetration_depth_divergence()
    test_slab_boundary_condition()
    test_slab_screening()
    test_cylinder_boundary_condition()
    test_cylinder_screening()
    test_rectangle_symmetry()
    test_2d_mesh_shapes()
    print("ALL TESTS PASSED SUCCESSFULLY (8/8)!")
