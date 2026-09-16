# My Digital Twin Garden — Claude Code Master Specification
Version: 0.1
Status: FOUNDATION LOCKED / IMPLEMENTATION SPECIFICATION
Target OS: Debian Linux
Primary development workflow: Claude Code / AI-agent driven
Primary user interface: React + React Three Fiber
Scientific simulation core: Python

## 0. Mission

Build a local-first, scientifically grounded spatial-temporal digital twin of a real garden.

The system SHALL:
1. represent the real garden geometry and objects;
2. model solar position, direct/diffuse/reflected light and shadow;
3. represent plants as functional-structural biological systems rather than static meshes;
4. support plant species/cultivar-specific parameter sets;
5. simulate water and nutrient constraints at a useful level;
6. run hybrid-timestep simulations;
7. support current-state forecasting and what-if scenarios;
8. ingest real-world measurements;
9. support calibration, validation, uncertainty and reproducibility;
10. render the current/predicted state interactively in React Three Fiber.

Important: this project is a scientific simulation with a 3D interface, NOT a game. Visual realism must never be used as evidence of scientific validity.

## 1. Non-Negotiable Engineering Principles

1. Domain/scientific logic MUST be independent from React, R3F and Three.js.
2. Rendering MUST be an output of domain state, never the source of biological truth.
3. Simulation state, model parameters, observations and predictions MUST remain separate.
4. Every scientifically meaningful quantity MUST have an explicit unit.
5. Every empirical/model parameter SHOULD have provenance: source, method, date/version, uncertainty when available.
6. Calibration data MUST NOT automatically become validation data.
7. Simulation runs MUST be reproducible through versioned parameters, model version and random seed when stochasticity is enabled.
8. Complex biology SHALL only be implemented when it has a clear predictive purpose and can be parameterized/validated.
9. Do not add dependencies merely because a research project uses them.
10. Prefer small, testable modules with explicit contracts.
11. Do not silently change scientific assumptions while refactoring.
12. AI agents MUST inspect existing code and relevant contracts before modifying files.
13. AI agents MUST avoid unrelated changes.
14. Every new model module MUST have tests and a short scientific contract.
15. Failed validation MUST be surfaced; never hide it by silently retuning parameters.

## 2. Scientific Scope

### 2.1 Core realism target

The intended model is:
- high realism: garden geometry;
- high realism: solar position and shadow;
- high realism: light distribution;
- high realism: plant architecture;
- high realism: photosynthesis/carbon processes;
- medium-high: water;
- medium: nutrients;
- medium: roots;
- low/not-core: molecular/hormonal/genetic mechanisms.

Target statement:

"Physiologically meaningful, architecturally explicit, environmentally coupled, experimentally calibratable."

### 2.2 Core feedback loop

Environment
-> light interception
-> photosynthesis
-> carbon production
-> carbon allocation
-> organ growth
-> new structure
-> new light interception
-> repeat

Water, temperature and nutrients modulate the functional processes.

### 2.3 Scientific references

The implementation should learn from, but not depend on:
- OpenAlea MetaFSPM: modular FSPM concepts, inputs/state variables/parameters, component coupling and timesteps.
- CPlantBox: plant/root architecture and plant-soil FSPM implementation patterns; reference only.
- GreenLab: source-sink allocation, phytomer-level modeling, parameter estimation, stochasticity and experiment/calibration methodology.
- Peer-reviewed plant physiology/FSPM literature for equations and parameters.

Do NOT add CPlantBox or MetaFSPM as mandatory runtime dependencies unless a separate decision explicitly authorizes it.

## 3. High-Level System Architecture

Browser/UI:
React + TypeScript
React Three Fiber + Three.js + Drei
Zustand for UI state

API:
FastAPI

Scientific simulation:
Python
NumPy
SciPy
Pydantic/dataclasses as appropriate

Data:
Project files (human-readable)
DuckDB for analytical observations/results when useful

Testing:
pytest for Python
Vitest for frontend
Playwright may be introduced later for end-to-end tests

Architecture:

