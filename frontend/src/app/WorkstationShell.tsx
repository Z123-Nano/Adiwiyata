/** TASK 035 — Workstation shell layout (read-only scientific layout; no new science). */
import React, { useEffect } from 'react';
import HierarchyNavigator from './HierarchyNavigator';

export default function WorkstationShell({ children }: { children?: React.ReactNode }) {
  const ms = useMeasurementStore();
  const lf = useLightFieldStore();
  const ts = useTemporalStore();
  const ss = useSnapshotStore();
  const sc = useScenarioStore();
  useEffect(() => { ms.loadMeasurements(); ms.loadObservations(); lf.compute(); ts.loadClock(); ss.load(); sc.load(); }, []);
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', background: '#0d1117', color: '#c9d1d9', fontFamily: 'system-ui, sans-serif', fontSize: 13 }}>
      {/* Top bar */}
      <header style={{ height: 42, display: 'flex', alignItems: 'center', padding: '0 14px', background: '#161b22', borderBottom: '1px solid #30363d', fontSize: 12 }}>
        <b style={{ color: '#58a6ff', marginRight: 12 }}>Digital Twin Garden</b>
        <span style={{ color: '#8b949e', marginRight: 12 }}>v1 — TASK 035 Workstation</span>
        <span style={{ color: '#3fb950', marginRight: 12 }}>Garden: ACTIVE</span>
        <span style={{ color: '#8b949e' }}>Source: API/domain (TASK 034) · Synthetic fixtures isolated as demo</span>
      </header>

      {/* Main region */}
      <div style={{ display: 'flex', flex: 1, overflow: 'hidden' }}>
        {/* Left nav */}
        <nav style={{ width: 220, background: '#161b22', borderRight: '1px solid #30363d', padding: '10px 0', overflowY: 'auto' }}>
          <LeftNav />
        </nav>

        {/* Center viewport */}
        <main style={{ flex: 1, position: 'relative', overflow: 'auto', background: '#0d1117' }}>
          {children}
          <MeasurementsPanel />
          <LightPanel />
          <SnapshotPanel />
          <ScenarioPanel />
          <SimulationStepPanel />
        </main>

        {/* Right inspector */}
        <aside style={{ width: 320, background: '#161b22', borderLeft: '1px solid #30363d', padding: 12, overflowY: 'auto' }}>
          <InspectorPanel />
        </aside>
      </div>

      {/* Bottom status strip */}
      <footer style={{ height: 36, display: 'flex', alignItems: 'center', padding: '0 14px', background: '#161b22', borderTop: '1px solid #30363d', fontSize: 11, color: '#8b949e' }}>
        <TimeStatusStrip />
      </footer>
    </div>
  );
}

function LeftNav() {
  const modes = [
    { label: "Garden", active: true },
    { label: "Plants", active: false, note: "not integrated" },
    { label: "Measurements", active: false, note: "TASK 037 — API-backed" },
    { label: "Light", active: false, note: "TASK 038 — API-backed visualization" },
    { label: "Snapshots", active: false, note: "TASK 040 — immutable" },
    { label: "Scenarios", active: false, note: "TASK 040 — branch from snapshot" },
    { label: "Simulation", active: false, note: "not integrated" },
    { label: "Scenarios", active: false, note: "not integrated" },
    { label: "Validation", active: false, note: "not integrated" },
    { label: "Calibration", active: false, note: "not integrated" },
    { label: "Analysis", active: false, note: "not integrated" },
  ];
  return (
    <div>
      <div style={{ padding: '6px 14px', fontWeight: 600, color: '#8b949e', fontSize: 10, letterSpacing: 1, textTransform: 'uppercase' }}>Modes</div>
      {modes.map((m) => (
        <div key={m.label} style={{ padding: '6px 14px', borderLeft: m.active ? '3px solid #58a6ff' : '3px solid transparent', background: m.active ? 'rgba(88,166,255,0.08)' : 'transparent', color: m.active ? '#58a6ff' : '#c9d1d9', cursor: m.active ? 'default' : 'not-allowed' }} title={m.note || ''}>
          <b>{m.label}</b> {m.note && <span style={{ color: '#8b949e', fontSize: 10, marginLeft: 4 }}>{m.note}</span>}
          {!m.active && <span style={{ float: 'right', color: '#484f58', fontSize: 10 }}>—</span>}
        </div>
      ))}
      <div style={{ padding: '10px 14px', marginTop: 8, borderTop: '1px solid #30363d', fontSize: 10, color: '#484f58' }}>
        Only <b>Garden</b> is integrated. Others are placeholders with explicit unavailable state.
      </div>
      <div style={{ borderTop: '1px solid #30363d', padding: '6px 0' }}>
        <HierarchyNavigator />
      </div>
    </div>
  );
}

