"""TASK 046P-D fixtures — synthetic CarbonPool + OrganSinkDemand."""
from simulation.core.carbon.pool import carbon_pool_from_reserve_and_net
from simulation.core.physiology.organ_sink_demand import OrganSinkDemand

# CASE A — positive pool 1.30 g_C, demand 1.00 g_C total
POOL_A = carbon_pool_from_reserve_and_net(0.40, 0.90, "p1", pool_id="pool_A", provenance="TASK_046P-D synthetic A", is_synthetic_example=True)
DEMAND_A1 = OrganSinkDemand(demand_id="d_a1", plant_id="p1", organ_id="leaf_1", organ_type="leaf", structural_proxy_value=1.0, sink_parameter_set_ref="s1", sink_coefficient_ref=2.0, potential_demand_g=0.60, timestep=3600.0, provenance="TASK_046P-D synthetic", is_synthetic_example=True)
DEMAND_A2 = OrganSinkDemand(demand_id="d_a2", plant_id="p1", organ_id="stem_1", organ_type="stem", structural_proxy_value=1.5, sink_parameter_set_ref="s1", sink_coefficient_ref=2.0, potential_demand_g=0.40, timestep=3600.0, provenance="TASK_046P-D synthetic", is_synthetic_example=True)

# CASE B — available 0.60, demand 1.00 (limited)
POOL_B = carbon_pool_from_reserve_and_net(0.0, 0.60, "p1", pool_id="pool_B", provenance="TASK_046P-D synthetic B", is_synthetic_example=True)
DEMAND_B = OrganSinkDemand(demand_id="d_b", plant_id="p1", organ_id="root_1", organ_type="root", structural_proxy_value=1.0, sink_parameter_set_ref="s1", sink_coefficient_ref=2.0, potential_demand_g=1.00, timestep=3600.0, provenance="TASK_046P-D synthetic", is_synthetic_example=True)

# CASE C — zero available
POOL_C = carbon_pool_from_reserve_and_net(0.0, 0.0, "p1", pool_id="pool_C", provenance="TASK_046P-D synthetic C", is_synthetic_example=True)
DEMAND_C = OrganSinkDemand(demand_id="d_c", plant_id="p1", organ_id="leaf_1", organ_type="leaf", structural_proxy_value=1.0, sink_parameter_set_ref="s1", sink_coefficient_ref=2.0, potential_demand_g=0.50, timestep=3600.0, provenance="TASK_046P-D synthetic", is_synthetic_example=True)

# CASE D — negative available (-0.40)
POOL_D = carbon_pool_from_reserve_and_net(0.10, -0.50, "p1", pool_id="pool_D", provenance="TASK_046P-D synthetic D", is_synthetic_example=True)
DEMAND_D = OrganSinkDemand(demand_id="d_d", plant_id="p1", organ_id="stem_1", organ_type="stem", structural_proxy_value=1.5, sink_parameter_set_ref="s1", sink_coefficient_ref=2.0, potential_demand_g=0.80, timestep=3600.0, provenance="TASK_046P-D synthetic", is_synthetic_example=True)

# CASE E — zero demand
POOL_E = carbon_pool_from_reserve_and_net(1.0, 0.3, "p1", pool_id="pool_E", provenance="TASK_046P-D synthetic E", is_synthetic_example=True)
DEMAND_E = OrganSinkDemand(demand_id="d_e", plant_id="p1", organ_id="leaf_1", organ_type="leaf", structural_proxy_value=1.0, sink_parameter_set_ref="s1", sink_coefficient_ref=2.0, potential_demand_g=0.0, timestep=3600.0, provenance="TASK_046P-D synthetic", is_synthetic_example=True)
