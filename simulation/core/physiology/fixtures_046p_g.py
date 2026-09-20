"""TASK 046P-G fixtures — synthetic PostAllocationCarbonState cases (MODEL A). Labeled synthetic; no empirical claim."""
from simulation.core.physiology.post_allocation_state import compute_post_allocation_state

# A sufficient source (reserve 0.40 + net 0.90 = 1.30; allocated 1.00; unallocated 0.30)
STATE_A = compute_post_allocation_state(
    previous_pool_id="pool_E_A", previous_allocation_id="res_E_A",
    source_available_carbon_g=1.30, unallocated_carbon_g=0.30, total_allocated_carbon_g=1.00,
    plant_id="p1", provenance="TASK_046P-G synthetic A (sufficient source)", is_synthetic_example=True)

# B exact allocation (available 1.30; allocated 1.30; unallocated 0)
STATE_B = compute_post_allocation_state(
    previous_pool_id="pool_E_F", previous_allocation_id="res_E_F",
    source_available_carbon_g=1.30, unallocated_carbon_g=0.0, total_allocated_carbon_g=1.30,
    plant_id="p1", provenance="TASK_046P-G synthetic B (exact)", is_synthetic_example=True)

# C limited source (available 0.60; allocated 0.60; unallocated 0)
STATE_C = compute_post_allocation_state(
    previous_pool_id="pool_E_B", previous_allocation_id="res_E_B",
    source_available_carbon_g=0.60, unallocated_carbon_g=0.0, total_allocated_carbon_g=0.60,
    plant_id="p1", provenance="TASK_046P-G synthetic C (limited)", is_synthetic_example=True)

# D negative available (reserve 0.10 + net -0.50 = -0.40)
STATE_D = compute_post_allocation_state(
    previous_pool_id="pool_E_C", previous_allocation_id="res_E_C",
    source_available_carbon_g=-0.40, unallocated_carbon_g=0.0, total_allocated_carbon_g=0.0,
    plant_id="p1", provenance="TASK_046P-G synthetic D (negative)", is_synthetic_example=True)

# E zero demand (available 1.30; allocated 0; unallocated 1.30)
STATE_E = compute_post_allocation_state(
    previous_pool_id="pool_E_E", previous_allocation_id="res_E_E",
    source_available_carbon_g=1.30, unallocated_carbon_g=1.30, total_allocated_carbon_g=0.0,
    plant_id="p1", provenance="TASK_046P-G synthetic E (zero demand -> all reserve)", is_synthetic_example=True)
