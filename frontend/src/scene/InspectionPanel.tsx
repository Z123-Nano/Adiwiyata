import { useSelection } from '../state/selectionStore'

export default function InspectionPanel() {
  const s = useSelection((st) => st.selected)
  if (!s) return null
  return (
    <div style={{ position: 'absolute', top: 12, right: 12, background: 'rgba(11,12,21,0.9)', color: '#fff', padding: 12, borderRadius: 8, fontFamily: 'system-ui', fontSize: 12, maxWidth: 220, zIndex: 10 }}>
      <b>Selected</b><br />
      id: {s.id}<br />
      type: {s.type}<br />
      parent_id: {s.parent_id || "—"}<br />
      local: [{s.local_pos[0].toFixed(2)},{s.local_pos[1].toFixed(2)},{s.local_pos[2].toFixed(2)}]<br />
      world: [{s.world_pos[0].toFixed(2)},{s.world_pos[1].toFixed(2)},{s.world_pos[2].toFixed(2)}]
    </div>
  )
}
