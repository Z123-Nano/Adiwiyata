"""Synthetic architecture fixtures — TASK 017. Explicit test; synthetic; no real measurements."""
from simulation.core.contracts.domain import PlantArchitecture, PlantOrgan

SYNTH_SEEDLING = PlantArchitecture(
    architecture_id="arch-017-seed",
    plant_id="plant-p1",
    root_organ_id="root-1",
    coordinate_frame="plant_local",
    local_origin=[0.0,0.0,0.0],
    organs=[
        PlantOrgan(id="root-1", plant_id="plant-p1", organ_type="root", parent_organ_id=None, children_ids=["stem-1"], local_position=[0,0,0], orientation=[0,0,1], length_m=0.05, radius_m=0.005, status="synthetic", schema_version="v1", provenance="fixture_TASK_017", is_synthetic_example=True),
        PlantOrgan(id="stem-1", plant_id="plant-p1", organ_type="stem", parent_organ_id="root-1", children_ids=["leaf-1","leaf-2"], local_position=[0,0,0.05], orientation=[0,0,1], length_m=0.08, radius_m=0.003, status="synthetic", schema_version="v1", provenance="fixture_TASK_017", is_synthetic_example=True),
        PlantOrgan(id="leaf-1", plant_id="plant-p1", organ_type="leaf", parent_organ_id="stem-1", children_ids=[], local_position=[0.02,0,0.08], orientation=[0.1,0,0.9], length_m=0.03, radius_m=0.001, status="synthetic", schema_version="v1", provenance="fixture_TASK_017", is_synthetic_example=True),
        PlantOrgan(id="leaf-2", plant_id="plant-p1", organ_type="leaf", parent_organ_id="stem-1", children_ids=[], local_position=[-0.02,0,0.08], orientation=[-0.1,0,0.9], length_m=0.03, radius_m=0.001, status="synthetic", schema_version="v1", provenance="fixture_TASK_017", is_synthetic_example=True),
    ],
    provenance="synthetic_architecture_TASK_017; seedling; no growth; no measurement",
    schema_version="v1",
    is_synthetic_example=True,
    notes="Minimal seedling: root + stem + 2 leaves; all geometry synthetic.",
)

SYNTH_BRANCHED = PlantArchitecture(
    architecture_id="arch-017-branch",
    plant_id="plant-p2",
    root_organ_id="root-b",
    coordinate_frame="plant_local",
    local_origin=[0,0,0],
    organs=[
        PlantOrgan(id="root-b", plant_id="plant-p2", organ_type="root", parent_organ_id=None, children_ids=["stem-b"], local_position=[0,0,0], orientation=[0,0,1], length_m=0.06, radius_m=0.006, status="synthetic", schema_version="v1", provenance="fixture_TASK_017", is_synthetic_example=True),
        PlantOrgan(id="stem-b", plant_id="plant-p2", organ_type="stem", parent_organ_id="root-b", children_ids=["branch-b1","branch-b2"], local_position=[0,0,0.06], orientation=[0,0,1], length_m=0.12, radius_m=0.004, status="synthetic", schema_version="v1", provenance="fixture_TASK_017", is_synthetic_example=True),
        PlantOrgan(id="branch-b1", plant_id="plant-p2", organ_type="branch", parent_organ_id="stem-b", children_ids=["leaf-b1"], local_position=[0.05,0,0.12], orientation=[0.5,0,0.5], length_m=0.06, radius_m=0.003, status="synthetic", schema_version="v1", provenance="fixture_TASK_017", is_synthetic_example=True),
        PlantOrgan(id="branch-b2", plant_id="plant-p2", organ_type="branch", parent_organ_id="stem-b", children_ids=["leaf-b2","leaf-b3"], local_position=[-0.05,0,0.12], orientation=[-0.5,0,0.5], length_m=0.06, radius_m=0.003, status="synthetic", schema_version="v1", provenance="fixture_TASK_017", is_synthetic_example=True),
        PlantOrgan(id="leaf-b1", plant_id="plant-p2", organ_type="leaf", parent_organ_id="branch-b1", children_ids=[], local_position=[0.05,0,0.18], orientation=[0.3,0,0.9], length_m=0.04, radius_m=0.001, status="synthetic", schema_version="v1", provenance="fixture_TASK_017", is_synthetic_example=True),
        PlantOrgan(id="leaf-b2", plant_id="plant-p2", organ_type="leaf", parent_organ_id="branch-b2", children_ids=[], local_position=[-0.05,0,0.18], orientation=[-0.3,0,0.9], length_m=0.04, radius_m=0.001, status="synthetic", schema_version="v1", provenance="fixture_TASK_017", is_synthetic_example=True),
        PlantOrgan(id="leaf-b3", plant_id="plant-p2", organ_type="leaf", parent_organ_id="branch-b2", children_ids=[], local_position=[-0.06,0.01,0.18], orientation=[-0.3,0.1,0.9], length_m=0.035, radius_m=0.001, status="synthetic", schema_version="v1", provenance="fixture_TASK_017", is_synthetic_example=True),
    ],
    provenance="synthetic_architecture_TASK_017; branched; no growth",
    schema_version="v1",
    is_synthetic_example=True,
    notes="Branched plant with 2 branches, 3 leaves; topology tree.",
)
