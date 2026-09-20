"""TASK 046O — Measured PPFD → PPFDSource → OrganLightExposure adapter.
Explicit only; no conversion from lux/relative_normalized/LightField.
Requires explicit organ_ref; no spatial interpolation; no broadcast.
Reuses 046B PPFDSource + 046C integration directly.
"""
from __future__ import annotations
from typing import Optional
from datetime import datetime
from simulation.core.contracts.domain import Measurement
from simulation.core.physiology.ppfd_source import PPFDSource
from simulation.core.physiology.organ_light_exposure_integration import integrate_ppfd_source_to_organ
from simulation.core.physiology.organ_light_exposure_integration import IntegrationResult

def ppfd_measurement_to_exposure(
    measurement: Measurement,
    organ_ref: Optional[str],
    plant_id: Optional[str] = None,
    architecture_id: Optional[str] = None,
    provenance_suffix: Optional[str] = None,
) -> IntegrationResult:
    """Explicit path: validated Measurement → PPFDSource (046B) → OrganLightExposure (046C).
    No implied spatial/organ inference; organ_ref required explicitly.
    Rejects non-PPFD measurements, invalid units, negative/NaN/inf values."""
    # Step 1 — variable must be PPFD
    if measurement.variable != "PPFD":
        return IntegrationResult(
            exposure=None, status="NOT_COMPUTABLE",
            note=f"Measurement variable '{measurement.variable}' not PPFD; lux/relative_normalized rejected."
        )
    # Step 2 — unit must be umol_photons_m2_s (exact; no silent relabel)
    if measurement.unit != "umol_photons_m2_s":
        return IntegrationResult(
            exposure=None, status="NOT_COMPUTABLE",
            note=f"Measurement unit '{measurement.unit}' not umol_photons_m2_s; no conversion."
        )
    # Step 3 — value must be finite, non-negative
    import math
    if measurement.value is None or not isinstance(measurement.value, (int, float)):
        return IntegrationResult(
            exposure=None, status="NOT_COMPUTABLE",
            note="Measurement value missing or non-numeric."
        )
    v = float(measurement.value)
    if not math.isfinite(v):
        return IntegrationResult(
            exposure=None, status="NOT_COMPUTABLE",
            note="Measurement PPFD not finite (NaN/inf); rejected."
        )
    if v < 0:
        return IntegrationResult(
            exposure=None, status="NOT_COMPUTABLE",
            note=f"Measurement PPFD negative ({v}); instant PPFD must be >=0."
        )
    # Step 3 — explicit organ association required (not spatial inference)
    if not organ_ref:
        return IntegrationResult(
            exposure=None, status="NOT_COMPUTABLE",
            note="Explicit organ association unavailable; no nearest-neighbor / spatial interpolation."
        )
    # Step 5 — build PPFDSource (046B) preserving all explicit metadata
    ppfd = PPFDSource(
        source_id=measurement.id,
        quantity_kind="PPFD",
        value=v,
        unit="umol_photons_m2_s",
        spectral_band="PAR_400_700",
        source_type="SYNTHETIC" if measurement.is_synthetic_example else "MEASURED",
        timestamp=measurement.timestamp.isoformat() if isinstance(measurement.timestamp, datetime) else (measurement.timestamp or None),
        timezone=None,
        spatial_ref=measurement.spatial_ref if measurement.spatial_ref else None,
        uncertainty_absolute=measurement.uncertainty,
        uncertainty_relative=None,
        instrument=measurement.instrument,
        method=measurement.method,
        calibration_ref=measurement.calibration_ref,
        calibration_version=None,
        model_reference=None,
        model_version=None,
        parameter_version="v1",
        status="AVAILABLE",
        provenance=(measurement.provenance or f"TASK_046O from measurement {measurement.id}") + (f"; {provenance_suffix}" if provenance_suffix else ""),
        note=(measurement.notes or "") + "; TASK_046O explicit measured PPFD; not derived from LightField.",
        is_synthetic_example=measurement.is_synthetic_example,
    )
    # Step 6 — integrate via 046C canonical (direct identity, no interpolation)
    result = integrate_ppfd_source_to_organ(
        source=ppfd,
        organ_ref=organ_ref,
        plant_id=plant_id,
        architecture_id=architecture_id,
        provenance_note=f"TASK_046O from measurement {measurement.id}; explicit organ_ref={organ_ref}; preserved source_type={ppfd.source_type}; no LightField conversion.",
    )
    return result