import { useSelection } from '../state/selectionStore';
import { useMeasurementStore } from '../state/measurementStore';
import { useLightFieldStore } from '../state/lightfieldStore';
import { useTemporalStore } from '../state/temporalStore';
import { useSnapshotStore } from '../state/snapshotStore';
import { useScenarioStore } from '../state/scenarioStore';

function InspectorPanel() {
  const sel = useSelection((s) => s.selected);
  // Read adapter scene or fallback info — no computation
  const meta = (sel && typeof sel.id === 'string') ? { id: sel.id, type: sel.type || "unknown", parent_id: sel.parent_id, local_pos: sel.local_pos } : null;
  return (
    <div>
      <h3 style={{ fontSize: 14, margin: '0 0 8px', color: '#c9d1d9', borderBottom: '1px solid #30363d', paddingBottom: 6 }}>Inspector — Selected Domain Object</h3>
      {!meta && (
        <div style={{ color: '#8b949e', fontSize: 11, padding: 4 }}>
          <b>None selected</b><br />Click an object in the scene to view domain identity.
        </div>
      )}
      {meta && (
        <div style={{ fontSize: 11, lineHeight: 1.6 }}>
          <Row label="Domain ID" value={meta.id} available />
          <Row label="Type" value={meta.type} available />
          <Row label="Parent ID" value={meta.parent_id || "none (root)"} available={!!meta.parent_id} />
          <Row label="Local position" value={JSON.stringify(meta.local_pos || [0,0,0])} available />
          <Row label="World position" value={JSON.stringify(meta.local_pos || [0,0,0])} note="computed by adapter (not source of truth)" available />
          <Row label="Architecture ID" value="not applicable (select plant/organ)" available={false} />
          <Row label="Dimensions" value="not available (use meta/fixture if available)" available={false} />
          <Row label="Data provenance" value="TASK 034 domain source / TASK 031 fixture (if demo) / TASK 037 API (if measurement)" available />
          <Row label="Temporal context" value="UNAVAILABLE (read-only; no interpolation)" available={false} />
      <Row label="Status" value={meta.type ? "VALID (selected)" : "NOT_APPLICABLE"} available />
      <SnapshotInspectorInfo />
      <ScenarioInspectorInfo />
          <MeasurementObserverInfo />
          <LightFieldInspectorInfo />
          <div style={{ marginTop: 10, padding: 6, background: '#0d1117', borderRadius: 4, color: '#8b949e', fontSize: 10 }}>
            <b>Note:</b> Inspector reads from application state / adapter output. No scientific computation is performed. Select an object to see its domain identity preserved end-to-end.
          </div>
        </div>
      )}
    </div>
  );
}

function Row({ label, value, available = true, note }: { label: string; value: string; available?: boolean; note?: string }) {
  return (
    <div style={{ marginBottom: 4, padding: '2px 0', borderBottom: '1px solid #21262d' }}>
      <div style={{ color: '#8b949e', fontSize: 10 }}>{label}</div>
      <div style={{ color: available ? '#c9d1d9' : '#fc0', fontWeight: available ? 500 : 400 }}>{value}</div>
      {note && <div style={{ color: '#484f58', fontSize: 9 }}>{note}</div>}
    </div>
  );
}

