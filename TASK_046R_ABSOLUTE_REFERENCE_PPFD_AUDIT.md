# TASK 046R — Absolute Reference PPFD Boundary & Relative Spatial Transfer Audit
Status: TASK_046R_B — REFERENCE_CONTRACT_FIRST (LightField relative-normalized transport is not yet defensible as dimensionless transfer factor T(x); needs explicit AbsolutePPFDReference contract defining reference plane/time/spectrum + explicit transfer-factor contract aligning normalization to physical reference before any scaling; 046O measured path preserved; no arbitrary PPFD conversion implemented).
Date: 2026-09-18; Mode: LOCAL/OFFLINE; executable source = truth; no upstream modifications.

## 1. Executive verdict (B)
Decision: B — REFERENCE_CONTRACT_FIRST. The current executable LightField (`relative_normalized`, normalized to synthetic clear-day max = 1.0, coarse orientation, no optics, no absolute magnitude, no spectral basis) does NOT provide a defensible dimensionless transfer factor `T(x) = PPFD(x) / PPFD_ref`. It provides relative spatial transport only. Before `PPFD_organ = PPFD_ref × T(x)` can be claimed, two explicit contracts must exist: (1) `AbsolutePPFDReference` defining the physical boundary (reference plane, location, time, spectral domain PAR 400–700, unit µmol/m²/s, provenance, uncertainty, source_type); and (2) a `TransferFactorContract` defining how LightField's `relative_normalized` values map to `T(x)` (normalization reference alignment, component handling direct/diffuse/reflected, orientation/occlusion adjustments). Without both, any scaling is unverified and risks inventing physical meaning from a synthetic normalization. 046O measured PPFD path remains the authoritative absolute source for now.

## 2. Research basis (supplied)
Hybrid FSPM (Q-B): absolute environmental PPFD + spatial transport → organ incident PPFD is defensible when reference and transfer are explicit. Ray-tracing FSPM gets absolute light via radiative transfer with optical properties; our repository lacks optical/radiative-transfer contracts, so Q-A unsupported. Measured PPFD (046O) can anchor absolute reference; LightField provides relative spatial variation; combining requires explicit contract, not arithmetic default.

## 3. Current LightField executable semantics (verified from 046Q audit)
- `LightComponents` / `LightSample`: `direct`, `diffuse`, `reflected`, `total` all `float ge=0 le=1`; `unit = "relative_normalized"`.
- Normalization note (contracts.py): "Relative intensity, NOT lux/PPFD; normalization = max expected direct + diffuse + reflected = 1.0 under clear daytime with full visibility."
- `LightField`: spatial grid (`regular_grid_horizontal`), `solar_reference`, `approximation_params`; no magnitude field; no spectral field.
- `approximation.py`: direct/diffuse/reflected computed via `sky_visibility`, `daylight_factor`, `reflectance` — all synthetic approximations, no physical solar irradiance input.
- `architecture_recompute.py`: provenance explicitly `coarse_orientation_aware=false; approximation=vertical_cylinder/regular_grid; no_optics_model; no_ppfd; relative_normalized_preserved`.
- No `W/m²`, `spectral_irradiance`, `photon_flux`, `radiance`, `DNI`, `DHI`, `Planck`, `wavelength` fields anywhere in `simulation/core/light/`.
- `OrganLightExposure` (physiology): `ppfd_value` requires `PPFDSource` (`umol_photons_m2_s`, `PAR_400_700`); `LightField relative_normalized must NOT masquerade as PPFD` (explicit contract prohibition).

## 4. Meaning of `relative_normalized` (Step 1/2)
Not a fraction of any physical reference. It is a synthetic normalization: the clearest daytime with full visibility = 1.0. At night = ~0; at partial sky = intermediate; under cloud = reduced; with reflection = added (possibly >1 after sum, since conservation not enforced). The value at a point represents relative visibility/modulation, not `PPFD(x)/PPFD_ref`. Therefore `T(x)` cannot be derived from it without redefining the normalization to a physical reference.

