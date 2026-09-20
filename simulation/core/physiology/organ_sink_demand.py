"""TASK 046H-E — OrganSinkDemand scientific result contract.
Potential carbon demand BEFORE allocation / limitation / growth.
Unit: g_C per timestep (explicit). Not allocated carbon."""
from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal

class OrganSinkDemand(BaseModel):
    """Per-organ potential carbon demand — pure derivation; no carbon supply input."""
    demand_id: str = Field(..., description="Stable demand result identity")
    plant_id: str = Field(..., description="Owning plant")
    architecture_id: Optional[str] = None
    organ_id: str = Field(..., description="Organ identity (PlantOrgan.id)")
    organ_type: Literal["root","stem","branch","leaf","flower","fruit","seed","axis","internode","bud","other"] = Field(...)
    # Structural proxy (explicit — no hidden inference)
    structural_proxy_value: Optional[float] = Field(None, description="Value of proxy quantity used (e.g. length_m in m)")
    structural_proxy_unit: Literal["m","m2","dimensionless","none"] = "m"
    structural_proxy_reference: Literal["length_m","radius_m","geometry_metadata","none"] = "length_m"
    # Developmental context (from 046H-D; not fabricated)
    developmental_state_ref: Optional[str] = Field(None, description="Reference to OrganDevelopmentalState.organ_developmental_state_id if used")
    growth_window_active: Optional[Literal["INSIDE","OUTSIDE","UNAVAILABLE"]] = None
    # Sink parameters
    sink_parameter_set_ref: str = Field(..., description="Reference to SinkParameterSet.parameter_set_id")
    sink_coefficient_ref: float = Field(..., description="Coefficient value used (g_C / m / timestep)")
    # Result
    potential_demand_g: float = Field(..., ge=0, description="Potential carbon demand for this timestep; g_C; never negative")
    demand_kind: Literal["POTENTIAL_CARBON_DEMAND"] = "POTENTIAL_CARBON_DEMAND"
    timestep: float = Field(..., gt=0, description="Simulation timestep in seconds")
    simulation_time_ref: Optional[str] = None
    # Status / provenance
    status: Literal["AVAILABLE","NOT_COMPUTABLE","UNAVAILABLE","ERROR"] = "AVAILABLE"
    provenance: Optional[str] = None
    source_reference: Optional[str] = None
    parameter_version: Optional[str] = "v1"
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"
    note: Optional[str] = Field(None, description="Limitations: structural proxy = length_m only; no biomass; physiological_age unavailable; no growth equation.")

    @model_validator(mode="after")
    def check_non_negative(self):
        if self.potential_demand_g < 0:
            raise ValueError("potential_demand_g must not be negative")
        if self.timestep <= 0:
            raise ValueError("timestep must be positive")
        return self

