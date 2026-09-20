/** TASK 039 — temporal state (read-only; no mutation; separate from render/store). */
import { create } from 'zustand';
import type { ClockApiResponse } from '../api/client';
import { apiClient } from '../api/client';

interface TemporalState {
  clock: ClockApiResponse | null;
  loading: boolean;
  error: string | null;
  displayMode: "observation" | "simulation";
  loadClock: () => Promise<void>;
  setDisplayMode: (m: "observation" | "simulation") => void;
}

export const useTemporalStore = create<TemporalState>((set) => ({
  clock: null,
  loading: false,
  error: null,
  displayMode: "observation",
  loadClock: async () => {
    set({ loading: true, error: null });
    try {
      const res = await apiClient.clock();
      set({ clock: res, loading: false });
    } catch (e: any) {
      set({ error: e?.message || String(e), loading: false, clock: null });
    }
  },
  setDisplayMode: (m) => set({ displayMode: m }),
}));
