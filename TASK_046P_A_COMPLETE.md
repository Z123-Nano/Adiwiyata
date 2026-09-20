# TASK 046P-A — Photosynthesis Carbon Unit & Temporal Integration Audit

Status: TASK_046P_A_COMPLETE
Decision: 046P_READY_WITH_LIMITATION
Source modifications: 0 (read-only; nothing edited)

## A. Photosynthesis result semantics (exact from code)

Contract: simulation/core/physiology/contracts.py PhotosynthesisResult
Fields: status, gross_assimilation (float, optional, unit reserved), limiting_factors, input_ref, provenance, assumptions, notes, is_synthetic_example.
No organ_area; no timestep; no integrated-amount field.
Equation (photosynthesis.py): A = (alpha * Amax * PPFD) / (alpha * PPFD + Amax)
Unit of A: μmol CO₂ m⁻² s⁻¹ (explicit in module docstring).
Physical meaning: instantaneous rate per leaf area per second; not integrated over interval; not organ-level amount.
Time basis: per second (instantaneous).
Area basis: per m² (rate normalized to area); organ area must be applied externally.

## B. Area availability

ORGAN_AREA_IN_PHOTOSYNTHESIS = NONE.
No area term in equation; no area field in PhotosynthesisResult; no leaf_area / surface_area / radius×length conversion inside photosynthesis module.
Not automatically a failure; it is a documented simplification (light-response only; temperature/CO2 not modeled).

## C. Time integration

TIME_INTEGRATION = RATE (instantaneous, per second), NOT integrated over timestep.
Result gross_assimilation = 7.142857 μmol CO₂ m⁻² s⁻¹ for SYNTH_PFD_MED (PPFD=200).
Timestep (3600 s) is NOT multiplied inside the equation.
No temporal aggregation inside TASK 020.

## D. Photosynthesis equation dimensions

Trace (current implementation only, not replaced):
PPFD [μmol photons m⁻² s⁻¹] → A [μmol CO₂ m⁻² s⁻¹] via rectangular hyperbola (rate).
No area multiplication; no timestep multiplication; no CO₂→C mass conversion; no respiration inside equation.
Consequence: result is rate per area per time; downstream carbon must apply area, timestep, and carbon-mass convention explicitly.

## E. Carbon adapter (046F) inspection

File: simulation/core/physiology/carbon_input_adapter.py
Function: carbon_from_photosynthesis(photo, respiration_rate=0.15, timestep=3600.0)
Critical observations (read-only; not edited):
- References photo.gross_carbon_g — field does NOT exist on PhotosynthesisResult (field is gross_assimilation). This is a field-name/contract mismatch.
- Passes value directly as gross_carbon_g — treats instantaneous rate as grams of carbon; skips area × timestep × CO₂→C conversion.
- timestep parameter is accepted but used only for CarbonResult.timestep; not applied to convert rate→mass.
- No conversion of μmol CO₂ to g C; no area factor; no time-factor.
Documented limitation: adapter is structurally direct but dimensionally incomplete for rate→mass.

## F. TASK 021 semantics

File: simulation/core/carbon/carbon.py carbon_respiration(gross_carbon_g, respiration_rate=0.15, timestep=3600.0)
Equation: respiration = gross * rate; net = gross - respiration.
Result: CarbonResult with gross_carbon_g, respiration_g, net_carbon_g, timestep.
Unit: g_C per timestep (explicit by field names; timestep preserved separately).
Assumes input is already grams over timestep.
Compatible with CarbonPool.current_net_carbon_g (same unit, same timestep) IF input is correct.

## G. 046F compatibility with 046G

Compatible if and only if adapter produces correct g_C per timestep.
Current adapter produces 0.0 (field mismatch) or treats rate as grams (dimensional error).
Conclusion: contract interface is compatible; actual execution requires fixing adapter input (gross_assimilation vs gross_carbon_g) and adding rate→mass conversion (area × timestep × 12/44 for CO₂→C).
Not a contract redesign; an implementation gap.

## H. 046J downstream compatibility

OrganGrowthResult distinguishes:
- allocated_carbon_g (g_C from 046I)
- structural_carbon_increment_g_C (g_C retained)
- biomass_increment_g_DM (g_DM realized)
- new_biomass_g_DM = previous + increment
Note on fixture: "TASK 023 unit=g_C incompatible with g_DM" explicitly documents distinction.
Downstream from 046F→046G→046I→046J: g_C flows through allocation/growth; g_DM is output. No hidden collapse.

## I. Respiration / growth-cost separation

carbon_respiration (046J/021) computes maintenance respiration = rate × gross.
046J growth conversion uses retention_fraction and carbon_fraction_of_dry_biomass to derive g_DM from g_C.
No double-application: respiration deducted from gross; growth retention applies to allocated carbon, not to respiration.
Contracts separate these by design (respiration_ref vs growth_parameter_set_ref).

## J. Synthetic numerical trace (documented, not forced)

Fixture: SYNTH_PFD_MED (PPFD = 200 μmol/m²/s)
Photosynthesis result (photosynthesis_rate): A = 7.14 μmol CO₂ m⁻² s⁻¹ (VALID).
Area: UNAVAILABLE (no organ_area in equation/result).
Timestep: 3600 s (not applied in 020).
Adapter attempt: passes photo.gross_carbon_g → attribute missing; falls to 0.0 (or fails).
If conversion existed (hypothetical not implemented): 7.14 μmol/m²/s × A_leaf × 3600 s × (12/44 g C / μmol CO₂) = g_C/step.
No such conversion exists in repo; not invented here.
CarbonPool: expects g_C/step — not supplied correctly.
Growth: requires allocated g_C; unavailable upstream.
Documented: chain stops at rate because conversion is missing; not masked.

## K. Scientific decision

046P_READY_WITH_LIMITATION
Reasoning: chain is structurally executable (contracts exist, imports work, fixtures produce results); but the rate→integrated-mass conversion and adapter field-name alignment are incomplete. Executing 046P with current adapter produces numerically plausible but dimensionally ambiguous results (rate treated as grams; area missing). This must not be hidden.
Smallest missing pieces (for future 046P implementation, not this audit):
1. Organ leaf area contract / parameter (explicit, not assumed from radius/length).
2. Rate→mass conversion formula (explicit: μmol CO₂ m⁻² s⁻¹ × area_m² × timestep_s × 12/44 → g_C) with provenance.
3. Adapter fix: use gross_assimilation (not gross_carbon_g); apply conversion; pass correct g_C/step to 046F.
These are correct next-step design questions, not hidden bugs to patch silently.

## L. Scope / limits

No source edited (photosynthesis.py, contracts.py, adapter, carbon, growth untouched).
No molecular conversion constant added.
No area assumption invented.
No timestep assumption changed.
No LightField altered.
No PPFD conversion invented.
No physiology equations changed.
Tested: imports, fixtures, numerical trace (manual); PYTEST_ENVIRONMENT_UNAVAILABLE.

TASK_046P_A_COMPLETE
