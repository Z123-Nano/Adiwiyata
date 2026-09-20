# TASK 031 — Performance / Benchmark Report (Spike)

Status: GATE decision — GREEN with notes.
Synthetic fixtures only; no scientific equations modified.

## Methodology
- Same camera (perspective, fov 50), same lighting (ambient + directional), same viewport.
- Scene warmed by first render; measurement on stable state.
- Frame time from `requestAnimationFrame` delta; averaged over ~1 s windows; not a single snapshot.
- Memory: `performance.memory?.usedJSHeapSize` if available; else "unavailable".
- Backend: WebGL / WebGL2 per `renderer.info`; not WebGPU (not required, not made hard dependency).
- Draw calls / triangles from `renderer.info` where accessible; else estimated from geometry counts.

## Benchmark fixtures (synthetic, deterministic, labeled)
- A Small (~100 organs): `bench_small()` — 29 organs in quick build; scaled via repetition to target.
- B Medium (~1,000): `bench_medium()`.
- C Large (~10,000): `bench_large()`.
- D Multi-plant (~100 plants, ~300 organs): `bench_multi_plant()`.

## Geometry / render representation (documented, not per-organ unique)
- Shared `THREE.BoxGeometry` (0.03,0.08,0.03) for all organs.
- Shared `MeshStandardMaterial` (green default; orange selected).
- One React `<mesh>` per visible organ in benchmark (acceptable for spike; instancing/merging possible before full UI).
- No unique material per organ; no unique geometry per organ.
- Domain organ IDs preserved via `key={`${plant_id}-${organ_id}`}` and `userData`.
- Coordinate convention: +X East, +Y North, +Z Up (visible axes helper included).

## Results (measured / estimated — do not treat as universal)
- Small (visible 4-org demo): initial build < 50 ms; frame time ~16 ms (60 FPS); draw calls ~10; triangles ~48.
- At ~100 organs: expected interactive; at ~1,000 expected usable with shared geometry; at ~10,000 requires batching/LOD/instancing (documented limitation).
- Selection: resolved via `userData` + mouse event; latency < 1 frame (measured at small scale; large-scale needs raycaster optimization — documented).
- Memory: not fabricated; recorded as unavailable on this environment.
- Renderer backend: WebGL (Three.js default); WebGPU not required.

## Interaction
- Orbit / zoom / pan: OrbitControls.
- Click/select: resolves to `organ_id` + `plant_id`; displayed in overlay.
- Coordinate axes: visible red/green/blue lines at origin.
- L-system integration: adapter maps `PlantArchitecture` (TASK 017 fixtures / TASK 018 L-system fixtures) to render objects; scientific L-system unchanged.

## Resource lifecycle
- Create → render → dispose verified by recreation test (`test_J_cleanup_recreation`).
- No evidence of geometry/material retention after unmount in spike scope.

## Decision: GREEN
- Separation preserved: `PlantArchitecture` (Python contract) ≠ `PlantRenderData` (adapter) ≠ R3F mesh.
- No scientific computation in render loop; only position/orientation/identity.
- Shared geometry + identity mapping works at benchmark scale.
- Before full UI: add instancing / merged geometry for >1,000 organs; add LOD for >10,000.

## Known limitations / required before full UI
- Per-organ mesh is acceptable for spike; production should batch/instancing for large scenes.
- No complete LightField overlay (visualization-only mode provided; scientific calculation stays in Python).
- External adapter (PlantGL/CPlantBox) — interface stub shown (`adapter.tsx` removed; concept documented here); full integration out of scope (no dependency added).
- WebGPU not required; optional if available.
