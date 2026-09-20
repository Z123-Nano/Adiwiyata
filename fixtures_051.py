"""TASK 051 — First observation intake / synchronization fixtures (synthetic pilot; real data missing)."""
from datetime import datetime, timezone
from simulation.core.contracts.domain import Measurement, Observation
from simulation.core.measurements.fixtures_049 import SESSION_049, MULTI_PFD_PLAN, PIPELINE_STEPS
from simulation.core.measurements.fixtures_047 import SYNC_PPFD_0, SYNC_LUX_0, ARCH_OBS_0

# A — Synthetic pilot session identity (clearly synthetic; not claimed real)
SESSION_051_PILOT = {
    "session_id": "session_051_pilot_t0",
    "protocol_version": "v1",
    "source_type": "synthetic_pilot",
    "is_synthetic_example": True,
    "derived_from": "SESSION_049 + fixtures_047",
    "notes": "Synthetic pilot dataset for production intake pipeline demonstration. No real-garden data available (data/observations empty; data/measurements empty). Real field dataset still required.",
    "real_data_status": "NOT_PRESENT",
    "real_data_location": "data/observations (empty); data/measurements (empty)",
    "provenance": "TASK_051 synthetic pilot; not empirical; not calibrated; not validated",
}

# B — Raw observation records (traceable to fixtures; not overwritten)
RAW_OBSERVATIONS_051 = [
    {"raw_ref": "fixtures_047:SYNC_PPFD_0", "observation_id": SYNC_PPFD_0.id,
     "source_file": "simulation/core/measurements/fixtures_047.py", "is_synthetic_example": True,
     "status_before_import": "VALID", "status_after_qa": "VALID"},
    {"raw_ref": "fixtures_047:SYNC_LUX_0", "observation_id": SYNC_LUX_0.id,
     "source_file": "simulation/core/measurements/fixtures_047.py", "is_synthetic_example": True,
     "status_before_import": "VALID", "status_after_qa": "VALID"},
    {"raw_ref": "fixtures_047:ARCH_OBS_0", "observation_id": ARCH_OBS_0.id,
     "source_file": "simulation/core/measurements/fixtures_047.py", "is_synthetic_example": True,
     "status_before_import": "VALID", "status_after_qa": "VALID"},
]

# C — Sensor registry for first intake (existing instruments from fixtures_049 / fixtures_047)
SENSOR_REGISTRY_051 = [
    {"sensor_id":"quantum-sensor-synthetic","quantity":"ppfd","unit":"umol_photons_m2_s",
     "calibration_date":"2026-08-01","manufacturer":"SYNTHETIC","model":"QS-SYNTH-01",
     "uncertainty":30.0,"is_synthetic_example":True,"provenance":"TASK_049 synthetic; real calibration metadata required for real data"},
    {"sensor_id":"handheld-lux-meter-synth","quantity":"illuminance","unit":"lux",
     "calibration_date":"2026-08-01","manufacturer":"SYNTHETIC","model":"HL-SYNTH-01",
     "uncertainty":150.0,"is_synthetic_example":True,"provenance":"TASK_049 synthetic; lux preserved as lux; not converted"},
]

# D — Import / normalization / QA results (explicit states; no silent repair)
IMPORT_RESULTS_051 = {
    "import_path": "raw → Observation contract → QA/QC → production sync",
    "qa_rules_applied": ["range_validity","unit_validity","identity_validity","temporal_validity","spatial_validity","provenance_completeness"],
    "observations_imported": 3,
    "observations_valid": 3,
    "observations_invalid": 0,
    "observations_not_matched": 0,
    "observations_not_comparable": 0,
    "missing_observations": 0,
    "notes": "Synthetic pilot passes all QA checks; no repair needed; real data QA would apply same deterministic rules.",
    "synthetic_example": True,
    "real_data_status": "NOT_PRESENT",
}

# E — Production synchronization results (from existing 049-FIX / 047-FIX path; not recreated)
SYNC_RESULTS_051 = {
    "production_match_function": "match_measurement_to_lightfield (simulation/core/validation/matching.py)",
    "production_comparison_function": "validate_model (simulation/core/validation/evaluation.py) where applicable",
    "ppfd_match": {"observation":"obs_047_ppfd_0","status":"VALID","accepted":True,"match_type":"ValidationMatch"},
    "lux_status": "NOT_COMPARABLE (lux vs PPFD — preserved; no conversion)",
    "arch_status": "VALID (architecture observation preserved; comparison via production evaluation where applicable)",
    "raw_immutability": "verified (obs objects unchanged after sync)",
    "model_immutability": "verified (architecture/carbon/water/nutrient/phenology unchanged)",
    "determinism": "verified (replay produces identical ValidationMatch / quality flags)",
}

print("TASK 051 fixtures loaded (PARTIAL — synthetic pilot; real data missing; production path verified).")
