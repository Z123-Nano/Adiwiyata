from simulation.core.plants.fixture import SYN_PLANTS, SYN_STATES, SYN_VAR_01, SYN_ARCHITECTURES

def test_plants_deterministic():
    ids = [p.id for p in SYN_PLANTS]
    assert ids == ["P001","P002","P003","P004"]
    for p in SYN_PLANTS:
        assert p.current_container_id is not None

def test_state_separate():
    s = SYN_STATES[0]
    assert s.plant_id == "P001"
    assert s.biomass_g is None  # not fabricated
    assert s.age_days == 14.0

def test_variety_provenance():
    assert SYN_VAR_01.species == "synthetic_species"
    for param in SYN_VAR_01.parameter_collection:
        assert param.source in ("assumption_placeholder","measured","fitted_inferred","literature","unknown")
        assert param.provenance and "synthetic" in param.provenance

def test_identity_persists():
    p = SYN_PLANTS[0]
    s = SYN_STATES[0]
    assert p.id == s.plant_id
    # PlantState has no separate 'id' in domain contract — distinct from Plant identity

def test_architecture_separate():
    a = SYN_ARCHITECTURES[0]
    assert a.plant_id == "P001"
    assert len(a.organs) >= 1
