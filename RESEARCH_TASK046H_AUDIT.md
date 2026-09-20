=== TASK 046H-RESEARCH FINAL AUDIT ===
Status: READ-ONLY. No .py / .ts / contract / fixture / test / config modified.
Repo: master; 046G CarbonPool 20/20 prior; 046E engine orchestration intact; 046F adapter intact.
Environment: pytest unavailable → manual verification; git status unchanged (only existing M/D from earlier turns).

1. CURRENT PLANT / ORGAN STATE
PlantOrgan (simulation/core/contracts/domain.py 96): id, plant_id, organ_type (literal 11 types), parent_organ_id, children_ids, local_position, orientation, length_m, radius_m, status, geometry_metadata, topology_ref, creation_index, provenance, schema_version, is_synthetic_example.
PlantArchitecture (line 114): topology + organ list reference.
REAL: organ_type; parent/child topology; geometry (partial: optional); provenance/version.
PARTIAL: geometry (length/radius optional, no biomass/density); creation_index (ordinal, not age).
MISSING: organ age; physiological/developmental age; initiation time; biomass; dry mass; growth rate; sink/source role; phenology stage at organ level.

PhenologyState (core/phenology/contracts.py 21): plant-level only — current_stage (STAGE_VOCAB 9 stages), stage_start_time, stage_start_age_days, transition_history, transition_count. No organ-level analog.
REAL (plant): stage + stage_start_age_days.
MISSING (organ): any developmental-state field.

2. CURRENT Organs Demand STATUS
TASK 022 CarbonSink (core/allocation/contracts.py 19-27): sink_id, plant_id, organ_id, sink_type (stem/root/leaf/reproductive/other/maintenance), demand: Optional[float] = None (unit contract says umol CO2 m^-2; fixtures label synthetic values 5/3/2/0/-1/None), priority/capacity extensible unenforced.
Fixtures (core/allocation/fixtures.py 17-22): SYNTH_SINK_STEM/ROOT/LEAF/ZERO/NEG/NOD — all is_synthetic_example=True; demand fixed; provenance labels synthetic.
Status: FIXTURE_ONLY. No derivation from PlantOrgan exists; no OrganSinkDemand contract exists; NO model pipeline PlantOrgan → demand.

3. SCIENTIFIC COMPARISON OF CANDIDATE DEMAND MODELS (table U section below; summarized)
A. Universal constant demand → rejected (S, no organ-type/model basis).
B. Demand = organ area/size without model → rejected (S; geometry alone uncalibrated, no growth window, no sink-strength parameter).
C. GreenLab-style sink function (sink strength = f(organ_type, physiological_age, parameter_set)) → DIRECTLY_APPLICABLE conceptually; but requires physiological_age/development_window/organ-stage — MISSING. Not implementable now without contract gap fill.
D. MuSCA-style structural-source-sink with transport/assimilate state → REFERENCE_ONLY; requires unavailable transport/concentration/arch-state beyond current Project.
E. Hybrid minimal: organ-type-specific structural-demand coefficient × current structural-size proxy (from length/radius) × timestep; explicit parameter provenance; no hidden age assumption; calibration possible when biomass-over-time observations available; compatible with TASK 022 if unit conversion layer added or if defined in g_C/timestep with explicit semantic — RECOMMENDED as minimum defensible.

4. GREENLAB FINDINGS
Sink strength relates to organ development via organ-type-specific sink functions modulated by physiological age / developmental stage (GreenLab: sink parameters per organ type; age from initiation; growth window defined; calibration from final size + growth curves). In this repo: organ-type category exists; physiological age and initiation time MISSING; growth window MISSING; parameter-set infrastructure (TASK 028 calibration framework) exists conceptually but not linked to organ-level sink parameters.
Classification: DIRECTLY_APPLICABLE in principle; ADAPTABLE with development-state contract; CURRENTLY REFERENCE_ONLY because required age/state unavailable.

