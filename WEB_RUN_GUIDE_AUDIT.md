# Web Run Guide Audit — Adiwiyata Digital Twin
Audit only; no code modified. Evidence from current repository (2026-09-19).

## 1. Current Web Architecture
- Frontend: React + TypeScript + Vite (frontend/package.json: name "dtg-f", dev "vite", build "tsc && vite build").
- Backend: FastAPI (simulation/api/app.py); title "Digital Twin Garden API" v1; docs_url "/docs"; CORS allows localhost:5173 / 3000 / 127.0.0.1:5173.
- Entry frontend: frontend/src/app/App.tsx (renders GardenCanvas + InspectionPanel; no routing; single-page synthetic viewer).
- Entry backend: simulation/api/app.py (FastAPI app instance; includes routers health/garden/plants/lightfield/measurement/observation/snapshot/scenario/prediction/forecast/validation/calibration/models/clock/simulation_step).
- API base URL (derived from CORS + standard FastAPI): http://localhost:8000/api/v1 (default uvicorn port; not explicitly overridden in app.py).
- Frontend dev server: Vite port 5173 (frontend/vite.config.ts: server { port: 5173, host: true }).
- Backend dev server: uvicorn on default 8000 (no custom port defined in app.py).

## 2. Exact Startup Commands
Working directory: /home/anomaly/Projects/Adiwiyata
Terminal 1 (backend):
  python -m uvicorn simulation.api.app:app --host 0.0.0.0 --port 8000 --reload
  (or: uvicorn simulation.api.app:app --port 8000, if uvicorn installed)
Terminal 2 (frontend):
  cd frontend && npm run dev
  (uses Vite server on 5173; npm present; node_modules present per inspection)
No additional services required (no separate DB server; DuckDB when used is embedded; no external message broker).
Python environment: current session has fastapi importable; no virtualenv requirement enforced by repo (not enforced; use existing interpreter).
Node: package-lock.json present; no engine field enforcing version; current node sufficient for Vite build.

## 3. Browser URL
- Frontend: http://localhost:5173 (Vite dev server)
- Backend/API docs: http://localhost:8000/docs (FastAPI auto-docs)
- API health example: http://localhost:8000/api/v1/health

## 4. Health Check
- Backend health endpoint exists at GET /api/v1/health (simulation/api/routers/health.py; returns {"status":"ok","api_version":"v1",...}).
- Verify with: curl http://localhost:8000/api/v1/health
- Frontend running: open http://localhost:5173; expect dark page with "My Digital Twin Garden — synthetic viewer (TASK 004)" header and 3D canvas.
- API alive / frontend-backend boundary: CORS configured for 5173; API routes exposed; no proxy layer needed for local dev.

## 5. What I Should See (current UI — actual source, not planned)
From frontend/src/app/App.tsx + GardenCanvas.tsx + InspectionPanel.tsx + fixtures/gardenFixture:
- Title header (absolute, top-left, white on dark).
- Synthetic 3D garden view (GardenCanvas): uses SYNTHETIC_HIERARCHY fixture (ground, buildings, racks, containers, plants, hierarchy); not real garden data.
- LightFieldMarkers: visualizes light-field total intensity (color scale from lightfieldStore result); shows relative-normalized values, not absolute PPFD.
- ObservationMarkers: shows synthetic observations from measurementStore.
- CoordinateGizmo: spatial reference.
- InspectionPanel (top-right, conditional): shows selected object's id / type / parent_id / local/world positions when selection exists (via selectionStore).
- No plants shown from real database (no real garden loaded); synthetic hierarchy only.
- No simulation timestep controls visible (no UI button for step/run/pause; clock module exists in backend but not exposed to UI).
- No measurement ingestion UI (no form for importing observations; only synthetic markers shown).
- No snapshot/scenario selection UI in App.tsx (routes not defined; no page navigation).
- No LightField absolute-PPFD display (LightField result shown as relative markers, not absolute umol_photons_m2_s).
- No temporal slider / clock display in UI (SimulationClock domain exists; not rendered).

