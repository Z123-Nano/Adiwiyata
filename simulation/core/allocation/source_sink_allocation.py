"""TASK 046I — Pure source-sink allocation derivation over CarbonPool + OrganSinkDemand list."""
from __future__ import annotations
from typing import Optional, List
from simulation.core.carbon.pool import CarbonPool
from simulation.core.physiology.organ_sink_demand import OrganSinkDemand
from simulation.core.allocation.source_sink_result_contract import SourceSinkAllocationResult, OrganAllocationItem

def allocate_carbon_to_sinks(
    carbon_pool: CarbonPool,
    sink_demands: List[OrganSinkDemand],
    result_id: str = "alloc_1",
) -> SourceSinkAllocationResult:
    """Pure; no mutation of carbon_pool or sink_demands; no growth; no topology."""
    # Status / validity checks
    if carbon_pool is None:
        return SourceSinkAllocationResult(
            result_id=result_id, plant_id="",
            timestep=0.0,
            source_available_carbon_g=0.0, allocatable_carbon_g=0.0,
            total_potential_demand_g=0.0, total_allocated_carbon_g=0.0,
            total_unmet_demand_g=0.0, unallocated_carbon_g=0.0,
            allocations=[], status="NOT_COMPUTABLE",
            provenance="TASK_046I blocked: carbon_pool missing",
            note="Allocation not performed: CarbonPool unavailable.")
    # Extract pool values without mutation
    plant_id = carbon_pool.plant_id
    if not plant_id:
        return SourceSinkAllocationResult(
            result_id=result_id, plant_id="",
            timestep=float(carbon_pool.timestep) if (getattr(carbon_pool,"timestep",None) and float(carbon_pool.timestep)>0) else 0.0,
            source_available_carbon_g=float(carbon_pool.available_carbon_g) if hasattr(carbon_pool,"available_carbon_g") else 0.0,
            allocatable_carbon_g=max(float(carbon_pool.available_carbon_g) if hasattr(carbon_pool,"available_carbon_g") else 0.0,0.0),
            total_potential_demand_g=0.0, total_allocated_carbon_g=0.0,
            total_unmet_demand_g=0.0, unallocated_carbon_g=0.0,
            allocations=[], status="NOT_COMPUTABLE",
            provenance="TASK_046I blocked: carbon_pool missing plant_id",
            note="Pool identity required; no fabricated identity.")
    # Timestep must exist and be positive per TASK 046G
    ts_raw = getattr(carbon_pool, "timestep", None)
    if ts_raw is None or (isinstance(ts_raw, (int,float)) and float(ts_raw) <= 0) or (isinstance(ts_raw, str) and (float(ts_raw) <= 0 if ts_raw.replace('.','',1).isdigit() else True)):
        return SourceSinkAllocationResult(
            result_id=result_id, plant_id=plant_id,
            timestep=0.0,
            source_available_carbon_g=float(carbon_pool.available_carbon_g) if hasattr(carbon_pool,"available_carbon_g") else 0.0,
            allocatable_carbon_g=max(float(carbon_pool.available_carbon_g) if hasattr(carbon_pool,"available_carbon_g") else 0.0,0.0),
            total_potential_demand_g=0.0, total_allocated_carbon_g=0.0,
            total_unmet_demand_g=0.0, unallocated_carbon_g=0.0,
            allocations=[], status="NOT_COMPUTABLE",
            provenance="TASK_046I blocked: invalid or missing timestep",
            note="Pool timestep missing or non-positive; not fabricated.")
    timestep = float(ts_raw)
    architecture_id = carbon_pool.architecture_id
    source_available = float(carbon_pool.available_carbon_g)
    allocatable = max(source_available, 0.0)
    pool_id = carbon_pool.pool_id
    # Demand validation: distinguish missing list from empty list; reject negative
    if sink_demands is None:
        return SourceSinkAllocationResult(
            result_id=result_id, plant_id=plant_id if 'plant_id' in locals() else (carbon_pool.plant_id or ""),
            timestep=float(carbon_pool.timestep) if carbon_pool.timestep else 0.0,
            source_available_carbon_g=float(carbon_pool.available_carbon_g) if hasattr(carbon_pool,"available_carbon_g") else 0.0,
            allocatable_carbon_g=max(float(carbon_pool.available_carbon_g) if hasattr(carbon_pool,"available_carbon_g") else 0.0, 0.0),
            total_potential_demand_g=0.0, total_allocated_carbon_g=0.0,
            total_unmet_demand_g=0.0,
            allocations=[], status="NOT_COMPUTABLE",
            provenance="TASK_046I blocked: sink_demands is None",
            note="Demand list missing.",
            unallocated_carbon_g=max(float(carbon_pool.available_carbon_g) if hasattr(carbon_pool,"available_carbon_g") else 0.0, 0.0))
    demands = []
    total_demand = 0.0
    for d in sink_demands:
        if d is None:
            return SourceSinkAllocationResult(
                result_id=result_id, plant_id=plant_id,
                timestep=timestep, source_available_carbon_g=source_available,
                allocatable_carbon_g=allocatable, total_potential_demand_g=total_demand,
                total_allocated_carbon_g=0.0, total_unmet_demand_g=0.0,
                unallocated_carbon_g=max(source_available,0.0), allocations=[],
                status="NOT_COMPUTABLE",
                provenance="TASK_046I blocked: None demand item in list",
                note="Invalid None item in sink_demands.")
        demand = float(d.potential_demand_g) if d.potential_demand_g is not None else 0.0
        if demand < -1e-6:
            return SourceSinkAllocationResult(
                result_id=result_id, plant_id=plant_id,
                timestep=timestep, source_available_carbon_g=source_available,
                allocatable_carbon_g=allocatable, total_potential_demand_g=total_demand,
                total_allocated_carbon_g=0.0, total_unmet_demand_g=0.0,
                unallocated_carbon_g=max(source_available,0.0), allocations=[],
                status="NOT_COMPUTABLE",
                provenance="TASK_046I blocked: negative demand in input",
                note="Invalid negative potential demand detected; not silently converted to zero.")
        demands.append((d, max(demand, 0.0)))
        total_demand += max(demand, 0.0)
    # Case 2 — zero total demand
    if total_demand <= 1e-9:
        items = []
        for d, val in demands:
            items.append(OrganAllocationItem(
                organ_id=d.organ_id or "",
                organ_type=d.organ_type or "other",
                potential_demand_g=val,
                allocated_carbon_g=0.0,
                unmet_demand_g=0.0,
                allocation_fraction=0.0,
                status="AVAILABLE",
                provenance=d.provenance or "TASK_046I"))
        return SourceSinkAllocationResult(
            result_id=result_id, plant_id=plant_id, architecture_id=architecture_id,
            carbon_pool_id=pool_id, timestep=timestep,
            simulation_time_ref=str(carbon_pool.simulation_time) if carbon_pool.simulation_time else None,
            source_available_carbon_g=source_available,
            allocatable_carbon_g=allocatable,
            total_potential_demand_g=0.0,
            total_allocated_carbon_g=0.0,
            total_unmet_demand_g=0.0,
            unallocated_carbon_g=allocatable,
            allocations=items,
            status="AVAILABLE",
            provenance=f"TASK_046I; pool={pool_id}; case=zero_demand; available={source_available}",
            note="No positive demand; all available carbon unallocated.",
            is_synthetic_example=carbon_pool.is_synthetic_example if hasattr(carbon_pool,"is_synthetic_example") else False)
    # Allocation computations
    total_alloc = 0.0
    items = []
    # Case 1 — no positive allocatable carbon (A <= 0)
    if allocatable <= 1e-9:
        for d, val in demands:
            items.append(OrganAllocationItem(
                organ_id=d.organ_id or "",
                organ_type=d.organ_type or "other",
                potential_demand_g=val,
                allocated_carbon_g=0.0,
                unmet_demand_g=val,
                allocation_fraction=0.0,
                status="AVAILABLE",
                provenance=d.provenance or "TASK_046I"))
        return SourceSinkAllocationResult(
            result_id=result_id, plant_id=plant_id, architecture_id=architecture_id,
            carbon_pool_id=pool_id, timestep=timestep,
            simulation_time_ref=str(carbon_pool.simulation_time) if carbon_pool.simulation_time else None,
            source_available_carbon_g=source_available,
            allocatable_carbon_g=0.0,
            total_potential_demand_g=total_demand,
            total_allocated_carbon_g=0.0,
            total_unmet_demand_g=total_demand,
            unallocated_carbon_g=max(float(carbon_pool.available_carbon_g) if hasattr(carbon_pool,"available_carbon_g") else 0.0, 0.0),
            allocations=items,
            status="AVAILABLE",
            provenance=f"TASK_046I; pool={pool_id}; case=negative_or_zero_source; available={source_available}",
            note="Source carbon non-positive; zero allocation; original pool unchanged; all demand unmet.",
            is_synthetic_example=carbon_pool.is_synthetic_example if hasattr(carbon_pool,"is_synthetic_example") else False)
    # Case 3 — sufficient (A >= D_total) and Case 4 — limited (0 < A < D_total)
    for d, val in demands:
        if total_demand <= allocatable + 1e-9:
            # Sufficient case
            allocated = val
            unmet = 0.0
            fraction = 1.0 if val > 1e-9 else 0.0
        else:
            # Limited — relative
            fraction = val / total_demand
            allocated = allocatable * fraction
            unmet = val - allocated
        # Round to avoid float drift; use tolerance at result level
        allocated = round(allocated, 10)
        unmet = round(unmet, 10)
        total_alloc += allocated
        items.append(OrganAllocationItem(
            organ_id=d.organ_id or "",
            organ_type=d.organ_type or "other",
            potential_demand_g=val,
            allocated_carbon_g=allocated,
            unmet_demand_g=unmet,
            allocation_fraction=fraction,
            status="AVAILABLE",
            provenance=d.provenance or "TASK_046I"))
    unallocated = round(allocatable - total_alloc, 10)
    # Force exact conservation for reported totals
    # (float rounding may leave 1e-9; result validator uses 1e-6)
    result = SourceSinkAllocationResult(
        result_id=result_id, plant_id=plant_id, architecture_id=architecture_id,
        carbon_pool_id=pool_id, timestep=timestep,
        simulation_time_ref=str(carbon_pool.simulation_time) if carbon_pool.simulation_time else None,
        source_available_carbon_g=source_available,
        allocatable_carbon_g=allocatable,
        total_potential_demand_g=total_demand,
        total_allocated_carbon_g=round(total_alloc, 10),
        total_unmet_demand_g=round(sum(i.unmet_demand_g for i in items), 10),
        unallocated_carbon_g=unallocated,
        allocations=items,
        status="AVAILABLE",
        provenance=f"TASK_046I; pool={pool_id}; case={'sufficient' if allocatable >= total_demand - 1e-9 else 'limited'}; source_available={source_available}",
        note="Proportional allocation only; no topology/priority; carbon_pool unchanged; demand preserved.",
        is_synthetic_example=getattr(carbon_pool,"is_synthetic_example",False) if hasattr(carbon_pool,"is_synthetic_example") else False,
    )
    return result
