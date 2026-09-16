/* Domain spatial model -> Three.js adapter (TASK 004). Domain is source of truth. */

export function toThreeVec(p: { x: number; y: number; z: number }): [number, number, number] {
  return [p.x, p.y, p.z]
}

export function toThreePos(t: { position: { x: number; y: number; z: number } }): [number, number, number] {
  return [t.position.x, t.position.y, t.position.z]
}
