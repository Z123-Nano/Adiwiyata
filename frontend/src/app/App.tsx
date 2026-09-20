import { useState } from 'react';
import GardenCanvas from '../scene/GardenCanvas';
import InspectionPanel from '../scene/InspectionPanel';
import { useGardenState } from '../state/gardenStore';
import { useLightFieldStore } from '../state/lightfieldStore';
import { useSelection } from '../state/selectionStore';
import { useTemporalStore } from '../state/temporalStore';

function TopBar() {
  const garden = useGardenState((s) => s.gardenData);
  const light = useLightFieldStore((s) => s.result);
  const sel = useSelection((st) => st.selected);
  return (
    <header style={{ height: 48, background: '#14161b', borderBottom: '1px solid #23262e', display: 'flex', alignItems: 'center', padding: '0 16px', gap: 16, fontFamily: 'system-ui, sans-serif', fontSize: 13, color: '#e6e8ee', userSelect: 'none' }}>
      <strong style={{ color: '#ffd166', fontSize: 15, letterSpacing: 0.5 }}>Adiwiyata Digital Twin</strong>
      <span style={{ color: '#8b949e', fontSize: 11 }}>|</span>
      <span style={{ color: '#8b949e' }}>{(garden as any)?.name || (garden as any)?.garden_id || 'Garden'}</span>
      <span style={{ flex: 1 }} />
      <span>LightField: {light ? (light.status || 'available') : '—'}</span>
      <span style={{ color: '#8b949e', fontSize: 11 }}>{sel ? `Selected: ${sel.id}` : 'No selection'}</span>
    </header>
  );
}

function LeftNav({ active, setActive }: { active: string; setActive: (s: string) => void }) {
  const items = [
    { id: 'garden', label: 'Garden' },
    { id: 'plants', label: 'Plants' },
    { id: 'architecture', label: 'Architecture' },
    { id: 'light', label: 'Light' },
    { id: 'measurements', label: 'Measurements' },
    { id: 'simulation', label: 'Simulation' },
    { id: 'snapshots', label: 'Snapshots' },
    { id: 'scenarios', label: 'Scenarios' },
  ];
  return (
    <nav style={{ width: 200, background: '#0f1118', borderRight: '1px solid #23262e', padding: 10, fontSize: 12, color: '#c4cbd6' }}>
      <div style={{ fontWeight: 700, color: '#ffd166', marginBottom: 8, fontSize: 13 }}>Workstation</div>
      {items.map((it) => (
        <button key={it.id} onClick={() => setActive(it.id)} style={{
          display: 'block', width: '100%', textAlign: 'left', padding: '6px 8px', marginBottom: 2,
          background: active === it.id ? '#1b1f2a' : 'transparent', border: 'none', borderRadius: 4,
          color: active === it.id ? '#ffd166' : '#c4cbd6', cursor: 'pointer', fontSize: 12
        }}>{it.label}</button>
      ))}
      <div style={{ marginTop: 16, padding: '6px 8px', borderTop: '1px solid #23262e', fontSize: 11, color: '#6b7280' }}>
        Synthetic pilot — TASK 052 workstation rebuild; real data from TASK 051 still pending.
      </div>
    </nav>
  );
}

