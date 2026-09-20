"""TASK 046I fixtures — synthetic; labeled."""
from simulation.core.carbon.pool import carbon_pool_from_reserve_and_net
from simulation.core.physiology.organ_sink_demand import OrganSinkDemand

# Positive pool 15 g
POOL_POS = carbon_pool_from_reserve_and_net(10.0, 5.0, "p1", pool_id="pool_046i_1", provenance="TASK_046I synthetic")
# Zero pool
POOL_ZERO = carbon_pool_from_reserve_and_net(0.0, 0.0, "p1", pool_id="pool_046i_0", provenance="TASK_046I synthetic")
# Negative pool -5 g
POOL_NEG = carbon_pool_from_reserve_and_net(10.0, -15.0, "p1", pool_id="pool_046i_neg", provenance="TASK_046I synthetic")

# Demand fixtures
DEMAND_1 = OrganSinkDemand(demand_id="d1", plant_id="p1", organ_id="leaf_1", organ_type="leaf", structural_proxy_value=1.0, sink_parameter_set_ref="s1", sink_coefficient_ref=2.0, potential_demand_g=2.0, timestep=3600.0, provenance="TASK_046I synthetic", is_synthetic_example=True)
DEMAND_2 = OrganSinkDemand(demand_id="d2", plant_id="p1", organ_id="stem_1", organ_type="stem", structural_proxy_value=1.5, sink_parameter_set_ref="s1", sink_coefficient_ref=2.0, potential_demand_g=3.0, timestep=3600.0, provenance="TASK_046I synthetic", is_synthetic_example=True)
