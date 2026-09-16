"""Synthetic validation fixtures — TASK 013. Labeled is_synthetic_example=True.
No real measurements; lux preserved; no conversion; no calibration."""
from datetime import datetime, timezone
from simulation.core.contracts.domain import Measurement
from simulation.core.measurements.fixtures import SYNTH_ILLUMINANCE

# A. Exact spatial match (same x,y as LightField sample at grid point)
SYNTH_MEASURE_EXACT = Measurement(
    id="m-val-exact-001",
    timestamp=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc),
    variable="illuminance",
    value=8200.0,
    unit="lux",
    spatial_ref={"x": 0.0, "y": 0.0, "z": 1.0},
    observer_source="test_example",
    is_synthetic_example=True,
    provenance="synthetic_validation_fixture_TASK_013; not calibrated; lux stays lux",
)

# B. Near match (within 0.4m of sample at (1,1))
SYNTH_MEASURE_NEAR = Measurement(
    id="m-val-near-001",
    timestamp=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc),
    variable="illuminance",
    value=7500.0,
    unit="lux",
    spatial_ref={"x": 1.05, "y": 1.02, "z": 1.0},
    observer_source="test_example",
    is_synthetic_example=True,
    provenance="synthetic_validation_fixture_TASK_013",
)

# C. Too far (should reject) — >0.5m from nearest sample at (2,2)
SYNTH_MEASURE_FAR = Measurement(
    id="m-val-far-001",
    timestamp=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc),
    variable="illuminance",
    value=3000.0,
    unit="lux",
    spatial_ref={"x": 10.0, "y": 10.0, "z": 1.0},
    observer_source="test_example",
    is_synthetic_example=True,
    provenance="synthetic_validation_fixture_TASK_013; expects distance-threshold rejection",
)

# D. Timestamp mismatch (different time — should flag/reject if temporal gate active)
SYNTH_MEASURE_TIME_BAD = Measurement(
    id="m-val-time-001",
    timestamp=datetime(2026,6,21,2,0,0,tzinfo=timezone.utc),
    variable="illuminance",
    value=200.0,
    unit="lux",
    spatial_ref={"x": 0.0, "y": 0.0, "z": 1.0},
    observer_source="test_example",
    is_synthetic_example=True,
    provenance="synthetic_validation_fixture_TASK_013; expects temporal mismatch flag",
)

# E. Observation (non-numeric) for structural check
SYNTH_OBS_STRUCT = Measurement(
    id="m-val-obs-001",
    timestamp=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc),
    variable="phenological_stage",
    value=0,  # not numeric light; observation style
    unit="category",
    spatial_ref={"x": 0.0, "y": 0.0},
    observer_source="test_example",
    is_synthetic_example=True,
    provenance="synthetic_validation_fixture_TASK_013; observation-style; not compared numerically",
)
