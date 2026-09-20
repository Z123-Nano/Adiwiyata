TASK 050-R — Research Gate: Environmental Coupling Necessity, Mechanism and Data Sufficiency
Status: RESEARCH / DECISION GATE (no production code changed; no calibration; no empirical validation; no new science invented)
Date: 2026-09-19
Interpretation: literature-backed, garden-specific analysis of environmental/developmental coupling requirements, data sufficiency, and identifiability for the active FSPM — PARTIAL/DEFER decisions only; no complete biological model claimed.

1. Research questions
- Which of phenology→growth, water→growth/physiology, nutrient→growth, physiological age, C–N, water–N are scientifically justified for the Adiwiyata digital twin today?
- Which have sufficient data (TASK 049 plan + fixtures) to identify parameters?
- Which require species-specific profiles not yet available?
- What is the smallest defensible environmental model that supports study objectives?

2. Repository findings (executable source, not filenames)
- Phenology: simulation/core/development/contracts.py OrganDevelopmentalState (TASK 024). physiological_age unavailable (F); growth_window unavailable (I); active_growth derived only when defined (J); chronological_age explicit (E). No growth-window definition exists.
- Water: simulation/core/water/contracts.py + balance.py. RootZoneState, WaterBalanceInput/Result, RootUptakeInput/Result executable. No interface to photosynthesis, growth, or carbon.
- Nutrient: simulation/core/nutrient/contracts.py + balance.py (balance_nutrient). NutrientPoolState (N/P/K identity preserved via element); NutrientBalanceInput/Result executable. No limitation/uptake coupling to growth or photosynthesis.
- Light/PPFD: existing 046M/046V/046W chain preserved; LightField ≠ PPFD enforced (046Q-B).
- Carbon: 020/021 unchanged; gross_carbon_g = integrated; reserve from 046Z preserved; no second respiration/conversion.
- Growth/Architecture: 046I/046J/046K/046L active via explicit PPFDSource (046AB); architecture unchanged at boundary.
- Clock: SimulationClock (TASK 007), fixed 3600s, domain time.
- Observations: fixtures_049/protocol_049 (session, sensor registry, multi-PPFD); fixtures_047 (Measurement/Observation with units/provenance/quality); production sync verified 049-FIX.
- Calibration readiness: TASK 048 parameter audit (alpha/pmax/retention/sink sensitivity ±10%; identifiability classification); dataset split designed; synthetic ground-truth only.

3. Literature sources (selected; sources recorded per instruction 8)
- FSPM architecture / source-sink / calibration reference: MetaFSPM (research reference, not runtime); CPlantBox (plant/root FSPM reference only); GreenLab (source-sink/calibration/stochasticity reference) — all reference-only per CLAUDE.md.
- Mechanistic C–N–water coupling example: recent 2026 FSPM work (CNW-Wheat) demonstrates organ-level carbon/nitrogen metabolism + water-flow integration including xylem water potential and hydraulics. Source type: literature-supported example of complexity. Relevance: shows genuine water-growth coupling requires hydraulic/state structure, not a scalar multiplier.
- Developmental modeling / thermal time / photoperiod: established plant-physiology literature (not specific repository dependencies). Source type: literature-supported. Limitations: species-dependent parameterization required; generic garden model needs calibration data.
- Data sufficiency / identifiability: TASK 048 calibration framework (synthetic; parameter sensitivity ±10%; dataset-split design). Repository-supported.
- Observation protocol / measurement design: TASK 049 fixtures/protocol (synthetic acquisition pipeline; multi-PPFD for alpha/pmax separation; spatial G0 +X/+Y/+Z). Repository-supported.
No fabricated citations; no literature presented as repository fact.

