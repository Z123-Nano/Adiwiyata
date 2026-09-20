"""TASK 046O fixtures — explicit measured PPFD and invalid cases."""
from datetime import datetime, timezone
from simulation.core.contracts.domain import Measurement
from simulation.core.physiology.ppfd_source import PPFDSource

# Valid measured PPFD — synthetic fixture labeled
MEASURED_PPFD_01 = Measurement(
    id="m-ppfd-001",
    timestamp=datetime(2026, 9, 18, 12, 0, 0, tzinfo=timezone.utc),
    variable="PPFD",
    value=450.0,
    unit="umol_photons_m2_s",
    location_target_id="leaf_1",
    spatial_ref={"x": 1.0, "y": 0.5, "z": 1.0},
    instrument="quantum-sensor-A",
    method="direct_par_sensor_at_receiver",
    observer_source="field_campaign_2026",
    uncertainty=25.0,
    provenance="TASK_046O synthetic measured PPFD fixture; not derived from LightField; not converted from lux",
    quality_flag="valid",
    notes="Explicit physical PPFD measurement; PAR 400-700 nm; valid for 046C integration.",
    is_synthetic_example=True,
)

# Zero PPFD — valid measurement
MEASURED_PPFD_ZERO = Measurement(
    id="m-ppfd-zero-001",
    timestamp=datetime(2026, 9, 18, 10, 30, 0, tzinfo=timezone.utc),
    variable="PPFD",
    value=0.0,
    unit="umol_photons_m2_s",
    instrument="quantum-sensor-A",
    method="direct_par_sensor",
    provenance="TASK_046O synthetic zero PPFD; valid; not missing.",
    is_synthetic_example=True,
)

# Invalid — lux (must be rejected)
MEASURED_LUX = Measurement(
    id="m-lux-001",
    timestamp=datetime(2026, 9, 18, 12, 0, 0, tzinfo=timezone.utc),
    variable="illuminance",
    value=8200.0,
    unit="lux",
    instrument="lux-meter",
    provenance="TASK_046O synthetic lux fixture; must NOT become PPFD",
    is_synthetic_example=True,
)

# Invalid — relative_normalized (must be rejected)
MEASURED_REL = Measurement(
    id="m-rel-001",
    timestamp=datetime(2026, 9, 18, 12, 0, 0, tzinfo=timezone.utc),
    variable="relative_normalized",
    value=0.85,
    unit="relative_normalized",
    provenance="TASK_046O synthetic relative_normalized; must NOT become PPFD",
    is_synthetic_example=True,
)

# Invalid — negative PPFD
MEASURED_NEG = Measurement(
    id="m-neg-001",
    timestamp=datetime(2026, 9, 18, 12, 0, 0, tzinfo=timezone.utc),
    variable="PPFD",
    value=-50.0,
    unit="umol_photons_m2_s",
    provenance="TASK_046O synthetic negative; must be rejected",
    is_synthetic_example=True,
)
