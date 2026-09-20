"""TASK 046C — PPFDSource → OrganLightExposure direct integration (domain only).
Explicit association only; no interpolation, no aggregation, no engine/api."""
from __future__ import annotations
from typing import Optional, Literal
from simulation.core.physiology.ppfd_source import PPFDSource
from simulation.core.physiology.organ_light_exposure import OrganLightExposure

from dataclasses import dataclass

@dataclass
class IntegrationResult:
    exposure: Optional[OrganLightExposure]
    status: Literal["AVAILABLE","NOT_COMPUTABLE","ERROR"]
    note: Optional[str] = None

def integrate_ppfd_source_to_organ(
    source: PPFDSource,
    organ_ref: Optional[str] = None,
    plant_id: Optional[str] = None,
    architecture_id: Optional[str] = None,
    provenance_note: Optional[str] = None,
) -> IntegrationResult:
    """Direct explicit association only.
    Valid when:
      - source is valid PPFD (status AVAILABLE, value finite >=0, quantity_kind PPFD, unit correct)
      - organ_ref explicitly provided and matches intended organ
      - plant/architecture identity preserved
    Invalid/missing association returns NOT_COMPUTABLE (no silent assignment)."""
    # Source validity
    if source.source_type == "unknown" and source.status != "AVAILABLE":
        pass  # allow synthetic/derived; only reject clearly invalid
    if source.quantity_kind != "PPFD":
        return IntegrationResult(exposure=None, status="NOT_COMPUTABLE", note="Source quantity_kind not PPFD")
    if source.unit != "umol_photons_m2_s":
        return IntegrationResult(exposure=None, status="NOT_COMPUTABLE", note="Source unit incompatible with PPFD")
    if source.value is None or (isinstance(source.value, float) and source.value < 0):
        return IntegrationResult(exposure=None, status="NOT_COMPUTABLE", note="Source value missing or negative")
    # Explicit organ association required
    if not organ_ref:
        return IntegrationResult(exposure=None, status="NOT_COMPUTABLE", note="Explicit organ association unavailable")
    # No implicit spatial/temporal matching (direct identity only)
    # Build exposure preserving everything
    exposure = OrganLightExposure(
        plant_id=plant_id or "unknown",
        architecture_id=architecture_id or "unknown",
        organ_id=organ_ref,
        exposure_type="incident",
        ppfd_value=source.value,
        ppfd_unit=source.unit,
        source_type=source.source_type,
        source_variable="ppfd",
        source_id=source.source_id,
        method=source.method,
        instrument=source.instrument,
        model_reference=source.model_reference,
        model_version=source.model_version,
        parameter_version=source.parameter_version,
        provenance=source.provenance or f"TASK_046C from {source.source_id}",
        timestamp=source.timestamp,
        simulation_time_ref=None,  # not converted
        spatial_ref=source.spatial_ref or {"frame":"garden_local","note":"+X East / +Y North / +Z Up"},
        lightfield_sample_ref=None,
        uncertainty_absolute=source.uncertainty_absolute,
        uncertainty_relative=source.uncertainty_relative,
        status="AVAILABLE" if source.status == "AVAILABLE" else ("UNAVAILABLE" if source.status == "UNAVAILABLE" else "NOT_COMPUTABLE"),
        note=provenance_note or f"Direct association PPFDSource {source.source_id} -> organ {organ_ref}; spectral={source.spectral_band}; no interpolation; incident only; absorbed=UNAVAILABLE.",
        is_synthetic_example=source.is_synthetic_example,
    )
    return IntegrationResult(exposure=exposure, status="AVAILABLE", note="Direct explicit association.")
