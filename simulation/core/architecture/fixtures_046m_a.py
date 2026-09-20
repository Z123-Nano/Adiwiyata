"""TASK 046M-A fixtures — synthetic architecture with leaf + stem + root."""
from simulation.core.contracts.domain import PlantArchitecture, PlantOrgan
from simulation.core.architecture.occluder_mapping import ArchitectureOccluderMappingConfig

ORG_LEAF = PlantOrgan(id="leaf_1", plant_id="p1", architecture_id="arch_1",
                      organ_type="leaf", local_position=[1.0, 0.5, 0.2],
                      orientation=[0.0, 0.0, 1.0], length_m=0.5, radius_m=0.05,
                      status="AVAILABLE")
ORG_STEM = PlantOrgan(id="stem_1", plant_id="p1", architecture_id="arch_1",
                      organ_type="stem", local_position=[0.5, 0.5, 0.0],
                      orientation=[0.0, 1.0, 0.0], length_m=0.3, radius_m=0.02,
                      status="AVAILABLE")
ORG_ROOT = PlantOrgan(id="root_1", plant_id="p1", architecture_id="arch_1",
                      organ_type="root", local_position=[0.0, 0.0, -0.2],
                      orientation=[0.0, 0.0, -1.0], length_m=0.4, radius_m=0.03,
                      status="AVAILABLE")
ARCH_3ORG = PlantArchitecture(
    architecture_id="arch_1", plant_id="p1", root_organ_id="root_1",
    coordinate_frame="plant_local", local_origin=[0.0, 0.0, 0.0],
    organs=[ORG_LEAF, ORG_STEM, ORG_ROOT],
    provenance="TASK_046M-A synthetic", is_synthetic_example=True,
)
CONFIG_DEFAULT = ArchitectureOccluderMappingConfig()