## 5. Transfer-factor eligibility (Step 2/3)
For `T(x)` to be valid: `T(x) = PPFD(x) / PPFD_ref` with explicit `PPFD_ref` (same spectral domain PAR 400–700, same time, same reference plane/context). Current LightField provides no `PPFD_ref`; normalization is synthetic; no guarantee that `total=1.0` at any point equals any physical PPFD; orientation/coarse occlusion means `direct` at a leaf surface may not correspond to actual direct PPFD at that surface. Therefore: NOT eligible as `T(x)` without contract.

## 6. Absolute reference requirements (Step 4/5)
Required `AbsolutePPFDReference` fields (minimum, derived from `PPFDSource` + spatial needs):
- `ref_id`, `value` (`float`, `umol_photons_m2_s`), `unit` fixed, `spectral_domain` (`PAR_400_700` or `EPAR_400_750`), `reference_location` (plane, height, garden coordinates +X East/+Y North/+Z Up), `timestamp` / `simulation_time_ref`, `source_type` (`MEASURED`/`SYNTHETIC`/`DERIVED_PHYSICALLY_VALID`/`MODELED`), `provenance`, `uncertainty` (optional but required for propagation), `status`.
- Reference plane: must match what `T(x)` would divide by. Options: open-sky reference plane above canopy (A); reference plane at garden z_height (C); local sensor plane (D). Must be explicitly chosen, not assumed.
- Component references: if scaling direct/diffuse separately, need `PPFD_direct_ref`, `PPFD_diffuse_ref`; if using total only, single `PPFD_ref` sufficient (but loses component separation).

## 7. Component implications (Step 5)
LightField separates `direct`/`diffuse`/`reflected` at sample. For independent component scaling: each needs its own reference PPFD from same temporal/spectral context. Most practical first step: single total reference (`PPFD_ref`) with `total_normalized` used as scalar `T(x)`. Component separation can come later with explicit component references and validated component transfer factors (future contract). Do NOT implement component scaling now — not enough evidence.

## 8. Reflection / composite (Step 6)
`total = direct + diffuse + reflected` can exceed 1 because normalization is per-component to clear-day max separately (not conserved). Reflection adds to total. This is acceptable for relative transport but means `total` cannot be interpreted as a fraction of incoming radiation without additional conservation modeling. No physical energy balance is claimed by current LightField.

## 9. Incident vs absorbed (Step 7)
LightField at sample is relative incident transport (direct from sun + diffuse from sky + reflected from surfaces). No optics, no leaf angle, no absorption coefficient, no APAR. Output must be incident PPFD (`OrganLightExposure.ppfd_value`, `exposure_type="incident"`). Absorbed PAR requires explicit optical contract (future) — not part of this audit.

## 10. 046O measured PPFD relation (Step 8, preserved)
Measured PPFD (`PPFDSource`) at a reference plane/time provides `PPFD_ref`. It can serve as:
- Absolute boundary input for hybrid Q-B (calibrate / anchor).
- Validation comparison for simulated organ PPFD after scaling.
- Not a substitute for spatial transport (measured at one point; LightField gives spatial pattern).
Must remain independent contract; not replaced by LightField. Future adapter: `LightField + PPFD_ref → OrganLightExposure.ppfd_value` only after transfer-factor contract validates.

## 11. Orientation limitation (Step 10)
`architecture_recompute.py` provenance: `coarse_orientation_aware=false; approximation=vertical_cylinder/regular_grid`. Leaves have different orientation from vertical cylinders; direct-ray occlusion depends on leaf normal vs sun direction; current occluder mapping approximates architecture as coarse cylinders/grid, not oriented surfaces. Thus `direct` at a leaf point from LightField may over/under-estimate actual direct PPFD independently of normalization. This limits defensibility of `T(x)` for leaves until orientation-aware occlusion + optics contract exists.

