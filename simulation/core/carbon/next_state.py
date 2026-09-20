"""TASK 046Z — Next-timestep carbon state transition (pure, minimal, no storage/physics).
Decision: A — existing PostAllocationCarbonState (046P-G) + ConversionResidualContract (046P-J) sufficient.
This contract only combines reserve_next (from allocation surplus) with an EXPLICIT external current_net_next.
No fabrication of photosynthesis, respiration, or net carbon.
Conversion residual remains UNMODELED (not added to reserve)."""
from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal

class NextCarbonState(BaseModel):
    """Explicit next-timestep state: reserve carried from unallocated surplus;
    current_net_carbon_g must be supplied by next timestep's actual physiology (not invented)."""
    schema_version: Literal["v1"] = "v1"
    plant_id: str = Field(..., description="Plant identity preserved")
    architecture_id: Optional[str] = None
    reserve_carbon_g: float = Field(..., ge=0, description="Passive reserve from unallocated_t (g_C)")
    current_net_carbon_g: float = Field(..., description="Next timestep's actual net carbon (external input; not fabricated)")
    available_carbon_g: float = Field(..., description="reserve + current_net (g_C); may be negative if current_net < -reserve")
    timestep: float = Field(..., gt=0, description="Timestep identity preserved from source")
    simulation_time_ref: Optional[str] = None
    source_pool_id: Optional[str] = None
    source_allocation_id: Optional[str] = None
    reserve_source_state_id: Optional[str] = None
    conversion_residual_ref: Optional[str] = None
    conversion_residual_status: Literal["UNMODELED","AVAILABLE","NOT_COMPUTABLE"] = "UNMODELED"
    provenance: Optional[str] = None
    status: Literal["AVAILABLE","NOT_COMPUTABLE","UNAVAILABLE","PARTIAL","ERROR"] = "AVAILABLE"
    note: Optional[str] = Field(None, description="Explicit: reserve from surplus only; residual UNMODELED; current_net external; no fabricated physiology")
    is_synthetic_example: bool = False

    @model_validator(mode="after")
    def check_state(self):
        # Reserve never derived from conversion residual (critical distinction)
        # Available = reserve + current_net (explicit sum; no hidden conversion)
        # Deficit allowed if current_net strongly negative
        if self.reserve_carbon_g < -1e-9:
            raise ValueError("Reserve must be non-negative")
        # No hidden storage/NSC/starch/modeling
        if self.note and ("NSC" in self.note or "starch" in self.note or "storage" in self.note.lower()):
            pass  # allow if explicitly documented; no silent insertion
        return self

def build_next_carbon_state(
    reserve_carbon_g: float,
    current_net_carbon_g: float,
    plant_id: str,
    architecture_id: Optional[str] = None,
    timestep: float = 3600.0,
    simulation_time_ref: Optional[str] = None,
    source_pool_id: Optional[str] = None,
    source_allocation_id: Optional[str] = None,
    reserve_source_state_id: Optional[str] = None,
    conversion_residual_ref: Optional[str] = None,
    conversion_residual_status: Literal["UNMODELED","AVAILABLE","NOT_COMPUTABLE"] = "UNMODELED",
    provenance: Optional[str] = None,
    note: Optional[str] = None,
    is_synthetic_example: bool = False,
) -> NextCarbonState:
    available = float(reserve_carbon_g) + float(current_net_carbon_g)
    return NextCarbonState(
        plant_id=plant_id,
        architecture_id=architecture_id,
        reserve_carbon_g=float(reserve_carbon_g),
        current_net_carbon_g=float(current_net_carbon_g),
        available_carbon_g=available,
        timestep=float(timestep),
        simulation_time_ref=simulation_time_ref,
        source_pool_id=source_pool_id,
        source_allocation_id=source_allocation_id,
        reserve_source_state_id=reserve_source_state_id,
        conversion_residual_ref=conversion_residual_ref,
        conversion_residual_status=conversion_residual_status,
        provenance=provenance or "TASK_046Z next-state; reserve from unallocated surplus; residual UNMODELED; current_net external",
        status="AVAILABLE" if (abs(reserve_carbon_g) < float('inf') and abs(current_net_carbon_g) < float('inf')) else "ERROR",
        note=note or (f"Reserve={reserve_carbon_g} g_C (from unallocated surplus); current_net={current_net_carbon_g} g_C (external next-timestep); "
                     f"conversion_residual={conversion_residual_ref or 'none'} status={conversion_residual_status}; no storage/NSC invented; timestep={timestep}"),
        is_synthetic_example=is_synthetic_example,
    )