Frontend
  <-> API contract
  <-> Simulation orchestration/domain
      - environment
      - FSPM
      - soil/water/nutrient
      - scenario
      - calibration/validation
  <-> data layer

R3F MUST NOT calculate scientific plant growth.

## 4. Repository Structure

Recommended initial repository:

digital-twin-garden/
├── CLAUDE.md
├── README.md
├── pyproject.toml
├── package.json
├── docs/
│   ├── FOUNDATION.md
│   ├── ARCHITECTURE.md
│   ├── MODEL_CONTRACTS.md
│   ├── VALIDATION.md
│   └── DEVELOPMENT.md
├── frontend/
│   ├── CLAUDE.md
│   └── src/
│       ├── app/
│       ├── scene/
│       ├── garden/
│       ├── plants/
│       ├── simulation-ui/
│       ├── state/
│       └── contracts/
├── api/
│   ├── CLAUDE.md
│   └── src/
├── simulation/
│   ├── CLAUDE.md
│   ├── core/
│   │   ├── engine/
│   │   ├── clock/
│   │   └── scheduler/
│   ├── environment/
│   │   ├── solar/
│   │   ├── light/
│   │   ├── weather/
│   │   └── water/
│   ├── plants/
│   │   ├── fspm/
│   │   ├── physiology/
│   │   ├── architecture/
│   │   ├── phenology/
│   │   ├── roots/
│   │   └── varieties/
│   ├── soil/
│   │   └── nutrients/
│   ├── scenarios/
│   ├── calibration/
│   └── validation/
├── data/
│   ├── garden/
│   ├── varieties/
│   ├── measurements/
│   ├── observations/
│   └── scenarios/
├── tests/
│   ├── simulation/
│   ├── api/
│   └── frontend/
└── scripts/

Folder-level CLAUDE.md files SHOULD define local responsibilities, allowed modifications, contracts and test commands.

## 5. World Model

### 5.1 Garden

Garden contains:
- location
- orientation
- coordinate system
- L-shaped boundary polygon
- terrain
- spatial objects
- containers
- plants
- events
- observations

### 5.2 Coordinate system

Use a local garden coordinate system with a physical reference point G0.

G0:
- is a stable physical benchmark;
- defines local origin;
- MUST NOT be assumed to be a GPS coordinate;
- SHALL be linked to global location/orientation metadata.

Recommended local axes:
- +X = East
- +Y = North
- +Z = Up

True-north orientation MUST be distinguished from magnetic compass readings. If magnetic measurements are used, record the raw magnetic bearing and the conversion method/declination source separately.

### 5.3 Spatial hierarchy

Objects MAY have parent-child transforms.

Example:
Garden
  -> Rack
     -> Tier
        -> Container
           -> Plant

A child local transform MUST be distinguishable from its world transform.

### 5.4 Spatial objects

Core object types:
- Boundary
- Terrain
- Building
- Fence/Wall
- Tree/Obstacle
- Rack
- Tier
- Container
- Plant

Geometry is a domain concept. It MUST NOT be represented as Three.js meshes inside the scientific core.

## 6. Container Model

Containers are first-class entities because the garden uses:
- polybags
- pots
- seedling trays

Container properties MAY include:
- type
- geometry
- material
- color
- volume
- growing-medium properties
- position/orientation
- parent
- drainage properties

Seedling trays MUST support cells:
Tray
  -> Cell
     -> Plant

Plants retain identity when transplanted. Transplanting changes the container relationship and records an event; it does not create a new plant identity.

## 7. Plant Identity vs Plant State vs Plant Architecture

These MUST be separated.

### Plant
Identity:
- plant_id
- species_id
- variety_id
- current_container_id
- lifecycle metadata

### PlantState
Time-varying biological condition:
- timestamp
- age
- developmental/phenological stage
- biomass
- carbon pool
- water status
- nutrient status
- stress state
- functional outputs

### PlantArchitecture
Structural representation:
- topology/graph
- organs
- geometry
- organ states

Architecture is NOT a render mesh.

## 8. Plant Structural Model

The plant architecture model SHOULD support:
- axis/stem hierarchy
- phytomer-like modular structures where appropriate
- internodes
- leaves
- buds
- flowers/fruits when applicable
- roots
- topology
- geometry

