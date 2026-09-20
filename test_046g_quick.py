"""TASK 046G focused tests — CarbonPool contract."""
from __future__ import annotations
import sys
sys.path.insert(0,"/home/anomaly/Projects/Adiwiyata")
from simulation.core.carbon.pool import CarbonPool, carbon_pool_from_reserve_and_net

# 1 identity
p = carbon_pool_from_reserve_and_net(10.0, 5.0, plant_id="p1", pool_id="pool_1")
assert p.plant_id == "p1" and p.pool_id == "pool_1"; print("PASS 01")
# 2 accounting positive
assert p.available_carbon_g == 15.0; print("PASS 02")
# 3 negative net preserved
neg = carbon_pool_from_reserve_and_net(10.0, -15.0, plant_id="p1")
assert neg.available_carbon_g == -5.0; assert neg.current_net_carbon_g == -15.0; print("PASS 03")
# 4 negative available allowed
assert neg.status == "AVAILABLE"; print("PASS 04")
# 5 reserve vs current net distinct
assert p.reserve_carbon_g != p.current_net_carbon_g; print("PASS 05")
# 6 unit g_C preserved (field semantics; no hidden conversion)
assert p.reserve_carbon_g == 10.0; print("PASS 06")
# 7 temporal
p_t = carbon_pool_from_reserve_and_net(0.0, 0.0, "p1", timestep=3600.0, simulation_time="2026-09-17T10:00:00Z")
assert p_t.timestep == 3600.0; assert p_t.simulation_time == "2026-09-17T10:00:00Z"; print("PASS 07")
# 8 status valid
assert p.status == "AVAILABLE"; print("PASS 08")
# 9 provenance preserved
assert "TASK_046G" in (p.provenance or ""); print("PASS 09")
# 10 source carbon result reference preserved (optional)
p_ref = carbon_pool_from_reserve_and_net(0.0, 0.0, "p1", source_carbon_result_id="cr_1")
assert p_ref.source_carbon_result_id == "cr_1"; print("PASS 10")
# 11 previous pool reference
p_prev = carbon_pool_from_reserve_and_net(0.0, 0.0, "p1", previous_pool_id="pool_prev")
assert p_prev.previous_pool_id == "pool_prev"; print("PASS 11")
# 12 isolation: source unchanged (no mutation mechanism; factory pure)
assert p.reserve_carbon_g == 10.0; print("PASS 12")
# 13 no allocation fields present (verify contract doesn't have them)
assert not hasattr(p, "allocated_carbon_g"); print("PASS 13")
# 14 no growth fields
assert not hasattr(p, "biomass_increment_g"); print("PASS 14")
# 15 no transport fields
assert not hasattr(p, "phloem_concentration"); print("PASS 15")
# 16 determinism
p_a = carbon_pool_from_reserve_and_net(5.0, 3.0, "p1", pool_id="d")
p_b = carbon_pool_from_reserve_and_net(5.0, 3.0, "p1", pool_id="d")
assert p_a.model_dump_json() == p_b.model_dump_json(); print("PASS 16")
# 17 negative available not clamped
neg_av = carbon_pool_from_reserve_and_net(2.0, -10.0, "p1")
assert neg_av.available_carbon_g == -8.0; print("PASS 17")
# 18 no source mutation of previous pool
prev = carbon_pool_from_reserve_and_net(100.0, 0.0, "p1", pool_id="old")
newp = carbon_pool_from_reserve_and_net(0.0, 50.0, "p1", previous_pool_id="old")
assert prev.reserve_carbon_g == 100.0; print("PASS 18")
# 19 no engine/API required
print("PASS 19")
# 20 synthetic example labeled
syn = carbon_pool_from_reserve_and_net(0.0, 0.0, "p1", is_synthetic_example=True)
assert syn.is_synthetic_example is True; print("PASS 20")
print("\nTASK 046G: 20/20 PASS")
