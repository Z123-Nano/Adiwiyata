import { useSelection } from '../state/selectionStore'
export default function GenericObject({ id, type, position, rotation, scale, meta, parent_id }: { id: string; type: string; position: [number,number,number]; rotation?: [number,number,number]; scale?: [number,number,number]; meta?: Record<string,any>; parent_id?: string }) {
  const select = useSelection((s) => s.select)
  const selectedId = useSelection((s) => s.selected?.id)
  const isSelected = selectedId === id
  const color = isSelected ? '#58a6ff' : (type === 'building' ? '#b0bec5' : type === 'fence' ? '#888' : type === 'tree' ? '#795548' : type === 'rack' ? '#607d8b' : type === 'tier' ? '#455a64' : type === 'container' ? '#8d6e63' : type === 'plant' ? '#2e7d32' : '#ffd166')
  const shape = type === 'building' ? <boxGeometry args={meta?.dims ? [meta.dims[0],meta.dims[1],meta.dims[2]] : [1,1,1]} /> : type === 'fence' ? <boxGeometry args={meta?.thickness && meta.height ? [meta.thickness,meta.height,meta.length||4] : [0.1,1,4]} /> : type === 'tree' ? <group><mesh position={[0,0.3,0]}><cylinderGeometry args={[0.2,0.2,0.6,12]} /><meshStandardMaterial color="#795548" /></mesh><mesh position={[0,0.9,0]}><sphereGeometry args={[0.5,12,12]} /><meshStandardMaterial color="#558b2f" /></mesh></group> : type === 'rack' ? <boxGeometry args={meta?.dims ? [meta.dims[0],meta.dims[1],meta.dims[2]] : [1.5,1.2,0.8]} /> : type === 'tier' ? <boxGeometry args={meta?.dims ? [meta.dims[0],meta.dims[1],meta.dims[2]] : [1,0.15,1]} /> : type === 'container' ? <cylinderGeometry args={[0.15,0.15,0.25,16]} /> : <sphereGeometry args={[0.12,12,12]} />
  return (
    <mesh position={position} rotation={rotation || [0,0,0]} scale={scale || [1,1,1]} onClick={() => select({ id, type, parent_id, local_pos: position, world_pos: position })}>
      {shape}
      <meshStandardMaterial color={color} />
    </mesh>
  )
}