Not every species must use the same structural representation.

L-System is a morphogenesis/procedural-rule mechanism, not the complete plant simulator.

Pipeline:
Species/developmental rules
-> morphogenesis
-> topology changes
-> geometry update
-> renderer

## 9. FSPM Functional Model

Core modules:
- light interception
- photosynthesis
- respiration
- carbon pool
- source-sink allocation
- organ growth
- phenology
- water status
- root uptake
- nutrient uptake

Each module MUST explicitly define:
- purpose
- inputs
- parameters
- state variables
- outputs
- units
- valid domain/ranges
- timestep
- dependencies
- validation strategy

Recommended conceptual module interface:

ModelContract:
  inputs
  parameters
  state
  process/rate
  outputs
  timestep
  update()

## 10. Light Model

Light model MUST support:
- solar position
- direct sunlight
- obstruction/shadow
- diffuse sky light
- reflected light approximation
- spatial light distribution
- plant/organ light exposure

Solar inputs:
- latitude
- longitude
- elevation where relevant
- date
- time
- timezone
- orientation/reference

Light chain:

solar position
-> direct ray/exposure
-> obstruction
+
diffuse sky
+
reflected approximation
-> local light field
-> plant/organ exposure

Lux is a real-world observation and calibration variable.

Do NOT equate lux directly with photosynthesis.

Where possible:
measured lux
-> light calibration/estimation
-> plant-relevant photon/light quantity
-> physiological model

For daylight, lux-to-PPFD conversion MAY be used as an approximation with documented assumptions. It MUST NOT be presented as a direct measurement unless a quantum/PAR sensor was actually used.

## 11. Light Spatial Resolution

Visual geometry can be high resolution.

Biological simulation SHOULD use process-appropriate resolution:
- world: object/obstacle scale
- plant: organ scale
- light: leaf or leaf-cluster/organ scale
- physiology: organ -> plant aggregation

Do not calculate biological processes on every render triangle.

## 12. Water Model

Water model SHOULD cover:
- rain
- irrigation
- growing-medium storage
- drainage
- root-zone available water
- root uptake
- plant water status
- water-stress effects

Water content and plant-available water are distinct.

Container type and medium properties MUST influence water dynamics.

Measurements may include:
- soil/media moisture
- irrigation volume/time
- drainage observations

Time series are preferred over one-off measurements when feasible.

## 13. Nutrient Model

Core nutrients:
- N
- P
- K

Potential extension:
- Ca
- Mg
- micronutrients

Core flow:
medium nutrient content
-> available nutrient
-> root uptake
-> plant nutrient status
-> physiological/growth response

Avoid implementing detailed soil chemistry until there is a clear experimental reason and data support.

pH MAY be included as an environmental variable affecting nutrient availability.

## 14. Root Model

Root system is part of the core model.

Core target:
- root architecture
- root depth/spread
- root-zone interaction with container/soil volume
- water uptake
- nutrient uptake

Advanced hydraulic networks are future extensions.

## 15. Phenology

Phenology MUST be separate from chronological age.

Potential stages:
- germination
- seedling
- vegetative
- flowering
- fruiting
- senescence

Drivers MAY include:
- thermal time/temperature
- photoperiod where species-relevant
- genotype/variety parameters
- environmental stress

Stage definitions MUST be observable/calibratable whenever possible.

## 16. Variety Profile

Variety is a parameter set, not a single growth-rate number.

VarietyProfile SHOULD support:
- identity
- morphology parameters
- photosynthesis parameters
- phenology parameters
- allocation/source-sink parameters
- root parameters
- stress response parameters
- parameter provenance

Each parameter SHOULD contain:
- parameter name
- value
- unit
- source
- method
- uncertainty
- valid range
- version

Sources may be:
- literature
- experiment
- fitted/inferred
- expert assumption

Never represent inferred values as measured values.

## 17. Source-Sink / Carbon

Functional flow:

light
-> photosynthesis
-> assimilate/carbon production
-> respiration/maintenance
-> available carbon
-> source-sink allocation
-> organ growth
-> architecture