5. MUSCA FINDINGS
MuSCA represents sink strength via structural biomass / assimilate availability interactions; uses spatial/structural info; requires transport/state fields not present in PlantOrgan; assimilation availability interacts with demand but transport/concentration fields absent.
Classification: REFERENCE_ONLY (structural concept informs geometry proxy use; full MuSCA requires unavailable fields).

6. DEVELOPMENTAL-AGE REQUIREMENTS (section H)
Distinction explicit (not merged):
- simulation time / world time / observation time → distinct; project clock (core/clock/) manages simulation time.
- chronological organ age = current_sim_time - initiation_time — MISSING (no initiation_time on PlantOrgan).
- physiological/developmental age = accumulated development since initiation / stage progression — MISSING (no organ-level phenology; plant-level only).
- phenological stage = plant-level STAGE_VOCAB — AVAILABLE at plant only.
Required for true GreenLab sink model: physiological / developmental age per organ. Classify: CONTRACT GAP.
Smallest missing contract: organ developmental context (initiated_at / organ_stage / growth_window_start_end / optionally physiological_age_days).

7. DEMAND UNIT / SEMANTIC RECOMMENDATION (K)
TASK 022 CarbonSink.demand contract states umol CO2 m^-2 — a surface-normalized photosynthetic-unit, NOT carbon mass per timestep.
TASK 023 GrowthResult uses biomass_increment_g with unit g_C.
TASK 021 carbon_respiration uses g_C.
OrganSinkDemand (proposed) should be defined explicitly: if intended to feed TASK 022 directly, must match or provide conversion; safest is to define OrganSinkDemand in g_C per timestep (potential carbon requirement) and add explicit conversion layer to umol CO2 m^-2 only when feeding TASK 022, OR redefine CarbonSink.demand semantics with contract change (out of 046H scope).
Distinction preserved: sink strength (relative/structural scalar, dimensionless or per-unit-structure) vs actual carbon demand (g_C/timestep) vs allocated carbon (TASK 022 output, same unit as demand or converted). Do NOT conflate.
Recommendation: OrganSinkDemand = potential carbon demand per timestep in g_C; sink_strength = organ-type parameter (g_C per structural-unit per timestep) separate.

8. PARAMETERIZATION / CALIBRATION FEASIBILITY (M, N, O)
Proposed minimal parameter set (conceptual only — no values created):
- sink_strength_coef[organ_type] — unit g_C · (structural_unit)^-1 · timestep^-1; provenance SYNTHETIC until calibrated; applicability per organ type; calibration feasible from biomass-over-time + geometry-over-time observations (TASK 028 framework supports parameter estimation from structured dataset; identifiability requires separation of structural-size effect from age effect — weak if only final size observed, stronger with time-series).
- structural_size_proxy — derived from length_m × radius_m² (proxy for structural volume/mass); PARTIAL (geometry optional); calibration feasible if dry-mass measurements available; otherwise proxy is assumption.
- timestep — REAL (clock); provenance preserved.
Identifiability observation: if only final organ size observed, coefficient and initiation time confounded; need time-series or explicit age/state to separate. Explicitly flagged.
No parameter values added (rule).

9. IDENTIFIABILITY OBSERVATIONS (O)
Scenario A: coefficient 1 + large initial size → same observed growth as coefficient 0.5 + small initial + longer window. Without age/window or biomass time-series: weakly identifiable.
Scenario B: only geometry at single time → cannot distinguish growth rate from current state.
Implication: calibration requires either (a) time-series biomass + geometry, or (b) explicit developmental-state contract + known initiation, to make sink-strength separable.

10. MINIMUM SCIENTIFICALLY VALID MODEL (P)
HYBRID_MINIMAL_SINK_MODEL:
- Inputs: PlantOrgan (organ_type, length_m, radius_m, geometry_metadata, provenance); parameter set (sink_strength_coef per organ_type, synthetic/provenance-labeled); timestep.
- Process: structural_proxy = f(length, radius) [explicit, not hidden]; potential_demand_g = coef[organ_type] × structural_proxy × timestep; status = AVAILABLE if inputs valid else NOT_COMPUTABLE; provenance = parameter_ref + synthetic label if applicable; no hidden age assumption.
- Exclusions (intentional): no physiological-age modulation (requires development-state contract); no phenology-window modulation (requires organ-level phenology); no transport/assimilate interaction (MuSCA out of scope); no hidden fixture demand; no geometry→demand direct without coefficient.
- Compatibility: TASK 022 via conversion layer or unit-aligned definition; TASK 023 via biomass_increment_g (same unit); PlantArchitecture via organ reference; future calibration (TASK 028) via structured dataset + parameter version.
- Limitation stated explicitly: potential demand is structural-potential, not full physiological-age-modulated demand; calibration requires biomass/geometry time-series or development-state addition.

