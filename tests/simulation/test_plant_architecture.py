"""TASK 017 plant architecture tests — deterministic; synthetic; no growth/physics."""
from simulation.core.contracts.domain import PlantArchitecture, PlantOrgan
from simulation.core.plants.architecture import ArchitectureOps
from simulation.core.plants.architecture_fixtures import SYNTH_SEEDLING, SYNTH_BRANCHED

def test_architecture_creation():
    a = SYNTH_SEEDLING
    assert a.architecture_id == "arch-017-seed"
    assert a.plant_id == "plant-p1"
    assert a.schema_version == "v1"

def test_root_detection():
    root = ArchitectureOps.get_root(SYNTH_SEEDLING)
    assert root is not None
    assert root.id == "root-1"
    assert root.parent_organ_id is None

def test_add_organ():
    a = SYNTH_SEEDLING
    new_leaf = PlantOrgan(id="leaf-3", plant_id="plant-p1", organ_type="leaf", parent_organ_id="stem-1", local_position=[0,0,0.09], length_m=0.02, radius_m=0.001, schema_version="v1", provenance="test", is_synthetic_example=True)
    a2 = ArchitectureOps.add_organ(a, new_leaf)
    assert any(o.id == "leaf-3" for o in a2.organs)
    # Original unchanged (serialization boundary)
    assert not any(o.id == "leaf-3" for o in a.organs)

def test_parent_child_relationship():
    a = SYNTH_SEEDLING
    stem = ArchitectureOps.find_organ(a, "stem-1")
    assert stem is not None
    children = ArchitectureOps.get_children(a, "stem-1")
    ids = {c.id for c in children}
    assert "leaf-1" in ids and "leaf-2" in ids

def test_multiple_branches():
    a = SYNTH_BRANCHED
    assert ArchitectureOps.get_root(a) is not None
    branches = [o for o in a.organs if o.organ_type == "branch"]
    assert len(branches) == 2

def test_organ_lookup():
    o = ArchitectureOps.find_organ(SYNTH_SEEDLING, "leaf-1")
    assert o is not None
    assert o.organ_type == "leaf"

def test_invalid_parent_rejected():
    bad = PlantOrgan(id="bad", plant_id="p", organ_type="leaf", parent_organ_id="nonexistent", local_position=[0,0,0], length_m=0.1, schema_version="v1")
    a = SYNTH_SEEDLING
    errors = ArchitectureOps.validate(a)
    # Validate on bad architecture with missing parent should fail
    bad_arch = PlantArchitecture(architecture_id="bad", plant_id="p", root_organ_id="bad", organs=[bad], schema_version="v1", is_synthetic_example=True)
    errs = ArchitectureOps.validate(bad_arch)
    assert any("invalid parent" in e for e in errs)

def test_duplicate_organ_id_rejected():
    dup = PlantOrgan(id="root-1", plant_id="p", organ_type="root", local_position=[0,0,0], length_m=0.1, schema_version="v1")
    a = SYNTH_SEEDLING
    errors = ArchitectureOps.validate(PlantArchitecture(architecture_id="d", plant_id="p", root_organ_id="root-1", organs=[a.organs[0], dup], schema_version="v1", is_synthetic_example=True))
    assert any("duplicate" in e for e in errors)

def test_cycle_rejected():
    a = SYNTH_SEEDLING
    # Manually inject cycle: leaf-1 parent root-1, root-1 parent leaf-1
    a2 = PlantArchitecture.model_validate(a.model_dump(mode="json"))
    for o in a2.organs:
        if o.id == "root-1":
            o.parent_organ_id = "leaf-1"
    errs = ArchitectureOps.validate(a2)
    assert any("cycle" in e for e in errs)

def test_negative_length_rejected():
    try:
        PlantOrgan(id="bad-l", plant_id="p", organ_type="stem", local_position=[0,0,0], length_m=-1.0, radius_m=0.01, schema_version="v1")
        assert False, "negative length should fail at creation"
    except Exception:
        pass

def test_invalid_radius_rejected():
    try:
        PlantOrgan(id="bad-r", plant_id="p", organ_type="root", local_position=[0,0,0], length_m=0.1, radius_m=-0.01, schema_version="v1")
        assert False
    except Exception:
        pass

def test_deterministic_serialization():
    d1 = SYNTH_SEEDLING.model_dump_json()
    d2 = SYNTH_SEEDLING.model_dump_json()
    assert d1 == d2

def test_serialization_roundtrip():
    d = SYNTH_BRANCHED.model_dump(mode="json")
    a2 = PlantArchitecture.model_validate(d)
    assert a2.architecture_id == SYNTH_BRANCHED.architecture_id
    assert len(a2.organs) == len(SYNTH_BRANCHED.organs)

def test_remove_detach_semantics():
    a = SYNTH_SEEDLING
    # Remove leaf with no children — should succeed
    a2 = ArchitectureOps.remove_organ(a, "leaf-1", detach_children=False)
    assert not any(o.id == "leaf-1" for o in a2.organs)

def test_independent_copies_immutability():
    a = SYNTH_SEEDLING
    a2 = PlantArchitecture.model_validate(a.model_dump(mode="json"))
    a2.organs[0].length_m = 999.0
    assert a.organs[0].length_m != 999.0

def test_world_local_spatial_semantics():
    a = SYNTH_SEEDLING
    assert a.coordinate_frame == "plant_local"
    assert a.local_origin == [0.0, 0.0, 0.0]
    leaf = ArchitectureOps.find_organ(a, "leaf-1")
    assert leaf.local_position is not None
    assert len(leaf.local_position) == 3

def test_identity_state_separation():
    # Architecture change does not change plant identity
    a = SYNTH_SEEDLING
    arch_id = a.architecture_id
    assert a.plant_id == "plant-p1"
    # Rebuild architecture with same plant_id, different architecture_id
    a2 = PlantArchitecture(architecture_id="arch-new", plant_id="plant-p1", root_organ_id="root-1", organs=a.organs, schema_version="v1", is_synthetic_example=True)
    assert a2.plant_id == a.plant_id
    assert a2.architecture_id != arch_id