Allocation MUST be organ-aware at the chosen model resolution.

The implementation MUST make assumptions about allocation explicit and testable.

## 18. Stochasticity

Biological variability SHOULD be supported.

Use a deterministic mode for debugging and a stochastic mode for biological variation.

Every stochastic simulation MUST record:
- random seed
- stochastic model version
- parameter set version

Randomness MUST be constrained by biological distributions/ranges; avoid arbitrary visual noise.

## 19. Environment vs Observation vs Prediction

These MUST remain distinct.

### EnvironmentState
Modelled or scenario environment at a simulation time.

### Measurement
Instrument-derived numeric measurement:
- timestamp
- variable
- value
- unit
- location
- instrument
- method
- uncertainty

### Observation
Human/qualitative observation:
- timestamp
- subject/location
- category
- description
- optional structured fields
- observer

### Prediction
Output of a simulation run.

Predictions MUST never silently overwrite observations.

## 20. Human Intervention Events

Human action is part of the digital twin.

Event examples:
- watering
- fertilization
- transplanting
- pruning
- repotting
- harvesting

Event:
- event_id
- timestamp
- type
- target
- parameters
- source/user

Interventions modify a simulation branch or actual recorded history according to context. Do not erase history.

## 21. Time Model and Hybrid Scheduler

Three concepts:
1. real/observation time
2. simulation time
3. plant age/developmental time

Environmental processes and biological processes MAY use different timesteps.

Initial configuration targets are adjustable, not hard-coded scientific truths:
- solar: minutes
- light: several minutes
- water/environment: tens of minutes to hours
- plant physiology/growth: hours to days
- structural events: event-driven and/or daily

The scheduler MUST allow:
- step
- run
- pause
- fast-forward
- replay
- checkpoint

Do not bind scientific timestep to rendering FPS.

## 22. Simulation State

SimulationState includes:
- simulation_time
- environment state
- soil/water state
- plant states
- plant architectures
- pending events
- scheduler state

SimulationRun includes:
- run_id
- source_state_id
- scenario_id
- model_version
- parameter_set_version
- random_seed
- forecast horizon
- assumptions
- checkpoints
- outputs
- uncertainty metadata

## 23. Prediction

Prediction is a simulation branch from a snapshot.

Current garden state
-> snapshot
-> scenario/assumptions
-> simulation
-> prediction

Prediction MUST NOT mutate the original garden state.

Prediction should record:
- forecast horizon
- assumptions
- scenario
- model version
- parameter set version
- initial snapshot
- random seed
- uncertainty

Predictions should be comparable with later real observations.

## 24. Scenario System

Scenario describes what is being tested.

Scenario includes:
- base state
- start/end time
- interventions
- environment assumptions
- parameter overrides (if explicitly allowed)
- random seed

Example scenarios:
- normal watering
- reduced watering
- pruning
- rack moved
- different light condition

Scenario MUST be reproducible.

SimulationRun is an execution of a Scenario.

## 25. Checkpointing and Replay

Checkpoints SHOULD capture:
- simulation time
- relevant plant state
- architecture
- environment
- soil/water state
- model version
- parameter set version
- random seed

Historical replay and predictive forecast use the same underlying simulation engine but different inputs/purposes.

## 26. Calibration and Validation

Verification:
"Did code implement the model correctly?"

Calibration:
"Which parameter values fit calibration observations?"

Validation:
"How well does the calibrated model predict independent observations?"

Calibration and validation datasets MUST be separable.

Validation should progress from:
1. geometry
2. solar position
3. shadow
4. light
5. physiology
6. plant growth
7. plant architecture
8. integrated garden behavior

Possible metrics:
- absolute error
- relative error
- RMSE/MAE where appropriate
- timing error
- spatial pattern agreement
- stage prediction error
- organ-level morphology error

Never declare a model valid solely because it looks visually plausible.

## 27. Identifiability and Observability

Before adding a parameter, ask:
1. What prediction does it improve?
2. Can it be measured directly?
3. If not, can it be inferred from observable data?
4. Can the parameter be uniquely identified from available experiments?
5. What validation observation will test it?

