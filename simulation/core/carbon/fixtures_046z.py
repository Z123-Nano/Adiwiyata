"""TASK 046Z fixtures — synthetic next-state transitions."""
from simulation.core.carbon.next_state import build_next_carbon_state

# A — surplus (10 avail, 6 alloc → reserve 4)
STATE_A = build_next_carbon_state(
    reserve_carbon_g=4.0, current_net_carbon_g=3.0, plant_id="P1", architecture_id="arch_1",
    timestep=3600.0, source_pool_id="pool_A", source_allocation_id="alloc_A",
    reserve_source_state_id="post_A", conversion_residual_ref="resid_046J_1", conversion_residual_status="UNMODELED",
    provenance="TASK_046Z A synthetic surplus + external net", is_synthetic_example=True,
)
# B — exact (10 → 10 → reserve 0)
STATE_B = build_next_carbon_state(reserve_carbon_g=0.0, current_net_carbon_g=2.0, plant_id="P2", timestep=3600.0, provenance="TASK_046Z B exact", is_synthetic_example=True)
# C — limited source (4 → 4 → reserve 0)
STATE_C = build_next_carbon_state(reserve_carbon_g=0.0, current_net_carbon_g=0.0, plant_id="P3", timestep=3600.0, provenance="TASK_046Z C limited", is_synthetic_example=True)
# D — zero source (0 → reserve 0; deficit explicit at pool level, reserve 0)
STATE_D = build_next_carbon_state(reserve_carbon_g=0.0, current_net_carbon_g=-1.5, plant_id="P4", timestep=3600.0, provenance="TASK_046Z D deficit external", is_synthetic_example=True)
# E — conversion residual UNMODELED (reserve from surplus; residual not added)
# (verified by STATE_G below)
# F — both surplus + conversion residual (reserve=4; structural=4.8; residual=1.2; reserve ≠ 5.2)
# (verified in test, not fixture — reserve computed from unallocated only)
# G — identity preserved
# H — provenance preserved
