# Model Contracts — TASK 002

Status: contracts defined; no physics or 3D generation yet.

## Principles (from master spec / CLAUDE.md)
- Plant identity != PlantState != PlantArchitecture
- Configuration != State != Measurement != Observation != Prediction
- Scenario != SimulationRun
- World geometry != Three.js render geometry
- Every scientific quantity has explicit unit when value known; missing = unknown, not zero.
- References (MetaFSPM / CPlantBox / GreenLab) inform architecture; not dependencies.

## Contract files
- Python source of truth: `simulation/core/contracts/domain.py` (Pydantic)
- Frontend consumption: `frontend/src/contracts/domain.ts` (types)
- API should use Python domain objects; DTOs only where distinct from scientific schema.

## Key contracts
- Garden / GardenReference (G0, +X East, +Y North, +Z Up) / Boundary (ordered polygon; L-shape allowed) / SpatialTransform (local + parent)
- Spatial hierarchy: Garden -> Rack -> RackTier -> Container / ContainerCell -> Plant
- Container (polybag/pot/seedling_tray/ground/other) with dimensions/volume/material/color/growing-medium/drainage
- Plant (identity) with species/variety/container reference
- PlantState (timestamp, age, stage, biomass, carbon, water, nutrient, stress) — separate from identity
- PlantArchitecture (topology, organs, geometry metadata) — no Three.js classes
- VarietyProfile / VarietyParameter (name/value/unit/source/method/uncertainty/valid range/version/provenance; source categories distinguish literature/measured/fitted/assumption/unknown)
- EnvironmentState / LightField (direct/diffuse/reflected; lux observed not = photosynthesis; estimated plant-relevant future)
- Measurement (value + required unit + provenance) / Observation (qualitative; separate from measurement)
- InterventionEvent (watering/fertilization/transplant/prune/repot/harvest)
- Scenario / SimulationState / SimulationRun / Prediction (Prediction is result/forecast, not mutable live state)
- ModelVersion / ParameterSetVersion

## Intentionally not modeled yet
- Solar/position/angle calculations
- Shadow propagation
- Photosynthesis / carbon allocation
- Water / nutrient dynamics
- Root growth / L-System / morphogenesis
- LightField calculation engine
- Calibration / validation algorithms
- 3D garden geometry generation

## Validation notes
- Tests in `tests/simulation/test_contracts.py` cover separation contracts (Plant/PlantState/PlantArchitecture, Garden/Boundary, VarietyParameter provenance, Measurement/Observation, Scenario/SimulationRun/Prediction separation, model versions).
- All contracts serializable to JSON-compatible primitives; no framework internals.

## Spatial model (TASK 003)
- G0 = local origin; +X East, +Y North, +Z Up.
- BoundaryPolygon supports arbitrary ordered polygons (L-shape synthetic fixture exists).
- Transform3D (position/rotation/scale) kept separate from Three.js types.
- SpatialNode supports parent-child; world transform derived conceptually (composition simplified at this layer).
- Actual garden measurements not imported; test geometry synthetic only.

## Simulation timing (TASK 007)
- Observation/world time = real-world timestamp.
- Simulation time = simulated date/time (SimulationClock).
- Plant age = biological time (derived from lifecycle, not simulation clock directly).
- Global clock + registered processes with different timesteps (e.g., solar 5 min, env 1 hr, plant 1 day — synthetic examples only).
- Actual timestep values are configuration choices, not universal biological truths.
- Scheduler executes due processes deterministically by priority/order; no hidden science inside scheduler.

## Solar position (TASK 008)
- Method: pvlib.solarposition.get_solarposition (NREL Solar Position Algorithm / SPA).
- Library: pvlib 0.15.2 (MIT license, maintained).
- Inputs: SolarLocation (latitude/longitude/elevation) + timezone-aware datetime.
- Outputs: SolarPosition (timestamp, lat/lon, azimuth_deg clockwise from true North, altitude_deg positive=above horizon, zenith_deg, above_horizon, method).
- Convention: azimuth 0°=N, 90°=E, 180°=S, 270°=W; no magnetic bearing.
- Refraction: included by SPA; not separately corrected.
- No shadow/light/plant logic; pure function callable from scheduler later.

## Direct shadow (TASK 009)
- First shadow layer only (direct); no diffuse/reflected/light-field.
- Sun direction convention: vector from sun toward ground; horizontal opposite sun azimuth; shadow falls away from sun (shadow direction = az + 180°).
- Analytical method: vertical occluder on horizontal plane; shadow length = height / tan(altitude) when sun above horizon.
- Supported occluder: vertical box (simplified); receiver: ground point.
- No Three.js shadow solver; domain-only.

## Light approximation (TASK 010)
- Components: direct (from solar/shadow), diffuse (clear-day sky baseline * sky_visibility * daytime), reflected (reflectance * visible_frac * incident * bounded coeff <=1).
- Units: relative_normalized [0-1] per component; total = sum (may exceed 1 because normalization is per-component, not global radiometric calibration).
- No lux/PPFD; not LightField; not photosynthesis.
- Diffuse preserved under direct shadow when daylight (not erased by shadow).
- Reflected bounded non-negative; zero reflectance => zero.

