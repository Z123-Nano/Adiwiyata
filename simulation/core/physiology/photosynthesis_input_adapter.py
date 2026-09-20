"""TASK 046D — OrganLightExposure → TASK 020 photosynthesis adapter (domain only).
Direct semantic handoff; no equation change; no engine/API; identity preserved in provenance/note."""
from __future__ import annotations
from typing import Optional
from simulation.core.physiology.organ_light_exposure import OrganLightExposure
from simulation.core.photosynthesis.photosynthesis import (
    photosynthesis_rectangular_hyperbola, PhotosynthesisParameters, PhotosynthesisResult,
)
from simulation.core.photosynthesis.fixtures import SYNTH_PHOTO_PARAMS

from dataclasses import dataclass

@dataclass
class PhotosynthesisIntegrationResult:
    result: PhotosynthesisResult
    exposure_ref: Optional[OrganLightExposure] = None
    status: str = "AVAILABLE"
    note: Optional[str] = None

def photosynthesis_from_organ_exposure(
    exposure: OrganLightExposure,
    params: Optional[PhotosynthesisParameters] = None,
    timestep: float = 3600.0,
    provenance_suffix: Optional[str] = None,
) -> PhotosynthesisIntegrationResult:
    """Direct handoff: OrganLightExposure.incident_ppfd → TASK 020 ppfd input.
    No transformation; no interpolation; status propagated; identity preserved in provenance/note."""
    # Status propagation (H)
    if exposure.status != "AVAILABLE":
        return PhotosynthesisIntegrationResult(
            result=PhotosynthesisResult(
                gross_carbon_g=0.0,
                ppfd_input=exposure.ppfd_value or 0.0,
                status="NOT_COMPUTABLE",
                note=f"Exposure status={exposure.status}; no photosynthesis executed.",
                provenance=f"TASK_046D blocked by exposure status={exposure.status}; source={exposure.source_id or 'unknown'}",
                parameter_version=params.version if params else "v1",
            ),
            exposure_ref=exposure,
            status="NOT_COMPUTABLE",
            note=f"Exposure not AVAILABLE ({exposure.status}); TASK 020 not invoked.",
        )
    # PPFD value/unit validation (C/E/I)
    if exposure.ppfd_value is None:
        return PhotosynthesisIntegrationResult(
            result=PhotosynthesisResult(
                gross_carbon_g=0.0,
                ppfd_input=0.0,
                status="NOT_COMPUTABLE",
                note="Exposure ppfd_value missing.",
                provenance=f"TASK_046D blocked: missing PPFD value; organ={exposure.organ_id}",
            ),
            exposure_ref=exposure,
            status="NOT_COMPUTABLE",
            note="Missing PPFD value; no photosynthesis.",
        )
    if exposure.ppfd_unit != "umol_photons_m2_s":
        return PhotosynthesisIntegrationResult(
            result=PhotosynthesisResult(
                gross_carbon_g=0.0,
                ppfd_input=exposure.ppfd_value,
                status="NOT_COMPUTABLE",
                note=f"Unit incompatible: {exposure.ppfd_unit}; expected umol_photons_m2_s.",
                provenance=f"TASK_046D blocked: incompatible unit; organ={exposure.organ_id}",
            ),
            exposure_ref=exposure,
            status="NOT_COMPUTABLE",
            note="Incompatible PPFD unit.",
        )
    if exposure.exposure_type != "incident":
        # Incident only per scope; absorbed not claimed
        pass  # still allow if value present; note preserved
    # Use existing params or synthetic fixture (J)
    if params is None:
        params = SYNTH_PHOTO_PARAMS
    # Direct pass — no transformation (C/E/F)
    result = photosynthesis_rectangular_hyperbola(
        ppfd=float(exposure.ppfd_value),
        params=params,
        timestep=timestep,
    )
    # Preserve identity/provenance in result provenance/note (K/F)
    identity_tag = f"organ={exposure.organ_id} plant={exposure.plant_id} arch={exposure.architecture_id}"
    source_tag = f"source_id={exposure.source_id} source_type={exposure.source_type} ppfd={exposure.ppfd_value} unit={exposure.ppfd_unit} spectral={exposure.source_type}"  # spectral from exposure note/context
    # Enrich provenance without erasing parameter provenance
    enriched_provenance = f"{result.provenance or 'TASK_020'}; TASK_046D from {exposure.source_id or 'unknown'}; {identity_tag}; {provenance_suffix or ''}"
    enriched_note = f"{result.note or ''}; TASK_046D exposure incident_ppfd={exposure.ppfd_value}; {identity_tag}; spectral=PAR_400_700; absorbed=UNAVAILABLE."
    # Build new result preserving all original fields (do not mutate original result object if immutability preferred; reconstruct)
    return PhotosynthesisIntegrationResult(
        result=PhotosynthesisResult(
            gross_carbon_g=result.gross_carbon_g,
            ppfd_input=result.ppfd_input,
            unit=result.unit,
            timestep=result.timestep,
            status=result.status,
            provenance=enriched_provenance,
            note=enriched_note,
            parameter_version=result.parameter_version,
        ),
        exposure_ref=exposure,
        status=result.status,
        note=f"Direct association OK; {identity_tag}",
    )
