import { toThreePos } from './DomainSceneAdapter'

export default function SpatialNodeRenderer({ id, transform, color="#4caf50" }: { id: string; transform: { position: { x: number; y: number; z: number } }; color?: string }) {
  return (
    <mesh position={toThreePos(transform)}>
      <boxGeometry args={[0.4,0.4,0.4]} />
      <meshStandardMaterial color={color} />
    </mesh>
  )
}
