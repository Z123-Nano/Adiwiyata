import { Line } from '@react-three/drei'
import { toThreeVec } from './DomainSceneAdapter'
import { Boundary } from '../contracts/domain'

export default function BoundaryRenderer({ poly }: { poly: Boundary }) {
  const pts = poly.points.map(p => [p[0], p[1], p[2]] as [number,number,number])
  // Line expects points as number[][]; close loop if needed
  const loop = pts.concat([pts[0]])
  return <Line points={loop as [number,number,number][]} color="#ffd166" lineWidth={2} />
}
