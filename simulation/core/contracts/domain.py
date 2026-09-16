"""Domain contracts — My Digital Twin Garden (TASK 002). No physics implemented."""
from __future__ import annotations
from datetime import datetime
from typing import Optional, Literal, List
from pydantic import BaseModel, Field

# --- Spatial / Reference ---
class GardenReference(BaseModel):
    """G0 local origin and orientation."""
    origin: list[float] = Field(default=[0.0, 0.0, 0.0], description="G0 position")
    north_bearing_deg: float = Field(default=0.0)
    coord_system: Literal["local-garden"] = "local-garden"

class SpatialTransform(BaseModel):
    position: list[float] = [0.0, 0.0, 0.0]
    rotation_euler_deg: list[float] = [0.0, 0.0, 0.0]
    scale: list[float] = [1.0, 1.0, 1.0]
    parent_id: Optional[str] = None

# --- Garden / Boundary ---
class Boundary(BaseModel):
    points: list[list[float]]  # ordered polygon (L-shape allowed)
    type: Literal["polygon", "other"] = "polygon"

class Garden(BaseModel):
    id: str
    reference: GardenReference
    boundary: Boundary
    objects: List[str] = Field(default_factory=list)

# --- Spatial objects ---
class SpatialObject(BaseModel):
    id: str
    type: Literal["building","fence","tree","rack","tier","container","container_cell","plant","other"]
    transform: SpatialTransform
    parent_id: Optional[str] = None

class Building(SpatialObject):
    pass

class FenceWall(SpatialObject):
    pass

class TreeObstacle(SpatialObject):
    pass

# --- Rack / Tier / Container ---
class RackTier(BaseModel):
    id: str
    parent_rack_id: str
    index: int
    transform: SpatialTransform

class Container(BaseModel):
    id: str
    container_type: Literal["polybag","pot","seedling_tray","ground","other"]
    dimensions: Optional[list[float]] = None  # [w,h,d]
    volume_l: Optional[float] = None
    material: Optional[str] = None
    color: Optional[str] = None
    growing_medium_ref: Optional[str] = None
    drainage_ref: Optional[str] = None
    transform: SpatialTransform
    parent_id: Optional[str] = None
    cell_ids: List[str] = Field(default_factory=list)

class ContainerCell(BaseModel):
    id: str
    parent_container_id: str
    index: int
    transform: SpatialTransform
    occupied_plant_id: Optional[str] = None

# --- Plant (identity) ---
class Plant(BaseModel):
    id: str
    species_id: Optional[str] = None
    variety_id: Optional[str] = None
    current_container_id: Optional[str] = None
    lifecycle_stage: Optional[str] = None  # planned; not computed

# --- PlantState (separate from identity/architecture) ---
class PlantState(BaseModel):
    plant_id: str
    timestamp: datetime
    age_days: Optional[float] = None  # planned; unknown if missing
    phenological_stage: Optional[str] = None
    biomass_g: Optional[float] = None
    carbon_pool_g: Optional[float] = None
    water_status: Optional[str] = None  # planned
    nutrient_status: Optional[str] = None
    stress_state: Optional[str] = None
    # unknown / not-applicable / zero must be explicit (not silent)

# --- PlantArchitecture (no Three.js) ---
class PlantOrgan(BaseModel):
    id: str
    organ_type: Literal["axis","internode","leaf","bud","flower","fruit","root","other"]
    topology_ref: Optional[str] = None

class PlantArchitecture(BaseModel):
    plant_id: str
    topology: Optional[str] = None
    organs: List[PlantOrgan] = Field(default_factory=list)
    geometry_metadata: Optional[dict] = None

# --- Variety ---
class VarietyParameter(BaseModel):
    name: str
    value: Optional[float] = None  # None = unknown / missing
    unit: Optional[str] = None  # required when value known; None if unknown
    source: Literal["literature","measured","fitted_inferred","assumption_placeholder","unknown"] = "unknown"
    method: Optional[str] = None
    uncertainty: Optional[float] = None
    valid_range: Optional[list] = None  # [min, max]
    version: Optional[str] = None
    provenance: Optional[str] = None

class VarietyProfile(BaseModel):
    species: str
    cultivar: Optional[str] = None
    description: Optional[str] = None
    parameter_collection: List[VarietyParameter] = Field(default_factory=list)

# --- Environment / Light ---
class EnvironmentState(BaseModel):
    timestamp: datetime
    solar_state: Optional[str] = None  # planned; not computed
    temperature_c: Optional[float] = None  # planned
    humidity_pct: Optional[float] = None
    precipitation_mm: Optional[float] = None
    water_availability: Optional[str] = None  # planned
    nutrient_environment: Optional[str] = None

