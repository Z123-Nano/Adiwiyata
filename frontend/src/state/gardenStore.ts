/** TASK 033 — application state boundary.
Source of truth for loaded domain data; render objects live in R3F, not here.
No scientific computation; no Three.js objects.
*/
import { create } from 'zustand'
import type { GardenApiResponse, PlantApiResponse } from '../api/client'

export interface RenderSceneNode {
  id: string; type: string; parent_id?: string;
  local_position: [number,number,number];
  world_position: [number,number,number];
  rotation?: [number,number,number]; scale?: [number,number,number];
  meta?: Record<string, unknown>;
  // identity preserved from domain
  domain_plant_id?: string; domain_organ_id?: string;
}

interface GardenState {
  // API/domain source
  gardenData: GardenApiResponse | null;
  plants: Record<string, PlantApiResponse>;
  loading: boolean;
  error: { code: string; message: string } | null;
  // Editable frontend state (separate from domain)
  selectedId: string | null;
  editableNotes: string;
  // Render-neutral scene data (produced by adapter, not source of truth)
  sceneNodes: RenderSceneNode[];
  // Actions
  loadGarden: () => Promise<void>;
  select: (id: string | null) => void;
  setScene: (nodes: RenderSceneNode[]) => void;
  setError: (e: { code: string; message: string } | null) => void;
  setNotes: (n: string) => void;
}

export const useGardenState = create<GardenState>((set) => ({
  gardenData: null, plants: {}, loading: false, error: null,
  selectedId: null, editableNotes: "",
  sceneNodes: [],
  loadGarden: async () => {
    set({ loading: true, error: null });
    try {
      const { apiClient } = await import('../api/client');
      const g = await apiClient.garden();
      set({ gardenData: g, loading: false });
    } catch (e: any) {
      set({ error: { code: e.code || "ERROR", message: e.message || String(e) }, loading: false });
    }
  },
  select: (id) => set({ selectedId: id }),
  setScene: (nodes) => set({ sceneNodes: nodes }),
  setError: (e) => set({ error: e }),
  setNotes: (n) => set({ editableNotes: n }),
}));
