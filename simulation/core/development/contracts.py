"""TASK 046H-D — Organ Developmental State domain contract.
Canonical representation of organ-level developmental context.
Not a sink-demand model; no derivation to OrganSinkDemand here.
References: PlantOrgan identity; PlantArchitecture; SimulationClock temporal semantics;
TASK 024 plant phenology (distinct from organ state)."""
from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal
from datetime import datetime

class OrganDevelopmentalState(BaseModel):
    """Organ-level developmental context — explicit, separate from plant phenology.
    Chronological age, physiological age, organ stage, initiation time all kept distinct.
    Physiological age is UNAVAILABLE until a domain definition exists (F/U).
    Growth window fields unavailable until a growth-window model is defined (I)."""
    organ_developmental_state_id: str = Field(..., description="Stable identity for this developmental-state record")
    plant_id: str = Field(..., description="Owning plant; required; not anonymous")
    architecture_id: Optional[str] = Field(None, description="Architecture reference; consistent with organ")
    organ_id: str = Field(..., description="Referenced organ identity (PlantOrgan.id); stable")
    organ_type: Literal["root","stem","branch","leaf","flower","fruit","seed","axis","internode","bud","other"] = Field(..., description="Organ type from PlantOrgan contract")
    parent_organ_id: Optional[str] = Field(None, description="Parent organ reference if available")
    # Initiation (D) — domain event, not inferred from observation/render/simulation time
    initiated_at: Optional[datetime] = Field(None, description="Organ initiation/reference timestamp; unavailable if unknown")
    # Chronological age (E) — explicit elapsed time since initiation, in days
    chronological_age_days: Optional[float] = Field(None, description="Chronological organ age in days since initiation; unavailable if initiation missing")
    # Physiological age (F) — explicitly NOT chronological age; unavailable until domain defined
    physiological_age: Optional[str] = Field(None, description="Physiological/developmental age category/index; unavailable — no domain definition yet")
    # Organ developmental stage (G) — optional; vocabulary future-defined; not copied from plant phenology
    organ_stage: Optional[str] = Field(None, description="Organ developmental stage (e.g., INITIATED/EXPANDING/MATURE/SENESCING/COMPLETED); vocabulary not yet enforced; unavailable if not set")
    # Growth window (I) — unavailable until model defined
    growth_window_start: Optional[datetime] = Field(None, description="Start of defined growth window; unavailable until model defined")
    growth_window_end: Optional[datetime] = Field(None, description="End of defined growth window; unavailable until model defined")
    # Active growth status (J) — not a boolean; derived from stage/context later, not inferred from geometry/biomass
    active_growth_status: Optional[Literal["ACTIVE","INACTIVE","COMPLETED","NOT_DEFINED"]] = Field(None, description="Derived status only when stage/context defines it; not inferred from geometry")
    # References (K) — references to temporal domain, not independent clocks
    simulation_time_ref: Optional[datetime] = Field(None, description="Reference to SimulationClock.simulation_time at state creation; context only")
    world_time_ref: Optional[datetime] = Field(None, description="Reference to SimulationClock.world_time; context only")
    observation_time_ref: Optional[datetime] = Field(None, description="Reference to last observation; context only")
    # Status / provenance (M/N)
    status: Literal["AVAILABLE","UNAVAILABLE","NOT_COMPUTABLE","ERROR"] = "AVAILABLE"
    provenance: Optional[str] = None
    source_reference: Optional[str] = Field(None, description="Source observation / model / inference reference; distinguish OBSERVED/MODELED/INFERRED/SYNTHETIC/CALIBRATED")
    source_type: Optional[Literal["OBSERVED","MODELED","INFERRED","SYNTHETIC","CALIBRATED"]] = None
    parameter_version: Optional[str] = "v1"
    schema_version: Literal["v1"] = "v1"
    is_synthetic_example: bool = False
    note: Optional[str] = Field(None, description="Explicit limitations (e.g., physiological_age unavailable; growth_window unavailable)")

    @model_validator(mode="after")
    def invariants(self):
        # 1 organ_id stable (presence enforced by required)
        # 3 architecture_id consistent (presence only; consistency enforced by caller)
        # 4 initiated_at does not move forward (immutability by design; no mutation mechanism)
        # 5 chronological_age non-negative
        if self.chronological_age_days is not None and self.chronological_age_days < 0:
            raise ValueError("chronological_age_days must not be negative")
        # 6 growth window order
        if (self.growth_window_start is not None and self.growth_window_end is not None
                and self.growth_window_end < self.growth_window_start):
            raise ValueError("growth_window_end must not precede growth_window_start")
        # 7 physiological_age is not automatically chronological_age (no derived relationship enforced here; both independent inputs)
        # 8 organ_stage is not automatically plant phenology (both independent)
        # 9 missing info remains explicit (optional fields allow None)
        # 10 source objects never mutated (factory pure — enforced by usage pattern, not mutable mechanism)
        return self

def organ_developmental_state(
    organ_developmental_state_id: str,
    plant_id: str,
    organ_id: str,
    organ_type: str,
    initiated_at: Optional[datetime] = None,
    chronological_age_days: Optional[float] = None,
    physiological_age: Optional[str] = None,
    organ_stage: Optional[str] = None,
    growth_window_start: Optional[datetime] = None,
    growth_window_end: Optional[datetime] = None,
    architecture_id: Optional[str] = None,
    parent_organ_id: Optional[str] = None,
    simulation_time_ref: Optional[datetime] = None,
    world_time_ref: Optional[datetime] = None,
    observation_time_ref: Optional[datetime] = None,
    provenance: Optional[str] = None,
    source_reference: Optional[str] = None,
    source_type: Optional[str] = None,
    active_growth_status: Optional[str] = None,
    status: Literal["AVAILABLE","UNAVAILABLE","NOT_COMPUTABLE","ERROR"] = "AVAILABLE",
    is_synthetic_example: bool = False,
    note: Optional[str] = None,
) -> OrganDevelopmentalState:
    """Deterministic factory — pure, no mutation of inputs, no inference from geometry/age/phenology."""
    return OrganDevelopmentalState(
        organ_developmental_state_id=organ_developmental_state_id,
        plant_id=plant_id,
        architecture_id=architecture_id,
        organ_id=organ_id,
        organ_type=organ_type,  # caller provides validated literal
        parent_organ_id=parent_organ_id,
        initiated_at=initiated_at,
        chronological_age_days=chronological_age_days,
        physiological_age=physiological_age,
        organ_stage=organ_stage,
        growth_window_start=growth_window_start,
        growth_window_end=growth_window_end,
        active_growth_status=active_growth_status,
        simulation_time_ref=simulation_time_ref,
        world_time_ref=world_time_ref,
        observation_time_ref=observation_time_ref,
        provenance=provenance or f"TASK_046H-D OrganDevelopmentalState v1; organ={organ_id}; status={status}",
        source_reference=source_reference,
        source_type=source_type,
        status=status,
        is_synthetic_example=is_synthetic_example,
        note=note or "Developmental-state representation only; no sink-demand/growth calculation; physiological_age unavailable until domain defined; growth_window unavailable until model defined.",
        parameter_version="v1",
    )
