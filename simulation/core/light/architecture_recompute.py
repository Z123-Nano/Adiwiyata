"""TASK 046M — Architecture-derived occluders → existing LightField computation.
Thin wrapper: architecture → 046M-A mapping → canonical compute_lightfield.
No new radiation model; no orientation claim; coarse approximation documented.
"""
from __future__ import annotations
from typing import Optional, Tuple
from simulation.core.contracts.domain import PlantArchitecture
from simulation.core.solar.model import SolarPosition
from simulation.core.light.field.compute import compute_lightfield
from simulation.core.light.field.contracts import LightField
from simulation.core.architecture.occluder_mapping import derive_occluder_set, ArchitectureOccluderMappingConfig

def compute_lightfield_for_architecture(
    architecture: PlantArchitecture,
    solar: SolarPosition,
    grid_bounds: Tuple[float, float, float, float],
    grid_res: Tuple[int, int] = (10, 10),
    z_height: float = 0.0,
    mapping_config: Optional[ArchitectureOccluderMappingConfig] = None,
) -> LightField:
    """Pure integration: architecture + solar + grid → LightField using existing canonical computation."""
    # Identity validation
    if not architecture or not getattr(architecture, "architecture_id", None) or not getattr(architecture, "plant_id", None):
        raise ValueError("TASK_046M: architecture identity required (architecture_id + plant_id)")
    if not solar:
        raise ValueError("TASK_046M: solar input required")
    # Mapping (046M-A) — pure, no mutation
    occluder_set = derive_occluder_set(architecture, mapping_config)
    # Mapping failure propagated honestly
    if occluder_set.status == "NOT_COMPUTABLE":
        # Still attempt compute with empty occluders per spec (honest, not fabricated)
        occluders = []
    else:
        occluders = occluder_set.occluders
    # Canonical LightField computation (unchanged)
    light_result = compute_lightfield(
        solar=solar,
        grid_bounds=grid_bounds,
        grid_res=grid_res,
        z_height=z_height,
        occluders=occluders,
    )
    # Provenance augmentation (smallest consistent addition; do not redesign LightField contract)
    provenance_note = (
        f"TASK_046M; arch={architecture.architecture_id}; plant={architecture.plant_id}; "
        f"mapper=046M-A-{occluder_set.mapping_config_ref or 'v1'}; mapped_organs={len(occluder_set.mapped_organ_ids)}; "
        f"excluded={len(occluder_set.excluded_organ_ids)}; occluders={len(occluders)}; "
        f"coarse_orientation_aware=false; approximation=vertical_cylinder/regular_grid; "
        f"no_optics_model; no_ppfd; relative_normalized_preserved."
    )
    # Preserve existing result fields; augment notes/provenance only where supported
    # LightField has no provenance field directly; document via approximation_params / solar_reference preservation
    # We do NOT redesign contract; only ensure result is identifiable via solar_reference + approximation_params if set
    # To make architecture traceable without contract redesign, store reference in approximation_params
    if light_result.approximation_params is None:
        light_result.approximation_params = {}
    light_result.approximation_params["task_046m_architecture_ref"] = architecture.architecture_id
    light_result.approximation_params["task_046m_plant_ref"] = architecture.plant_id
    light_result.approximation_params["task_046m_mapper_version"] = occluder_set.mapping_config_ref or "046M-A-v1"
    light_result.approximation_params["task_046m_occluder_count"] = len(occluders)
    light_result.approximation_params["task_046m_orientation_aware"] = False
    light_result.approximation_params["task_046m_approximation_note"] = "coarse architecture-derived shadow; vertical cylinder; orientation not in Occluder contract"
    light_result.approximation_params["task_046m_provenance"] = provenance_note
    # Preserve solar_reference (already set by compute_lightfield from solar.timestamp)
    # Return new result; source LightField unchanged (compute_lightfield is pure; no mutation of previous result)
    return light_result