function RightInspector() {
  const sel = useSelection((st) => st.selected);
  const light = useLightFieldStore((s) => s.result);
  return (
    <aside style={{ width: 260, background: '#0f1118', borderLeft: '1px solid #23262e', padding: 14, fontSize: 12, color: '#c4cbd6', overflow: 'auto' }}>
      <h3 style={{ color: '#ffd166', fontSize: 13, margin: '0 0 8px', borderBottom: '1px solid #23262e', paddingBottom: 6 }}>Inspector</h3>
      {sel ? (
        <div>
          <b>id</b>: {sel.id}<br />
          <b>type</b>: {sel.type}<br />
          <b>parent</b>: {sel.parent_id || '—'}<br />
          <b>local</b>: [{sel.local_pos[0].toFixed(2)}, {sel.local_pos[1].toFixed(2)}, {sel.local_pos[2].toFixed(2)}]<br />
          <b>world</b>: [{sel.world_pos[0].toFixed(2)}, {sel.world_pos[1].toFixed(2)}, {sel.world_pos[2].toFixed(2)}]<br />
          <div style={{ marginTop: 8, padding: 6, background: '#1b1f2a', borderRadius: 4, fontSize: 11 }}>
            <b>Architecture</b> — identity preserved by 046AF; delta refs from growth stage (if available).<br />
            <b>Light</b> — LightField status: {light ? (light.status || 'available') : '—'}; relative-normalized shown (not absolute PPFD).<br />
            <b>PPFD</b> — absolute reference requires 046O/046V path; not directly rendered here.<br />
            <b>Measurement</b> — observation sync from 047-FIX available; real dataset from TASK 051 not yet supplied.
          </div>
        </div>
      ) : (
        <div>
          <div style={{ color: '#ffd166', fontWeight: 700, marginBottom: 6 }}>Garden Summary</div>
          <div style={{ fontSize: 11, lineHeight: 1.5 }}>
            <b>Reference</b>: G0 (+X East / +Y North / +Z Up)<br />
            <b>Boundary</b>: L-shaped; rack / tier / container hierarchy<br />
            <b>LightField</b>: relative-normalized (current contract); absolute PPFD via 046V<br />
            <b>Simulation</b>: clock 3600s; step/run/pause not exposed in UI (backend /clock endpoint available)<br />
            <b>Observation</b>: synthetic pilot (TASK 051 PARTIAL); real measurements required<br />
            <b>State</b>: architecture unchanged at boundary; carbon reserve + current_net preserved (046Z)
          </div>
          <div style={{ marginTop: 10, padding: 6, background: '#1b1f2a', borderRadius: 4, fontSize: 11, color: '#8b949e' }}>
            First real observation intake (TASK 051) completed as synthetic pilot only. Data directories (data/observations, data/measurements) remain empty. Real-garden measurement campaign still required: calibrated PPFD, architecture, environment, phenology events, sensor registry, multi-PPFD.
          </div>
        </div>
      )}
    </aside>
  );
}

function BottomBar() {
  const temporal = useTemporalStore((s) => s.clock);
  return (
    <footer style={{ height: 40, background: '#14161b', borderTop: '1px solid #23262e', display: 'flex', alignItems: 'center', padding: '0 16px', gap: 16, fontSize: 11, color: '#8b949e', fontFamily: 'system-ui, sans-serif' }}>
      <span>Simulation: <b style={{ color: '#c4cbd6' }}>{(temporal as any)?.step_id || '—'}</b></span>
      <span>Step: <b style={{ color: '#c4cbd6' }}>{(temporal as any)?.timestep || 3600}</b>s</span>
      <span>Clock: <b style={{ color: '#c4cbd6' }}>{(temporal as any)?.simulation_time_ref || '—'}</b></span>
      <span style={{ flex: 1 }} />
      <span>Status: <b style={{ color: '#ffd166' }}>READY</b> — synthetic viewer (TASK 052 workstation rebuild); no calibration; real data not yet supplied</span>
    </footer>
  );
}

export default function App() {
  const [active, setActive] = useState('garden');
  return (
    <div style={{ height: '100vh', width: '100vw', background: '#0b0c15', overflow: 'hidden', display: 'flex', flexDirection: 'column', fontFamily: 'system-ui, sans-serif' }}>
      <TopBar />
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        <LeftNav active={active} setActive={setActive} />
        <main style={{ flex: 1, position: 'relative', overflow: 'hidden' }}>
          <GardenCanvas />
        </main>
        <RightInspector />
      </div>
      <BottomBar />
    </div>
  );
}
