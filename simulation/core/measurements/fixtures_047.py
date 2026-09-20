"""TASK 047 — Synthetic observation fixtures (synthetic only; no empirical claim)."""
from datetime import datetime, timezone
from simulation.core.contracts.domain import Measurement, Observation
from simulation.core.contracts.domain import PlantArchitecture
from simulation.core.contracts.domain import PlantOrgan

# A — Measured PPFD (absolute, PAR, explicit identity)
SYNC_PPFD_0 = Measurement(
    id="obs_047_ppfd_0", timestamp=datetime(2026,9,19,12,0,0,tzinfo=timezone.utc),
    variable="ppfd", value=420.0, unit="umol_photons_m2_s",
    location_target_id="org_leaf_1_046AF", spatial_ref={"x":1.0,"y":2.0,"z":0.5,"frame":"garden_local","note":"+X East / +Y North / +Z Up"},
    instrument="quantum-sensor-synthetic", method="direct_sensor_at_leaf_1",
    observer_source="synthetic_047_example", uncertainty=30.0,
    provenance="TASK_047 synthetic PPFD measurement; not empirical; matched to organ_leaf_1_046AF",
    quality_flag="VALID", notes="Synthetic measured PPFD at t0; preserved as absolute umol_photons_m2_s; no lux conversion.",
    is_synthetic_example=True)

# B — Illuminance lux (preserved as lux; NOT converted to PPFD)
SYNC_LUX_0 = Measurement(
    id="obs_047_lux_0", timestamp=datetime(2026,9,19,12,0,0,tzinfo=timezone.utc),
    variable="illuminance", value=8200.0, unit="lux",
    location_target_id="tier-1-cell-a",
    instrument="handheld-lux-meter-synth", method="direct_reading",
    observer_source="synthetic_047_example", uncertainty=150.0,
    provenance="TASK_047 synthetic lux; preserved as lux; no implicit PPFD conversion",
    quality_flag="VALID", notes="Lux remains lux; NOT comparable to PPFD directly; NOT used for photosynthesis input.",
    is_synthetic_example=True)

# C — Architecture observation (spatial, explicit identity)
ARCH_OBS_0 = Observation(
    id="obs_047_arch_0", timestamp=datetime(2026,9,19,12,0,0,tzinfo=timezone.utc),
    observation_type="architecture_spatial", target_plant_id="p1", target_organ_id="leaf_1",
    spatial_ref={"x":1.0,"y":2.0,"z":0.5,"frame":"garden_local"},
    value_numeric=0.23, unit="m", content="architecture_spatial", quality_flag="VALID", variable="organ_length",
    observer_source="synthetic_047_example", uncertainty=0.02,
    provenance="TASK_047 synthetic architecture observation; compared to model length 0.15 (t0) / 0.20 (t1); discrepancy stored",
    is_synthetic_example=True)

# D — Wrong organ identity (NOT_MATCHED expected)
SYNC_PPFD_BAD_ORGAN = Measurement(
    id="obs_047_ppfd_bad_organ", timestamp=datetime(2026,9,19,12,0,0,tzinfo=timezone.utc),
    variable="ppfd", value=500.0, unit="umol_photons_m2_s",
    location_target_id="unknown_organ_99",
    observer_source="synthetic_047_bad_organ", uncertainty=20.0,
    provenance="TASK_047 synthetic; wrong organ identity → NOT_MATCHED",
    quality_flag="NOT_MATCHED", notes="Target organ identity does not exist in current architecture; no nearest-organ guess.",
    is_synthetic_example=True)

# E — Wrong timestamp (NOT_MATCHED / NOT_COMPARABLE expected at t2)
SYNC_PPFD_BAD_TIME = Measurement(
    id="obs_047_ppfd_bad_time", timestamp=datetime(2026,9,19,10,0,0,tzinfo=timezone.utc),
    variable="ppfd", value=380.0, unit="umol_photons_m2_s",
    location_target_id="org_leaf_1_046AF",
    observer_source="synthetic_047_bad_time", uncertainty=25.0,
    provenance="TASK_047 synthetic; time 10:00 vs simulation 12:00 t0 → temporal mismatch",
    quality_flag="NOT_MATCHED", notes="Observation timestamp does not match target simulation timestep; not silently carried.",
    is_synthetic_example=True)