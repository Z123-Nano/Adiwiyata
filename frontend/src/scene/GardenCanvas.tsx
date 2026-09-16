import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import { SYNTHETIC_HIERARCHY } from '../fixtures/gardenFixture'
import CoordinateGizmo from './CoordinateGizmo'
import BoundaryRenderer from './BoundaryRenderer'
import GenericObject from './GenericObject'
import { Boundary } from '../contracts/domain'

function computeWorld(p: typeof SYNTHETIC_HIERARCHY[0], parentWorld?: [number,number,number]) {
  // Simplified accumulation: parent world + local (rotation not fully decomposed; adequate for synthetic visual)
  const pw = parentWorld || [0,0,0]
  return [pw[0]+p.position[0], pw[1]+p.position[1], pw[2]+p.position[2]] as [number,number,number]
}

export default function GardenCanvas() {
  const nodes = SYNTHETIC_HIERARCHY
  // Build a lookup for parent world accumulation (simplified; single-level parents only for fixtures)
  const world: Record<string,[number,number,number]> = {}
  for (const n of nodes) {
    const pw = n.parent_id ? world[n.parent_id] || [0,0,0] : [0,0,0]
    world[n.id] = [pw[0]+n.position[0], pw[1]+n.position[1], pw[2]+n.position[2]]
  }
  const boundary: Boundary = { points: [[0,0,0],[4,0,0],[4,1,0],[2,1,0],[2,3,0],[0,3,0],[0,0,0]], type: "polygon" }
  return (
    <Canvas camera={{ position: [6, 4, 6], fov: 45 }} shadows>
      <ambientLight intensity={0.6} />
      <directionalLight position={[3, 6, 3]} intensity={1.0} castShadow />
      <CoordinateGizmo />
      <BoundaryRenderer poly={boundary} />
      {nodes.map(n => (
        <group key={n.id} position={world[n.id]} rotation={n.rotation} scale={n.scale}>
          <GenericObject id={n.id} type={n.type} position={[0,0,0]} parent_id={n.parent_id} meta={n.meta} />
        </group>
      ))}
      <OrbitControls />
      <gridHelper args={[12, 12, '#555555', '#333333']} />
    </Canvas>
  )
}
