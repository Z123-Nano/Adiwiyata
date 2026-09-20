# TASK 046Q — Physical LightField → Absolute PPFD Audit & Contract Decision
Status: TASK_046Q_B — ABSOLUTE_REFERENCE_INPUT_REQUIRED (LightField is relative-normalized transport only; needs explicit absolute boundary — measured PPFD from 046O or physical radiometric input — before organ incident PPFD can be computed; no arithmetic conversion invented; 046O path preserved; all upstream contracts unchanged).
Date: 2026-09-18; Mode: LOCAL/OFFLINE; executable source = truth; no web/search.

## 1. Executive verdict (B)
LightField produces only relative-normalized spatial transport (`direct`/`diffuse`/`reflected`/`total` in [0,1]; `unit = "relative_normalized"`; normalization = max expected = 1.0). It has no absolute radiometric magnitude, no spectral data, no photon-flux basis, no optics model, and coarse orientation awareness (`coarse_orientation_aware=false`). Therefore it CANNOT produce absolute organ-level incident PPFD (`µmol photons m^-2 s^-1`) without an explicit absolute boundary input. Decision: B — ABSOLUTE_REFERENCE_INPUT_REQUIRED. Hybrid target architecture (Q-B): keep relative LightField + add explicit absolute reference (measured PPFD via 046O or physical solar input) to derive organ PPFD. No arbitrary conversion invented; measured PPFD path (046O) preserved intact; no upstream modifications.

## 2. Research basis (supplied)
PPFD = incident photon flux density (400–700 nm), absolute (`µmol photons m^-2 s^-1`); radiometric-to-photon conversion requires explicit spectral basis; FSPM uses architecture → light interception → photosynthesis with absolute PPFD at organ; relative intensity alone is insufficient for physiological photosynthesis. Used for framing only; no external claims.

## 3. LightField executable architecture (verified, unmodified)
- Contract: `LightComponents` / `LightSample` (`simulation/core/light/contracts.py` lines 6–15)
- Fields: `direct`, `diffuse`, `reflected` [0,1]; `total` = sum; `unit = "relative_normalized"`; note: "Relative intensity, NOT lux/PPFD; normalization = max expected direct + diffuse + reflected = 1.0"
- `LightField`: `extent_*`, `resolution`, `samples`, `sampling_strategy = "regular_grid_horizontal"`, `solar_reference`, `approximation_params`; no magnitude, no spectral, no photon fields.
- `approximation.py`: direct / diffuse / reflected approximated (sky visibility, daylight factor, reflection coeff); all [0,1]; no absolute scaling.
- `architecture_recompute.py`: architecture → occluder mapping (`derive_occluder_set`) → existing `compute_lightfield`; provenance notes `coarse_orientation_aware=false; approximation=vertical_cylinder/regular_grid; no_optics_model; no_ppfd; relative_normalized_preserved`.
- `compute_lightfield`: pure integration; no radiative-transfer magnitude computation.

## 4. Units / quantities audit (Step 1/Step 4)
Every LightField quantity classified:
- `direct`: C — normalized relative (fraction of max clear-day direct)
- `diffuse`: C — normalized relative
- `reflected`: C — normalized relative
- `total`: C — normalized relative (sum; may exceed 1 if overlaps; not conserved absolute)
- `unit`: explicitly `"relative_normalized"`
- No field: W/m², spectral irradiance, photon flux, PPFD, PAR, wavelength, Planck, spectral power distribution, solar irradiance, DNI, DHI, radiance, radiant flux.
- Absolute physical quantities: ABSENT.

## 5. Absolute-vs-relative audit
No absolute radiometric source exists in LightField pipeline. Normalization uses clear-day maximum = 1.0. Cannot derive PPFD from relative values without external absolute reference (e.g., measured clear-day PPFD at reference plane, or physical solar irradiance with spectral conversion). No calibration coefficient defined.

## 6. Spectral audit (Step 8)
No spectral information: no wavelength distribution, no PAR weighting, no photon-energy spectrum, no fixed conversion factor (e.g., 2.02 µmol/J) justifiable. Broadband relative intensity cannot be converted to photon flux without spectral basis. Explicit limitation documented.

## 7. Incident vs absorbed audit (Step 7)
LightField at sample gives relative incident transport (direct + diffuse + reflected), not absorbed. `OrganLightExposure` (line 6–21 `organ_light_exposure.py`) defines `exposure_type: "incident" | "absorbed" | "not_computable"`; `ppfd_value` requires valid PPFD source (`umol_photons_m2_s`); `absorption` only if explicit absorption input/model provided (not invented). LightField must NOT be passed to `ppfd_value` (contract explicitly forbids: "LightField relative_normalized or lux must NOT masquerade as PPFD").

## 8. Direct / diffuse / reflected / occlusion audit (Step 6)
Transport geometry present: direct (solar + shadow), diffuse (approximation), reflected (approximation), occlusion via architecture-derived occluders (`derive_occluder_set`). Surface orientation: COARSE (`coarse_orientation_aware=false`; vertical cylinder / regular grid approximation); no orientation-aware radiative transfer. Surface optics: NONE (`no_optics_model`). Radiation conservation: NOT asserted (relative sum can exceed 1; no incoming-flux balance). So: transport yes, physical magnitude no, orientation approximate, optics absent.

