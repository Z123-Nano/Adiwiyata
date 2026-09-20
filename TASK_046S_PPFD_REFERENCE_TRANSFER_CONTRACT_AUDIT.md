# TASK 046S — Absolute Reference PPFD + Spatial Transfer-Factor Contract Audit
Status: TASK_046S_B — REFERENCE_AND_TRANSFER_CONTRACT_REQUIRED (current relative_normalized not defensible as T(x); requires AbsolutePPFDReference + SpatialPPFDTransferFactor contracts; no arbitrary conversion; 046O preserved; upstream unchanged).
Date: 2026-09-18; Mode: LOCAL/OFFLINE; executable source = truth.

## 1. Executive verdict (B)
Decision: B. The current executable LightField (`unit="relative_normalized"`, normalization = synthetic clear-day max direct+diffuse+reflected = 1.0, `coarse_orientation_aware=false`) does NOT define a defensible dimensionless transfer factor `T(x) = PPFD(x)/PPFD_ref`. Its denominator is a synthetic computational maximum, not a physical reference plane; its values are linear [0,1] relative to that undefined maximum; total is sum (not conserved); components are independently normalized to the same synthetic denominator. Therefore both contracts must be created before any `PPFD_organ = PPFD_ref × T(x)` claim: (1) `AbsolutePPFDReference` defining physical boundary (value µmol/m²/s PAR 400–700, geometry, time, provenance, uncertainty); and (2) `SpatialPPFDTransferFactor` defining how `relative_normalized` maps to `T(x)` (normalization alignment, component handling, orientation limitations). No scaling implemented; 046O measured path preserved; no upstream modifications.

## 2. Research basis (supplied)
Hybrid FSPM uses absolute environmental PPFD + spatial transport → local/organ PPFD; transfer factor requires explicit physical reference; normalization alone insufficient; spectral basis required for photon conversion; calibration/validation needed for spatial transfer.

## 3. Current LightField semantics (verified, unchanged)
- Contract (`simulation/core/light/contracts.py` line 6–16): `LightSample` fields direct/diffuse/reflected/total [0,1], `unit="relative_normalized"`; normalization note: "max expected direct + diffuse + reflected = 1.0 under clear daytime with full visibility".
- Denominator: synthetic maximum (clear daytime, full visibility, not a physical plane or open-sky measurement).
- Numerator: direct/diffuse/reflected at grid point from approximation (sky visibility / daylight factor / reflection coeff).
- Linearity: linear [0,1]; stable under solar angle/architecture because max scales with conditions (not fixed reference).
- Components: independently normalized (each to same synthetic max); total = sum (not conserved; can exceed 1).
- No absolute magnitude; no spectral; no optics; no photon flux; no W/m².

## 4. Meaning of relative_normalized (Step 1/2)
Not `PPFD(x)/PPFD_ref`. It is `component_at_point / synthetic_clear_day_max`. The denominator changes with solar conditions and architecture; it is not a stable physical reference. Calling it `T(x)` without contract requires defining denominator = physical PPFD_ref — which current executable does not support.

## 5. Transfer-factor eligibility (Step 2/3)
Required for `T(x)`: both numerator and denominator refer to same physical photon quantity, same PAR band, same time, same context, same compatible geometry. Current LightField has numerator (relative) but denominator undefined (synthetic). Therefore NOT eligible. Option B (needs both contracts) is correct; option A (ready) false; option D (ambiguous) false because semantics are explicit; option C (redefine) not needed if contracts align normalization to reference.

## 6. Absolute reference contract (Step 3/4)
`AbsolutePPFDReference` minimum fields (derived from `PPFDSource` + spatial needs):
- `ref_id`; `ppfd_value` (`float`, `ge=0`, unit `umol_photons_m^-2_s^-1`); `unit` fixed; `spectral_domain` (`PAR_400_700`); `reference_geometry` (explicit plane/context, e.g., open-sky reference plane at garden height, or local sensor plane); `timestamp` / `simulation_time_ref`; `spatial_ref` (`x,y,z,frame="garden_local"` per domain convention); `source_type` (`MEASURED`/`SYNTHETIC`/`DERIVED_PHYSICALLY_VALID`/`MODELED`/`unknown`); `provenance`; `uncertainty` (optional but required for propagation); `instrument` if measured; `status`; `schema_version`; `is_synthetic_example`.
- Reference geometry must match what the future `SpatialPPFDTransferFactor` divides by. For LightField (regular grid horizontal at z), reference plane is likely garden-level horizontal plane (`+Z` up) at grid height, or open-sky above canopy — must be explicit.
- 046O measured PPFD can populate this when sensor position/time/spectral domain match.

## 7. Transfer-factor contract (Step 5)
`SpatialPPFDTransferFactor` minimum fields:
- `ref_id` (links `AbsolutePPFDReference`);
- `lightfield_id` (links `LightField` identity — `solar_reference`, `approximation_params`);
- `target_id` / `target_location` (organ/point `x,y,z` in garden local); `target_organ_id` / `target_plant_id`;
- `t_x` (`float`, dimensionless, `ge=0`); computed as `PPFD_target / PPFD_ref` after alignment; NOT `relative_normalized` directly;
- `direct_t` / `diffuse_t` / `reflected_t` optional (if component scaling supported); else `total_t` only;
- `normalization_alignment_note` (explicit definition of how `relative_normalized` maps to `t` — e.g., "relative_normalized × synthetic_clear_day_max = PPFD_target / PPFD_ref only when both measured under identical solar/atmospheric conditions and normalization reference is defined");
- `orientation_limitation_note` (coarse orientation, vertical cylinder approximation);
- `time_alignment` (reference timestamp = LightField solar_reference = target time);
- `spectral_alignment` (both PAR 400–700);
- `provenance`; `uncertainty` if supported; `status`; `schema_version`; `is_synthetic_example`.

