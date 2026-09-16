/* Domain contracts — frontend consumption. No Three.js, no physics. */

export interface GardenReference {
  origin: [number, number, number];
  north_bearing_deg: number;
  coord_system: "local-garden";
}

export interface SpatialTransform {
  position: [number, number, number];
  rotation_euler_deg: [number, number, number];
  scale: [number, number, number];
  parent_id?: string;
}

export interface Boundary {
  points: [number, number, number][]; // ordered polygon
  type: "polygon" | "other";
}

export interface Garden {
  id: string;
  reference: GardenReference;
  boundary: Boundary;
  objects: string[];
}

export interface SpatialObject {
  id: string;
  type: "building" | "fence" | "tree" | "rack" | "tier" | "container" | "container_cell" | "plant" | "other";
  transform: SpatialTransform;
  parent_id?: string;
}

export interface Container {
  id: string;
  container_type: "polybag" | "pot" | "seedling_tray" | "ground" | "other";
  dimensions?: [number, number, number];
  volume_l?: number;
  material?: string;
  color?: string;
  growing_medium_ref?: string;
  drainage_ref?: string;
  transform: SpatialTransform;
  parent_id?: string;
  cell_ids: string[];
}

export interface ContainerCell {
  id: string;
  parent_container_id: string;
  index: number;
  transform: SpatialTransform;
  occupied_plant_id?: string;
}

export interface Plant {
  id: string;
  species_id?: string;
  variety_id?: string;
  current_container_id?: string;
  lifecycle_stage?: string;
}

export interface PlantState {
  plant_id: string;
  timestamp: string; // ISO-8601
  age_days?: number; // unknown if missing; do not default to 0
  phenological_stage?: string;
  biomass_g?: number;
  carbon_pool_g?: number;
  water_status?: string;
  nutrient_status?: string;
  stress_state?: string;
}

export interface PlantOrgan {
  id: string;
  organ_type: "axis" | "internode" | "leaf" | "bud" | "flower" | "fruit" | "root" | "other";
  topology_ref?: string;
}

export interface PlantArchitecture {
  plant_id: string;
  topology?: string;
  organs: PlantOrgan[];
  geometry_metadata?: Record<string, unknown>;
}

export interface VarietyParameter {
  name: string;
  value?: number; // unknown if missing; not silently zero
  unit?: string; // required when value known
  source: "literature" | "measured" | "fitted_inferred" | "assumption_placeholder" | "unknown";
  method?: string;
  uncertainty?: number;
  valid_range?: [number, number];
  version?: string;
  provenance?: string;
}

export interface VarietyProfile {
  species: string;
  cultivar?: string;
  description?: string;
  parameter_collection: VarietyParameter[];
}

export interface EnvironmentState {
  timestamp: string;
  solar_state?: string; // planned
  temperature_c?: number;
  humidity_pct?: number;
  precipitation_mm?: number;
  water_availability?: string;
  nutrient_environment?: string;
}

export interface LightField {
  timestamp: string;
  direct_component?: number;
  diffuse_component?: number;
  reflected_component?: number;
  illuminance_lux?: number; // observed; NOT photosynthesis
  estimated_plant_relevant?: number;
  spatial_association?: string;
}

export interface Measurement {
  id: string;
  timestamp: string;
  variable: string;
  value: number;
  unit: string; // explicit; never silent
  location_target_id?: string;
  instrument?: string;
  method?: string;
  uncertainty?: number;
  provenance?: string;
}

export interface Observation {
  id: string;
  timestamp: string;
  target_id?: string;
  category?: string;
  content: string;
  structured_attributes?: Record<string, unknown>;
  observer_source?: string;
}

export interface InterventionEvent {
  id: string;
  timestamp: string;
  event_type: "watering" | "fertilization" | "transplanting" | "pruning" | "repotting" | "harvesting" | "other";
  target_id: string;
  parameters?: Record<string, unknown>;
  user_source?: string;
}

export interface Scenario {
  id: string;
  name: string;
  description?: string;
  base_snapshot_ref?: string;
  time_range?: [string, string]; // planned
  assumptions: string[];
  interventions: string[]; // event refs
  parameter_overrides?: Record<string, unknown>;
  random_seed?: number;
}

export interface SimulationState {
  simulation_time: number;
  environment_state?: EnvironmentState;
  soil_water_state_ref?: string;
  plant_states: string[];
  architectures_ref: string[];
  pending_events: string[];
}

export interface SimulationRun {
  id: string;
  source_state_ref: string;
  scenario_ref?: string;
  model_version_ref?: string;
  parameter_set_version_ref?: string;
  random_seed?: number;
  forecast_horizon?: number;
  assumptions: string[];
  checkpoints_ref?: string[];
  uncertainty_refs?: string[];
}

export interface Prediction {
  id: string;
  source_snapshot_ref: string;
  forecast_time: number;
  plant_states_ref: string[];
  architectures_ref: string[];
  scenario_ref?: string;
}

export interface ModelVersion {
  model_name: string;
  version: string;
  component_versions?: Record<string, string>;
  equations_ref?: string;
  dependency_metadata?: Record<string, unknown>;
}

export interface ParameterSetVersion {
  parameter_set_id: string;
  version: string;
  source_ref?: string;
  applicability_scope?: string;
}
