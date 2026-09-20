"""TASK 046P-C — CarbonBalance (TASK 021) → CarbonPool (TASK 046G) boundary.
No allocation (046I); no growth conversion (046J); no second integration.
Explicit reserve required; net from TASK 021; available = reserve + net."""
from __future__ import annotations
from typing import Optional
from simulation.core.carbon.carbon import CarbonResult, carbon_respiration
from simulation.core.carbon.pool import CarbonPool, carbon_pool_from_reserve_and_net

def build_carbon_pool_from_balance(
    carbon_balance_result: CarbonResult,
    reserve_carbon_g: float,
    plant_id: str,
    architecture_id: Optional[str] = None,
    pool_id: Optional[str] = None,
    previous_pool_id: Optional[str] = None,
    timestep: float = 3600.0,
    simulation_time: Optional[str] = None,
    provenance_suffix: Optional[str] = None,
    parameter_version: Optional[str] = "v1",
    is_synthetic_example: bool = False,
) -> CarbonPool:
    """Pure integration: TASK 021 net → CarbonPool with explicit reserve.
    No allocation; no remobilization; no growth conversion."""
    # STEP 1 — verify TASK 021 identity
    if carbon_balance_result.status != "AVAILABLE":
        return CarbonPool(
            pool_id=pool_id or f"pool_{plant_id}_unavailable",
            plant_id=plant_id,
            architecture_id=architecture_id,
            reserve_carbon_g=reserve_carbon_g,
            current_net_carbon_g=0.0,
            available_carbon_g=reserve_carbon_g,
            timestep=timestep,
            simulation_time=simulation_time,
            status="NOT_COMPUTABLE",
            provenance=f"TASK_046P-C blocked: TASK 021 carbon status={carbon_balance_result.status}; no pool.",
            note="Upstream carbon balance unavailable; reserve preserved; pool not constructed.",
            source_carbon_result_id=getattr(carbon_balance_result, "result_id", None),
            previous_pool_id=previous_pool_id,
            parameter_version=parameter_version,
            is_synthetic_example=is_synthetic_example,
        )
    # STEP 2 — consume canonical net field (no recomputation)
    net = carbon_balance_result.net_carbon_g
    # STEP 6 — preserve sign; do not clamp negative
    # Step 4 — reserve explicit; no automatic carryover from previous pool
    pool = carbon_pool_from_reserve_and_net(
        reserve_carbon_g=float(reserve_carbon_g),
        current_net_carbon_g=float(net),
        plant_id=plant_id,
        pool_id=pool_id,
        previous_pool_id=previous_pool_id,
        architecture_id=architecture_id,
        timestep=timestep,
        simulation_time=simulation_time,
        provenance=f"TASK_046P-C from TASK_021 net={net}; reserve={reserve_carbon_g}; available={float(reserve_carbon_g)+float(net)}; {provenance_suffix or ''}",
        note=f"TASK_046P-C boundary: reserve={reserve_carbon_g} + net={net} = available={float(reserve_carbon_g)+float(net)}; sign preserved; g_C; no allocation; no 046J.",
        source_carbon_result_id=getattr(carbon_balance_result, "result_id", None),
        parameter_version=parameter_version,
        is_synthetic_example=is_synthetic_example,
    )
    # STEP 9 — source lineage preserved; previous_pool only when explicitly supplied (already handled)
    # STEP 14 — provenance records source, method, timestep, simulation_time
    return pool