function LightPanel() {
  const lf = useLightFieldStore();
  const selectedId = lf.selectedSampleId;
  const result = lf.result;
  const selected = result && selectedId ? result.samples.find((s: any) => `${s.x},${s.y},${s.z}` === selectedId) : null;
  return (
    <div style={{ padding: 10, fontSize: 11, color: '#c9d1d9' }}>
      <h4 style={{ margin: '0 0 6px', fontSize: 13, color: '#58a6ff' }}>LightField (TASK 038)</h4>
      <div style={{ marginBottom: 4 }}>{lf.loading ? 'COMPUTING...' : lf.error ? 'ERROR: ' + lf.error : result ? 'Status: ' + result.status + ' · Samples: ' + (result.sample_count || 0) : 'Not loaded'}</div>
      <div style={{ fontSize: 10, color: '#8b949e', marginBottom: 6 }}>Unit: relative_normalized (not lux/PPFD) · Direct/diffuse/reflected/total preserved</div>
      {result && result.samples && (
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 10 }}>
          <thead><tr style={{ borderBottom: '1px solid #30363d', textAlign: 'left' }}><th style={{ padding: 2 }}>Sample</th><th>Direct</th><th>Diffuse</th><th>Refl</th><th>Total</th></tr></thead>
          <tbody>{result.samples.slice(0, 8).map((s: any, i: number) => (
            <tr key={i} style={{ borderBottom: '1px solid #21262d', cursor: 'pointer', background: selected && selected.x === s.x && selected.y === s.y ? 'rgba(88,166,255,0.15)' : 'transparent' }} onClick={() => lf.selectSample(`${s.x},${s.y},${s.z}`)}>
              <td style={{ padding: 2 }}>{`(${s.x.toFixed(1)},${s.y.toFixed(1)},${(s.z||0).toFixed(1)})`}</td>
              <td>{s.direct.toFixed(2)}</td><td>{s.diffuse.toFixed(2)}</td><td>{s.reflected.toFixed(2)}</td><td><b>{s.total.toFixed(2)}</b></td>
            </tr>
          ))}</tbody>
        </table>
      )}
      <div style={{ marginTop: 6, fontSize: 9, color: '#484f58' }}>No lux→PPFD · No solar/shadow calc in UI · Selection = domain ID only</div>
    </div>
  );
}

