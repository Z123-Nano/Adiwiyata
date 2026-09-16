"""Synthetic plant fixtures — TASK 006. Synthetic only, clearly marked."""
from datetime import datetime
from simulation.core.contracts.domain import (
    Plant, PlantState, PlantArchitecture, PlantOrgan,
    VarietyProfile, VarietyParameter,
)

# Synthetic variety profile — clearly placeholder
SYN_VAR_01 = VarietyProfile(
    species="synthetic_species",
    cultivar="synthetic_variety_01",
    description="Synthetic example variety — placeholder only",
    parameter_collection=[
        VarietyParameter(name="growth_rate", value=None, unit="cm/d", source="assumption_placeholder", method="placeholder", provenance="TASK_006_synthetic"),
        VarietyParameter(name="max_height", value=120.0, unit="cm", source="assumption_placeholder", method="placeholder", provenance="TASK_006_synthetic"),
    ],
)

# Synthetic plants linked to existing TASK 005 container IDs
SYN_PLANTS = [
    Plant(id="P001", species_id="synthetic_species", variety_id="synthetic_variety_01", current_container_id="c1", lifecycle_stage="seedling"),
    Plant(id="P002", species_id="synthetic_species", variety_id="synthetic_variety_01", current_container_id="c2", lifecycle_stage="vegetative"),
    Plant(id="P003", species_id="synthetic_species", variety_id="synthetic_variety_01", current_container_id="cell-a", lifecycle_stage="seedling"),
    Plant(id="P004", species_id="synthetic_species", variety_id="synthetic_variety_01", current_container_id="cell-b", lifecycle_stage="seedling"),
]

SYN_STATES = [
    PlantState(plant_id="P001", timestamp=datetime.now(), age_days=14.0, phenological_stage="seedling", biomass_g=None, carbon_pool_g=None, water_status=None, nutrient_status=None, stress_state=None),
    PlantState(plant_id="P002", timestamp=datetime.now(), age_days=45.0, phenological_stage="vegetative", biomass_g=None, carbon_pool_g=None, water_status="adequate", nutrient_status=None, stress_state=None),
    PlantState(plant_id="P003", timestamp=datetime.now(), age_days=7.0, phenological_stage="seedling", biomass_g=None, carbon_pool_g=None, water_status=None, nutrient_status=None, stress_state=None),
    PlantState(plant_id="P004", timestamp=datetime.now(), age_days=7.0, phenological_stage="seedling", biomass_g=None, carbon_pool_g=None, water_status=None, nutrient_status=None, stress_state=None),
]

SYN_ARCHITECTURES = [
    PlantArchitecture(plant_id="P001", topology="simple", organs=[PlantOrgan(id="o1", organ_type="axis")]),
    PlantArchitecture(plant_id="P002", topology="simple", organs=[PlantOrgan(id="o2", organ_type="axis"), PlantOrgan(id="o3", organ_type="leaf")]),
]