## 8. Direct / diffuse / reflected implications (Step 7)
Current LightField separates components at sample. For total-only scaling: single `PPFD_ref` sufficient; `T_total(x) = total(x) / max_clear_day` only after defining `max_clear_day` = physical PPFD_ref (not synthetic). For component scaling: need `PPFD_direct_ref`, `PPFD_diffuse_ref`, `PPFD_reflected_ref` — not available; do NOT implement independent component scaling now. Component separation can be preserved for future contract but not used for absolute PPFD until references exist.

## 9. Incident vs absorbed (Step 7 boundary)
Output must be `OrganLightExposure.ppfd_value` (incident PPFD, `umol_photons_m^-2_s^-1`, PAR 400–700). No absorbed PAR / APAR / optical absorption model exists. LightField gives relative incident transport; after reference + transfer contracts, scale applies to incident field only. No claim of absorbed PAR.

## 10. 046O measured PPFD relation (Step 10)
`PPFDSource` (measured: `source_type="MEASURED"`) can populate `AbsolutePPFDReference`. Conditions for valid reference: sensor at defined reference geometry; timestamp aligned; PAR 400–700; provenance/uncertainty recorded; status `AVAILABLE`. Use 046O for both calibration (compare `T_observed` vs `T_model`) and anchoring (define `PPFD_ref`). Do NOT replace LightField with single-point measurement; use point to anchor spatial pattern.

## 11. Time alignment (Step 8)
Require: `reference.timestamp == LightField.solar_reference` (or explicitly mapped via `simulation_time_ref` / `timestamp`); `target.time == same`. No interpolation. Existing contracts preserve identity; no enforcement mechanism currently; future adapter must check equality.

## 12. Spectral alignment (Step 9)
Both reference and LightField target PAR 400–700 (broadband). No spectral LightField; no fixed µmol/J invented; broadband relative acceptable for baseline if reference is broadband PAR. If spectral variation matters (e.g., canopy filtering), future spectral LightField model required first.

## 13. Orientation limitation (Step 12)
`architecture_recompute.py` provenance: `coarse_orientation_aware=false`. Leaves oriented differently from vertical cylinder occluders. Direct ray occlusion at leaf surface unreliable. Transfer factor for direct component at leaf-level should carry orientation limitation note; do NOT claim precision for leaf-normal direct PPFD until orientation-aware occlusion exists.

## 14. Uncertainty (Step 13)
Conceptually: `σ_organ_ppfd² ≈ (T² × σ_ref²) + (PPFD_ref² × σ_T²) + cross_term`. `σ_ref` from measurement/instrument; `σ_T` from approximation (coarse orientation, synthetic normalization, no optics, grid resolution). No contract implements propagation; future `TransferFactorContract` can include `uncertainty`. Document both sources; do not invent statistical model.

## 15. Contract options comparison (Step 14)
- S-A (AbsolutePPFDReference only): sufficient if LightField already defensible as T(x) — it is not (normalization undefined relative to physical reference). So S-A alone insufficient.
- S-B (Both contracts): required. Defines reference boundary AND explains how relative_normalized maps to physical ratio.
- S-C (Component references): future enhancement; not required for baseline total PPFD.
- S-D (Redefine LightField): possible if normalization must change from synthetic max to physical ratio; but contract-based alignment (S-B) preserves existing LightField while making mapping explicit, avoiding redesign.

## 16. Final decision (B — REFERENCE_AND_TRANSFER_CONTRACT_REQUIRED)
Not A (current field not valid T). Not C (redefinition not required if contract aligns). Not D (ambiguous — semantics clear). B: create both contracts explicitly; do NOT scale until both define the mapping; preserve 046O; preserve LightField; no arbitrary conversion; document orientation limitation.

## 17. Required next contracts (explicit, not invented)
1. `AbsolutePPFDReference` (boundary input contract).
2. `SpatialPPFDTransferFactor` (mapping contract linking reference + LightField → target).
3. (Future after validation) `LightFieldToOrganPPFD` adapter applying contracts to produce `OrganLightExposure.ppfd_value`.
4. (Future only if needed) `SpectralLightField` / orientation-aware occlusion — not required for baseline B.

## 18. Files inspected (unmodified)
- `simulation/core/light/contracts.py`, `approximation.py`, `architecture_recompute.py`, `field/contracts.py`, `field/compute.py`
- `simulation/core/shadow/direct.py`, `shadow/model.py`
- `simulation/core/solar/model.py`, `solar/calculate.py`
- `simulation/core/physiology/organ_light_exposure.py`, `ppfd_source.py`, `photosynthesis_integration_contracts.py`
- `simulation/core/physiology/photosynthesis_params.py`
- Related fixtures/tests referenced (046M/046O); not edited.

## 19. Tests / audits
Verified via direct source inspection: `relative_normalized` semantics explicit; `no_ppfd` documented; `coarse_orientation_aware=false`; `OrganLightExposure` forbids masquerade; `PPFDSource` requires absolute; 046O path intact; no conversion code present; no upstream edited. PYTEST_UNAVAILABLE reported; no false test claims.

## 20. Limitations
- LightField normalization remains synthetic; not physically calibrated.
- Transfer-factor contract must explicitly define normalization-to-reference mapping; without validation dataset, T remains theoretical.
- Orientation limitation means direct-component transfer at leaf surfaces is approximate; full accuracy requires future orientation-aware occlusion + optics.
- No spectral LightField; broadband PAR assumption only.
- Uncertainty propagation not implemented; conceptual only.
- This is contract design, not implementation of scaled PPFD.