## 12. Uncertainty (Step 9, documented)
Both reference PPFD (measurement error, instrument calibration, temporal variability) and LightField (approximation error, coarse orientation, synthetic normalization, no spectral) contribute. Current contracts have no explicit uncertainty propagation model for LightField. Future adapter must document both sources; do not invent statistical model without contract.

## 13. Hybrid model comparison (Step 10 / Step 11)
- R-A (Global reference scaling): requires defensible `T(x)`; not ready (no transfer-factor contract; normalization undefined relative to physical reference; orientation coarse).
- R-B (Reference contract + transfer-factor contract): requires `AbsolutePPFDReference` + `TransferFactorContract` defining normalization alignment; supports current LightField + 046O; scientifically defensible when contracts validated; RECOMMENDED path.
- R-C (Component references): requires separate direct/diffuse reference PPFDs + validated component transfer; more complex; future after R-B.
- R-D (Full physical radiative transfer): requires optics, spectral, orientation-aware occlusion, conservation; not current scope; future architecture feedback possible.

## 14. Decision (B — REFERENCE_CONTRACT_FIRST) — with path to Q-B
B — REFERENCE_CONTRACT_FIRST. Do NOT implement `PPFD_organ = PPFD_ref × T(x)` yet. First: explicit `AbsolutePPFDReference` contract (define reference plane, value, spectral domain, provenance, uncertainty, status). Second: explicit `TransferFactorContract` (define `T(x)` semantics: how `relative_normalized` maps to physical ratio; whether total or component; orientation/optics adjustments; validation against 046O). Only after both contracts exist and are validated can hybrid Q-B operate. Current LightField remains relative transport only.

## 15. Required future contracts (explicit)
1. `AbsolutePPFDReference` — reference PPFD boundary (value, unit, spectral domain PAR 400–700, location/plane, timestamp, provenance, source_type, uncertainty, status).
2. `TransferFactorContract` — defines `T(x)` from `LightField` samples; aligns `relative_normalized` normalization to `PPFD_ref`; specifies component handling; documents orientation/coarse-approximation limitations; requires validation against 046O.
3. `LightFieldToOrganPPFD` adapter (optional, after 1+2): takes `LightField` + `AbsolutePPFDReference` + `TransferFactorContract`, produces `OrganLightExposure.ppfd_value` with `exposure_type="incident"` only; no absorption; provenance links both inputs.
4. `OrganLightExposure.absorption` only when separate optical contract exists (future; not now).

## 16. Files inspected (read, unchanged)
- `simulation/core/light/contracts.py` (LightComponents / LightSample / LightField)
- `simulation/core/light/approximation.py`
- `simulation/core/light/architecture_recompute.py`
- `simulation/core/light/field/contracts.py` / `compute.py`
- `simulation/core/physiology/organ_light_exposure.py`
- `simulation/core/physiology/ppfd_source.py`
- `simulation/core/photosynthesis/integration_contracts.py` / `photosynthesis_integration.py`
- `simulation/core/shadow/direct.py`, `shadow/model.py`
- `simulation/core/solar/model.py`, `solar/calculate.py`
- Existing fixtures/tests from 046M / 046O (referenced; not edited)
No upstream modifications; no PPFD conversion code created.

## 17. Tests / audits
Verified via source inspection (no new execution needed for contract audit): `relative_normalized` unit; `no_ppfd`; `coarse_orientation_aware=false`; `OrganLightExposure` forbids masquerade; `PPFDSource` requires absolute; 046O path intact. PYTEST_UNAVAILABLE reported honestly; no false test claims.

## 18. Limitations
- LightField normalization is synthetic (clear-day max = 1.0); not calibrated to any physical reference.
- Architecture occluder orientation coarse; leaf-level T(x) unreliable until orientation-aware model.
- No spectral data; fixed µmol/J unjustified.
- No explicit uncertainty model for LightField.
- Hybrid Q-B requires future contracts; not implemented now.
- Decision is B, not A — no arbitrary scaling permitted.
