"""Light approximation tests — TASK 010. Invariants + analytical reference."""
from simulation.core.light.approximation import diffuse_approximation, reflected_approximation, combined_light
from simulation.core.light.contracts import DiffuseApproximation, ReflectedApproximation, LightComponents

def test_diffuse_night_zero():
    d = diffuse_approximation(1.0, -5.0)
    assert d.diffuse_output == 0.0
    assert d.daylight_factor == 0.0

def test_diffuse_day_full_sky():
    d = diffuse_approximation(1.0, 45.0)
    assert d.diffuse_output == 1.0
    assert d.sky_visibility_fraction == 1.0

def test_diffuse_reduced_sky():
    d = diffuse_approximation(0.5, 30.0)
    assert d.diffuse_output == 0.5

def test_diffuse_complete_shadow_keeps_diffuse():
    d = diffuse_approximation(0.8, 30.0)
    assert d.diffuse_output > 0.4

def test_reflected_zero_reflectance():
    r = reflected_approximation(0.0, 1.0, 0.8)
    assert r.reflected_output == 0.0

def test_reflected_increases_with_reflectance():
    r1 = reflected_approximation(0.2, 1.0, 1.0)
    r2 = reflected_approximation(0.8, 1.0, 1.0)
    assert r2.reflected_output > r1.reflected_output
    assert r2.reflected_output <= 1.0

def test_reflected_non_negative():
    r = reflected_approximation(0.5, 0.5, 0.5)
    assert r.reflected_output >= 0.0

def test_reflected_bounded():
    r = reflected_approximation(1.0, 1.0, 1.0, coeff=1.0)
    assert r.reflected_output <= 1.0

def test_combined_separate_identity():
    c = combined_light(0.8, DiffuseApproximation(sky_visibility_fraction=1.0, daylight_factor=1.0, diffuse_output=0.6, daylight_baseline=1.0), ReflectedApproximation(surface_reflectance=0.3, visible_surface_fraction=0.5, incident_environmental=0.5, reflection_coefficient=0.3, reflected_output=0.045))
    assert c.direct == 0.8
    assert c.diffuse == 0.6
    assert c.reflected == 0.045
    assert c.unit == "relative_normalized"

def test_diffuse_bound_01():
    d = diffuse_approximation(2.0, 45.0)
    assert d.sky_visibility_fraction == 1.0
    assert d.diffuse_output <= 1.0