4. Phenology → Growth analysis
Mechanism options compared (instruction 2): chronological age; thermal time; photothermal time; explicit stage; organ-specific developmental state.
Current model reality: OrganDevelopmentalState holds chronological_age_days + optional stage vocabulary; physiological_age unavailable; growth_window unavailable; active_growth not inferable.
Scientific necessity for digital twin objective: partial — stage tracking useful for plant identity/observation sync; growth eligibility requires growth_window definition, which does not exist.
Data: TASK 049 has no scheduled phenology-event observations (initiation/flowering/senescence); only architecture measurements at t0.
Parameter burden: stage-transition rules + thermal/photoperiod coefficients + species profile.
Identifiability (TASK 048): confounded with architecture/carbon/sink; cannot separate stage effect from environment without dedicated observations.
Recommendation: DEFER_UNTIL_DATA. Chronological age + stage record preserved; growth-window coupling deferred until growth-window model + phenology-event observations exist.

5. Physiological Age analysis
Active model equations requiring physiological age: none. Photosynthesis uses PPFDSource; carbon uses integrated gross_carbon_g; growth uses architecture delta refs; allocation uses sink demand — none reference physiological_age.
Can be represented by stage: yes, for current executable model.
Would add information vs hidden parameter: at current state, another unidentifiable scalar; no observation exists to distinguish.
Observations needed: organ-level developmental-state tracking over time; thermal-time accumulation; environmental forcing records linked to initiation.
Recommendation: DO NOT IMPLEMENT. Documented because active model does not require it; adding it without identification pathway violates identifiability (TASK 048 / instruction 10).

6. Water → Physiology/Growth analysis
Mechanisms evaluated (instruction 4): soil/root-zone storage; plant water status; transpiration; stomatal regulation; hydraulic conductance; turgor-driven growth; water-limited photosynthesis.
Example of required complexity (CNW-Wheat 2026): includes xylem water potential, hydraulic architecture, organ-level C-N-water coupling. Not reducible to growth × scalar.
Current repository: balance executable; RootUptakeResult exists; PlantWaterStatus exists — but no output targets photosynthesis, growth, or carbon.
Data needed (instruction 11): root-zone moisture at container/rack scale; plant water status (pressure potential / relative water content) if coupling to photosynthesis/growth is required; temporal resolution matching timestep (3600s); for multiple plants/racks.
TASK 049 data availability: only environment + architecture + PPFD observations; no soil moisture / plant water status measurements planned.
Parameter count if implemented: storage curves, hydraulic conductance, stomatal response, turgor-growth relation — high; species-specific.
Identifiability: confounds with light, carbon, architecture; cannot separate water limitation from sink limitation without paired water-state + growth-rate observations.
Recommendation: DEFER_UNTIL_DATA. Keep executable balance; document missing interface explicitly; do not fabricate scalar multiplier.

7. Nutrient → Physiology/Growth analysis
Mechanisms: N acquisition; N assimilation; allocation; photosynthetic-capacity dependency; organ-growth dependency; C–N interaction; water–N interaction.
Current repository: NutrientPoolState (element identity N/P/K); balance executable; no limitation contract.
Data needed: soil N / tissue N; uptake measurements; timing relative to growth stage; spatial (container/rack) resolution.
TASK 049 plan: no soil/tissue nutrient observations; only multi-PPFD light campaign.
Parameter burden: uptake rates, allocation fractions, C–N ratios — moderate-to-high; species/cultivar dependent.
Recommendation: DEFER_UNTIL_DATA. Pool bookkeeping preserved; limitation coupling deferred until tissue/soil observations available.

8. C–N interaction analysis
Mechanism: carbon + nitrogen metabolism coupled at organ level (CNW-Wheat reference). Requires paired tissue C/N, organ-level allocation, uptake timing.
Data: tissue C/N measurements; organ growth rates; photosynthetic capacity measurements; temporal pairing.
TASK 049: none of above planned.
Recommendation: DEFER_UNTIL_DATA. Not required for minimal model.

9. Water–N interaction analysis
Mechanism: water availability affects nutrient uptake; nutrient status affects transpiration / hydraulic architecture. Requires paired water-state + nutrient-state + plant-state observations.
Data: root-zone water + soil nutrient + plant tissue at same times/places.
Task 049: absent.
Recommendation: DEFER_UNTIL_DATA.

