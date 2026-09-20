"""TASK 046M fixtures — solar + architecture for integration."""
from simulation.core.solar.model import SolarPosition
from datetime import datetime, timezone
from simulation.core.architecture.fixtures_046m_a import ARCH_3ORG

SOLAR_NOON = SolarPosition(
    timestamp=datetime(2026, 9, 17, 12, 0, 0, tzinfo=timezone.utc),
    latitude_deg=45.0, longitude_deg=10.0,
    azimuth_deg=180.0, altitude_deg=60.0, zenith_deg=30.0,
    above_horizon=True, method="synthetic",
)
ARCH_A = ARCH_3ORG