11. PROPOSED Organs SinkDemand CONTRACT FIELDS (Q — conceptual, not implemented)
- sink_demand_id, organ_id, plant_id, architecture_id, organ_type, structural_size_proxy, sink_strength_coef_ref, potential_demand_g (float, g_C per timestep), timestep, simulation_time, status, provenance, parameter_version, is_synthetic_example, note (explicit limitation: age/state unavailable if applicable), schema_version.
NOT implemented.

12. SCIENTIFIC AUDIT TABLES (U)
Candidate model | Main inputs | Output semantics | Data requirements | Calibration feasibility | Project fit | Main gap
A universal const | none | fixed g_C | none | impossible | poor | no model basis
B geometry-only | length/radius | g_C by area | geometry optional | weak (single time) | partial | no sink parameter, no age
C GreenLab sink | organ_type + phys_age + params | g_C by age-window | age/init + params + biomass time-series | good if data available | concept applicable; currently unavailable | physiological age / initiation / organ stage MISSING
D MuSCA structural | biomass + structure + transport | assim-available-modulated | transport/concentration + biomass + spatial | moderate | reference only | transport/state fields MISSING
E HYBRID MINIMAL (recommended) | organ_type + geometry + coef + timestep | potential g_C / timestep | geometry + coefficient + timestep | moderate (time-series improves) | best current fit; explicit limits | age/window not represented; calibration partial without time-series

Required variable | Project status | Scientifically required? | Next contract
organ_type | REAL | yes | none
geometry (length/radius) | PARTIAL | yes (proxy) | none (optional fields exist)
physiological/developmental age | MISSING | yes for full GreenLab | organ development-state contract (initiated_at / organ_stage / growth_window)
biomass / dry mass | MISSING | yes for calibration | measurement/observation contract extension (already in 012, but organ-level biomass not linked)
initiation time | MISSING | yes for age | same development-state contract
sink_strength parameters | MISSING (fixture only) | yes | parameter set contract linked to organ type (TASK 028-compatible)
phenology at organ level | MISSING | yes for window | same development-state contract

13. REPOSITORY / TEST OBSERVATIONS (X)
- 046G quick test 20/20 verified (carbon pool). Prior session only quick tests for 046F; pytest unavailable now.
- No test failure caused by this audit (no code changed).
- Environment limitation: pytest missing; manual verification used; no silent pass fabricated.
- Source isolation preserved: CarbonPool unchanged; engine unchanged; fixtures unchanged.

14. EXACT MODEL RECOMMENDATION (V)
HYBRID_MINIMAL_SINK_MODEL
Evidence: GreenLab requires developmental age/parameters unavailable; MuSCA requires unavailable transport; geometry-only rejected (S); universal constant rejected (S). Hybrid uses available organ_type + partial geometry + explicit synthetic/provenance-parameter reference, excludes age/window intentionally (not hidden), defines potential demand in g_C/timestep compatible with TASK 021/023, and flags calibration limits honestly.

15. NEXT-CONTRACT DECISION (W)
NEEDS_DEVELOPMENT_STATE_CONTRACT_FIRST
Exactly missing: organ-level developmental context (initiated_at / physiological_age_days / organ_stage / growth_window_start_end / optionally sink-role initialization). Without this, any demand model that claims developmental-window modulation would be fabricated. Once that contract exists, HYBRID_MINIMAL can add age-modulation layer and become closer to GreenLab-style; calibration improves with biomass time-series.
No production code / contract / fixture / test created.
STOP.
