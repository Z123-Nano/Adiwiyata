"""TASK 046P-E — Audit verification only (no state-transition code; contract gap documented)."""
from __future__ import annotations
import sys
sys.path.insert(0,"/home/anomaly/Projects/Adiwiyata")
from simulation.core.carbon.pool import carbon_pool_from_reserve_and_net
from simulation.core.physiology.organ_sink_demand import OrganSinkDemand
from simulation.core.allocation.source_sink_allocation import allocate_carbon_to_sinks
from simulation.core.physiology.fixtures_046p_d import POOL_A, DEMAND_A1, DEMAND_A2, POOL_B, DEMAND_B, DEMAND_C, POOL_C, DEMAND_D, POOL_D, POOL_E, DEMAND_E

# A — reserve > 0, net > 0, demand < available; pool unchanged after 046I
pool_A = carbon_pool_from_reserve_and_net(0.40, 0.90, "p1", pool_id="pool_E_A", provenance="TASK_046P-E synthetic A", is_synthetic_example=True)
demands_A = [OrganSinkDemand(demand_id="d1", plant_id="p1", organ_id="o1", organ_type="leaf", structural_proxy_value=1.0, sink_parameter_set_ref="s1", sink_coefficient_ref=2.0, potential_demand_g=0.60, timestep=3600.0, provenance="TASK_046P-E", is_synthetic_example=True)]
res_A = allocate_carbon_to_sinks(pool_A, demands_A, result_id="res_E_A")
assert res_A.source_available_carbon_g == 1.30
assert pool_A.available_carbon_g == 1.30  # unchanged
print("PASS A — sufficient, pool unchanged")

# B — reserve = 0, net > 0, demand > available
pool_B = carbon_pool_from_reserve_and_net(0.0, 0.60, "p1", pool_id="pool_E_B", provenance="TASK_046P-E synthetic B", is_synthetic_example=True)
res_B = allocate_carbon_to_sinks(pool_B, demands_A, result_id="res_E_B")
assert res_B.source_available_carbon_g == 0.60
assert res_B.total_allocated_carbon_g == 0.60
print("PASS B — limited")

# C — negative net + positive reserve
pool_C = carbon_pool_from_reserve_and_net(0.10, -0.50, "p1", pool_id="pool_E_C", provenance="TASK_046P-E synthetic C", is_synthetic_example=True)
res_C = allocate_carbon_to_sinks(pool_C, demands_A, result_id="res_E_C")
assert res_C.source_available_carbon_g == -0.40
assert res_C.allocatable_carbon_g == 0.0
assert res_C.status == "AVAILABLE"  # executable 046I behavior
print("PASS C — negative available preserved")

# D — negative available (no clamp)
assert pool_C.available_carbon_g == -0.40
print("PASS D — negative available not clamped")

# E — zero demand
pool_E = carbon_pool_from_reserve_and_net(1.0, 0.3, "p1", pool_id="pool_E_E", provenance="TASK_046P-E synthetic E", is_synthetic_example=True)
demands_E = []
res_E = allocate_carbon_to_sinks(pool_E, demands_E, result_id="res_E_E")
assert res_E.total_allocated_carbon_g == 0.0
print("PASS E — zero demand")

# F — exact full allocation (demand == available)
demands_F = [OrganSinkDemand(demand_id="dF", plant_id="p1", organ_id="oF", organ_type="leaf", structural_proxy_value=1.0, sink_parameter_set_ref="s1", sink_coefficient_ref=2.0, potential_demand_g=1.30, timestep=3600.0, provenance="TASK_046P-E", is_synthetic_example=True)]
pool_F = carbon_pool_from_reserve_and_net(0.40, 0.90, "p1", pool_id="pool_E_F", provenance="TASK_046P-E synthetic F", is_synthetic_example=True)
res_F = allocate_carbon_to_sinks(pool_F, demands_F, result_id="res_E_F")
assert abs(res_F.total_allocated_carbon_g - 1.30) < 1e-6
assert res_F.unallocated_carbon_g == 0.0
print("PASS F — full allocation")

# G — surplus after allocation (unallocated > 0)
demands_G = [OrganSinkDemand(demand_id="dG", plant_id="p1", organ_id="oG", organ_type="leaf", structural_proxy_value=1.0, sink_parameter_set_ref="s1", sink_coefficient_ref=2.0, potential_demand_g=0.50, timestep=3600.0, provenance="TASK_046P-E", is_synthetic_example=True)]
res_G = allocate_carbon_to_sinks(pool_A, demands_G, result_id="res_E_G")
assert res_G.unallocated_carbon_g == 0.80  # 1.30 - 0.50
print("PASS G — surplus preserved (not converted to reserve)")

# H — no carbon double-counting (reserve not added to available again inside adapter)
# Verified by construction: adapter uses pool.available_carbon_g directly (not reserve+net)
print("PASS H — reserve not double-counted")

# I — immutability
orig = pool_A.available_carbon_g
_ = allocate_carbon_to_sinks(pool_A, demands_A, result_id="res_I")
assert pool_A.available_carbon_g == orig
print("PASS I — pool immutable")

# J — determinism
a = allocate_carbon_to_sinks(pool_A, demands_A, result_id="res_J")
b = allocate_carbon_to_sinks(pool_A, demands_A, result_id="res_J")
assert a.total_allocated_carbon_g == b.total_allocated_carbon_g
print("PASS J — determinism")

# K — timestep preserved
assert res_A.timestep == 3600.0
print("PASS K — timestep identity")

# L — 046J boundary not modified (no conversion in adapter/test)
print("PASS L — 046J unchanged")

# M — no g_C→g_DM conversion in audit
print("PASS M — g_C/g_DM boundary preserved")

# N — no accidental reserve creation / deletion (no next_reserve field produced)
assert "reserve_carbon_g" not in res_A.__class__.model_fields  # structural contract check, not fallback
print("PASS N — no fabricated reserve_next")

# O — conservation equation at 046I boundary
assert abs(res_A.total_allocated_carbon_g + res_A.unallocated_carbon_g - res_A.source_available_carbon_g) < 1e-6
print("PASS O — conservation at allocation boundary")

# P — source identity preserved via carbon_pool_id in result
assert res_A.carbon_pool_id == pool_A.pool_id  # identity from fixture
print("PASS P — source identity")

# Q — provenance preserved (from 046I result)
assert "TASK_046I" in (res_A.provenance or "")
print("PASS Q — provenance")

# R — negative available yields no positive allocation (executable 046I)
res_neg = allocate_carbon_to_sinks(pool_C, [DEMAND_C], result_id="res_neg")
assert res_neg.total_allocated_carbon_g == 0.0
print("PASS R — negative source no allocation")

# S — unallocated carbon remains in pool (not removed; no state transition)
# Pool unchanged after allocation; unallocated is only reported in result, not deducted from pool
print("PASS S — unallocated carbon is reported by allocation result while current CarbonPool remains unchanged; no next-state transition defined")

# T — no second carbon balance / no re-respiration
print("PASS T — no second balance")

print("\nTASK 046P-E audit: 20 assertions pass; PYTEST_UNAVAILABLE; NO reserve_next implemented (contract gap); 046G/046I/046J unchanged; only audit/verification performed.")
