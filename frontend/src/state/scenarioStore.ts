/** TASK 040 — Scenario state (derived branch; source snapshot preserved). */
import { create } from 'zustand';
import type { ScenarioApiResponse } from '../api/client';
import { apiClient } from '../api/client';
interface ScenarioState {
  scenarios: ScenarioApiResponse[]; selectedId: string | null; loading: boolean; error: string | null;
  load: () => Promise<void>; select: (id: string | null) => void;
  branchFromSnapshot: (sourceId: string, overrides?: Record<string,unknown>) => Promise<void>;
}
export const useScenarioStore = create<ScenarioState>((set) => ({
  scenarios: [], selectedId: null, loading: false, error: null,
  load: async () => { set({loading:true,error:null}); try { const r = await apiClient.scenarios(); set({scenarios:r.scenarios||[],loading:false}); } catch(e:any){ set({error:e?.message||String(e),loading:false}); } },
  select: (id) => set({selectedId:id}),
  branchFromSnapshot: async (sourceId, overrides={}) => {
    set({loading:true,error:null}); try {
      const s = await apiClient.createScenario({source_snapshot_id:sourceId, overrides});
      set((state: any) => ({scenarios: [...(state.scenarios || []), s], selectedId: s.scenario_id, loading:false}));
    } catch(e:any){ set({error:e?.message||String(e),loading:false}); }
  },
}));