class LightField(BaseModel):
    timestamp: datetime
    direct_component: Optional[float] = None  # planned
    diffuse_component: Optional[float] = None
    reflected_component: Optional[float] = None
    illuminance_lux: Optional[float] = None  # observed; not = photosynthesis
    estimated_plant_relevant: Optional[float] = None  # planned
    spatial_association: Optional[str] = None  # e.g., organ/plant ref

# --- Measurement / Observation ---
class Measurement(BaseModel):
    id: str
    timestamp: datetime
    variable: str  # extensible vocabulary; e.g. illuminance, temperature, soil_moisture
    value: float
    unit: str  # required; never silent; lux stays lux; never converted to PPFD
    location_target_id: Optional[str] = None  # named SpatialObject / container / plant
    spatial_ref: Optional[dict] = None  # e.g. {"x":0,"y":0,"z":0} or garden ref; not hard-coded dimensions
    instrument: Optional[str] = None  # instrument name/type; do not invent serial numbers
    instrument_id: Optional[str] = None  # identifier only if actually known
    method: Optional[str] = None
    calibration_ref: Optional[str] = None  # only if actually known; never fabricated
    observer_source: Optional[str] = None  # observer or data source
    uncertainty: Optional[float] = None  # known = value; unknown/absent = None, NOT zero
    provenance: Optional[str] = None  # source, method, version/date, notes
    quality_flag: Optional[str] = None  # optional; not statistical QC yet
    notes: Optional[str] = None  # raw-context preservation; do not smooth/remove
    is_synthetic_example: bool = False  # synthetic fixtures must be explicitly labeled

class Observation(BaseModel):
    id: str
    timestamp: datetime
    target_id: Optional[str] = None  # plant / container / object reference
    observation_type: Optional[str] = None  # e.g. phenological_stage, status, event
    category: Optional[str] = None  # qualitative / photographic / event / structured
    content: str  # human-readable; non-numeric observations preserved here
    structured_attributes: Optional[dict] = None  # structured payload; numeric only when appropriate and with unit
    value_numeric: Optional[float] = None  # only when observation includes a measurement-like number; never assume
    unit: Optional[str] = None  # required when value_numeric present; lux stays lux
    location_target_id: Optional[str] = None
    spatial_ref: Optional[dict] = None
    method: Optional[str] = None
    observer_source: Optional[str] = None
    uncertainty: Optional[float] = None  # only when applicable; unknown = None
    notes: Optional[str] = None  # provenance / context; do not fabricate
    provenance: Optional[str] = None
    quality_flag: Optional[str] = None
    is_synthetic_example: bool = False

# --- Events ---
class InterventionEvent(BaseModel):
    id: str
    timestamp: datetime
    event_type: Literal["watering","fertilization","transplanting","pruning","repotting","harvesting","other"]
    target_id: str
    parameters: Optional[dict] = None
    user_source: Optional[str] = None

# --- Scenario / Simulation ---
class Scenario(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    base_snapshot_ref: Optional[str] = None
    time_range: Optional[list] = None  # [start, end] planned
    assumptions: List[str] = Field(default_factory=list)
    interventions: List[str] = Field(default_factory=list)  # event refs
    parameter_overrides: Optional[dict] = None
    random_seed: Optional[int] = None

class SimulationState(BaseModel):
    simulation_time: float  # planned; float seconds/days
    environment_state: Optional[EnvironmentState] = None
    soil_water_state_ref: Optional[str] = None
    plant_states: List[str] = Field(default_factory=list)
    architectures_ref: List[str] = Field(default_factory=list)
    pending_events: List[str] = Field(default_factory=list)

class SimulationRun(BaseModel):
    id: str
    source_state_ref: str
    scenario_ref: Optional[str] = None
    model_version_ref: Optional[str] = None
    parameter_set_version_ref: Optional[str] = None
    random_seed: Optional[int] = None
    forecast_horizon: Optional[float] = None
    assumptions: List[str] = Field(default_factory=list)
    checkpoints_ref: Optional[List[str]] = None
    uncertainty_refs: Optional[List[str]] = None

class Prediction(BaseModel):
    id: str
    source_snapshot_ref: str
    forecast_time: float
    plant_states_ref: List[str] = Field(default_factory=list)
    architectures_ref: List[str] = Field(default_factory=list)
    scenario_ref: Optional[str] = None
    # Not mutable live Garden state; separate result representation

# --- Model registry contracts ---
class ModelVersion(BaseModel):
    model_name: str
    version: str  # semantic
    component_versions: Optional[dict] = None
    equations_ref: Optional[str] = None
    dependency_metadata: Optional[dict] = None

class ParameterSetVersion(BaseModel):
    parameter_set_id: str
    version: str
    source_ref: Optional[str] = None
    applicability_scope: Optional[str] = None