10. Species dependence analysis
Garden contains multiple plants (P001 registry); varieties include UNKNOWN until profile established (fixture). Generic mechanism required for digital twin; species-specific parameterization requires cultivar data not yet collected.
Phenology: stage vocabulary optional; thermal-time parameters species-specific.
Water: hydraulic/stomatal parameters species-specific.
Nutrient: uptake/assimilation species-specific.
Recommendation: where species-specific, mark REQUIRES_SPECIES_PROFILE (growth-window, physiological-age if ever needed, water/hydraulic, nutrient-uptake). Generic stage/water-balance/nutrient-balance can remain executable independently.

11. Data sufficiency analysis (TASK 049 + fixtures)
Available / collectable under current plan:
- Light/PPFD: yes (multi-level campaign; 046V-046W chain)
- Architecture: yes (3D imaging; observation contract 046K)
- Environment: partial (environment measurement in pipeline)
- Soil/root-zone water: DATA_UNAVAILABLE / DATA_EXPENSIVE (not in 049 protocol)
- Plant water status: DATA_UNAVAILABLE
- Soil nutrient / tissue N: DATA_UNAVAILABLE
- Phenology events (initiation / flowering / senescence): DATA_UNAVAILABLE
- Species/cultivar profiles: DATA_COLLECTABLE (requires identification/cultivar survey)
Conclusion: only light + architecture + basic environment observations sufficient for current executable loop; environmental-coupling parameters not identifiable.

12. Parameter / identifiability analysis (TASK 048 context)
Sensitivity ±10% established for alpha/pmax/retention/sink. Adding environmental coupling parameters (water-stress coefficient, nutrient limitation scalar, thermal-time coefficient, stage-transition probabilities) without dedicated observations creates unidentifiable confounding with architecture, carbon, and sink.
Identifiability requires: independent dataset split; paired observations of driver + response; no calibration/validation leakage (TASK 029 / 028 rules). Current 049 design does not provide independent datasets for water/nutrient/phenology drivers.
Recommendation: do not add coupling parameters until observation protocol expanded.

13. Complexity comparison
Minimal (current executable): light → photosynthesis → carbon → allocation → growth → arch + separate water balance + separate nutrient balance + phenology record. Supported; data sufficient; identifiable.
Moderate (+phenology stage + basic water balance coupling via explicit interface, not invented multiplier): requires phenology-event observations + basic root-zone moisture. Partially justifiable but not yet data-supported.
Full mechanistic (CNW-Wheat-style C–N-water-hydraulic): requires tissue C/N, xylem potential, hydraulic architecture, stage transitions, environmental forcing at organ scale. Data and parameter burden high; not justified by current observation plan.
Recommendation: stay minimal; document interfaces as deferred.

14. Garden relevance
Objective: high-realism spatial-temporal digital twin with explicit environment coupling. Minimal model satisfies observation-sync / architecture / carbon / light foundation; deferred couplings do not block core objective because architecture-environment feedback preserved via existing light/ppfd/growth path.

15. Candidate observation requirements (for deferred couplings)
Phenology→Growth: initiation/flowering/senescence event log linked to architecture; thermal-time / photoperiod records.
Water→Physiology: root-zone moisture (container/rack); plant water status (pressure/potential or RWC); temporal resolution = timestep.
Nutrient→Growth: soil N at container/rack; plant tissue N; uptake timing; paired with growth-rate observations.
Physiological age: initiation time per organ + thermal accumulation; requires long-term tracking.

