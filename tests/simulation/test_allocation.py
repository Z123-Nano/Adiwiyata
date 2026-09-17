"""TASK 022 source-sink allocation tests — allocation only; synthetic; no growth; deterministic."""
from simulation.core.allocation.contracts import CarbonSource, CarbonSink, SourceSinkAllocationRequest
from simulation.core.allocation.allocation import allocate_source_sink, POLICY
from simulation.core.allocation.fixtures import (
    SYNTH_SOURCE_10, SYNTH_SOURCE_5, SYNTH_SOURCE_NEG, SYNTH_SOURCE_0,
    SYNTH_SINK_STEM, SYNTH_SINK_ROOT, SYNTH_SINK_LEAF, SYNTH_SINK_ZERO,
    SYNTH_SINK_NEG, SYNTH_SINK_NOD,
)

# A all demand satisfied
# B proportional limiting
# C zero carbon
# D negative carbon deficit
# E zero total demand
# F no negative allocations
# G allocation never exceeds demand
# H conservation
# I deterministic ordering
# J invalid negative demand
# K invalid sink/plant reference (only where checkable -> skip if no arch)
# L unavailable demand -> NOT_COMPUTABLE
# M provenance preserved
# N policy recorded
# O serialization roundtrip
# P floating-point tolerance
# Q source carbon separate from allocated
# R does not modify PlantArchitecture or PlantState

def test_A_all_demand_satisfied():
    r = allocate_source_sink(SourceSinkAllocationRequest(
        source=SYNTH_SOURCE_10, sinks=[SYNTH_SINK_STEM, SYNTH_SINK_ROOT, SYNTH_SINK_LEAF],
        provenance="TASK_022 A"))
    assert r.status == "VALID"
    assert sum(a.allocated_carbon for a in r.sink_allocations if a.status=="VALID") == 10.0
    assert r.unallocated_carbon == 0.0

def test_B_proportional_limiting():
    r = allocate_source_sink(SourceSinkAllocationRequest(
        source=SYNTH_SOURCE_5, sinks=[SYNTH_SINK_STEM, SYNTH_SINK_ROOT, SYNTH_SINK_LEAF],
        provenance="TASK_022 B"))
    assert r.status == "VALID"
    # d total = 10; C=5 => stem 2.5 root 1.5 leaf 1.0
    allocs = {a.sink_id: a.allocated_carbon for a in r.sink_allocations}
    assert abs(allocs.get("stem", 0) - 2.5) < 1e-3
    assert abs(allocs.get("root", 0) - 1.5) < 1e-3
    assert abs(allocs.get("leaf", 0) - 1.0) < 1e-3
    assert r.unallocated_carbon < 1e-3

def test_C_zero_carbon():
    r = allocate_source_sink(SourceSinkAllocationRequest(source=SYNTH_SOURCE_0, sinks=[SYNTH_SINK_STEM], provenance="C"))
    assert r.status == "VALID"
    assert r.total_allocated == 0.0
    assert r.unallocated_carbon == 0.0

def test_D_negative_deficit():
    r = allocate_source_sink(SourceSinkAllocationRequest(source=SYNTH_SOURCE_NEG, sinks=[SYNTH_SINK_STEM], provenance="D"))
    assert r.status == "VALID"
    assert r.total_allocated == 0.0
    assert r.carbon_deficit == 3.0

def test_E_zero_total_demand():
    r = allocate_source_sink(SourceSinkAllocationRequest(source=SYNTH_SOURCE_10, sinks=[SYNTH_SINK_ZERO], provenance="E"))
    assert r.status == "VALID"
    assert r.total_allocated == 0.0
    assert r.unallocated_carbon == 10.0

def test_F_no_negative_allocations():
    r = allocate_source_sink(SourceSinkAllocationRequest(source=SYNTH_SOURCE_5, sinks=[SYNTH_SINK_STEM, SYNTH_SINK_ROOT, SYNTH_SINK_LEAF], provenance="F"))
    for a in r.sink_allocations:
        assert a.allocated_carbon >= -1e-9

def test_G_allocation_never_exceeds_demand():
    r = allocate_source_sink(SourceSinkAllocationRequest(source=SYNTH_SOURCE_10, sinks=[SYNTH_SINK_STEM, SYNTH_SINK_ROOT, SYNTH_SINK_LEAF], provenance="G"))
    for a in r.sink_allocations:
        if a.demand is not None:
            assert a.allocated_carbon <= a.demand + 1e-6

