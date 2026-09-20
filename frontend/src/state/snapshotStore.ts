/** TASK 040 — Snapshot state (immutable reference only). */
import { create } from 'zustand';
import type { SnapshotApiResponse } from '../api/client';
import { apiClient } from '../api/client';
interface SnapshotState {
  snapshots: SnapshotApiResponse[]; selectedId: string | null; loading: boolean; error: string | null;
  load: () => Promise<void>; select: (id: string | null) => void;
}
export const useSnapshotStore = create<SnapshotState>((set) => ({
  snapshots: [], selectedId: null, loading: false, error: null,
  load: async () => { set({loading:true,error:null}); try { const r = await apiClient.snapshots(); set({snapshots:r.snapshots||[],loading:false}); } catch(e:any){ set({error:e?.message||String(e),loading:false}); } },
  select: (id) => set({selectedId:id}),
}));
