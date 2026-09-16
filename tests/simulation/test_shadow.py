"""Direct shadow tests — TASK 009. Analytical reference + sanity."""
from simulation.core.shadow.direct import sun_direction_from_solar, shadow_length_vertical_box, direct_shadow
from simulation.core.shadow.model import Occluder, SolarPosition
from simulation.core.solar.model import SolarLocation
from simulation.core.solar.calculate import calculate_solar_position
from datetime import datetime, timezone

def test_sun_direction_unit():
    sun = calculate_solar_position(SolarLocation(latitude_deg=40, longitude_deg=-74), datetime(2026, 6, 21, 12, 0, 0, tzinfo=timezone.utc))
    d = sun_direction_from_solar(sun)
    # Downward component negative when sun above horizon
    assert d.dz < 0
    mag = (d.dx**2 + d.dy**2 + d.dz**2)**0.5
    assert abs(mag - 1.0) < 1e-6

def test_shadow_length_high_alt():
    # High sun -> short shadow
    L = shadow_length_vertical_box(1.0, 60.0)
    assert L < 1.0
    assert L > 0

def test_shadow_length_low_alt():
    # Low sun -> long shadow
    L = shadow_length_vertical_box(1.0, 10.0)
    assert L > 5.0

def test_shadow_length_below_horizon():
    assert shadow_length_vertical_box(1.0, -5.0) == 0.0

def test_shadow_direction_opposite_sun():
    occluder = Occluder(id="wall", position=(0,0,0), dimensions=(1,1,2), height_m=2.0)
    sun = calculate_solar_position(SolarLocation(latitude_deg=40, longitude_deg=-74), datetime(2026, 6, 21, 12, 0, 0, tzinfo=timezone.utc))
    res = direct_shadow(occluder, sun)
    # Shadow direction should be opposite sun azimuth
    expected_dir = (sun.azimuth_deg + 180.0) % 360.0
    assert abs(res.shadow_direction_deg - expected_dir) < 1e-3

def test_no_shadow_below_horizon():
    occluder = Occluder(id="w", position=(0,0,0), height_m=2.0)
    # Force low alt via manual SolarPosition
    sun = SolarPosition(timestamp=datetime.now(timezone.utc), latitude_deg=40, longitude_deg=-74, azimuth_deg=180, altitude_deg=-10, zenith_deg=100, above_horizon=False, method="test")
    res = direct_shadow(occluder, sun)
    assert res.sun_above_horizon is False
    assert res.shadowed is False
    assert res.shadow_length_m is None

def test_receiver_shadowed():
    # Vertical wall at (0,0), receiver directly behind (along shadow direction from sun az ~180 => shadow dir ~0)
    occluder = Occluder(id="w", position=(0,0,0), height_m=2.0)
    # Sun az 180 (south) -> shadow dir 0 (north); receiver at (0,1,0) should be shadowed if L > 1
    sun = SolarPosition(timestamp=datetime.now(timezone.utc), latitude_deg=40, longitude_deg=-74, azimuth_deg=180.0, altitude_deg=45.0, zenith_deg=45.0, above_horizon=True, method="test")
    res = direct_shadow(occluder, sun, receiver_pos=(0.1, 1.5, 0))
    # At alt 45, L = 2 / tan(45) = 2; receiver at y=1.5 within 2
    assert res.shadowed is True

def test_receiver_outside_shadow():
    occluder = Occluder(id="w", position=(0,0,0), height_m=2.0)
    sun = SolarPosition(timestamp=datetime.now(timezone.utc), latitude_deg=40, longitude_deg=-74, azimuth_deg=180.0, altitude_deg=45.0, zenith_deg=45.0, above_horizon=True, method="test")
    res = direct_shadow(occluder, sun, receiver_pos=(0.1, 3.0, 0))
    assert res.shadowed is False

def test_shadow_length_vs_altitude():
    # Analytical: L = h / tan(alt); at 30° L=1.73; at 60° L=0.58
    for alt, expected_approx in [(30, 1.73), (60, 0.58)]:
        L = shadow_length_vertical_box(1.0, alt)
        assert abs(L - expected_approx) < 0.05