## TASK 012 — Measurement / Observation ingestion
- Measurement = instrument reading from physical system; raw value preserved, unit required (lux stays lux), uncertainty explicit (None = unknown, not zero), provenance / instrument / method / observer / spatial_ref documented. Synthetic fixtures labeled is_synthetic_example=True.
- Observation = recorded physical/biological state or event; non-numeric content preserved, structured_attributes for structured payload, value_numeric + unit only when measurement-like; not conflated with Measurement.
- Simulation result / LightField / Prediction are model outputs; NOT measurements or observations.
- Persistence: JSON via Pydantic model_dump/model_validate; no DB dependency; human-readable.
- No calibration, validation, PPFD conversion, or parameter fitting performed in this milestone.

## TASK 014 — Snapshot / Checkpoint
- Snapshot: point-in-time simulation state (snapshot_id, simulation_time, world_time, clock_state, scheduler_state, model_version_ref, parameter_set_ref, garden_ref, plant_states_refs, environment_state_ref, provenance, schema_version v1, random_seed optional/None=absent).
- Checkpoint: persisted Snapshot artifact (is_checkpoint=True); same fields; save/load via JSON.
- Immutability: deep-boundary via model_dump/model_validate; restore creates new objects; mutation of one does not affect others.
- Clock/scheduler preserved: SimulationClock (start/current/end/paused) + SimulationScheduler (processes with id/timestep/priority/enabled/next_run); no invented fields.
- Random: explicit seed where available; None = not applicable (not zero).
- State separation preserved: Snapshot != Scenario != Prediction != Measurement != Observation.
- Serialization: JSON via Pydantic; deterministic; no DB.

## TASK 015 — Scenario Branching
- Scenario: hypothetical branch from Snapshot (source_snapshot_ref required); modifications + optional parameter_overrides; not execution; not prediction.
- Branch isolation: source snapshot unchanged; branched state independent via serialization boundary.
- Modification semantics: environment/spatial/intervention/parameter overrides (config, not calibrated biology); provenance preserved.
- Deterministic equivalence: same source + same modifications => equivalent branch.
- No simulation run; no clock advance; no biology; no TASK 016.

## TASK 016 — Prediction (infrastructure only)
- Prediction / PredictionRequest contracts (v1); baseline vs scenario_ref; status lifecycle; target_time timezone-aware.
- Explicit NOT_COMPUTABLE / INCONCLUSIVE when forecasting model unavailable; no fabricated growth/biomass/yield/photosynthesis.
- Uncertainty semantics: unknown / not_modelled / qualitative / quantified; not_modelled preserved.
- Source snapshot + optional scenario; source unchanged; deterministic; persistence JSON.
- No biological forecast; no calibration; no model edits.

## TASK 017 — Plant Architecture
- PlantArchitecture (architecture_id / plant_id / root_organ_id / coordinate_frame / local_origin / organs / provenance / v1).
- PlantOrgan (id / plant_id / organ_type vocabulary root/stem/branch/leaf/flower/fruit/seed/axis/internode/bud/other / parent_organ_id / children_ids / local_position / orientation / length_m >=0 / radius_m >=0 / status / provenance).
- Topology: tree/graph; root no parent; parent resolves; cycles rejected; duplicate IDs rejected; removal requires detach or denies if children.
- Geometry independent of Three.js; domain-only local/world coordinates; +X East / +Y North / +Z Up.
- Synthetic fixtures: seedling + branched; no real measurements; no growth/physics.
- No L-system (TASK 018); no physiology (TASK 019+).

## TASK 018 — L-System Morphogenesis Prototype
- LSystemGrammar (axiom / rules / max_iterations / max_symbol_count / turn_angle / segment_length / provenance / v1).
- Rewrite: simultaneous symbol replacement; iterations >=0; deterministic; limits enforced (no silent truncation).
- Interpreter: turtle (F extend, +/- rotate around Z axis, [/] stack); produces PlantArchitecture; domain-local +X/E +Y/N +Z/U; no Three.js; no growth/biology.
- Architecture conversion: valid topology via validation; root/parent/children consistent; synthetic fixtures (straight + branch).
- Analytical geometry verified independently; no implementation-as-reference.
- Explicit: structural prototype only; not biological validation; TASK 018 does not establish realism; TASK 019+ needed.

## TASK 019 — Plant Physiology Contracts (infrastructure only)
- PlantPhysiologyState / PhotosynthesisResult / RespirationResult / CarbonBalanceResult / LightInput / EnvironmentInput / PlantPhysiolInput (v1).
- Explicit placeholders (None = unavailable); no zero-filling; status NOT_IMPLEMENTED / NOT_COMPUTABLE preserved.
- Units declared per field; lux/relative_normalized not converted; no PPFD inference.
- Temporal/spatial references preserved; provenance/uncertainty preserved.
- No equations; no growth; no calibration; no TASK 020.
