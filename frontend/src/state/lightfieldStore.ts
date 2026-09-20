/** TASK 038 — LightField state (API-backed; no Three.js objects). */
import { create } from 'zustand';
import type { LightFieldApiResponse, LightSampleApiResponse } from '../api/client';
import { apiClient } from '../api/client';

interface LightFieldState {
  result: LightFieldApiResponse | null;
  loading: boolean;
  error: string | null;
  selectedSampleId: string | null; // domain id derived from index/coords, not Three.js
  compute: (payload?: { solar_ref?: string; extent?: number[] }) => Promise<void>;
  selectSample: (id: string | null) => void;
}

export const useLightFieldStore = create<LightFieldState>((set) => ({
  result: null,
  loading: false,
  error: null,
  selectedSampleId: null,
  compute: async (payload) => {
    set({ loading: true, error: null });
    try {
      const res = await apiClient.lightfield(payload);
      set({ result: res, loading: false });
    } catch (e: any) {
      set({ error: e?.message || String(e), loading: false, result: null });
    }
  },
  selectSample: (id) => set({ selectedSampleId: id }),
}));