## 9. 046O measured PPFD relationship (Step 9, preserved)
Path: `measured PPFD` → `PPFDSource` (`ppfd_source.py`) → `OrganLightExposure` (`ppfd_value` in `umol_photons_m2_s`, `spectral_band = "PAR_400_700"`) → `Photosynthesis` (via `photosynthesis_integration_contracts` / `photosynthesis_integration.py`). LightField must NOT replace this. Measured PPFD remains the authoritative absolute source for physiology; LightField provides spatial transport variation only (relative). Hybrid Q-B uses relative LightField + absolute reference (046O or physical input) to compute organ incident PPFD.

## 10. Architectural model comparison (Step 10)
- Q-A (Absolute physical light model): requires full radiative-transfer with spectral input, absolute magnitude, orientation-aware optics, conservation — NOT supported by current executable.
- Q-B (Hybrid calibration): relative LightField (transport) + explicit absolute boundary input (measured PPFD or physical solar) → organ PPFD. Supported by existing contracts; requires only adding absolute reference input to LightField pipeline (not redesigning LightField itself). RECOMMENDED target.
- Q-C (Measured-only): restricts physiology to measured points only; simpler but loses spatial interpolation from LightField. Viable but more restrictive than Q-B.

## 11. Required absolute input (Step 5)
Minimum: one of:
- `PPFDSource` (measured `umol photons m^-2 s^-1`, PAR 400–700) at reference point / time; or
- Physical solar irradiance (`W m^-2`) + spectral basis + photon-conversion model (explicit, calibrated) at reference.
Then: `organ_ppfd = reference_ppfd × light_sample.total` (with appropriate geometry/orientation/optics adjustments if added later). Currently: no such scaling exists; reference must be explicitly provided.

## 12. Scientific invariants preserved
- PPFD = absolute incident photon flux (`µmol photons m^-2 s^-1`); never relative-normalized.
- `lux → PPFD`: no conversion (no spectral basis, no photometric definition for plant PAR).
- `relative LightField → PPFD`: no direct conversion (no absolute baseline).
- `W/m² → PPFD`: requires spectral basis; not present.
- `absorbed PAR → incident PPFD`: must not map without optical model.
- 046O path untouched; `OrganLightExposure.ppfd_value` requires valid PPFD source — never from LightField.

## 13. Decision (B)
B — ABSOLUTE_REFERENCE_INPUT_REQUIRED.
LightField is relative-normalized spatial transport; it can remain so; to derive absolute organ incident PPFD, an explicit absolute boundary input (measured PPFD via 046O or physical radiometric input with spectral basis) must be supplied; no arbitrary multiplier or conversion invented; 046O path preserved; Q-B is target architecture.

## 14. Required future contract (explicit, not invented)
- `AbsolutePPFDReference` / `LightFieldAbsoluteInput` contract: defines reference PPFD source (`PPFDSource` or physical solar with spectral conversion), reference location/time, scaling method to LightField samples (direct/diffuse/reflected components), and validation against 046O measured data.
- `LightFieldToPPFD` adapter: reads `LightSample.total` (relative) and applies `reference_ppfd * total` (with orientation/optics adjustments if future model adds them); produces `OrganLightExposure.ppfd_value` only when source is `DERIVED_PHYSICALLY_VALID` with explicit provenance.
- Do NOT redesign `LightField` itself (relative transport contract correct); add absolute input contract separately.
- Spectral contract if physical solar input used (wavelength distribution → photon conversion factor explicitly derived, not fixed).

## 15. Files inspected (read, unchanged)
- `simulation/core/light/contracts.py` (LightComponents / LightSample / LightField)
- `simulation/core/light/approximation.py`
- `simulation/core/light/architecture_recompute.py`
- `simulation/core/light/field/contracts.py` (LightField / LightSample)
- `simulation/core/light/field/compute.py`
- `simulation/core/physiology/organ_light_exposure.py` (OrganLightExposure — incident only; absorbed needs explicit model)
- `simulation/core/physiology/ppfd_source.py` (PPFDSource — absolute µmol/m²/s)
- `simulation/core/physiology/photosynthesis_integration_contracts.py` / `photosynthesis_integration.py`
- `simulation/core/physiology/photosynthesis_params.py` / `photosynthesis.py`
- `simulation/core/shadow/direct.py`, `shadow/model.py`
- `simulation/core/solar/model.py` / `solar/calculate.py`
- Related fixtures/tests (046M, 046O, light validation) — referenced, not edited.
No upstream edits.

## 16. Files changed
Report only: `TASK_046Q_PHYSICAL_PPFD_AUDIT.md`. No code modifications.

## 17. Tests / audits
Reused existing light/PPFD fixtures and contracts; verified `unit = "relative_normalized"`; verified `OrganLightExposure` forbids masquerade; verified `PPFDSource` requires absolute; verified 046O path intact; verified `architecture_recompute` provenance notes `no_ppfd; relative_normalized_preserved`. No new assertions needed (audit of existing contracts sufficient); PYTEST_UNAVAILABLE reported.

## 18. Limitations
- LightField is intentionally approximation/relative; converting to absolute requires external reference not yet defined.
- Architecture occluder orientation is coarse; full radiative transfer not claimed.
- No spectral data; fixed conversion factor unjustified.
- Measured PPFD calibration dataset not yet defined for spatial interpolation (future work).
- Decision does not implement Q-A (full physical model) because repository lacks spectral/optical/absolute inputs; Q-B is appropriate intermediate.