Avoid over-parameterization.

## 28. Uncertainty

Sources:
- measurement uncertainty
- parameter uncertainty
- initial-state uncertainty
- model-form uncertainty
- stochastic variability
- future environment uncertainty

Longer prediction horizons SHOULD generally expose increasing uncertainty unless a model/observation structure justifies otherwise.

Avoid false precision.

## 29. Experiment Design

The project SHOULD eventually support controlled experiments for parameter estimation.

A good experiment:
- changes a known condition;
- records initial state;
- records time series;
- records observable outputs;
- preserves an independent validation set.

Examples:
- light comparison
- watering treatment
- substrate/container comparison
- cultivar comparison

Do not collect measurements without a clear model/validation question.

## 30. Model Registry

Create a registry that identifies:
- model name
- model version
- component versions
- equations/document version
- dependency versions
- parameter set version

Every SimulationRun MUST be traceable to a registry record.

## 31. API Boundary

Frontend receives/returns domain DTOs.

Example:
GardenDTO
PlantDTO
PlantStateDTO
PlantArchitectureDTO
EnvironmentStateDTO
LightFieldDTO
MeasurementDTO
ScenarioDTO
SimulationRunDTO
PredictionDTO

The API is a transport boundary, not the scientific source of truth.

## 32. Frontend Concepts

Main application modes:

1. World
   - edit/view garden geometry

2. Plant
   - inspect species/variety/container/state

3. Simulation
   - timeline
   - play/pause
   - step
   - speed
   - date/time

4. Analysis
   - shadow
   - light
   - lux/estimated PPFD/DLI
   - water
   - growth

5. Validation
   - measured vs predicted
   - error plots
   - observation comparison

Main UI:
- 3D viewport
- left world/object panel
- right inspector
- bottom timeline
- analysis overlays

## 33. Rendering Rules

R3F:
- visualizes domain state;
- does not own scientific state;
- does not calculate biological equations;
- does not run FSPM every frame.

Simulation engine:
- runs on simulation time;
- produces domain states;
- frontend renders the current selected/checkpoint state.

## 34. Performance Rules

Do not:
- run Python FSPM on render frames;
- create one expensive Three.js mesh per tiny organ when instancing is appropriate;
- recalculate unchanged environment state unnecessarily;
- send enormous state payloads every frame.

Use:
- simulation checkpoints
- cached/static geometry
- memoized derived data
- instancing where appropriate
- incremental updates
- batched API results

Optimization must not alter scientific semantics.

## 35. MVP Acceptance Criteria

MVP-1 must prove:

A. World:
- real garden geometry can be represented;
- L-shaped boundary works;
- rack/tier/container hierarchy works;
- plant positions are persistent.

B. Sun/light:
- date/time/location produce sun position;
- direct shadow changes with time;
- diffuse/reflected approximations exist;
- light can be sampled at measurement points.

C. Measurement:
- lux measurements can be stored;
- observations can be stored;
- measured vs modelled light can be compared.

D. Simulation:
- current state can be snapshotted;
- simulation can step/run/pause/fast-forward;
- simulation run is reproducible.

E. Prediction:
- a 30-day forecast can branch from the current garden state;
- original garden state remains unchanged;
- scenario can be compared.

MVP-1 does NOT require full photosynthesis/carbon/root/nutrient physiology.

## 36. AI-Agent Development Rules

Claude MUST:
1. Read root CLAUDE.md.
2. Read the nearest relevant directory CLAUDE.md before modifying that domain.
3. Inspect existing files/tests before coding.
4. State a short implementation plan before non-trivial changes.
5. Work within the requested scope.
6. Add/update tests for behavior changes.
7. Run relevant tests/type checks.
8. Report remaining failures honestly.
9. Update contracts/docs if a public interface changes.
10. Never invent scientific parameter values without marking them as assumptions/placeholders.
11. Prefer a TODO/explicit missing-data error over fabricated scientific data.
12. Never silently use validation data for calibration.
13. Never change model equations during a refactor unless requested.
14. Preserve units and parameter provenance.
15. Ask for clarification if a scientific requirement is ambiguous.

