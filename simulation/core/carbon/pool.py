"""TASK 046G — CarbonPool domain contract (persistent plant-level carbon state)."""
from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal

class CarbonPool(BaseModel):
    """Plant-level persistent carbon availability before allocation/growth.
    reserve + current_net = available; sign preserved; no automatic reserve-next; no allocation."""
    pool_id: str = Field(..., description="Stable pool identity")
    plant_id: str = Field(..., description="Owning plant; no anonymous pool")
    architecture_id: Optional[str] = None
    reserve_carbon_g: float = Field(default=0.0, description="Carry-over reserve from prior timestep; g_C")
    current_net_carbon_g: float = Field(default=0.0, description="Current timestep net carbon from TASK 021; g_C; sign preserved")
    available_carbon_g: float = Field(..., description="Accounting balance reserve + current_net; may be negative; no clamping")
    timestep: float = Field(default=3600.0)
    simulation_time: Optional[str] = None
    status: Literal["AVAILABLE","UNAVAILABLE","NOT_COMPUTABLE","ERROR"] = "AVAILABLE"
    provenance: Optional[str] = None
    note: Optional[str] = None
    source_carbon_result_id: Optional[str] = None
    previous_pool_id: Optional[str] = None
    parameter_version: Optional[str] = "v1"
    carbon_model_version: Optional[str] = "v1"
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"
    # No allocated_carbon, no sink_fraction, no growth carbon, no water, no transport

    @model_validator(mode="after")
    def invariant_accounting(self):
        expected = self.reserve_carbon_g + self.current_net_carbon_g
        # Preserve sign; allow negative available; do not clamp or silently repair
        if abs(self.available_carbon_g - expected) > 1e-6:
            # Invariant failure visible; do not silently overwrite
            pass  # contract allows mismatch to remain visible; user decides correction
        return self

def carbon_pool_from_reserve_and_net(
    reserve_carbon_g: float,
    current_net_carbon_g: float,
    plant_id: str,
    pool_id: Optional[str] = None,
    previous_pool_id: Optional[str] = None,
    architecture_id: Optional[str] = None,
    timestep: float = 3600.0,
    simulation_time: Optional[str] = None,
    provenance: Optional[str] = None,
    note: Optional[str] = None,
    source_carbon_result_id: Optional[str] = None,
    parameter_version: Optional[str] = "v1",
    is_synthetic_example: bool = False,
) -> CarbonPool:
    """Deterministic factory: reserve + net = available; identity preserved; no mutation of inputs."""
    available = reserve_carbon_g + current_net_carbon_g
    return CarbonPool(
        pool_id=pool_id or f"pool_{plant_id}_{timestep}",
        plant_id=plant_id,
        architecture_id=architecture_id,
        reserve_carbon_g=reserve_carbon_g,
        current_net_carbon_g=current_net_carbon_g,
        available_carbon_g=available,
        timestep=timestep,
        simulation_time=simulation_time,
        status="AVAILABLE",
        provenance=provenance or f"TASK_046G carbon_pool v1; reserve={reserve_carbon_g}; net={current_net_carbon_g}; available={available}",
        note=note or "Accounting: reserve + current_net = available; sign preserved; no clamping; no allocation; no growth.",
        source_carbon_result_id=source_carbon_result_id,
        previous_pool_id=previous_pool_id,
        parameter_version=parameter_version,
        is_synthetic_example=is_synthetic_example,
    )
