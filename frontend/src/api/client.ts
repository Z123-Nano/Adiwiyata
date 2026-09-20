/** TASK 033 — thin typed API client for /api/v1 garden endpoints.
Transport adapter only; no scientific computation.
*/
export interface GardenApiResponse {
  garden_id: string;
  status: "VALID" | "INVALID_INPUT" | "NOT_COMPUTABLE" | "INCONCLUSIVE" | "FAILED";
  provenance?: string;
  objects?: string[];
}

export interface PlantApiResponse {
  plant_id: string;
  identity?: { id: string; species_id?: string; variety_id?: string };
  state_ref?: string;
  architecture_summary?: { organs?: number };
  phenology?: { stage?: string };
  provenance?: string;
  status?: string;
}

const BASE = "http://localhost:8000/api/v1";

async function fetchJSON<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, init ? { ...init, headers: { ...(init.headers || {}), "Content-Type": "application/json" } } : undefined);
  if (!res.ok) {
    const body = await res.json().catch(() => ({})) as { detail?: string; code?: string };
    const err = new Error(body.detail || `HTTP ${res.status}`) as any;
    err.status = res.status;
    err.code = body.code || (res.status === 404 ? "NOT_FOUND" : "ERROR");
    throw err;
  }
  return res.json() as Promise<T>;
}

export interface MeasurementApiResponse {
  id: string; timestamp: string; variable: string; value: number; unit: string;
  location_target_id?: string; spatial_ref?: Record<string, number>;
  instrument?: string; method?: string; observer_source?: string;
  uncertainty?: number | null; provenance?: string; quality_flag?: string;
  notes?: string; is_synthetic_example?: boolean; status: string;
}
export interface MeasurementListApiResponse { measurements: MeasurementApiResponse[]; provenance?: string; note?: string }
export interface ObservationApiResponse {
  id: string; timestamp: string; target_id?: string; observation_type?: string; category?: string;
  content: string; structured_attributes?: Record<string, unknown>; value_numeric?: number | null;
  unit?: string | null; location_target_id?: string; spatial_ref?: Record<string, number>;
  method?: string; observer_source?: string; uncertainty?: number | null;
  notes?: string; provenance?: string; quality_flag?: string; is_synthetic_example?: boolean; status: string;
}
export interface ObservationListApiResponse { observations: ObservationApiResponse[]; provenance?: string; note?: string }

export interface LightSampleApiResponse {
  x: number; y: number; z: number;
  direct: number; diffuse: number; reflected: number; total: number;
  unit: "relative_normalized";
}
export interface LightFieldApiResponse {
  extent_min: number[]; extent_max: number[]; resolution: number[];
  sampling_strategy: "regular_grid_horizontal"; solar_reference?: string;
  sample_count: number; samples: LightSampleApiResponse[];
  status: string; provenance?: string; note?: string;
}

export interface ClockApiResponse {
  simulation_time?: string; world_time?: string; observation_time?: string;
  timestep?: number | null; timestep_mode?: string; timezone?: string;
  plant_age?: string; forecast_target?: string; scheduler_status?: string; clock_status?: string;
  provenance?: string; version?: string; note?: string;
}

export interface SnapshotApiResponse { snapshot_id: string; timestamp?: string; source_state_ref?: string; version?: string; provenance?: string; status: string; is_immutable?: boolean; notes?: string }
export interface ScenarioApiResponse { scenario_id: string; source_snapshot_id?: string; status: string; provenance?: string; overrides?: Record<string,unknown>; notes?: string; is_derived?: boolean }

export const apiClient = {
  garden: () => fetchJSON<GardenApiResponse>("/garden"),
  gardenObjects: () => fetchJSON<{ objects: string[]; provenance?: string }>("/garden/objects"),
  plant: (id: string) => fetchJSON<PlantApiResponse>(`/plants/${encodeURIComponent(id)}`),
  health: () => fetchJSON<{ status: string; api_version: string }>("/health"),
  measurements: () => fetchJSON<MeasurementListApiResponse>("/measurements"),
  measurement: (id: string) => fetchJSON<MeasurementApiResponse>(`/measurements/${encodeURIComponent(id)}`),
  observations: () => fetchJSON<ObservationListApiResponse>("/observations"),
  observation: (id: string) => fetchJSON<ObservationApiResponse>(`/observations/${encodeURIComponent(id)}`),
  lightfield: (payload?: { solar_ref?: string; extent?: number[] }) => fetchJSON<LightFieldApiResponse>("/lightfield/compute", { method: "POST", body: JSON.stringify(payload || { solar_ref: "synthetic", extent: [0,0,5,5] }) }),
  clock: () => fetchJSON<ClockApiResponse>("/simulation/clock"),
  snapshots: () => fetchJSON<{snapshots:SnapshotApiResponse[]}>("/snapshots"),
  snapshot: (id: string) => fetchJSON<SnapshotApiResponse>(`/snapshots/${encodeURIComponent(id)}`),
  scenarios: () => fetchJSON<{scenarios:ScenarioApiResponse[]}>("/scenarios"),
  scenario: (id: string) => fetchJSON<ScenarioApiResponse>(`/scenarios/${encodeURIComponent(id)}`),
  createScenario: (payload: {source_snapshot_id:string; overrides?:Record<string,unknown>}) => fetchJSON<ScenarioApiResponse>("/scenarios", {method:"POST", body: JSON.stringify(payload)}),
  simulationStep: (payload: {source_ref:string; source_type?:string}) => fetchJSON<any>("/simulation/step", {method:"POST", body: JSON.stringify(payload)}),
};
