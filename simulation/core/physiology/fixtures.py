"""Synthetic physiology fixtures — TASK 019. Explicit placeholders; no invented values."""
from datetime import datetime, timezone
from simulation.core.physiology.contracts import PlantPhysiologyState, LightInput, EnvironmentInput, PhotosynthesisResult

SYNTH_STATE = PlantPhysiologyState(
    plant_id="plant-p1",
    timestamp=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc),
    gross_carbon_assimilation=None,
    respiration_carbon_loss=None,
    net_carbon=None,
    carbon_pool_g=None,
    carbon_allocation_state=None,
    plant_water_status=None,
    root_zone_water_ref=None,
    transpiration_rate_ref=None,
    nitrogen_status=None,
    phosphorus_status=None,
    potassium_status=None,
    nutrient_limitation=None,
    stomatal_conductance_ref=None,
    co2_reference_ppm=None,
    plant_temperature_c=None,
    thermal_state=None,
    status="NOT_IMPLEMENTED",
    uncertainty_status="not_modelled",
    model_ref=None,
    provenance="synthetic_fixture_TASK_019; placeholders only; no equations",
    notes="All biological quantities unavailable — contract only.",
    is_synthetic_example=True,
)

SYNTH_LIGHT_INPUT = LightInput(
    source="LightField",
    sample_ref="sample-001",
    variable="relative_normalized",
    value=0.72,
    unit="relative_normalized",
    timestamp=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc),
    provenance="synthetic_TASK_019; lux not converted; relative_normalized preserved",
    is_synthetic_example=True,
)

SYNTH_PHOTOSYNTHESIS_RESULT = PhotosynthesisResult(
    status="NOT_IMPLEMENTED",
    gross_assimilation=None,
    limiting_factors=["model_not_available"],
    provenance="synthetic_TASK_019; no equation implemented",
    notes="Photosynthesis process not implemented; placeholder only.",
    is_synthetic_example=True,
)
