# CLAUDE.md — My Digital Twin Garden

## Role
You are the primary software engineering agent for My Digital Twin Garden, a local-first, scientifically grounded spatial-temporal digital twin of a real garden with a Functional-Structural Plant Model (FSPM).

This is NOT a game and NOT merely a 3D garden visualizer.

Read `CLAUDE_MASTER_SPEC.md` before major architectural or scientific decisions.

## Source of Truth
1. `CLAUDE.md` — operational rules.
2. `CLAUDE_MASTER_SPEC.md` / `docs/SPEC.md` — detailed specification.
3. Domain-level `CLAUDE.md` files — local rules.
4. Source code + tests — current implementation.

Do not silently change scientific assumptions.

## Stack
Frontend:
- React
- TypeScript
- Vite
- React Three Fiber
- Three.js
- Drei
- Zustand

Scientific core:
- Python
- NumPy
- SciPy
- Pydantic/dataclasses as appropriate

API:
- FastAPI

Data:
- Human-readable project files
- DuckDB when analytical storage is useful

Testing:
- pytest
- Vitest
- Playwright later if needed

### Hard boundary
R3F/Three.js is visualization only.

Do NOT put plant growth, photosynthesis, carbon allocation, water/nutrient physiology, or FSPM scheduling inside React components or render loops.

## Scientific Principles
Target:
- high realism: garden geometry, solar/shadow, light distribution, plant architecture, photosynthesis/carbon;
- medium-high: water;
- medium: nutrients and roots;
- low/not-core: molecular/hormonal/genetic detail.

Target statement:
"Physiologically meaningful, architecturally explicit, environmentally coupled, experimentally calibratable."

Core feedback:
environment → light interception → photosynthesis → carbon → allocation → organ growth → new structure → new light interception.

Complexity must have:
1. clear predictive value;
2. parameter observability/identifiability;
3. feasible calibration;
4. available validation data.

## References
MetaFSPM, CPlantBox, and GreenLab are references only unless explicitly promoted to runtime dependencies.

Use them to inform:
- FSPM architecture/coupling;
- plant/root structure;
- source-sink modeling;
- calibration;
- stochasticity;
- experiment design.

Do not add them as dependencies just because they appear in the specification.

## Data Separation
Keep these distinct:
- Configuration = model/variety parameters.
- State = current simulated condition.
- Measurement = instrument-derived numeric data.
- Observation = human/qualitative observation.
- Prediction = simulation output.
- Scenario = experiment definition.
- SimulationRun = execution from a specific snapshot.

## Scientific Data Rules
Every scientific quantity must have an explicit unit.
Parameters should record provenance:
- source;
- method;
- version/date;
- uncertainty where available.

Never fabricate scientific values. Unknown values must be explicit placeholders or missing-data errors.

Do not silently retune parameters to make validation pass.
Do not use validation data as calibration data.
Do not equate lux directly with photosynthesis.

## Simulation Rules
Separate:
- observation/world time;
- simulation time;
- plant age/development time.

Use hybrid timesteps. Never bind scientific simulation to the R3F render loop.

Correct pattern:
simulation clock → scheduler → scientific model updates → domain state → frontend rendering.

Support:
- step;
- run;
- pause;
- fast-forward;
- checkpoint;
- replay;
- prediction branching.

Prediction must start from a snapshot and must not mutate the original Garden state.

## Spatial Rules
Use a local garden coordinate system with stable physical reference point `G0`.

Default:
- +X = East
- +Y = North
- +Z = Up

Distinguish magnetic bearing from true bearing.

Spatial hierarchy may be:
Garden → Rack → Tier → Container → Plant

Local child transforms may be stored; world transforms are derived.

Domain geometry must remain independent of Three.js meshes.

## Plant Rules
Keep separate:
- Plant identity;
- PlantState;
- PlantArchitecture.

PlantArchitecture contains topology, organs and geometry.

L-System is a morphogenesis/procedural mechanism, not the complete biological model.

Not every species must use the same structural representation.

## Model Contract
Every scientific model should define:
- purpose;
- inputs;
- parameters;
- state variables;
- outputs;
- units;
- valid ranges;
- timestep;
- dependencies;
- validation strategy.

Conceptual interface:
ModelContract
- inputs
- parameters
- state
- process/rate
- outputs
- timestep
- update()

## Validation
Validation hierarchy:
1. geometry
2. solar position
3. shadow
4. light
5. physiology
6. plant growth
7. plant architecture
8. integrated garden behavior

Use objective comparisons where appropriate:
- MAE/RMSE;
- relative error;
- timing error;
- spatial pattern agreement;
- morphology;
- stage prediction;
- uncertainty.

Visual plausibility is not scientific validation.

## MVP Priority
First prove:
1. garden geometry;
2. L-shaped boundary;
3. rack/tier/container hierarchy;
4. plant placement;
5. solar position;
6. direct shadow;
7. diffuse/reflected approximation;
8. LightField;
9. measurement ingestion;
10. light validation;
11. snapshots/checkpoints;
12. scenarios;
13. current-state prediction.

Do not begin full physiology before the early foundation is stable.

## Initial Task Sequence
TASK 001 — repository/tooling bootstrap
TASK 002 — domain/data contracts
TASK 003 — garden spatial model + G0
TASK 004 — R3F garden viewer
TASK 005 — building/fence/tree/rack/container hierarchy
TASK 006 — plant identity/state scaffolding
TASK 007 — simulation clock/scheduler
TASK 008 — solar position
TASK 009 — direct shadow
TASK 010 — diffuse/reflected light approximation
TASK 011 — LightField
TASK 012 — measurement/observation ingestion
TASK 013 — light validation
TASK 014 — snapshot/checkpoint
TASK 015 — scenario system
TASK 016 — prediction branching
TASK 017+ — plant architecture and physiology

Do not jump ahead without a clear reason.

## AI-Agent Rules
Before modifying:
1. Read relevant docs.
2. Inspect existing code/tests.
3. Identify smallest affected scope.
4. Give a short implementation plan for non-trivial tasks.
5. Preserve contracts unless the task explicitly changes them.

During:
- make small focused changes;
- avoid unrelated edits;
- prefer explicit typed code;
- isolate randomness;
- add/update tests;
- preserve units/provenance;
- keep frontend/scientific boundaries clean.

After:
- run relevant tests and type checks;
- report failures honestly;
- update contracts/docs when public behavior changes.

## Task Format
For non-trivial tasks use:
### Goal
### Scope
### Contract
### Acceptance Criteria
### Tests
### Scientific Notes
### Deliverables

If scientific requirements are ambiguous, ask a focused clarification instead of inventing assumptions.

## Definition of Done
A feature is done when:
- contract exists;
- implementation exists;
- tests pass;
- units are explicit;
- assumptions are documented;
- parameter sources are documented;
- stochastic behavior is reproducible when applicable;
- validation path exists;
- frontend consumes domain output without owning scientific logic;
- no unrelated changes are included.

## Current Status
Foundation v0.1 is conceptually locked.

Decisions:
- R3F = visualization/interaction
- Python = scientific simulation core
- FastAPI = API boundary
- human-readable project data + DuckDB = data layer
- MetaFSPM = architecture/coupling reference
- CPlantBox = plant/root FSPM reference only
- GreenLab = source-sink/calibration/stochasticity reference
- FSPM = realistic target, implemented incrementally
- Garden state can be snapshotted and branched for prediction
- calibration, validation, uncertainty and reproducibility are first-class concerns

Next implementation phase: TASK 001.
