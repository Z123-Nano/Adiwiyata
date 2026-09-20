"""TASK 046M-A — Architecture → Light Occluder Mapping Contract.
Pure mapping; no light computation; no mutation of architecture.
Explicit approximation: structural organs mapped to vertical cylinder occluders
for shadow/occlusion approximation; root excluded by default.
"""
from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from simulation.core.contracts.domain import PlantArchitecture, PlantOrgan
from simulation.core.shadow.model import Occluder

class ArchitectureOccluderMappingConfig(BaseModel):
    """Explicit synthetic mapping parameters; provenance preserved."""
    mapping_version: str = "046M-A-v1"
    include_organ_types: List[str] = Field(default_factory=lambda: [
        "leaf","stem","branch","flower","fruit","axis","internode","bud"
    ])
    exclude_organ_types: List[str] = Field(default_factory=lambda: ["root"])
    geometry_primitive: Literal["cylinder","box","point","other"] = "cylinder"
    use_plant_local_origin: bool = True  # add architecture.local_origin to organ.local_position
    height_source: Literal["length_m","radius_m","fixed"] = "length_m"
    provenance: Optional[str] = "TASK_046M-A synthetic mapping"
    is_synthetic_example: bool = True

class ArchitectureOccluderSet(BaseModel):
    """Result of mapping PlantArchitecture → list of Occluders compatible with compute_lightfield."""
    source_architecture_id: str
    source_plant_id: str
    occluders: List[Occluder] = Field(default_factory=list)
    mapping_config_ref: Optional[str] = None
    mapped_organ_ids: List[str] = Field(default_factory=list)
    excluded_organ_ids: List[str] = Field(default_factory=list)
    approximation_notes: Optional[str] = (
        "Vertical cylinder approximation from length_m+radius_m; "
        "position = local_position + local_origin (plant_local->garden); "
        "orientation vector preserved in notes only — shadow model uses vertical extent."
    )
    provenance: Optional[str] = None
    status: Literal["AVAILABLE","NOT_COMPUTABLE"] = "AVAILABLE"
    is_synthetic_example: bool = True

def derive_occluder_set(
    architecture: PlantArchitecture,
    config: Optional[ArchitectureOccluderMappingConfig] = None,
) -> ArchitectureOccluderSet:
    """Pure: architecture + config → occluder set; no mutation; no light computation."""
    if config is None:
        config = ArchitectureOccluderMappingConfig()
    # Identity / validity
    if not architecture or not architecture.architecture_id or not architecture.plant_id:
        return ArchitectureOccluderSet(
            source_architecture_id=getattr(architecture, "architecture_id", ""),
            source_plant_id=getattr(architecture, "plant_id", ""),
            status="NOT_COMPUTABLE",
            provenance="TASK_046M-A blocked: architecture identity missing",
            is_synthetic_example=True,
        )
    # Build occluders only from supported organs with explicit geometric data
    occluders: List[Occluder] = []
    mapped_ids: List[str] = []
    excluded_ids: List[str] = []
    origin = architecture.local_origin or [0.0, 0.0, 0.0]
    for org in architecture.organs or []:
        if not org.id:
            excluded_ids.append("(no id)")
            continue
        # Explicit participation rule
        if org.organ_type in config.exclude_organ_types:
            excluded_ids.append(org.id)
            continue
        if config.include_organ_types and org.organ_type not in config.include_organ_types:
            excluded_ids.append(org.id)
            continue
        # Geometry must be present for credible occlusion
        if org.local_position is None or org.length_m is None or org.length_m < 0:
            excluded_ids.append(org.id)
            continue
        # Position mapping: plant-local → garden-world via local_origin
        lx, ly, lz = (org.local_position[0] if len(org.local_position) > 0 else 0.0,
                      org.local_position[1] if len(org.local_position) > 1 else 0.0,
                      org.local_position[2] if len(org.local_position) > 2 else 0.0)
        ox, oy, oz = (origin[0] if len(origin) > 0 else 0.0,
                      origin[1] if len(origin) > 1 else 0.0,
                      origin[2] if len(origin) > 2 else 0.0)
        x = lx + ox if config.use_plant_local_origin else lx
        y = ly + oy if config.use_plant_local_origin else ly
        z = lz + oz if config.use_plant_local_origin else lz
        # Cylinder approximation: height = length_m; radius = radius_m or default 0.05
        radius = org.radius_m if org.radius_m is not None and org.radius_m >= 0 else 0.05
        height = float(org.length_m)
        # Dimensions: cylinder mapping uses dimensions as (radius, radius, height) for compatibility; shadow uses height_m + position
        dims = (radius, radius, height)
        occluders.append(Occluder(
            id=f"occl_{org.id}",
            geometry=config.geometry_primitive,
            position=(x, y, z),
            dimensions=dims,
            height_m=height,
        ))
        mapped_ids.append(org.id)
    return ArchitectureOccluderSet(
        source_architecture_id=architecture.architecture_id,
        source_plant_id=architecture.plant_id,
        occluders=occluders,
        mapping_config_ref=config.mapping_version,
        mapped_organ_ids=mapped_ids,
        excluded_organ_ids=excluded_ids,
        provenance=f"TASK_046M-A; config={config.mapping_version}; mapped={len(mapped_ids)}; excluded={len(excluded_ids)}; source_arch={architecture.architecture_id}; approximation=cylinder/vertical; no mutation.",
        status="AVAILABLE" if architecture.organs else "NOT_COMPUTABLE",
        is_synthetic_example=True,
    )
