"""Source-sink allocation — TASK 022. Proportional by demand; no growth; deterministic; same unit as TASK 021."""
from __future__ import annotations
from typing import Optional
from simulation.core.allocation.contracts import (
    CarbonSource, CarbonSink, SourceSinkAllocationRequest,
    SourceSinkAllocationResult, SinkAllocation,
)

TOL = 1e-6

POLICY = "proportional_demand"


def allocate_source_sink(request: SourceSinkAllocationRequest) -> SourceSinkAllocationResult:
    # Propagate upstream invalid/non-computable source if request indicates it
    if request.source.status in ("INVALID_INPUT", "NOT_COMPUTABLE", "NOT_IMPLEMENTED"):
        return SourceSinkAllocationResult(
            status=request.source.status,
            source_carbon=request.source.available_carbon,
            total_allocated=0.0,
            unallocated_carbon=0.0,
            carbon_deficit=max(0.0, -request.source.available_carbon),
            sink_allocations=[],
            unmet_demand_total=0.0,
            conservation_check="upstream source status propagated",
            provenance=request.provenance or "TASK_022; upstream source invalid",
            notes="Source status not VALID; allocation deferred.",
            is_synthetic_example=request.is_synthetic_example,
        )
    source = request.source
    available = source.available_carbon
    # Negative available: deficit, no allocation
    if available < 0:
        deficit = -available
        return SourceSinkAllocationResult(
            status="VALID",
            source_carbon=available,
            total_allocated=0.0,
            unallocated_carbon=0.0,
            carbon_deficit=deficit,
            sink_allocations=[],
            unmet_demand_total=0.0,
            conservation_check=f"deficit={deficit}; source={available}; allocated=0",
            provenance=request.provenance or "TASK_022; negative source => deficit only",
            notes="Negative available carbon; no sink allocation; deficit recorded.",
            is_synthetic_example=request.is_synthetic_example,
        )
    # Validate sinks
    allocs: list[SinkAllocation] = []
    eligible: list[CarbonSink] = []
    invalid_reasons: list[str] = []
    for s in sorted(request.sinks, key=lambda x: x.sink_id):
        if s.demand is None:
            allocs.append(SinkAllocation(
                sink_id=s.sink_id, allocated_carbon=0.0, demand=None,
                unmet_demand=0.0, status="NOT_COMPUTABLE",
            ))
            invalid_reasons.append(f"{s.sink_id}: demand unavailable")
            continue
        if s.demand < 0:
            allocs.append(SinkAllocation(
                sink_id=s.sink_id, allocated_carbon=0.0, demand=s.demand,
                unmet_demand=0.0, status="INVALID_INPUT",
            ))
            invalid_reasons.append(f"{s.sink_id}: negative demand={s.demand}")
            continue
        # capacity unenforced in v1; check only negative
        if s.capacity is not None and s.capacity < 0:
            allocs.append(SinkAllocation(
                sink_id=s.sink_id, allocated_carbon=0.0, demand=s.demand,
                unmet_demand=0.0, status="INVALID_INPUT",
            ))
            invalid_reasons.append(f"{s.sink_id}: negative capacity")
            continue
        eligible.append(s)
    # If any sink had invalid input, result reflects that but still attempts valid sinks? Per spec: explicit errors preferred.
    # For simplicity: if any INVALID_INPUT sink present and no eligible sinks => INVALID_INPUT; else proceed with eligible.
    if invalid_reasons:
        # Keep eligible allocation if any eligible remain; else INVALID_INPUT
        if not eligible:
            return SourceSinkAllocationResult(
                status="INVALID_INPUT",
                source_carbon=available,
                total_allocated=0.0,
                unallocated_carbon=available,
                carbon_deficit=0.0,
                sink_allocations=allocs,
                unmet_demand_total=sum(a.unmet_demand for a in allocs),
                conservation_check="invalid sink input; no eligible sinks",
                provenance=request.provenance or "TASK_022; sink invalid",
                notes="; ".join(invalid_reasons),
                is_synthetic_example=request.is_synthetic_example,
            )
    # Proportional by demand (v1 policy)
    total_demand = sum(s.demand for s in eligible if s.demand is not None)
    if total_demand <= 0:
        # Zero or no demand among eligible: all unallocated; eligible get 0
        result_allocs = allocs + [
            SinkAllocation(sink_id=s.sink_id, allocated_carbon=0.0, demand=s.demand,
                           unmet_demand=s.demand or 0.0, status="VALID")
            for s in sorted(eligible, key=lambda x: x.sink_id)
        ]
        # Sort deterministically
        result_allocs.sort(key=lambda a: a.sink_id)
        total_alloc = 0.0
        unmet = sum(s.demand or 0.0 for s in eligible)
        return SourceSinkAllocationResult(
            status="VALID",
            source_carbon=available,
            total_allocated=total_alloc,
            unallocated_carbon=available,
            carbon_deficit=0.0,
            sink_allocations=result_allocs,
            unmet_demand_total=unmet,
            conservation_check=f"total_demand={total_demand}; allocated=0; unallocated={available}",
            provenance=request.provenance or "TASK_022; zero demand => unallocated",
            notes="Zero total eligible demand.",
            is_synthetic_example=request.is_synthetic_example,
        )
    C = available
    allocations_by_id: dict[str, float] = {}
    for s in sorted(eligible, key=lambda x: x.sink_id):
        d = s.demand or 0.0
        alloc = (d / total_demand) * C
        # Cap at demand (if total demand > C, proportional satisfies this by construction; guard for fp)
        alloc = min(alloc, d)
        allocations_by_id[s.sink_id] = alloc
    # Recompute after caps to ensure conservation with floating point
    total_alloc = sum(allocations_by_id.values())
    unallocated = C - total_alloc
    # Build allocations; include already-invalid ones (preserved in order sorted by sink_id, valid first then invalid by insertion already)
    complete_allocs = list(allocs) + [
        SinkAllocation(
            sink_id=s.sink_id,
            allocated_carbon=round(allocations_by_id[s.sink_id], 6),
            demand=s.demand,
            unmet_demand=max(0.0, (s.demand or 0.0) - allocations_by_id[s.sink_id]),
            status="VALID",
        )
        for s in sorted(eligible, key=lambda x: x.sink_id)
    ]
    # Fix typo above by rebuilding cleanly
    complete_allocs = []
    # Start with previously computed invalid/service sinks (from allocs, sorted already by insertion order -> sort for determinism)
    for a in sorted(allocs, key=lambda x: x.sink_id):
        complete_allocs.append(a)
    for s in sorted(eligible, key=lambda x: x.sink_id):
        alloc = allocations_by_id[s.sink_id]
        d = s.demand or 0.0
        complete_allocs.append(SinkAllocation(
            sink_id=s.sink_id,
            allocated_carbon=round(alloc, 6),
            demand=d,
            unmet_demand=max(0.0, d - alloc),
            status="VALID",
        ))
    # Re-sort all by sink_id for deterministic output
    complete_allocs.sort(key=lambda a: a.sink_id)
    total_alloc = sum(a.allocated_carbon for a in complete_allocs if a.status == "VALID")
    # Note: only valid allocations count toward conservation; invalid receive 0 by construction
    unallocated = C - total_alloc
    # Floating-point guard: if close to zero treat as zero; don't widen arbitrarily
    if abs(unallocated) < TOL:
        unallocated = 0.0
    if abs(total_alloc) < TOL:
        total_alloc = 0.0
    # Conservation description
    conservation = f"sum(allocated)={total_alloc}; unallocated={unallocated}; source={C}; diff={round(C - (total_alloc + unallocated), 8)}"
    # Unmet demand total only from eligible sinks
    unmet_total = sum(max(0.0, (s.demand or 0.0) - allocations_by_id[s.sink_id]) for s in eligible)
    return SourceSinkAllocationResult(
        status="VALID",
        source_carbon=C,
        total_allocated=round(total_alloc, 6),
        unallocated_carbon=round(unallocated, 6),
        carbon_deficit=0.0,
        sink_allocations=complete_allocs,
        unmet_demand_total=round(unmet_total, 6),
        conservation_check=conservation,
        provenance=request.provenance or "TASK_022; proportional_demand v1",
        notes="Proportional allocation by eligible demand. Not growth.",
        is_synthetic_example=request.is_synthetic_example,
    )
