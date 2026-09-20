"""TASK 046L fixtures — synthetic architecture with one leaf."""
from simulation.core.contracts.domain import PlantArchitecture, PlantOrgan
from simulation.core.architecture.growth_delta import ArchitectureGrowthDelta

org = PlantOrgan(id="leaf_1", plant_id="p1", architecture_id="arch_1", organ_type="leaf", length_m=0.5, status="AVAILABLE")
ARCH = PlantArchitecture(
    architecture_id="arch_1", plant_id="p1", root_organ_id="leaf_1",
    organs=[org], topology="leaf_1", provenance="TASK_046L synthetic", is_synthetic_example=True,
)
DELTA_POS = ArchitectureGrowthDelta(
    result_id="delta_1", plant_id="p1", architecture_id="arch_1", organ_id="leaf_1",
    organ_type="leaf", previous_biomass_g_DM=2.0, biomass_increment_g_DM=0.4,
    new_biomass_g_DM=2.4, geometry_dimension="length_m",
    previous_length_m=0.5, delta_length_m=0.02, proposed_length_m=0.52,
    relation_type="specific_length_linear", parameter_set_ref="arch_v1_leaf",
    timestep=3600.0, status="AVAILABLE", provenance="TASK_046K", is_synthetic_example=True,
)
DELTA_ZERO = ArchitectureGrowthDelta(
    result_id="delta_0", plant_id="p1", architecture_id="arch_1", organ_id="leaf_1",
    organ_type="leaf", previous_biomass_g_DM=2.0, biomass_increment_g_DM=0.0,
    new_biomass_g_DM=2.0, geometry_dimension="length_m",
    previous_length_m=0.5, delta_length_m=0.0, proposed_length_m=0.5,
    relation_type="specific_length_linear", parameter_set_ref="arch_v1_leaf",
    timestep=3600.0, status="AVAILABLE", provenance="TASK_046K zero", is_synthetic_example=True,
)
