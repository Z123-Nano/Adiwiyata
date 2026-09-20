"""TASK 050 — Synthetic environmental integration fixtures (PARTIAL; no invented coupling)."""
from datetime import datetime, timezone
from simulation.core.development.contracts import OrganDevelopmentalState
from simulation.core.water.contracts import RootZoneState, WaterInput, WaterBalanceInput
from simulation.core.nutrient.contracts import NutrientPoolState, NutrientInput, NutrientBalanceInput
from simulation.core.light.field.contracts import LightField
from simulation.core.orchestration.contracts import FSPMTimestepResult

# A — Phenology state at t0 (existing contract; physiological_age unavailable; growth_window unavailable)
PHENO_T0 = OrganDevelopmentalState(
    organ_developmental_state_id="dev_P001_leaf_1_t0",
    plant_id="P001", architecture_id="arch_046AF_1", organ_id="org_leaf_1_046AF",
    organ_type="leaf", initiated_at=datetime(2026,1,1,tzinfo=timezone.utc),
    chronological_age_days=120.0,
    physiological_age=None,  # explicitly unavailable — no domain definition (TASK 024 limitation)
    organ_stage="MATURE",  # vocabulary optional; not enforced
    growth_window_start=None, growth_window_end=None,  # unavailable until model defined
    active_growth_status="NOT_DEFINED",  # derived only when stage/context defines; not inferred
    simulation_time_ref=datetime(2026,9,19,12,0,tzinfo=timezone.utc),
    provenance="TASK_050 synthetic; phenology stage record only; growth_window unavailable",
    is_synthetic_example=True,
)

# B — Water state (existing contract executable; continuity preserved; no plant-coupling interface defined)
WATER_T0 = RootZoneState(
    root_zone_id="rz_P001_t0",
    plant_id="P001", container_id="tier-1-cell-a",
    storage_mm=25.0, field_capacity_mm=40.0, wilting_point_mm=10.0,
    irrigation_input_mm=0.0, drainage_mm=0.0,
    provenance="TASK_050 synthetic; water balance executable; downstream growth coupling NOT_DEFINED",
    is_synthetic_example=True,
)

# C — Nutrient state (pool identity preserved; N/P/K separate; no limitation interface)
NUTRIENT_T0 = NutrientPoolState(
    root_zone_id="rz_P001_t0",
    plant_id="P001",
    nutrient="N",  # element identity preserved; separate pools needed for P/K
    total_amount_mg=120.0, available_amount_mg=100.0, unavailable_amount_mg=20.0,
    provenance="TASK_050 synthetic; N/P/K separate; nutrient-to-growth limitation NOT_IMPLEMENTED",
    is_synthetic_example=True,
)

# D — Combined environmental input for 4-timestep loop (light, water input, nutrient input, phenology reference)
ENV_INPUT_T0 = {
    "light": {"solar_reference":"t0_2026-09-19_12:00","ppfd_absolute_ref":420.0},
    "water": WaterInput(amount_l=5.0, source_type="irrigation", provenance="TASK_050 synthetic"),
    "nutrient": NutrientInput(nutrient="N", amount_mg=10.0, provenance="TASK_050 synthetic"),
    "phenology_ref": PHENO_T0.organ_developmental_state_id,
}

print("TASK 050 fixtures loaded (PARTIAL): phenology state executable (growth_window unavailable); water executable (no growth interface); nutrient executable (no limitation interface).")
