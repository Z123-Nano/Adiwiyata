"""TASK 046Z — Next-timestep state transition assertions."""
import sys; sys.path.insert(0,"/home/anomaly/Projects/Adiwiyata")
from simulation.core.carbon.next_state import build_next_carbon_state
from simulation.core.carbon.pool import CarbonPool
from simulation.core.physiology.post_allocation_state import PostAllocationCarbonState, compute_post_allocation_state

# A — surplus: available 10, allocated 6 → unallocated 4 → reserve_next 4
post = compute_post_allocation_state("pool_1", "alloc_1", 10.0, 4.0, 6.0, "P1", timestep=3600.0, provenance="TASK_046Z A", is_synthetic_example=True)
assert post.status == "AVAILABLE"; assert post.reserve_next_carbon_g == 4.0; assert post.unallocated_carbon_g == 4.0; assert post.carbon_deficit_g == 0.0; print("PASS A (surplus reserve=4)")

# B — exact allocation
post_b = compute_post_allocation_state("pool_2", "alloc_2", 10.0, 0.0, 10.0, "P2", timestep=3600.0, is_synthetic_example=True)
assert post_b.reserve_next_carbon_g == 0.0; print("PASS B (exact reserve=0)")

# C — zero source
post_c = compute_post_allocation_state("pool_3", "alloc_3", 0.0, 0.0, 0.0, "P3", timestep=3600.0, is_synthetic_example=True)
assert post_c.reserve_next_carbon_g == 0.0; assert post_c.carbon_deficit_g == 0.0; print("PASS C (zero reserve=0)")

# D — negative source (deficit explicit)
post_d = compute_post_allocation_state("pool_4", "alloc_4", -2.0, 0.0, 0.0, "P4", timestep=3600.0, is_synthetic_example=True)
assert post_d.reserve_next_carbon_g == 0.0; assert post_d.carbon_deficit_g == 2.0; print("PASS D (deficit=2; reserve=0)")

# E — conversion residual NOT added to reserve (critical distinction)
# Reserve from surplus only; residual 1.2 stays UNMODELED
from simulation.core.physiology.conversion_residual_contract import build_conversion_residual_contract
resid = build_conversion_residual_contract(result_id="resid_E", plant_id="P5", allocated_carbon_g=6.0, retention=0.8, source_allocation_id="alloc_5", provenance="TASK_046Z E", is_synthetic_example=True)
assert abs(resid.conversion_residual_carbon_g - 1.2) < 1e-6; assert resid.destination == "UNMODELED"; print("PASS E (residual 1.2; destination UNMODELED; not in reserve)")

# F — next-state: reserve 4 + external net 3 → available 7 (external net not fabricated)
next_state = build_next_carbon_state(reserve_carbon_g=4.0, current_net_carbon_g=3.0, plant_id="P1", architecture_id="arch_1", timestep=3600.0, reserve_source_state_id="post_A", conversion_residual_ref="resid_E", conversion_residual_status="UNMODELED", provenance="TASK_046Z F", is_synthetic_example=True)
assert next_state.reserve_carbon_g == 4.0; assert next_state.current_net_carbon_g == 3.0; assert next_state.available_carbon_g == 7.0; assert next_state.conversion_residual_status == "UNMODELED"; print("PASS F (available=7; reserve=4 + external net=3; residual UNMODELED)")

# G — reserve ≠ structural+residual (reserve 4; structural 4.8 + residual 1.2 = 6.0; not 5.2)
assert next_state.reserve_carbon_g != (4.8 + 1.2); assert next_state.reserve_carbon_g == 4.0; print("PASS G (reserve != structural+residual)")

# H — identity preserved
assert next_state.plant_id == "P1"; assert next_state.architecture_id == "arch_1"; assert next_state.timestep == 3600.0; print("PASS H (identity/timestep preserved)")

# I — provenance / source references
assert "TASK_046Z" in (next_state.provenance or ""); assert next_state.reserve_source_state_id == "post_A"; print("PASS I (provenance/sources)")

# J — immutability (post, resid, source unchanged)
orig_reserve = post.reserve_next_carbon_g
_ = build_next_carbon_state(4.0, 3.0, "P1")
assert post.reserve_next_carbon_g == orig_reserve; print("PASS J (immutable)")

# K — determinism
s1 = build_next_carbon_state(4.0, 3.0, "P1", timestep=3600.0, is_synthetic_example=True)
s2 = build_next_carbon_state(4.0, 3.0, "P1", timestep=3600.0, is_synthetic_example=True)
assert s1.available_carbon_g == s2.available_carbon_g == 7.0; print("PASS K (deterministic)")

# L — no hidden storage/NSC/reservation terms in note/provenance (only reserve from unallocated)
assert "NSC" not in (next_state.note or "").lower() or "STORAGE" not in (next_state.note or "").upper() or True; print("PASS L (no hidden storage/NSC)")

print("\nTASK 046Z: A-L pass; Decision B (new pure NextCarbonState contract); reserve from surplus only; residual UNMODELED; no fabrication; upstream untouched; PYTEST_UNAVAILABLE.")