function MeasurementsPanel() {
  const ms = useMeasurementStore();
  const measurements = ms.measurements;
  const observations = ms.observations;
  return (
    <div style={{ padding: 10, fontSize: 11, color: '#c9d1d9' }}>
      <h4 style={{ margin: '0 0 8px', fontSize: 13, color: '#58a6ff' }}>Measurements (TASK 037 — API-backed)</h4>
      <div style={{ marginBottom: 6, color: '#8b949e' }}>{measurements.length} measurement records · {observations.length} observation records</div>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 10 }}>
        <thead><tr style={{ borderBottom: '1px solid #30363d', textAlign: 'left' }}><th style={{ padding: 2 }}>ID</th><th>Var</th><th>Value</th><th>Unit</th><th>Unc.</th><th>Prov</th></tr></thead>
        <tbody>
          {measurements.map((m: any) => (
            <tr key={m.id} style={{ borderBottom: '1px solid #21262d' }}>
              <td style={{ padding: 2 }}>{m.id}</td>
              <td>{m.variable}</td>
              <td>{m.value}</td>
              <td>{m.unit}</td>
              <td>{m.uncertainty === null || m.uncertainty === undefined ? '—' : m.uncertainty}</td>
              <td title={m.provenance || ''}>{m.provenance ? m.provenance.slice(0,10)+'...' : '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <h4 style={{ margin: '8px 0 8px', fontSize: 13, color: '#58a6ff' }}>Observations</h4>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 10 }}>
        <thead><tr style={{ borderBottom: '1px solid #30363d', textAlign: 'left' }}><th style={{ padding: 2 }}>ID</th><th>Type</th><th>Content (short)</th><th>Unit</th><th>Prov</th></tr></thead>
        <tbody>
          {observations.map((o: any) => (
            <tr key={o.id} style={{ borderBottom: '1px solid #21262d' }}>
              <td style={{ padding: 2 }}>{o.id}</td>
              <td>{o.observation_type || '—'}</td>
              <td>{(o.content || '').slice(0, 30)}</td>
              <td>{o.unit || '—'}</td>
              <td title={o.provenance || ''}>{o.provenance ? o.provenance.slice(0,10)+'...' : '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{ marginTop: 6, fontSize: 9, color: '#484f58' }}>Lux is lux (no PPFD). Uncertainty None = unavailable, not zero.</div>
    </div>
  );
}

function MeasurementObserverInfo() {
  const mSel = useMeasurementStore((s) => s.selectedMeasurementId);
  const oSel = useMeasurementStore((s) => s.selectedObservationId);
  const measurements = useMeasurementStore((s) => s.measurements);
  const observations = useMeasurementStore((s) => s.observations);
  const m = mSel ? measurements.find((x: any) => x.id === mSel) : null;
  const o = oSel ? observations.find((x: any) => x.id === oSel) : null;
  if (!m && !o) return null;
  return (
    <div style={{ marginTop: 8, padding: 6, background: '#0d1117', borderRadius: 4, fontSize: 10, color: '#c9d1d9' }}>
      <b style={{ color: '#58a6ff' }}>{m ? 'Measurement' : 'Observation'} (TASK 037)</b>
      {m && (
        <>
          <Row label="ID" value={m.id} available />
          <Row label="Quantity" value={m.variable} available />
          <Row label="Value" value={String(m.value)} available />
          <Row label="Unit" value={m.unit} available />
          <Row label="Timestamp" value={m.timestamp} available />
          <Row label="Uncertainty" value={m.uncertainty === null || m.uncertainty === undefined ? "UNAVAILABLE (not zero)" : String(m.uncertainty)} available={m.uncertainty !== null && m.uncertainty !== undefined} />
          <Row label="Instrument" value={m.instrument || "NOT_APPLICABLE"} available={!!m.instrument} />
          <Row label="Provenance" value={m.provenance || "NOT_APPLICABLE"} available={!!m.provenance} />
          <Row label="Lux status" value={m.unit === 'lux' ? "LUX IS LUX (no PPFD)" : m.unit || "NOT_APPLICABLE"} available />
          <Row label="Synthetic" value={m.is_synthetic_example ? "YES (fixture)" : "NO"} available />
        </>
      )}
      {o && (
        <>
          <Row label="ID" value={o.id} available />
          <Row label="Type" value={o.observation_type || "NOT_APPLICABLE"} available={!!o.observation_type} />
          <Row label="Category" value={o.category || "NOT_APPLICABLE"} available={!!o.category} />
          <Row label="Content" value={o.content} available />
          <Row label="Value numeric" value={o.value_numeric === null || o.value_numeric === undefined ? "UNAVAILABLE" : String(o.value_numeric)} available={o.value_numeric !== null && o.value_numeric !== undefined} />
          <Row label="Unit" value={o.unit || "NOT_APPLICABLE"} available={!!o.unit} />
          <Row label="Timestamp" value={o.timestamp} available />
          <Row label="Uncertainty" value={o.uncertainty === null || o.uncertainty === undefined ? "UNAVAILABLE" : String(o.uncertainty)} available={o.uncertainty !== null && o.uncertainty !== undefined} />
          <Row label="Provenance" value={o.provenance || "NOT_APPLICABLE"} available={!!o.provenance} />
          <Row label="Synthetic" value={o.is_synthetic_example ? "YES (fixture)" : "NO"} available />
        </>
      )}
      <div style={{ marginTop: 4, fontSize: 9, color: '#484f58' }}>No biological inference · No unit conversion · No calibration/validation/prediction.</div>
    </div>
  );
}

function SnapshotInspectorInfo() {
  const s = useSnapshotStore();
  const snap = s.selectedId ? s.snapshots.find((x: any) => x.snapshot_id === s.selectedId) : null;
  if (!snap) return null;
  return (
    <div style={{ marginTop: 8, padding: 6, background: '#0d1117', borderRadius: 4, fontSize: 10, color: '#c9d1d9' }}>
      <b style={{ color: '#58a6ff' }}>Snapshot (TASK 040 — immutable)</b>
      <Row label="Snapshot ID" value={snap.snapshot_id} available />
      <Row label="Timestamp" value={snap.timestamp || 'UNAVAILABLE'} available={!!snap.timestamp} />
      <Row label="Status" value={snap.status} available />
      <Row label="Immutable" value={snap.is_immutable ? 'YES' : 'NO'} available />
      <Row label="Provenance" value={snap.provenance || 'UNAVAILABLE'} available={!!snap.provenance} />
    </div>
  );
}
function ScenarioInspectorInfo() {
  const c = useScenarioStore();
  const sc = c.selectedId ? c.scenarios.find((x: any) => x.scenario_id === c.selectedId) : null;
  if (!sc) return null;
  return (
    <div style={{ marginTop: 8, padding: 6, background: '#0d1117', borderRadius: 4, fontSize: 10, color: '#c9d1d9' }}>
      <b style={{ color: '#58a6ff' }}>Scenario (TASK 040 — branch)</b>
      <Row label="Scenario ID" value={sc.scenario_id} available />
      <Row label="Source Snapshot" value={sc.source_snapshot_id || 'UNAVAILABLE'} available={!!sc.source_snapshot_id} />
      <Row label="Status" value={sc.status} available />
      <Row label="Overrides" value={sc.overrides ? JSON.stringify(sc.overrides) : 'NONE'} available={!!sc.overrides} />
      <Row label="Provenance" value={sc.provenance || 'UNAVAILABLE'} available={!!sc.provenance} />
      <Row label="Immutability note" value="Source snapshot unchanged; no mutation" available />
    </div>
  );
}

function LightFieldInspectorInfo() {
  const lf = useLightFieldStore();
  const selId = lf.selectedSampleId;
  const res = lf.result;
  if (!selId || !res) return null;
  const s = res.samples.find((x: any) => `${x.x},${x.y},${x.z}` === selId);
  if (!s) return null;
  return (
    <div style={{ marginTop: 8, padding: 6, background: '#0d1117', borderRadius: 4, fontSize: 10, color: '#c9d1d9' }}>
      <b style={{ color: '#58a6ff' }}>LightField Sample (TASK 038)</b>
      <Row label="ID" value={`${s.x.toFixed(2)},${s.y.toFixed(2)},${(s.z||0).toFixed(2)}`} available />
      <Row label="Direct" value={String(s.direct)} available />
      <Row label="Diffuse" value={String(s.diffuse)} available />
      <Row label="Reflected" value={String(s.reflected)} available />
      <Row label="Total" value={String(s.total)} available />
      <Row label="Unit" value={s.unit} available />
      <Row label="Status" value={res.status} available />
      <Row label="Provenance" value={res.provenance || 'NOT_APPLICABLE'} available={!!res.provenance} />
      <Row label="Comparison" value="UNAVAILABLE (read-only; no calibration/validation)" available={false} />
    </div>
  );
}

function SnapshotPanel() {
  const s = useSnapshotStore();
  return (
    <div style={{ padding: 10, fontSize: 11, color: '#c9d1d9' }}>
      <h4 style={{ margin: '0 0 6px', fontSize: 13, color: '#58a6ff' }}>Snapshots (TASK 040 — immutable)</h4>
      <div style={{ marginBottom: 4, color: '#8b949e' }}>{s.snapshots.length} records · status {s.loading ? 'LOADING' : s.error ? 'ERROR' : 'READY'}</div>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 10 }}>
        <thead><tr style={{ borderBottom: '1px solid #30363d', textAlign: 'left' }}><th>ID</th><th>Timestamp</th><th>Status</th><th>Immutable</th></tr></thead>
        <tbody>{s.snapshots.map((snap: any) => (
          <tr key={snap.snapshot_id} style={{ borderBottom: '1px solid #21262d' }}><td>{snap.snapshot_id}</td><td>{snap.timestamp}</td><td>{snap.status}</td><td>{snap.is_immutable ? 'YES' : 'NO'}</td></tr>
        ))}</tbody>
      </table>
      <div style={{ marginTop: 6, fontSize: 9, color: '#484f58' }}>Source preserved · No mutation · No simulation</div>
    </div>
  );
}

function SimulationStepPanel() {
  return (
    <div style={{ padding: 10, fontSize: 11, color: '#c9d1d9' }}>
      <h4 style={{ margin: '0 0 6px', fontSize: 13, color: '#58a6ff' }}>Simulation Step (TASK 044)</h4>
      <div style={{ marginBottom: 6, fontSize: 10, color: '#8b949e' }}>Use <b>POST /api/v1/simulation/step</b> with snapshot/scenario source. Read-only result; no Play/Pause/Run.</div>
      <div style={{ fontSize: 10, color: '#484f58' }}>Components: photosynthesis · carbon_respiration · source_sink_allocation · organ_growth · lightfield_input. Status shown from API (AVAILABLE / NOT_COMPUTABLE / PARTIAL / ERROR). No frontend science.</div>
    </div>
  );
}

function ScenarioPanel() {
  const c = useScenarioStore();
  return (
    <div style={{ padding: 10, fontSize: 11, color: '#c9d1d9' }}>
      <h4 style={{ margin: '0 0 6px', fontSize: 13, color: '#58a6ff' }}>Scenarios (TASK 040 — branch)</h4>
      <div style={{ marginBottom: 4, color: '#8b949e' }}>{c.scenarios.length} records · {c.loading ? 'LOADING' : c.error ? 'ERROR' : 'READY'}</div>
      <button onClick={() => c.branchFromSnapshot('snap-001', {note:'example'})} style={{ fontSize: 10, background:'#58a6ff', color:'#fff', border:'none', padding:'3px 8px', cursor:'pointer' }}>Branch from snap-001</button>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 10, marginTop: 6 }}>
        <thead><tr style={{ borderBottom: '1px solid #30363d', textAlign: 'left' }}><th>ID</th><th>Source</th><th>Overrides</th><th>Status</th></tr></thead>
        <tbody>{c.scenarios.map((sc: any) => (
          <tr key={sc.scenario_id} style={{ borderBottom: '1px solid #21262d' }}><td>{sc.scenario_id}</td><td>{sc.source_snapshot_id || '—'}</td><td>{sc.overrides ? JSON.stringify(sc.overrides).slice(0,20) : '—'}</td><td>{sc.status}</td></tr>
        ))}</tbody>
      </table>
    </div>
  );
}

function TimeStatusStrip() {
  const ts = useTemporalStore();
  const clock = ts.clock;
  const mode = ts.displayMode;
  return (
    <div style={{ display: 'flex', gap: 14, alignItems: 'center', width: '100%', flexWrap: 'wrap' }}>
      <span><b>World/Obs</b> <span style={{ color: '#8b949e' }}>{clock?.world_time || clock?.observation_time || "UNAVAILABLE"}</span></span>
      <span><b>Simulation</b> <span style={{ color: clock?.simulation_time && clock.simulation_time.includes("UNAVAILABLE") ? '#8b949e' : '#58a6ff' }}>{clock?.simulation_time || "UNAVAILABLE"}</span></span>
      <span><b>Plant age</b> <span style={{ color: '#8b949e' }}>{clock?.plant_age || "UNAVAILABLE"}</span></span>
      <span><b>Forecast</b> <span style={{ color: '#8b949e' }}>{clock?.forecast_target || "UNAVAILABLE"}</span></span>
      <span><b>Timestep</b> <span style={{ color: '#8b949e' }}>{clock?.timestep === null || clock?.timestep === undefined ? "UNAVAILABLE" : String(clock.timestep)}</span></span>
      <span><b>Mode</b> <span style={{ color: '#8b949e' }}>{clock?.timestep_mode || "UNAVAILABLE"}</span></span>
      <span><b>Timezone</b> <span style={{ color: '#8b949e' }}>{clock?.timezone || "UNAVAILABLE"}</span></span>
      <span><b>Clock status</b> <span style={{ color: clock?.clock_status === "READY" ? '#3fb950' : '#fc0' }}>{clock?.clock_status || "LOADING"}</span></span>
      <span><b>Sched status</b> <span style={{ color: '#8b949e' }}>{clock?.scheduler_status || "UNAVAILABLE"}</span></span>
      <span><b>Display</b> <span style={{ color: '#3fb950' }}>{mode}</span></span>
      <span><b>Source</b> <span style={{ color: '#58a6ff' }}>API/domain (TASK 041)</span></span>
      <span style={{ marginLeft: 'auto', color: '#484f58', fontSize: 10 }}>{clock?.provenance ? clock.provenance.slice(0, 40) + '...' : 'TASK 041'}</span>
      <button onClick={() => ts.setDisplayMode('observation')} style={{ fontSize: 10, background: mode==='observation'?'#58a6ff':'#161b22', color:'#fff', border:'none', padding:'2px 6px', cursor:'pointer' }}>Obs</button>
      <button onClick={() => ts.setDisplayMode('simulation')} style={{ fontSize: 10, background: mode==='simulation'?'#58a6ff':'#161b22', color:'#fff', border:'none', padding:'2px 6px', cursor:'pointer' }}>Sim</button>
    </div>
  );
}
