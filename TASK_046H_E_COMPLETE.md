=== TASK 046H-E FINAL VERIFICATION ===
Status: TASK_046H_E_COMPLETE (not BLOCKED — defensible structural proxy exists).

1. Files changed / added (only new; no modifications to 046A-046H-D / 022 / 023 / engine / carbon / pool / fixtures / contracts):
   - simulation/core/physiology/sink_params.py
   - simulation/core/physiology/organ_sink_demand.py
   - simulation/core/physiology/fixtures.py (updated — synthetic fixture labeled)
   - tests/simulation/test_task046h_e_quick.py
   - TASK_046H_E_COMPLETE.md (this file)

2. Actual formula (explicit; no hidden coefficient):
   potential_demand_g = sink_coefficient_g_per_m_per_timestep × structural_proxy_value(length_m) × developmental_activity_factor
   - structural_proxy_reference = "length_m" (unit m) — explicit domain quantity from PlantOrgan contract.
   - coefficient = synthetic example (2.5 g_C/m/timestep); provenance states not calibrated.
   - developmental_activity_factor = 1.0 inside/unknown growth window; 0.0 when window defined and simulation time outside window; 1.0 conservative when window undefined.
   - No physiological-age factor (unavailable — not fabricated).

3. Exact structural proxy:
   - PlantOrgan.length_m (float, unit m, optional, domain-defined).
   - Not arbitrary; not rendered mesh; not pixel count; not fabricated biomass; not undocumented cylinder volume (radius not combined).
   - If length_m is None or negative → NOT_COMPUTABLE (honest failure).

4. Units explicit:
   - potential_demand_g: g_C per timestep.
   - structural_proxy: m.
   - coefficient: g_C · m^-1 · timestep^-1.
   - timestep: seconds (reference, not hidden rescaling factor).
   - demand_kind = POTENTIAL_CARBON_DEMAND (not allocated carbon).

5. Developmental semantics (from 046H-D, not fabricated):
   - chronological_age_days used only as reference, not as sink factor (no age-based sink curve implemented — out of scope).
   - physiological_age: unavailable (field present but not used as factor; no arbitrary assignment).
   - organ_stage: available from 046H-D but not used as quantitative factor (no stage → coefficient mapping invented).
   - growth_window_start/end: used when both defined and simulation_time_ref comparable; before start / after end → factor 0; inside → 1; unavailable → 1 (conservative, documented).
   - No synthetic stage values invented.

6. Parameter semantics:
   - SinkParameterSet: parameter_set_id, organ_type, sink_coefficient_g_per_m_per_timestep (>0 enforced), structural_proxy_reference (explicit), structural_proxy_unit, provenance, source_type (SYNTHETIC), parameter_version, is_synthetic_example, note.
   - No hidden constants; no global parameter table; no calibration performed.

7. Tests run / counts:
   - TARGETED: 32 assertions in test_task046h_e_quick.py — all PASS (manual; pytest unavailable — reported honestly).
   - Prior chain 046A-046G / 046H-D preserved; no unrelated modifications.

8. Known limitations (explicit; not hidden):
   - Structural proxy = length_m only; no biomass, surface area, or organ volume contract exists.
   - Sink coefficient synthetic; not empirically calibrated.
   - No physiological-age sink modulation (requires future domain definition).
   - No growth-window curve (binary eligible/ineligible only; no developmental-stage coefficient).
   - No integration with TASK 022 (allocation) — derivation produces potential demand only.
   - No integration with TASK 023 (growth) — no biomass increment computed.
   - No carbon-pool interaction (demand independent of availability, per invariant).
   - No photosynthesis / respiration / light-field involvement.

9. Scientific integrity checks passed:
   - No lux/PPFD conversion.
   - No LightField → PPFD conversion.
   - No photosynthesis equation.
   - No allocation executed.
   - No geometry mutation (PlantOrgan unchanged after derivation; verified by model_dump_json identity).
   - No DevelopmentalState mutation (verified).
   - Demand never negative (contract + derivation enforce >=0; 0 when outside window or missing proxy).
   - Deterministic (identical inputs → identical JSON).

10. Explicit statement: NOT integrated with TASK 022.
    OrganSinkDemand is potential-demand only. TASK 022 (allocate_sources / CarbonSink) consumes this separately when the allocation pipeline is designed. No source-sink allocation, no carbon transport, no priority/stage-dependency logic added.

DECISION: TASK_046H_E_COMPLETE
