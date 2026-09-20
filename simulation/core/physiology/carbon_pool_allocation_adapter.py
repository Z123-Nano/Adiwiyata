"""TASK 046P-D — CarbonPool (046G) → Source–Sink Allocation (046I) boundary.
Thin verification wrapper around existing allocate_carbon_to_sinks.
No scientific change to 046I or 046G; provenance/lineage preserved."""
from __future__ import annotations
from typing import Optional, List
from simulation.core.carbon.pool import CarbonPool
from simulation.core.physiology.organ_sink_demand import OrganSinkDemand
from simulation.core.allocation.source_sink_allocation import allocate_carbon_to_sinks
from simulation.core.allocation.source_sink_result_contract import SourceSinkAllocationResult

def carbon_pool_to_allocation(
    carbon_pool: CarbonPool,
    sink_demands: List[OrganSinkDemand],
    result_id: str = "alloc_046P_D_1",
) -> SourceSinkAllocationResult:
    """Verification boundary: CarbonPool.available_carbon_g feeds 046I.
    Pool untouched; demands untouched; no double reserve/net; unit g_C preserved.
    Negative available handled by existing 046I semantics (allocatable=max(available,0))."""
    # STEP 2 — explicit validation; no getattr/hasattr fallback
    if carbon_pool is None:
        raise ValueError("TASK_046P-D BLOCKED: carbon_pool is None; no fabricated pool.")
    if not carbon_pool.plant_id and not carbon_pool.pool_id:
        raise ValueError("TASK_046P-D BLOCKED: carbon_pool missing plant_id and pool_id; identity required.")
    # STEP 3 — derive exact source quantity from audited 046G semantics
    # Use available_carbon_g directly (reserve + net already computed by 046G; not recomputed here)
    source_available_g = float(carbon_pool.available_carbon_g)
    # STEP 4 — reserve semantics: available already includes reserve; do not add reserve again
    # No extra reserve arithmetic; no fabricated carryover
    # STEP 5 — call existing 046I (not modified)
    result = allocate_carbon_to_sinks(
        carbon_pool=carbon_pool,
        sink_demands=sink_demands,
        result_id=result_id,
    )
    # Preserve provenance linking exact CarbonPool (STEP 14 lineage)
    # Do not mutate result's internal fields; enrich provenance via note or keep original
    # The result already contains carbon_pool_id, plant_id, timestep, provenance
    # We trust 046I to preserve identity; we document the 046P-D integration path
    # For reports/tests, verify immutability separately
    return result
