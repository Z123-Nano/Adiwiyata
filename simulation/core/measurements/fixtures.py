"""Synthetic measurement / observation fixtures — TASK 012.
Every synthetic entry labeled is_synthetic_example=True and notes say test/example.
No real garden measurements; no invented survey values.
Lux preserved as lux; no PPFD conversion; no parameter fitting.
"""
from datetime import datetime, timezone
from simulation.core.contracts.domain import Measurement, Observation

# A. Numeric measurement — illuminance (lux, not PPFD), synthetic
SYNTH_ILLUMINANCE = Measurement(
    id="m-synth-ill-001",
    timestamp=datetime(2026, 6, 21, 12, 0, 0, tzinfo=timezone.utc),
    variable="illuminance",
    value=8200.0,
    unit="lux",
    location_target_id="tier-1-cell-a",
    instrument="handheld-lux-meter",
    instrument_id=None,  # not actually known — not invented
    method="direct_reading_at_receiver_height_1m",
    observer_source="test_example_not_real_garden",
    uncertainty=150.0,
    provenance="synthetic_example_for_TASK_012; not calibrated; not compared to LightField",
    quality_flag="example",
    notes="Synthetic fixture — raw value 8200 lux preserved; no smoothing, no conversion.",
    is_synthetic_example=True,
)

# B. Temperature measurement — synthetic
SYNTH_TEMPERATURE = Measurement(
    id="m-synth-temp-001",
    timestamp=datetime(2026, 6, 21, 12, 30, 0, tzinfo=timezone.utc),
    variable="temperature",
    value=22.5,
    unit="C",
    location_target_id="g1",
    spatial_ref={"x": 0.5, "y": 1.0, "z": 0.0},
    instrument="digital-thermometer",
    method="shielded_air_at_1m",
    observer_source="test_example",
    uncertainty=None,  # unknown — must not become zero
    provenance="synthetic_example",
    is_synthetic_example=True,
)

# C. Soil moisture — synthetic (measurement) with unknown uncertainty
SYNTH_SOIL_MOISTURE = Measurement(
    id="m-synth-soil-001",
    timestamp=datetime(2026, 6, 21, 11, 0, 0, tzinfo=timezone.utc),
    variable="soil_moisture",
    value=0.32,
    unit="m3/m3",
    instrument="tensiometer",
    method="gravimetric_reference_not_applied",
    observer_source="test_example",
    uncertainty=None,
    provenance="synthetic_example; no calibration performed",
    is_synthetic_example=True,
)

# D. Categorical / structured observation — phenological stage (non-numeric)
SYNTH_PHENO_OBS = Observation(
    id="o-synth-pheno-001",
    timestamp=datetime(2026, 6, 21, 10, 0, 0, tzinfo=timezone.utc),
    target_id="plant-p1",
    observation_type="phenological_stage",
    category="structured",
    content="Flowering observed on lower inflorescence; not full bloom.",
    structured_attributes={"stage": "flowering_early", "percent_open": 30},
    value_numeric=None,  # not a measurement
    unit=None,
    observer_source="test_example",
    method="visual_inspection_10min_interval",
    notes="Synthetic observation — no biological interpretation; recording only.",
    provenance="synthetic_example_for_TASK_012",
    is_synthetic_example=True,
)

# E. Event observation — transplant event
SYNTH_TRANSPLANT_OBS = Observation(
    id="o-synth-tp-001",
    timestamp=datetime(2026, 6, 21, 9, 0, 0, tzinfo=timezone.utc),
    target_id="plant-p2",
    observation_type="intervention_event",
    category="event",
    content="Transplant from seedling_tray to container; root disturbance minimal.",
    structured_attributes={"from_container": "tray-3", "to_container": "pot-c1"},
    observer_source="test_example",
    provenance="synthetic_example",
    is_synthetic_example=True,
)

SYNTHETIC_MEASUREMENTS = [SYNTH_ILLUMINANCE, SYNTH_TEMPERATURE, SYNTH_SOIL_MOISTURE]
SYNTHETIC_OBSERVATIONS = [SYNTH_PHENO_OBS, SYNTH_TRANSPLANT_OBS]
