"""Solar position calculation — pure function, deterministic, timezone-aware."""
from datetime import datetime
import pvlib
from simulation.core.solar.model import SolarPosition, SolarLocation

# Convention document: azimuth clockwise from true North; altitude positive = above horizon.
# No magnetic bearing used.

def calculate_solar_position(location: SolarLocation, timestamp: datetime) -> SolarPosition:
    if timestamp.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware")
    # pvlib expects datetime with tzinfo; converts to UTC internally
    sol = pvlib.solarposition.get_solarposition(
        time=timestamp,
        latitude=location.latitude_deg,
        longitude=location.longitude_deg,
    )
    # sol columns: zenith, azimuth; pvlib azimuth clockwise from north; altitude = 90 - zenith
    az = float(sol.azimuth.iloc[0])
    zen = float(sol.zenith.iloc[0])
    alt = 90.0 - zen
    # Normalize azimuth to [0, 360)
    az = az % 360.0
    above = alt > 0.0
    return SolarPosition(
        timestamp=timestamp,
        latitude_deg=location.latitude_deg,
        longitude_deg=location.longitude_deg,
        azimuth_deg=round(az, 4),
        altitude_deg=round(alt, 4),
        zenith_deg=round(zen, 4),
        above_horizon=above,
    )
