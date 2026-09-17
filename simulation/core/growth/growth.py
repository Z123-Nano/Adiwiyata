"""Organ growth — TASK 023. Mass-first; synthetic efficiency/density; no species realism."""
from __future__ import annotations
from typing import Optional
from simulation.core.growth.contracts import OrganGrowthInput, OrganGrowthResult, GrowthParam

def _find_param(params, name, default):
    for p in params:
        if p.name == name:
            return p.value
    return default

def grow_organ(inp: OrganGrowthInput) -> OrganGrowthResult:
    # Propagate upstream invalid input status
    if inp.status in ("INVALID_INPUT", "NOT_COMPUTABLE", "NOT_IMPLEMENTED"):
        return OrganGrowthResult(
            organ_id=inp.organ_id, plant_id=inp.plant_id,
            status=inp.status,
            carbon_used=0.0, carbon_remaining=inp.allocated_carbon,
            biomass_change=0.0,
            provenance=inp.provenance or "TASK_023; upstream invalid",
            notes="Upstream input status propagated.",
            is_synthetic_example=inp.is_synthetic_example,
        )
    # Negative allocated carbon
    if inp.allocated_carbon < 0:
        return OrganGrowthResult(
            organ_id=inp.organ_id, plant_id=inp.plant_id,
            status="INVALID_INPUT",
            carbon_used=0.0, carbon_remaining=0.0,
            biomass_change=0.0,
            provenance=inp.provenance or "TASK_023; negative allocated carbon",
            notes="Negative allocated carbon rejected.",
            is_synthetic_example=inp.is_synthetic_example,
        )
    # Zero carbon
    if inp.allocated_carbon == 0.0:
        return OrganGrowthResult(
            organ_id=inp.organ_id, plant_id=inp.plant_id,
            status="VALID",
            carbon_used=0.0, carbon_remaining=0.0,
            biomass_change=0.0,
            geometry_status="NOT_COMPUTABLE",
            provenance=inp.provenance or "TASK_023; zero growth",
            notes="Zero allocated carbon => zero growth; state unchanged.",
            updated_state_reference=dict(inp.current_organ_state),
            is_synthetic_example=inp.is_synthetic_example,
        )
    # Unsupported organ -> NOT_IMPLEMENTED (only explicit support later)
    if inp.organ_type not in ("stem","branch","leaf","root"):
        return OrganGrowthResult(
            organ_id=inp.organ_id, plant_id=inp.plant_id,
            status="NOT_IMPLEMENTED",
            carbon_used=0.0, carbon_remaining=inp.allocated_carbon,
            biomass_change=0.0,
            provenance=inp.provenance or "TASK_023; unsupported organ",
            notes=f"Organ type '{inp.organ_type}' growth not implemented.",
            is_synthetic_example=inp.is_synthetic_example,
        )
    # Growth parameters (synthetic only)
    efficiency = _find_param(inp.growth_params, "carbon_to_biomass_efficiency", 0.5)
    derive_geometry = bool(_find_param(inp.growth_params, "derive_geometry", 0.0))
    density = _find_param(inp.growth_params, "tissue_density_g_m3", 500.0) if derive_geometry else None
    # Biomass increment = allocated * efficiency (explicit synthetic conversion; not calibrated)
    biomass_change = inp.allocated_carbon * efficiency
    carbon_used = inp.allocated_carbon  # model consumes all allocated; remainder = unconverted
    carbon_remaining = inp.allocated_carbon - carbon_used  # 0 unless efficiency <1 with different accounting
    # If efficiency < 1, represent unconverted carbon as remaining (not structural)
    if efficiency < 1.0:
        carbon_remaining = inp.allocated_carbon * (1.0 - efficiency)
        carbon_used = inp.allocated_carbon * efficiency
    # Geometry only when explicitly requested and density given
    length_change = None
    radius_change = None
    geom_status = "NOT_COMPUTABLE"
    updated = dict(inp.current_organ_state)
    if derive_geometry and density is not None and density > 0:
        # Simplified: assume biomass increment produces proportional length increase for cylinder-like organ
        # Synthetic reference only; not species-specific
        old_len = inp.current_organ_state.get("length_m") or 1.0
        old_rad = inp.current_organ_state.get("radius_m") or 0.1
        # Volume approx = pi r^2 L; delta V = biomass / density; delta L proportional (hold r constant for simplicity)
        if old_len > 0 and old_rad > 0:
            vol = 3.14159 * old_rad * old_rad * old_len
            delta_vol = biomass_change / density
            delta_len = (delta_vol / (3.14159 * old_rad * old_rad)) if old_rad > 0 else 0.0
            length_change = round(delta_len, 6)
            radius_change = 0.0  # fixed-term simplification; documented limitation
            updated["length_m"] = round(old_len + delta_len, 6)
            updated["radius_m"] = old_rad  # unchanged
            geom_status = "COMPUTED"
    return OrganGrowthResult(
        organ_id=inp.organ_id,
        plant_id=inp.plant_id,
        timestep_seconds=inp.timestep_seconds,
        carbon_used=round(carbon_used, 6),
        carbon_remaining=round(carbon_remaining, 6),
        biomass_change=round(biomass_change, 6),
        biomass_unit="g_m2",
        length_change_m=length_change,
        radius_change_m=radius_change,
        geometry_status=geom_status,
        updated_state_reference=updated,
        status="VALID",
        provenance=inp.provenance or "TASK_023; growth v1 synthetic",
        notes="Mass-first growth; geometry only if derive_geometry=True with synthetic density. Not calibrated.",
        is_synthetic_example=inp.is_synthetic_example or any(p.is_synthetic_example for p in inp.growth_params),
        model_version="v1",
    )
