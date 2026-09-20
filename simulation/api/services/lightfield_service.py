"""LightField service — delegates to domain compute; no duplication of physics."""
from datetime import datetime, timezone
from simulation.core.light.field.compute import compute_lightfield
from simulation.core.solar.model import SolarPosition
from simulation.core.light.field.contracts import LightField as DomainLightField

def compute_lightfield_service(grid_bounds=(0,5,0,5), grid_res=(8,8), z_height=0.0):
    # Synthetic solar for demonstration / fixture mode; domain remains source of truth
    solar = SolarPosition(
        timestamp=datetime(2026, 6, 21, 12, 0, 0, tzinfo=timezone.utc),
        latitude_deg=51.5,
        longitude_deg=0.0,
        azimuth_deg=180.0,
        altitude_deg=45.0,
        zenith_deg=45.0,
        above_horizon=True,
    )
    result: DomainLightField = compute_lightfield(solar, grid_bounds, grid_res, z_height, occluders=[])
    return result
