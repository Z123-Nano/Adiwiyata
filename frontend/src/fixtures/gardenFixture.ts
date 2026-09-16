/** Synthetic garden fixtures (TASK 005) — NOT real measurements. */
export interface FixtureNode {
  id: string; type: string; parent_id?: string;
  position: [number,number,number]; rotation: [number,number,number]; scale: [number,number,number];
  meta?: Record<string, unknown>; // dims, material, etc.
}

export const SYNTHETIC_HIERARCHY: FixtureNode[] = [
  // Garden root objects
  { id: "b1", type: "building", parent_id: undefined, position: [-3.5, 0.6, -2], rotation: [0,0,0], scale: [1.2,1.2,1.2], meta: { dims: [1.2,1.2,1.2] } },
  { id: "f1", type: "fence", parent_id: undefined, position: [-1, 0, -4], rotation: [0, Math.PI/2, 0], scale: [0.1, 1.2, 4], meta: { length: 4, height: 1.2, thickness: 0.1 } },
  { id: "t1", type: "tree", parent_id: undefined, position: [-2, 0.3, 2], rotation: [0,0,0], scale: [0.4, 0.6, 0.4], meta: { trunk: [0.2,0.6], canopy: [0.8,0.8] } },
  // Rack
  { id: "rack1", type: "rack", parent_id: undefined, position: [1.5, 0, 1.5], rotation: [0,0.2,0], scale: [1.5,1.2,0.8], meta: { dims: [1.5,1.2,0.8] } },
  // Tier 1
  { id: "tier1", type: "tier", parent_id: "rack1", position: [0, 0, 0], rotation: [0,0,0], scale: [1,0.15,1], meta: { index: 1, dims: [1,0.15,1] } },
  // Tier 2
  { id: "tier2", type: "tier", parent_id: "rack1", position: [0, 0.45, 0], rotation: [0,0,0], scale: [1,0.15,1], meta: { index: 2, dims: [1,0.15,1] } },
  // Tier 3
  { id: "tier3", type: "tier", parent_id: "rack1", position: [0, 0.9, 0], rotation: [0,0,0], scale: [1,0.15,1], meta: { index: 3, dims: [1,0.15,1] } },
  // Containers on tiers
  { id: "c1", type: "container", parent_id: "tier1", position: [-0.3, 0.15, 0], rotation: [0,0,0], scale: [0.35,0.2,0.35], meta: { type: "polybag", dims: [0.35,0.2,0.35] } },
  { id: "c2", type: "container", parent_id: "tier1", position: [0.3, 0.15, 0], rotation: [0,0,0], scale: [0.35,0.2,0.35], meta: { type: "pot", dims: [0.35,0.2,0.35] } },
  { id: "c3", type: "container", parent_id: "tier2", position: [0, 0.15, 0], rotation: [0,0,0], scale: [0.35,0.2,0.35], meta: { type: "polybag", dims: [0.35,0.2,0.35] } },
  { id: "c4", type: "container", parent_id: "tier3", position: [0, 0.15, 0], rotation: [0,0,0], scale: [0.35,0.2,0.35], meta: { type: "seedling_tray", dims: [0.35,0.2,0.35], cells: ["cell-a","cell-b","cell-c"] } },
  // Tray cells + plants
  { id: "cell-a", type: "container_cell", parent_id: "c4", position: [-0.12, 0.05, -0.12], rotation: [0,0,0], scale: [0.08,0.05,0.08], meta: { index: 0 } },
  { id: "cell-b", type: "container_cell", parent_id: "c4", position: [0.12, 0.05, -0.12], rotation: [0,0,0], scale: [0.08,0.05,0.08], meta: { index: 1 } },
  { id: "cell-c", type: "container_cell", parent_id: "c4", position: [0, 0.05, 0.12], rotation: [0,0,0], scale: [0.08,0.05,0.08], meta: { index: 2 } },
  // Plants attached to containers / cells
  { id: "plant-c1", type: "plant", parent_id: "c1", position: [0, 0.2, 0], rotation: [0,0,0], scale: [0.08,0.15,0.08], meta: { species: "tomato" } },
  { id: "plant-c2", type: "plant", parent_id: "c2", position: [0, 0.2, 0], rotation: [0,0,0], scale: [0.08,0.15,0.08], meta: { species: "basil" } },
  { id: "plant-c3", type: "plant", parent_id: "cell-a", position: [0, 0.05, 0], rotation: [0,0,0], scale: [0.06,0.08,0.06], meta: { species: "lettuce" } },
  { id: "plant-c4", type: "plant", parent_id: "cell-b", position: [0, 0.05, 0], rotation: [0,0,0], scale: [0.06,0.08,0.06], meta: { species: "lettuce" } },
];
