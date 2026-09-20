/** TASK 037 — measurement / observation application state (API-backed; no render objects). */
import { create } from 'zustand';
import type { MeasurementApiResponse, ObservationApiResponse } from '../api/client';
import { apiClient } from '../api/client';

interface MeasurementState {
  measurements: MeasurementApiResponse[];
  observations: ObservationApiResponse[];
  loading: boolean;
  error: string | null;
  selectedMeasurementId: string | null;
  selectedObservationId: string | null;
  loadMeasurements: () => Promise<void>;
  loadObservations: () => Promise<void>;
  selectMeasurement: (id: string | null) => void;
  selectObservation: (id: string | null) => void;
}

export const useMeasurementStore = create<MeasurementState>((set) => ({
  measurements: [],
  observations: [],
  loading: false,
  error: null,
  selectedMeasurementId: null,
  selectedObservationId: null,
  loadMeasurements: async () => {
    set({ loading: true, error: null });
    try {
      const res = await apiClient.measurements();
      set({ measurements: res.measurements || [], loading: false });
    } catch (e: any) {
      set({ error: e?.message || String(e), loading: false });
    }
  },
  loadObservations: async () => {
    set({ loading: true, error: null });
    try {
      const res = await apiClient.observations();
      set({ observations: res.observations || [], loading: false });
    } catch (e: any) {
      set({ error: e?.message || String(e), loading: false });
    }
  },
  selectMeasurement: (id) => set({ selectedMeasurementId: id }),
  selectObservation: (id) => set({ selectedObservationId: id }),
}));
