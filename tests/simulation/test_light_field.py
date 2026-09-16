"""LightField tests — TASK 011. Analytical/invariant; synthetic only."""
from simulation.core.light.field.contracts import LightSample, LightField
from simulation.core.light.field.compute import compute_lightfield
from simulation.core.solar.model import SolarLocation
from simulation.core.solar.calculate import calculate_solar_position
from simulation.core.shadow.model import Occluder
from datetime import datetime, timezone

def test_empty_open_scene_day():
    solar = calculate_solar_position(SolarLocation(latitude_deg=40, longitude_deg=-74), datetime(2026, 6, 21, 12, 0, 0, tzinfo=timezone.utc))
    field = compute_lightfield(solar, (0, 4, 0, 3), (5, 4))
    assert len(field.samples) == 20
    s = field.samples[0]
    assert s.direct > 0
    assert s.diffuse > 0
    assert s.total == s.direct + s.diffuse + s.reflected
    assert s.unit == "relative_normalized"

def test_night_direct_and_diffuse_daylight_zero():
    solar = calculate_solar_position(SolarLocation(latitude_deg=40, longitude_deg=-74), datetime(2026, 6, 21, 2, 0, 0, tzinfo=timezone.utc))
    field = compute_lightfield(solar, (0, 2, 0, 2), (3, 3))
    for s in field.samples:
        assert s.direct == 0.0
        assert s.diffuse == 0.0  # night => daylight factor 0
        assert s.reflected >= 0.0

def test_direct_shadow_reduces_direct_keeps_diffuse():
    solar = calculate_solar_position(SolarLocation(latitude_deg=40, longitude_deg=-74), datetime(2026, 6, 21, 12, 0, 0, tzinfo=timezone.utc))
    occ = Occluder(id="wall", position=(2, 0, 0), dimensions=(0.2, 2, 2), height_m=2.0)
    # Sample inside shadow (near wall base along shadow direction from sun az ~81° -> shadow dir ~261°)
    # Approximate: point at (2, 1) likely shadowed; open point at (0.5, 0.5) likely direct
    field = compute_lightfield(solar, (0, 4, 0, 3), (4, 4), occluders=[occ])
    # At least some direct=0 with diffuse>0
    shadowed_samples = [s for s in field.samples if s.direct == 0.0 and s.diffuse > 0]
    assert len(shadowed_samples) > 0
    direct_samples = [s for s in field.samples if s.direct > 0.0]
    assert len(direct_samples) > 0

def test_spatial_variation_different_direct():
    solar = calculate_solar_position(SolarLocation(latitude_deg=40, longitude_deg=-74), datetime(2026, 6, 21, 12, 0, 0, tzinfo=timezone.utc))
    occ = Occluder(id="w", position=(2, 0, 0), dimensions=(0.2, 2, 2), height_m=2.0)
    field = compute_lightfield(solar, (0, 4, 0, 3), (4, 4), occluders=[occ])
    vals = [s.direct for s in field.samples]
    assert max(vals) > min(vals)

def test_resolution_increases_samples():
    solar = calculate_solar_position(SolarLocation(latitude_deg=40, longitude_deg=-74), datetime(2026, 6, 21, 12, 0, 0, tzinfo=timezone.utc))
    f1 = compute_lightfield(solar, (0, 2, 0, 2), (2, 2))
    f2 = compute_lightfield(solar, (0, 2, 0, 2), (4, 4))
    assert len(f2.samples) == 4 * len(f1.samples)

def test_sample_positions_deterministic():
    solar = calculate_solar_position(SolarLocation(latitude_deg=40, longitude_deg=-74), datetime(2026, 6, 21, 12, 0, 0, tzinfo=timezone.utc))
    f1 = compute_lightfield(solar, (0, 2, 0, 2), (3, 3))
    f2 = compute_lightfield(solar, (0, 2, 0, 2), (3, 3))
    assert [s.x for s in f1.samples] == [s.x for s in f2.samples]

def test_component_identity_preserved():
    solar = calculate_solar_position(SolarLocation(latitude_deg=40, longitude_deg=-74), datetime(2026, 6, 21, 12, 0, 0, tzinfo=timezone.utc))
    field = compute_lightfield(solar, (0, 2, 0, 2), (3, 3))
    s = field.samples[0]
    assert s.total == s.direct + s.diffuse + s.reflected
    assert s.direct >= 0 and s.diffuse >= 0 and s.reflected >= 0
    assert s.unit == "relative_normalized"

def test_invalid_resolution_rejected():
    solar = calculate_solar_position(SolarLocation(latitude_deg=40, longitude_deg=-74), datetime(2026, 6, 21, 12, 0, 0, tzinfo=timezone.utc))
    try:
        compute_lightfield(solar, (0, 2, 0, 2), (0, 3))
        assert False
    except ValueError:
        pass