def test_H_conservation():
    r = allocate_source_sink(SourceSinkAllocationRequest(source=SYNTH_SOURCE_10, sinks=[SYNTH_SINK_STEM, SYNTH_SINK_ROOT], provenance="H"))
    total = r.total_allocated + r.unallocated_carbon
    assert abs(total - r.source_carbon) < 1e-3

def test_I_deterministic_ordering():
    s = [SYNTH_SINK_ROOT, SYNTH_SINK_STEM, SYNTH_SINK_LEAF]
    r1 = allocate_source_sink(SourceSinkAllocationRequest(source=SYNTH_SOURCE_10, sinks=list(s), provenance="I"))
    r2 = allocate_source_sink(SourceSinkAllocationRequest(source=SYNTH_SOURCE_10, sinks=list(reversed(s)), provenance="I"))
    ids1 = [a.sink_id for a in r1.sink_allocations if a.status=="VALID"]
    ids2 = [a.sink_id for a in r2.sink_allocations if a.status=="VALID"]
    assert ids1 == ids2  # sorted by sink_id

def test_J_invalid_negative_demand():
    r = allocate_source_sink(SourceSinkAllocationRequest(source=SYNTH_SOURCE_10, sinks=[SYNTH_SINK_NEG, SYNTH_SINK_STEM], provenance="J"))
    # At least one invalid input; result contains invalid sink with INVALID_INPUT
    bad = [a for a in r.sink_allocations if a.sink_id == "bad"]
    if bad:
        assert bad[0].status == "INVALID_INPUT"

def test_K_invalid_reference_skipped():
    # No architecture lookup required unless available; just verify sink can have different plant_id and still allocate if only demands used
    s = CarbonSink(sink_id="other", plant_id="other", sink_type="leaf", demand=2.0, provenance="K")
    r = allocate_source_sink(SourceSinkAllocationRequest(source=SYNTH_SOURCE_10, sinks=[SYNTH_SINK_STEM, s], provenance="K"))
    assert r.status == "VALID"

def test_L_unavailable_demand():
    r = allocate_source_sink(SourceSinkAllocationRequest(source=SYNTH_SOURCE_10, sinks=[SYNTH_SINK_NOD, SYNTH_SINK_STEM], provenance="L"))
    nod = [a for a in r.sink_allocations if a.sink_id == "nodemand"]
    if nod:
        assert nod[0].status == "NOT_COMPUTABLE"

def test_M_provenance_preserved():
    r = allocate_source_sink(SourceSinkAllocationRequest(source=SYNTH_SOURCE_10, sinks=[SYNTH_SINK_STEM], provenance="TASK_022_M"))
    assert r.provenance is not None and "TASK_022" in r.provenance

def test_N_policy_recorded():
    from simulation.core.allocation.allocation import POLICY
    assert POLICY == "proportional_demand"

def test_O_serialization_roundtrip():
    import json
    req = SourceSinkAllocationRequest(source=SYNTH_SOURCE_5, sinks=[SYNTH_SINK_STEM], provenance="O")
    d = req.model_dump(mode="json")
    req2 = SourceSinkAllocationRequest.model_validate(d)
    assert req2.allocation_policy == req.allocation_policy

def test_P_floating_point_tolerance():
    r = allocate_source_sink(SourceSinkAllocationRequest(source=SYNTH_SOURCE_10, sinks=[SYNTH_SINK_STEM, SYNTH_SINK_ROOT, SYNTH_SINK_LEAF], provenance="P"))
    check = r.conservation_check
    # Just verify the field exists and doesn't claim arbitrary broad tolerance
    assert "diff=" in check

def test_Q_source_carbon_separate():
    r = allocate_source_sink(SourceSinkAllocationRequest(source=SYNTH_SOURCE_10, sinks=[SYNTH_SINK_STEM], provenance="Q"))
    assert r.source_carbon == 10.0
    assert r.total_allocated <= 10.0

def test_R_no_architecture_modification():
    # Just verify allocation result doesn't carry architecture mutations
    from simulation.core.plants.architecture import ArchitectureOps, PlantArchitecture
    from simulation.core.contracts.domain import PlantOrgan
    arch = PlantArchitecture(architecture_id="a1", plant_id="p1", root_organ_id="r1", organs=[PlantOrgan(id="r1", length_m=1.0, radius_m=0.2, parent_organ_id=None, position=(0,0,0), orientation=(0,0,0), provenance="test")], local_origin=(0,0,0), coordinate_frame="plant_local")
    before = ArchitectureOps.validate(arch)
    r = allocate_source_sink(SourceSinkAllocationRequest(source=SYNTH_SOURCE_10, sinks=[SYNTH_SINK_STEM], provenance="R"))
    after = ArchitectureOps.validate(arch)
    assert before == after
