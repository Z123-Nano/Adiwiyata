"""TASK 049 — Synthetic measurement-acquisition fixtures (prototype protocol)."""
from datetime import datetime, timezone
from simulation.core.contracts.domain import Measurement, Observation
from simulation.core.measurements.fixtures_047 import SYNC_PPFD_0, SYNC_LUX_0, ARCH_OBS_0

# 1. Garden geometry / coordinate frame (explicit; registered to G0)
GARDEN_PROBE = {
    "boundary_shape":"L-shaped",
    "reference_point":"G0",
    "frame":"+X East / +Y North / +Z Up",
    "units":"m",
    "note":"Spatial hierarchy: Garden → Rack → Tier → Container → Plant (per CLAUDE.md)",
    "synthetic_example":True,
}

# 2. Plant identity registry (persistent IDs — not row/index)
PLANT_REGISTRY = [
    {"plant_id":"P001","species":"Solanum_lycopersicum","cultivar":"UNKNOWN","container_id":"C01","install_date":"2026-05-01","identity_confidence":"high","notes":"Synthetic registry; stable across observations"},
    {"plant_id":"P002","species":"Solanum_lycopersicum","cultivar":"UNKNOWN","container_id":"C02","install_date":"2026-05-01","identity_confidence":"high","notes":"Synthetic registry"},
]

# 3. Sensor registry (explicit metadata; synthetic)
SENSOR_REGISTRY = [
    {"sensor_id":"ppfd_ref_01","type":"quantum_sensor","manufacturer":"Synthetic","model":"QM-01","calibration_date":"2026-09-01","uncertainty_abs":25.0,"unit":"umol_photons_m2_s","orientation":"horizontal_at_z=0","note":"Explicit; not invented; calibration reference required for real use","is_synthetic_example":True},
    {"sensor_id":"lux_01","type":"lux_meter","manufacturer":"Synthetic","model":"LX-01","calibration_date":"2026-09-01","uncertainty_abs":150.0,"unit":"lux","orientation":"horizontal_at_1m","note":"Lux preserved; no PPFD conversion","is_synthetic_example":True},
]

# 4. Measurement session (reproducible protocol; explicit provenance)
SESSION_049 = {
    "session_id":"session_049_t0",
    "start_time":"2026-09-19T12:00:00Z",
    "end_time":"2026-09-19T12:30:00Z",
    "operator":"synthetic_protocol",
    "weather_context":"synthetic_clear",
    "coordinate_frame":"garden_local_G0",
    "sensor_inventory":["ppfd_ref_01","lux_01"],
    "protocol_version":"v1",
    "notes":"Synthetic pilot session; not empirical validation; no calibration performed.",
    "is_synthetic_example":True,
}

# 5. Multi-PPFD measurement design (addressing 048 identifiability requirement)
MULTI_PFD_PLAN = {
    "description":"Multi-PPFD series required to separate alpha / pmax (TASK 048); at least 3 levels.",
    "levels": [
        {"label":"low","target_ppfd_approx":200,"method":"under-canopy / shaded reference"},
        {"label":"mid","target_ppfd_approx":400,"method":"representative organ location"},
        {"label":"high","target_ppfd_approx":800,"method":"above-canopy / open reference"},
    ],
    "temporal_resolution":"per-step (3600s); series at same session or consecutive days",
    "spatial_resolution":"organ-level where feasible; fixed sensor points for reference",
    "replicate":"sensor repeat at each point; plant-level biological replicate separate",
    "note":"Synthetic design; real sensor calibration required before any fitting.",
    "is_synthetic_example":True,
}

# 6. Acquisition pipeline (synthetic end-to-end test reference)
PIPELINE_STEPS = [
    "session_start",
    "sensor_inventory_check",
    "spatial_registration_G0",
    "PPFD_reference_measurement_046O_path",
    "arch_measurement_046K_path",
    "environment_measurement",
    "quality_check",
    "raw_store",
    "processed_observation_contract",
    "TASK_047_sync",
    "observed_vs_simulated",
    "dataset_role_assign",
]