## 6. Scientific Engine vs Web UI — Evidence-Based Matrix
| Capability | Scientific backend exists? | API exposed? | UI exposed? | How to access |
|---|---|---|---|---|
| Architecture (domain) | Yes (development/contracts; 046AF) | Yes (/api/v1/garden, /plants, /architectures via routers) | Partial — synthetic hierarchy only; no real arch loader UI | Backend router; UI shows synthetic fixture only |
| LightField | Yes (light/field/contracts; 046M) | Yes (/api/v1/lightfield) | Yes — LightFieldMarkers render relative-normalized totals from store | Frontend Canvas |
| Absolute PPFD | Yes (physiology/ppfd_source; 046O/046V) | Yes via measurement/observation routers; not direct PPFD endpoint | Partial — markers show relative; no absolute umol_photons_m2_s display | API / fixtures |
| OrganLightExposure | Yes (contracts/domain) | Not visible as separate endpoint in router list; embedded in pipeline | No | Domain only |
| Photosynthesis | Yes (020) | Not individually routed; integrated via simulation_step / forecast | No | Domain only |
| Carbon (pool/next state) | Yes (021/046G/046Z) | Not individually routed | No | Domain only |
| Allocation (046I) | Yes | Not individually routed | No | Domain only |
| Growth (046J) | Yes | Not individually routed | No | Domain only |
| Architecture feedback (046L) | Yes | Not individually routed | Partial (synthetic delta refs not shown) | Domain only |
| SimulationClock (007) | Yes | Yes (/api/v1/clock) | No — no clock UI control | Backend router only |
| Observation sync (047-FIX) | Yes (matching.py; evaluation.py) | Yes (/api/v1/observation, /measurement, /validation) | Partial — ObservationMarkers show synthetic obs; no import form | UI markers + backend routes |
| Water (025) | Yes (water/contracts/balance) | Not individually routed in router list (no /water) | No | Domain only |
| Nutrients (026) | Yes (nutrient/contracts/balance) | Not individually routed | No | Domain only |
| Phenology (024) | Yes (development/contracts) | Not individually routed | No | Domain only |
| Forecast / prediction (030) | Yes (forecast/contracts) | Yes (/api/v1/forecast, /prediction) | No | API docs only |
| Validation (029) | Yes (validation/contracts) | Yes (/api/v1/validation) | No | API docs only |
| Calibration (028) | Yes (calibration) | Yes (/api/v1/calibration) | No | API docs only |
| Snapshot / scenario (014/015) | Yes (contracts) | Yes (/api/v1/snapshot, /scenario) | No | API docs only |

Evidence: router import list (app.py line 4); App.tsx (no route/navigation); scene components (Canvas + markers + panel) only.

## 7. Latest Scientific Pipeline Exposure (046AE / 046AF / 047-FIX / 048 / 049-FIX / 051)
Per actual router/source inspection — domain exists; UI does NOT expose these specifically; API may expose via generic routers.
- 046AE (integrated timestep): DOMAIN ONLY. Orchestrator fspm_timestep exists; not exposed via dedicated UI or named route.
- 046AF (full pipeline): DOMAIN ONLY. Same reason.
- 047-FIX (observation sync / ValidationMatch): API AVAILABLE (observation/measurement/validation routers present; matching.py used by production). UI: partial (ObservationMarkers show synthetic observations; no sync display, no match-status panel, no ValidationMatch visualization).
- 048 (calibration framework): API AVAILABLE (/calibration router exists). UI: NOT AVAILABLE (no calibration UI in App.tsx).
- 049-FIX (measurement protocol): DOMAIN ONLY (protocol fixtures, sensor registry, multi-PPFD design). No UI for protocol execution or dataset design.
- 051 (first intake): DOMAIN ONLY / SYNTHETIC PILOT complete (fixtures_051, test, PARTIAL report). No UI for ingestion form; pipeline exists in backend/validation, not rendered.

## 8. How to Run a Scientific Simulation from the Web
Not possible from current UI (App.tsx has no simulation controls: no step button, no timetable, no run/pause, no parameter panel, no snapshot selection). From backend, simulation-step router exists (/api/v1/simulation_step) and clock router (/api/v1/clock), but frontend does not call them for user interaction.
What IS possible from UI (actual): open browser → see synthetic 3D view with light-field markers and synthetic observation markers; click/select an object to see id/type/position in InspectionPanel. No model output inspection from browser.

## 9. How to View the 3D Digital Twin
Current actual steps (based on App.tsx / GardenCanvas.tsx / fixtures):
1. Start backend (terminal 1) and frontend (terminal 2).
2. Open http://localhost:5173.
3. Observe dark background with title; 3D canvas loads synthetic hierarchy (ground/buildings/racks/containers/plants) from SYNTHETIC_HIERARCHY fixture.
4. LightFieldMarkers render (colored dots/markers based on relative-normalized intensity from lightfieldStore).
5. ObservationMarkers render synthetic observations.
6. Click/select an object in canvas → InspectionPanel (top-right) shows selected id/type/parent/local/world.
7. No time control; no plant hierarchy drill-down; no measurement table; no snapshot picker.

## 10. End-to-End Safe Read-Only Procedure
1. Backend start: python -m uvicorn simulation.api.app:app --port 8000 (working dir /home/anomaly/Projects/Adiwiyata).
2. Frontend start: cd frontend && npm run dev (port 5173).
3. Open http://localhost:5173.
4. See synthetic garden with markers.
5. Click a marker/object → InspectionPanel shows identity/position.
6. Backend check: curl http://localhost:8000/api/v1/health (read-only, safe).
7. API check (read-only): curl http://localhost:8000/api/v1/garden or /observations (if available; check docs at /docs).
8. No state mutated; no calibration triggered; no model updated; raw fixtures unchanged.

