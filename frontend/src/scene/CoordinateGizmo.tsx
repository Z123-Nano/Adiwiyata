import { Line } from '@react-three/drei'

export default function CoordinateGizmo() {
  return (
    <group position={[0, 0, 0]}>
      {/* +X East red */}
      <Line points={[[0,0,0],[1.5,0,0]]} color="#ff5252" lineWidth={3} />
      <mesh position={[1.6,0,0]}>
        <coneGeometry args={[0.08,0.25,16]} />
        <meshStandardMaterial color="#ff5252" />
      </mesh>
      {/* +Y North green */}
      <Line points={[[0,0,0],[0,1.5,0]]} color="#69f0ae" lineWidth={3} />
      <mesh position={[0,1.6,0]} rotation={[0,0,Math.PI/2]}>
        <coneGeometry args={[0.08,0.25,16]} />
        <meshStandardMaterial color="#69f0ae" />
      </mesh>
      {/* +Z Up blue */}
      <Line points={[[0,0,0],[0,0,1.5]]} color="#448aff" lineWidth={3} />
      <mesh position={[0,0,1.6]} rotation={[Math.PI/2,0,0]}>
        <coneGeometry args={[0.08,0.25,16]} />
        <meshStandardMaterial color="#448aff" />
      </mesh>
      {/* G0 label */}
      <mesh position={[0,0,0]} rotation={[-Math.PI/2,0,0]}>
        <planeGeometry args={[0.9,0.3]} />
        <meshStandardMaterial color="#ffffff" transparent opacity={0.8} />
      </mesh>
    </group>
  )
}
