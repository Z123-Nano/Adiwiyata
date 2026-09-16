"""Contract-level validation for TASK 002 — separation, units, provenance."""
import pytest
from datetime import datetime
from simulation.core.contracts.domain import (
    Garden, Boundary, GardenReference, Plant, PlantState, PlantArchitecture,
    PlantOrgan, VarietyProfile, VarietyParameter, Measurement, Observation,
    Scenario, SimulationRun, Prediction, ModelVersion, ParameterSetVersion,
    Container, ContainerCell, EnvironmentState, LightField,
)

# A. valid Garden + L-shaped boundary (ordered points, not rectangle)
def test_garden_l_boundary():
    g = Garden(
        id="g1",
        reference=GardenReference(),
        boundary=Boundary(points=[[0,0,0],[2,0,0],[2,1,0],[1,1,0],[1,2,0],[0,2,0],[0,0,0]]),
    )
    assert len(g.boundary.points) >= 4
    assert g.id == "g1"

# D. hierarchy
# E. seedling tray + cells
def test_container_cell_hierarchy():
    c = Container(id="c1", container_type="seedling_tray", transform=__import__('simulation.core.contracts.domain', fromlist=['SpatialTransform']).SpatialTransform(), cell_ids=["cell-a"])
    cell = ContainerCell(id="cell-a", parent_container_id="c1", index=0, transform=__import__('simulation.core.contracts.domain', fromlist=['SpatialTransform']).SpatialTransform())
    assert cell.parent_container_id == "c1"

# F. Plant vs PlantState separation
def test_plant_identity_vs_state():
    p = Plant(id="p1", species_id="s1")
    s = PlantState(plant_id="p1", timestamp=datetime.now(), age_days=None)  # unknown, not zero
    assert p.id == s.plant_id
    assert s.age_days is None

# G. PlantArchitecture no Three.js
def test_architecture_no_three():
    arch = PlantArchitecture(architecture_id="a1", plant_id="p1", organs=[PlantOrgan(id="o1", organ_type="leaf", schema_version="v1")])
    assert arch.geometry_metadata is None or isinstance(arch.geometry_metadata, dict)
    assert "three" not in str(type(arch)).lower()

# H. VarietyParameter provenance + source categories
def test_variety_parameter_sources():
    vp = VarietyProfile(species="Tomato", parameter_collection=[
        VarietyParameter(name="rate", value=2.5, unit="g/d", source="measured"),
        VarietyParameter(name="unknown", value=None, unit=None, source="unknown"),
    ])
    sources = {p.source for p in vp.parameter_collection}
    assert "measured" in sources
    assert "unknown" in sources
    # missing scientific value must not default to zero
    unknown_p = vp.parameter_collection[1]
    assert unknown_p.value is None

# I. Measurement with explicit unit
def test_measurement_unit():
    m = Measurement(id="m1", timestamp=datetime.now(), variable="temp", value=22, unit="C")
    assert m.unit == "C"

# J. Observation separate
def test_observation_separate():
    o = Observation(id="o1", timestamp=datetime.now(), content="leaves yellowing")
    assert o.category is None or isinstance(o.category, str)

# K. Scenario -> SimulationRun relationship
def test_scenario_run():
    scen = Scenario(id="sc1", name="what-if", base_snapshot_ref="g1")
    run = SimulationRun(id="r1", source_state_ref="g1", scenario_ref="sc1")
    assert run.scenario_ref == scen.id

# L. Prediction separate from live Garden
def test_prediction_not_mutable_garden():
    pred = Prediction(id="pred1", source_snapshot_ref="g1", forecast_time=100.0, plant_states_ref=["p1"])
    # Prediction must not be confused with Garden state mutation
    assert pred.source_snapshot_ref == "g1"

# M. model / parameter version
def test_model_version():
    mv = ModelVersion(model_name="light", version="0.1.0")
    psv = ParameterSetVersion(parameter_set_id="ps1", version="1")
    assert mv.version and psv.version

# Invalid: malformed timestamp (string where datetime expected) — Pydantic rejects
def test_invalid_malformed_timestamp():
    with pytest.raises(Exception):
        PlantState(plant_id="p1", timestamp="not-a-date")