## 11. Seed / Demo Data
- Synthetic fixture: frontend/src/fixtures/gardenFixture.ts (SYNTHETIC_HIERARCHY); used by GardenCanvas when no real garden prop provided.
- No real garden seed file in data/; empty observations/measurements directories.
- First real session requires external dataset per TASK 051 (data/observations, calibrated PPFD, architecture, environment, sensor registry, multi-PPFD).

## 12. Dependency Status (verified, not fixed)
- frontend/node_modules: present (partial inspection; "agent-base" shown; full Vite build likely works given package-lock.json).
- Python environment: fastapi importable; no missing import errors for core domain (observed in prior session runs).
- No missing package.json install needed unless fresh clone (package-lock.json present; npm install safe if needed — suggested, not executed).
- No database server required (DuckDB embedded; not running externally).
- Port 5173 / 8000: assume available; if occupied, change vite.config.ts / uvicorn port explicitly (not done).

## 13. Known Startup Issues (configuration-derived, verified)
- If backend not started: frontend CORS allowed but API calls will fail silently (UI shows synthetic markers, not server data); health check fails.
- Wrong Python environment: fastapi/import errors if interpreter lacks installed packages (current session has them; unknown for fresh shell).
- Frontend on wrong port: vite.config.ts locked to 5173; if occupied, server fails.
- No .env or backend URL env configured for frontend (CORS hard-coded in app.py; frontend doesn't proxy, so same-machine works).
- Backend docs at /docs require backend running; if not, 404.
- No error handling UI for backend failure (App.tsx has no error boundary / loading state for API).

## 14. Read-Only Safety Confirmed
- No source file edited in this audit.
- No dependency installed / updated.
- No configuration modified.
- No database/state altered.
- No scientific module changed.
- No new API routes / UI components added.

## 15. Required Report (this file)
Sections 1–14 cover architecture, commands, URL, health, UI contents, scientific matrix, pipeline exposure, workflow, viewing, end-to-end, seed data, dependencies, failure modes, read-only confirmation.

## 16. Source Evidence (exact files)
- Repository root: /home/anomaly/Projects/Adiwiyata
- architecture: frontend/package.json; frontend/vite.config.ts; frontend/src/app/App.tsx; simulation/api/app.py
- UI contents: frontend/src/app/App.tsx; frontend/src/scene/GardenCanvas.tsx; frontend/src/scene/InspectionPanel.tsx; frontend/src/fixtures/gardenFixture.ts
- backend routes: simulation/api/app.py; simulation/api/routers/*.py (list verified)
- scientific modules (referenced, not changed): simulation/core/light/field/contracts.py; simulation/core/development/contracts.py; simulation/core/water/contracts.py; simulation/core/nutrient/contracts.py; simulation/core/validation/matching.py; simulation/core/validation/evaluation.py; simulation/core/orchestration/fspm_timestep.py
- fixtures / data: fixtures_049/protocol_049; fixtures_047; fixtures_050/051; data/observations; data/measurements
- reports: TASK_046AF_COMPLETE.md; TASK_049_COMPLETE.md; TASK_050_PARTIAL.md; TASK_050R_RESEARCH.md; TASK_051_PARTIAL.md (all preserved unedited)

## HOW TO RUN IT NOW
1. Terminal 1 (backend): python -m uvicorn simulation.api.app:app --host 0.0.0.0 --port 8000 --reload
2. Terminal 2 (frontend): cd frontend && npm run dev
3. Open browser: http://localhost:5173
4. See: dark synthetic garden viewer with LightField markers + synthetic observation markers + selectable objects (InspectionPanel shows id/type/position)
5. Verify backend: curl http://localhost:8000/api/v1/health (expect ok)
6. Verify API docs (optional, read-only): http://localhost:8000/docs

## WHAT IS CURRENTLY VISIBLE FROM BROWSER
- Synthetic 3D garden scene (fixture-based, not real garden).
- LightField relative-normalized markers (not absolute PPFD).
- Synthetic observation markers (from fixtures; not real measurements).
- Selection inspector (id/type/parent/local/world).
- Title + dark theme.
- No simulation control UI; no measurement ingestion UI; no snapshot/scenario picker; no architecture comparison panel; no clock display; no real-data display.

## WHAT IS BACKEND-ONLY (not exposed in current UI)
- Full FSPM pipeline (046AE / 046AF): light/PPFD/photosynthesis/carbon/allocation/growth/architecture (domain only).
- Observation synchronization (047-FIX): match_measurement_to_lightfield + ValidationMatch (API available; UI partial — markers only, no match-status display).
- Calibration framework (048): /calibration router; no UI.
- Forecast / prediction (030): /forecast / /prediction routers; no UI.
- Validation (029): /validation router; no UI.
- Snapshot / scenario (014/015): routers; no UI.
- Clock (007): /clock router; no UI.
- Water / nutrient / phenology modules (025/026/024): domain only; no dedicated API routes or UI.
- Real observation intake (051): pipeline executed in domain/fixtures/test; no ingestion form UI.
- Multi-PPFD measurement design (049-FIX): fixtures/protocol only; not rendered.

Co-Authored-By: Claude Code <noreply@anthropic.com>
