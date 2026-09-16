import { create } from 'zustand'
export interface Selection {
  id: string; type: string; parent_id?: string;
  local_pos: [number,number,number]; world_pos: [number,number,number];
}
interface Store { selected: Selection | null; select: (s: Selection | null) => void }
export const useSelection = create<Store>((set) => ({ selected: null, select: (s) => set({ selected: s }) }))
