"""TASK 046P-C fixtures — synthetic TASK 021 → CarbonPool."""
from simulation.core.carbon.carbon import CarbonResult
from simulation.core.physiology.carbon_pool_adapter import build_carbon_pool_from_balance

BALANCE_01 = CarbonResult(
    gross_carbon_g=1.20,
    respiration_g=0.30,
    net_carbon_g=0.90,
    timestep=3600.0,
    status="AVAILABLE",
    provenance="TASK_021 synthetic; gross=1.20; resp=0.30; net=0.90",
    parameter_version="v1",
    is_synthetic_example=True,
    result_id="bal_01",
)

RESERVE_01 = 0.40  # explicit; not automatically carried
EXPECTED_AVAILABLE = 1.30

# Negative net
BALANCE_NEG = CarbonResult(gross_carbon_g=0.5, respiration_g=0.9, net_carbon_g=-0.4, timestep=3600.0, status="AVAILABLE", provenance="TASK_021 negative", parameter_version="v1", is_synthetic_example=True, result_id="bal_neg")
RESERVE_NEG = 1.0
EXPECTED_NEG_AVAILABLE = 0.6