def derive_organ_sink_demand(
    organ,  # PlantOrgan (domain only; read-only)
    sink_parameters,  # SinkParameterSet
    developmental_state=None,  # OrganDevelopmentalState or None
    timestep: float = 3600.0,
    simulation_time_ref: Optional[str] = None,
    provenance_suffix: Optional[str] = None,
) -> OrganSinkDemand:
    """Pure derivation — no mutation, no carbon source access, no photosynthesis.
    Formula: potential_demand_g = coef * length_m if proxy available and window eligible.
    Developmental gating: window inside → eligible (factor 1); outside → 0; unavailable → 1 (conservative, documented)."""
    # Identity
    plant_id = getattr(organ, "plant_id", None) or "unknown"
    architecture_id = getattr(organ, "topology_ref", None)
    organ_id = getattr(organ, "id", None) or "unknown"
    organ_type = getattr(organ, "organ_type", "other")
    # Structural proxy audit (Step 2 — explicit, not hidden)
    length_m = getattr(organ, "length_m", None)
    if length_m is None or length_m < 0:
        return OrganSinkDemand(
            demand_id=f"demand_{organ_id}_notcomputable",
            plant_id=plant_id,
            architecture_id=architecture_id,
            organ_id=organ_id,
            organ_type=organ_type,
            structural_proxy_value=None,
            structural_proxy_unit="m",
            structural_proxy_reference="length_m",
            developmental_state_ref=getattr(developmental_state, "organ_developmental_state_id", None) if developmental_state else None,
            growth_window_active="UNAVAILABLE",
            sink_parameter_set_ref=sink_parameters.parameter_set_id,
            sink_coefficient_ref=sink_parameters.sink_coefficient_g_per_m_per_timestep,
            potential_demand_g=0.0,
            demand_kind="POTENTIAL_CARBON_DEMAND",
            timestep=timestep,
            simulation_time_ref=simulation_time_ref,
            status="NOT_COMPUTABLE",
            provenance=f"TASK_046H-E NOT_COMPUTABLE; structural_proxy (length_m) missing or negative; organ={organ_id}",
            source_reference=provenance_suffix,
            parameter_version="v1",
            is_synthetic_example=True,
            note="Blocked: no defensible structural proxy available (length_m missing/negative).",
        )
    # Developmental gating (Step 6)
    window_active = "UNAVAILABLE"
    factor = 1.0
    if developmental_state is not None:
        start = getattr(developmental_state, "growth_window_start", None)
        end = getattr(developmental_state, "growth_window_end", None)
        if start is not None and end is not None:
            sim_ref = simulation_time_ref
            if sim_ref is not None:
                try:
                    from datetime import datetime
                    if isinstance(sim_ref, str):
                        sim_dt = datetime.fromisoformat(sim_ref.replace("Z", "+00:00"))
                    else:
                        sim_dt = sim_ref
                    if sim_dt < start:
                        window_active = "OUTSIDE"
                        factor = 0.0
                    elif sim_dt > end:
                        window_active = "OUTSIDE"
                        factor = 0.0
                    else:
                        window_active = "INSIDE"
                        factor = 1.0
                except Exception:
                    window_active = "UNAVAILABLE"
                    factor = 1.0  # conservative: if comparison fails, don't fabricate zero
            else:
                # Window defined but simulation time reference unavailable — conservative eligible
                window_active = "INSIDE"
                factor = 1.0
        else:
            window_active = "UNAVAILABLE"
            factor = 1.0
    # Derivation (pure; no allocation; no carbon pool; no photosynthesis)
    demand = sink_parameters.sink_coefficient_g_per_m_per_timestep * float(length_m) * factor
    # Explicit limitation note
    note_text = (
        "Potential carbon demand (HYBRID_MINIMAL_SINK_MODEL). "
        "Structural proxy = length_m (unit m); no biomass/surface-area contract; "
        "physiological_age unavailable; growth_window used when defined; "
        "not allocated carbon; not growth; no geometry mutation."
    )
    return OrganSinkDemand(
        demand_id=f"demand_{organ_id}_{int(timestep)}",
        plant_id=plant_id,
        architecture_id=architecture_id,
        organ_id=organ_id,
        organ_type=organ_type,
        structural_proxy_value=float(length_m),
        structural_proxy_unit="m",
        structural_proxy_reference="length_m",
        developmental_state_ref=getattr(developmental_state, "organ_developmental_state_id", None) if developmental_state else None,
        growth_window_active=window_active,
        sink_parameter_set_ref=sink_parameters.parameter_set_id,
        sink_coefficient_ref=sink_parameters.sink_coefficient_g_per_m_per_timestep,
        potential_demand_g=float(demand),
        demand_kind="POTENTIAL_CARBON_DEMAND",
        timestep=timestep,
        simulation_time_ref=simulation_time_ref,
        status="AVAILABLE",
        provenance=(provenance_suffix or "TASK_046H-E") + f"; coeff={sink_parameters.sink_coefficient_g_per_m_per_timestep}; proxy=length_m; factor={factor}; window={window_active}",
        source_reference=provenance_suffix,
        parameter_version="v1",
        is_synthetic_example=sink_parameters.is_synthetic_example,
        note=note_text,
    )


def organ_sink_demand(
    demand_id: str,
    plant_id: str,
    organ_id: str,
    organ_type: str,
    structural_proxy_value: Optional[float],
    sink_parameter_set_ref: str,
    sink_coefficient_ref: float,
    timestep: float,
    architecture_id: Optional[str] = None,
    developmental_state_ref: Optional[str] = None,
    growth_window_active: Optional[str] = None,
    simulation_time_ref: Optional[str] = None,
    provenance: Optional[str] = None,
    source_reference: Optional[str] = None,
    is_synthetic_example: bool = False,
    note: Optional[str] = None,
) -> OrganSinkDemand:
    # Derivation is done externally; this factory receives computed value
    # to keep separation; for direct use, see derive_organ_sink_demand
    demand = structural_proxy_value if structural_proxy_value is not None else 0.0
    # Note: actual coefficient multiplication done by derivation function
    return OrganSinkDemand(
        demand_id=demand_id,
        plant_id=plant_id,
        architecture_id=architecture_id,
        organ_id=organ_id,
        organ_type=organ_type,
        structural_proxy_value=structural_proxy_value,
        structural_proxy_unit="m",
        structural_proxy_reference="length_m",
        developmental_state_ref=developmental_state_ref,
        growth_window_active=growth_window_active,
        sink_parameter_set_ref=sink_parameter_set_ref,
        sink_coefficient_ref=sink_coefficient_ref,
        potential_demand_g=float(demand * sink_coefficient_ref) if structural_proxy_value is not None else 0.0,
        demand_kind="POTENTIAL_CARBON_DEMAND",
        timestep=timestep,
        simulation_time_ref=simulation_time_ref,
        status="AVAILABLE" if structural_proxy_value is not None else "NOT_COMPUTABLE",
        provenance=provenance or f"TASK_046H-E OrganSinkDemand v1; organ={organ_id}; proxy=length_m; coeff_ref={sink_coefficient_ref}",
        source_reference=source_reference,
        parameter_version="v1",
        is_synthetic_example=is_synthetic_example,
        note=note or "Potential demand only; no allocation; structural proxy = length_m (no biomass); physiological age unavailable.",
    )