Claude SHOULD:
- favor simple, explicit code;
- use typed interfaces;
- keep scientific functions deterministic when possible;
- isolate randomness;
- use small functions/classes;
- create focused tests;
- avoid premature abstractions.

## 37. Claude Task Format

Every implementation task SHOULD be specified as:

# TASK <id>: <title>

## Context
Why this exists.

## Goal
Exact outcome.

## In Scope
Allowed files/modules.

## Out of Scope
Things that must not be changed.

## Contract
Inputs, outputs, units and behavior.

## Acceptance Criteria
Observable pass/fail conditions.

## Tests
Required tests.

## Scientific Notes
Equations/assumptions/references.

## Validation
How the result will be checked.

## Deliverables
Files/results expected.

## 38. Initial Development Order

TASK 001
Repository + tooling + CLAUDE instructions

TASK 002
Core domain contracts

TASK 003
Garden spatial model + G0/local coordinates

TASK 004
R3F garden viewer

TASK 005
Building/fence/tree/rack/container hierarchy

TASK 006
Plant identity + plant state scaffolding

TASK 007
Simulation clock/scheduler

TASK 008
Solar position model

TASK 009
Direct shadow model

TASK 010
Diffuse/reflected light approximation

TASK 011
LightField model

TASK 012
Measurement/observation ingestion

TASK 013
Light validation tools

TASK 014
Simulation snapshot/checkpoint system

TASK 015
Scenario system

TASK 016
Prediction branching

TASK 017
Plant architecture abstraction

TASK 018
Procedural/L-System morphogenesis prototype

TASK 019
Physiology contracts

TASK 020
Photosynthesis model

TASK 021
Carbon/respiration

TASK 022
Source-sink allocation

TASK 023
Organ growth

TASK 024
Phenology

TASK 025
Water/root model

TASK 026
Nutrient model

TASK 027
Stochastic individual variation

TASK 028
Calibration/parameter fitting

TASK 029
Validation suite

TASK 030
Advanced forecasting and model comparison

Do NOT jump to TASK 020+ before TASK 001-014 are stable.

## 39. Scientific Data Policy

Never hard-code a literature value into a model without:
- parameter name
- unit
- source
- citation/DOI when available
- scope/species applicability
- uncertainty or limitation when known

If data is unavailable:
- mark it as missing;
- provide an explicit placeholder;
- do not fabricate values.

## 40. Testing Pyramid

Unit tests:
- equations
- coordinate transforms
- solar calculations
- light calculations
- state transitions

Integration tests:
- light -> photosynthesis
- water -> root uptake -> plant status
- architecture -> light exposure
- scheduler -> model execution

End-to-end:
- load garden
- select plant
- change time
- run simulation
- view prediction
- compare observation

Scientific regression tests:
- fixed input fixture
- fixed expected output range
- fixed model version
- fixed random seed where applicable

## 41. Definition of Done

A feature is NOT done when it "looks right".

A feature is done when:
- contract exists;
- implementation exists;
- tests pass;
- units are explicit;
- parameter sources are documented;
- behavior is reproducible if stochastic;
- scientific assumptions are documented;
- validation path exists;
- frontend uses the domain output without owning scientific logic.

## 42. Agent Safety / Scope Boundary

Claude MUST NOT:
- rewrite architecture globally without authorization;
- add unrelated frameworks;
- add remote services without approval;
- add cloud dependencies to a local-first feature;
- introduce a second state-management system unnecessarily;
- fork a research model/library into the project without explicit approval;
- use CPlantBox/MetaFSPM as runtime dependencies just because they are referenced in docs;
- change the scientific scope silently.

CPlantBox, MetaFSPM and GreenLab are references unless a separate implementation decision explicitly promotes a component to dependency.

## 43. Final Project Mental Model

Real garden
-> measurements + observations
-> digital world state
-> environment model
-> FSPM
-> simulation
-> prediction
-> real-world observation
-> validation/calibration
-> improved model

3D rendering is the interface to that model, not the model itself.
