/** TASK 033 — DomainSceneAdapter.
Domain objects (Garden / SpatialObject / Plant / PlantArchitecture) → render-neutral scene nodes.
No Three.js; no scientific calculation; preserves IDs and transforms.
*/
import type { Garden, SpatialObject, Plant, Container, ContainerCell } from '../contracts/domain'

// Back-compat for BoundaryRenderer / SpatialNodeRenderer (TASK 031 / 033)
export function toThreeVec(p: { x: number; y: number; z: number }): [number, number, number] {
  return [p.x, p.y, p.z];
}
export function toThreePos(t: { position: { x: number; y: number; z: number } }): [number, number, number] {
  return [t.position.x, t.position.y, t.position.z];
}

export interface SceneNode {
  id: string;
  type: string; // "building" | "fence" | "tree" | "rack" | "tier" | "container" | "container_cell" | "plant" | "other"
  parent_id?: string;
  local_position: [number, number, number];
  world_position: [number, number, number];
  rotation?: [number, number, number];
  scale?: [number, number, number];
  meta?: Record<string, unknown>;
  domain_plant_id?: string;
  domain_organ_id?: string;
}

function accumulateWorld(
  obj: { id: string; transform: { position: [number,number,number]; parent_id?: string } },
  lookup: Record<string, [number,number,number]>,
  parentWorld?: [number,number,number]
): [number,number,number] {
  const pw = parentWorld || [0,0,0];
  const local = obj.transform.position || [0,0,0];
  const w: [number,number,number] = [pw[0]+local[0], pw[1]+local[1], pw[2]+local[2]];
  lookup[obj.id] = w;
  return w;
}

export function adaptGardenToScene(
  garden: Garden,
  objects: SpatialObject[] = [],
  plants: Plant[] = [],
  architectures: Record<string, { organs?: { id: string; parent_organ_id?: string; local_position?: number[]; organ_type?: string; plant_id?: string }[] }> = {}
): SceneNode[] {
  const nodes: SceneNode[] = [];
  const world: Record<string, [number,number,number]> = {};
  // Boundary / root reference preserved
  if (garden?.boundary) {
    nodes.push({ id: "boundary", type: "boundary", local_position: [0,0,0], world_position: [0,0,0], meta: { points: garden.boundary.points, type: garden.boundary.type } });
  }
  // Spatial hierarchy
  const lookup = new Map<string, { parent?: string; local: [number,number,number] }>();
  for (const o of objects) {
    lookup.set(o.id, { parent: o.parent_id, local: o.transform.position || [0,0,0] });
  }
  // Build world positions (simple accumulation — adequate for boundary/objects; full tree requires ordered top-down)
  for (const o of objects) {
    const pw = (o.parent_id && world[o.parent_id]) ? world[o.parent_id] : [0,0,0];
    const w = [pw[0]+(o.transform.position[0]||0), pw[1]+(o.transform.position[1]||0), pw[2]+(o.transform.position[2]||0)] as [number,number,number];
    world[o.id] = w;
    nodes.push({
      id: o.id,
      type: o.type as SceneNode["type"],
      parent_id: o.parent_id,
      local_position: o.transform.position || [0,0,0],
      world_position: w,
      rotation: o.transform.rotation_euler_deg ? [o.transform.rotation_euler_deg[0]||0, o.transform.rotation_euler_deg[1]||0, o.transform.rotation_euler_deg[2]||0] : undefined,
      scale: o.transform.scale || [1,1,1],
      meta: { dims: (o as any).dimensions || undefined, spec: o.id },
      domain_plant_id: (o as any).occupied_plant_id || undefined,
    });
  }
  // Plants (identity + architecture reference)
  for (const pl of plants) {
    nodes.push({
      id: pl.id,
      type: "plant",
      local_position: [0,0,0],
      world_position: (world[pl.id] || [0,0,0]) as [number,number,number],
      meta: { species_id: pl.species_id, variety_id: pl.variety_id },
      domain_plant_id: pl.id,
    });
  }
  // Plant architectures (organs mapped as scene nodes for selection / identity)
  for (const [plantId, arch] of Object.entries(architectures)) {
    if (!arch || !arch.organs) continue;
    for (const organ of arch.organs) {
      const parentWorld = (organ.parent_organ_id && world[organ.parent_organ_id]) ? world[organ.parent_organ_id] : [0,0,0];
      const local = (organ.local_position as number[] || [0,0,0]) as [number,number,number];
      const w = [parentWorld[0]+local[0], parentWorld[1]+local[1], parentWorld[2]+local[2]] as [number,number,number];
      nodes.push({
        id: organ.id,
        type: (organ.organ_type as SceneNode["type"]) || "other",
        parent_id: organ.parent_organ_id,
        local_position: local,
        world_position: w,
        meta: { plant_id: organ.plant_id || plantId, organ_type: organ.organ_type },
        domain_plant_id: organ.plant_id || plantId,
        domain_organ_id: organ.id,
      });
    }
  }
  return nodes;
}

// Minimal adapter for direct domain object (without full garden) — useful for plant inspection
export function adaptPlantToScene(plant: Plant, architecture?: { organs?: any[] }): SceneNode[] {
  const nodes: SceneNode[] = [];
  nodes.push({ id: plant.id, type: "plant", local_position: [0,0,0], world_position: [0,0,0], meta: { species_id: plant.species_id, variety_id: plant.variety_id }, domain_plant_id: plant.id });
  if (architecture?.organs) {
    for (const o of architecture.organs) {
      nodes.push({
        id: o.id, type: (o.organ_type as SceneNode["type"]) || "other",
        parent_id: o.parent_organ_id, local_position: (o.local_position as number[] || [0,0,0]) as [number,number,number],
        world_position: (o.local_position as number[] || [0,0,0]) as [number,number,number],
        meta: { plant_id: o.plant_id || plant.id, organ_type: o.organ_type },
        domain_plant_id: o.plant_id || plant.id, domain_organ_id: o.id,
      });
    }
  }
  return nodes;
}
