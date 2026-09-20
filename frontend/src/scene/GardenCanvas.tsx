import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import { SYNTHETIC_HIERARCHY } from '../fixtures/gardenFixture'
import CoordinateGizmo from './CoordinateGizmo'
import BoundaryRenderer from './BoundaryRenderer'
import GenericObject from './GenericObject'
import { Boundary } from '../contracts/domain'
import { adaptGardenToScene } from './DomainSceneAdapter'
import type { SceneNode } from './DomainSceneAdapter'
import type { Garden } from '../contracts/domain'

import { useMeasurementStore } from '../state/measurementStore';
import { useLightFieldStore } from '../state/lightfieldStore';

function LightFieldMarkers() {
  const result = useLightFieldStore((s) => s.result);
  if (!result || !result.samples || result.samples.length === 0) return null;
  // Shared geometry / material; selection handled by store, not Three.js objects
  return (
    <>
      {result.samples.map((s: any, i: number) => {
        const intensity = s.total || 0;
        const color = intensity > 0.7 ? "#ffb86c" : intensity > 0.3 ? "#ffd166" : "#8b949e";
        return (
          <mesh key={`lf-${i}`} position={[s.x, s.y, s.z || 0]} >
            <sphereGeometry args={[0.06, 8, 8]} />
            <meshStandardMaterial color={color} />
          </mesh>
        );
      })}
    </>
  );
}

function ObservationMarkers() {
  // Lightweight shared geometry; domain ID preserved; no unique material
  const obs = useMeasurementStore((s) => s.observations);
  return (
    <>
      {obs.filter((o: any) => o.spatial_ref && typeof o.spatial_ref.x === 'number').map((o: any) => (
        <mesh key={o.id} position={[o.spatial_ref.x, o.spatial_ref.y, o.spatial_ref.z || 0]}>
          <sphereGeometry args={[0.08, 8, 8]} />
          <meshStandardMaterial color="#ffb86c" />
        </mesh>
      ))}
    </>
  );
}

function computeWorld(p: typeof SYNTHETIC_HIERARCHY[0], parentWorld?: [number,number,number]) {
  const pw = parentWorld || [0,0,0]
  return [pw[0]+p.position[0], pw[1]+p.position[1], pw[2]+p.position[2]] as [number,number,number]
}

export interface GardenCanvasProps {
  garden?: Garden;
  objects?: any[];
  plants?: any[];
  architectures?: Record<string, any>;
  demoFixture?: boolean; // if true, use benchmark fixtures explicitly
}

export default function GardenCanvas({ garden, objects, plants, architectures, demoFixture }: GardenCanvasProps = {}) {
  // Production path: adapter from domain objects if provided
  let sceneNodes: SceneNode[] = []
  let sourceNote = ""
  if (!demoFixture && garden) {
    try {
      sceneNodes = adaptGardenToScene(garden, objects || [], plants || [], architectures || {})
      sourceNote = "TASK 033 — domain adapter (Garden + objects + plants + architectures)"
    } catch {
      sourceNote = "TASK 033 — adapter error, falling back to fixture"
      sceneNodes = []
    }
  }
  // Fallback / explicit demo: synthetic fixtures only when no domain data or demo mode
  const useFixture = demoFixture || (!garden && sceneNodes.length === 0)
  if (useFixture) {
    sourceNote = sourceNote || "Synthetic pilot — Adiwiyata Digital Twin (workstation rebuild; real data from TASK 051 still pending)"
  }

  // Render nodes for adapter path
  const nodes = useFixture ? SYNTHETIC_HIERARCHY.map((n: any) => ({
    id: n.id, type: n.type, parent_id: n.parent_id,
    local_position: n.position || [0,0,0],
    world_position: [0,0,0] as [number,number,number],
    meta: n.meta,
    domain_plant_id: undefined,
  })) : sceneNodes

  // World accumulation (same logic as fixture path — adequate for both)
  const world: Record<string,[number,number,number]> = {}
  // First pass: build parent lookup from adapter nodes (use userData mapping later for selection)
  const parentOf: Record<string, string | undefined> = {}
  for (const n of nodes) parentOf[n.id] = n.parent_id
  // Simple accumulation (depth-first order assumed; sufficient for demo + adapter output)
  for (const n of nodes) {
    const pw = (n.parent_id && world[n.parent_id]) ? world[n.parent_id] : [0,0,0]
    world[n.id] = [pw[0]+(n.local_position?.[0]||0), pw[1]+(n.local_position?.[1]||0), pw[2]+(n.local_position?.[2]||0)] as [number,number,number]
  }

  const boundary: Boundary = { points: [[0,0,0],[4,0,0],[4,1,0],[2,1,0],[2,3,0],[0,3,0],[0,0,0]], type: "polygon" }

  return (
    <>
      <div style={{ position: 'absolute', top: 8, left: 8, zIndex: 10, color: '#fff', fontFamily: 'sans-serif', fontSize: 11, background: 'rgba(0,0,0,0.6)', padding: 6, borderRadius: 4 }}>
        <b>Adiwiyata Digital Twin</b> &nbsp;|&nbsp; {sourceNote} &nbsp;|&nbsp; +X East · +Y North · +Z Up<br />
        <span style={{ opacity: 0.8 }}>{useFixture ? "Synthetic pilot (TASK 052 workstation) — real-garden observations pending (TASK 051)" : "Domain adapter mode (API/domain)"}</span>
      </div>
      <Canvas camera={{ position: [6, 4, 6], fov: 45 }} shadows>
        <ambientLight intensity={0.6} />
        <directionalLight position={[3, 6, 3]} intensity={1.0} castShadow />
        <CoordinateGizmo />
        <BoundaryRenderer poly={boundary} />
        {nodes.map(n => (
          <group key={n.id} position={world[n.id] || [0,0,0]}>
            <GenericObject
              id={n.id}
              type={n.type}
              position={[0,0,0]}
              parent_id={n.parent_id}
              meta={n.meta || { domain_ref: n.id, source: sourceNote }}
            />
          </group>
        ))}
        <ObservationMarkers />
        <LightFieldMarkers />
        <OrbitControls />
        <gridHelper args={[12, 12, '#555555', '#333333']} />
      </Canvas>
    </>
  )
}