16. Final decision table (instruction 18 required)
| Missing Interface            | Recommendation         | Scientific Basis                          | Required Data                        | Why                                                  |
| ---------------------------- | ---------------------- | ---------------------------------------- | ------------------------------------ | ---------------------------------------------------- |
| Phenology → Growth           | DEFER_UNTIL_DATA       | Stage vocabulary exists; growth_window undefined; chronology sufficient now | Phenology events + growth-window model | No growth-window contract; confounds with architecture/carbon |
| Physiological Age            | DO NOT IMPLEMENT       | Active model uses stage/chronology, not physiological age; no identification pathway | Tissue/state tracking over time        | Would add unidentifiable scalar; not required by current equations |
| Water → Physiology/Growth    | DEFER_UNTIL_DATA       | Balance executable; CNW-Wheat shows true coupling needs hydraulics/state | Root-zone moisture + plant water status + temporal pairing | No interface in contracts; scalar multiplier not defensible |
| Nutrient → Physiology/Growth | DEFER_UNTIL_DATA       | Pools executable; no limitation contract exists | Soil N + tissue N + uptake + growth-rate pairing | No limitation equation defined; parameter identification impossible |
| C–N interaction              | DEFER_UNTIL_DATA       | CNW-Wheat reference shows complexity; needs paired C/N tissue + allocation | Tissue C/N + organ growth + photosynthesis pairing | High parameter/data burden; not needed for minimal model |
| Water–N interaction          | DEFER_UNTIL_DATA       | Coupled uptake/transpiration requires paired water + nutrient observations | Root-zone water + soil nutrient + plant state | Confounded with light/carbon/architecture; no independent dataset |

17. Recommended minimal environmental model
Keep executable: light/PPFD (046V-046W) → photosynthesis (020) → carbon (021) → pool (046G) → allocation (046I) → growth (046J) → architecture delta (046L) → architecture (046AF/046Z); plus separate executable state modules (phenology record, water balance, nutrient balance) with explicit documented non-coupling. This satisfies instruction 13 comparison: minimal = sufficient for current data + identifiable; moderate/full deferred to future observation campaigns.

18. Implementation order (if/when deferred items adopted)
1. Phenology events + growth-window model + stage-transition rules (+ observations).
2. Root-zone water measurements + basic water-state coupling interface (explicit, not invented multiplier).
3. Soil/tissue nutrient observations + nutrient limitation contract (if justified by data).
4. C–N / water–N only after 1–3 data foundations established.

19. Deferred mechanisms (explicit; not hidden)
- Phenology growth-window coupling.
- Water-status → photosynthesis/growth interface.
- Nutrient limitation → growth interface.
- Physiological-age equation.
- C–N / water–N coupled equations.
- Any scalar environmental penalty without mechanistic contract.

20. Explicit non-recommendations
- DO NOT implement physiological age.
- DO NOT invent water-stress coefficient / nutrient limitation multiplier / stomatal model / transpiration equation / hydraulic model / new photosynthesis equation / new allocation theory.
- DO NOT calibrate or fit coupling parameters with existing fixtures (no independent dataset; TASK 028/029 rules preserved).
- DO NOT treat relative LightField = PPFD; DO NOT convert lux → PPFD.
- DO NOT assume “well watered / well fertilized” as default.

21. Sources and publication dates (recorded per instruction 21)
- MetaFSPM / CPlantBox / GreenLab: references, not runtime dependencies; repository guidance (CLAUDE.md).
- CNW-Wheat 2026: literature-supported example of C–N–water organ-level coupling complexity (instruction 4 / 8).
- TASK 024/025/026 contracts: repository-supported (development/water/nutrient contracts + fixtures).
- TASK 048 calibration: repository-supported (parameter sensitivity / dataset design / synthetic only).
- TASK 049 protocol: repository-supported (multi-PPFD / observation / session / sensor registry fixtures).
- Standard FSPM development/thermal-time literature: literature-supported (instruction 8); species-dependence noted.

22. Uncertainty / limitations
- Species profiles not yet collected → some recommendations conditional on cultivar identification.
- No empirical garden measurements yet → all coupling recommendations deferred to data-collection phase.
- Synthetic fixtures only; no predictive validation claimed.
- Identifiability of any future coupling depends on expanded observation protocol (section 15), not only on model structure.
- Report does not claim biological completeness; only documents which mechanisms are justified by current contracts + data.

23. Final conclusion (instruction 28 / 26)
TASK 050-R closes the research gate honestly: existing executable modules (phenology record, water balance, nutrient balance) preserved; missing interfaces documented with explicit reasons (missing contracts, missing observations, identifiability limits, species-dependence); recommendations categorized per instruction 12; no production code changed; no calibration / no empirical validation / no new science invented. Next phase: expand observation protocol (section 15) before attempting deferred couplings.
Co-Authored-By: Claude Code <noreply@anthropic.com>
