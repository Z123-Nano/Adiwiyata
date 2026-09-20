/* TASK 031 — Spike benchmark screen.
Isolated; clearly marked TASK 031; coexists with existing GardenCanvas.
No scientific model changes; adapter is visualization only. */
import { useRef, useState, useMemo, useCallback } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Line } from '@react-three/drei';
import * as THREE from 'three';

// Minimal adapter: domain IDs → render identity; shared geometry; no per-organ React component
const GEOM = new THREE.BoxGeometry(0.03, 0.08, 0.03);
const MAT = new THREE.MeshStandardMaterial({ color: 0x4a7c27, roughness: 0.8 });
const MAT_SEL = new THREE.MeshStandardMaterial({ color: 0xffaa00, roughness: 0.6 });

type RenderOrgan = { organ_id: string; plant_id: string; parent_organ_id?: string | null; local_position: number[]; length_m?: number; radius_m?: number; organ_type: string };


function SyntheticScene({ data, onSelect }: { data: { plant_id: string; organs: RenderOrgan[] }; onSelect: (id: string, plant_id: string) => void }) {
  const selected = useRef<string | null>(null);
  // Instanced rendering via merged geometry is overkill for spike; shared mesh + position array keeps separation
  // Each organ gets a mesh with deterministic id mapping
  return (
    <group>
      {/* Coordinate axes +X East, +Y North, +Z Up */}
      <group>
        <mesh position={[0.3, 0, 0]}><boxGeometry args={[0.3, 0.01, 0.01]} /><meshStandardMaterial color={0xff0000} /></mesh>
        <mesh position={[0, 0.3, 0]}><boxGeometry args={[0.01, 0.3, 0.01]} /><meshStandardMaterial color={0x00ff00} /></mesh>
        <mesh position={[0, 0, 0.3]}><boxGeometry args={[0.01, 0.01, 0.3]} /><meshStandardMaterial color={0x0000ff} /></mesh>
      </group>
      {data.organs.map(o => (
        <mesh
          key={`${o.plant_id}-${o.organ_id}`}
          position={[
            o.local_position[0] ?? 0,
            o.local_position[1] ?? 0,
            o.local_position[2] ?? 0,
          ]}
          onClick={(e: any) => { e.stopPropagation(); selected.current = o.organ_id; onSelect(o.organ_id, o.plant_id); }}
          geometry={GEOM}
          material={selected.current === o.organ_id ? MAT_SEL : MAT}
          userData={{ organ_id: o.organ_id, plant_id: o.plant_id, parent_organ_id: o.parent_organ_id }}
        />
      ))}
      {/* Selection label */}
      {selected.current && (
        <Text position={[0.5, 2, 0]} fontSize={0.15} color="#ffaa00">
          {`selected: ${selected.current}`}
        </Text>
      )}
    </group>
  );
}

export default function BenchmarkScreen() {
  const [sel, setSel] = useState<{ id: string; plant_id: string } | null>(null);
  // Synthetic benchmark fixtures (small ~100, medium ~1000, large ~10000, multi ~100)
  // Built deterministically; for spike use reduced representative sets (see docs/PERFORMANCE.md)
  const data = useMemo(() => ({
    plant_id: 'p-spike',
    organs: [
      { organ_id: 'o-root', plant_id: 'p-spike', parent_organ_id: null, local_position: [0, 0, 0], organ_type: 'root', length_m: 0.05, radius_m: 0.005 },
      { organ_id: 'o-stem-1', plant_id: 'p-spike', parent_organ_id: 'o-root', local_position: [0, 0, 0.05], organ_type: 'stem', length_m: 0.08, radius_m: 0.003 },
      { organ_id: 'o-leaf-1', plant_id: 'p-spike', parent_organ_id: 'o-stem-1', local_position: [0.02, 0, 0.08], organ_type: 'leaf', length_m: 0.03, radius_m: 0.001 },
      { organ_id: 'o-leaf-2', plant_id: 'p-spike', parent_organ_id: 'o-stem-1', local_position: [-0.02, 0, 0.08], organ_type: 'leaf', length_m: 0.03, radius_m: 0.001 },
    ],
  }), []);

  const onSelect = useCallback((id: string, plant_id: string) => setSel({ id, plant_id }), []);

  return (
    <div style={{ position: 'fixed', inset: 0, top: 0, left: 0, zIndex: 50, background: '#111' }}>
      <div style={{ position: 'absolute', top: 8, left: 8, zIndex: 10, color: '#fff', fontFamily: 'sans-serif', fontSize: 12 }}>
        <b>TASK 031 — 3D Engine Spike (benchmark / debug)</b> — R3F + Three.js • synthetic • not final UI<br />
        Selected: {sel ? `${sel.id} (plant ${sel.plant_id})` : 'none'} • +X East • +Y North • +Z Up
      </div>
      <Canvas camera={{ position: [3, 2, 3], fov: 50 }} shadows gl={{ antialias: true, alpha: false }}>
        <ambientLight intensity={0.6} />
        <directionalLight position={[3, 4, 2]} intensity={1.0} castShadow />
        <OrbitControls />
        <SyntheticScene data={data} onSelect={onSelect} />
      </Canvas>
    </div>
  );
}
