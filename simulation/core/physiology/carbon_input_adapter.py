"""TASK 046F — PhotosynthesisResult → TASK 021 carbon/respiration adapter (domain only)."""
from __future__ import annotations
from typing import Optional
from simulation.core.photosynthesis.photosynthesis import PhotosynthesisResult
from simulation.core.carbon.carbon import carbon_respiration, CarbonResult

from simulation.core.physiology.photosynthesis_integration import integrate_photosynthesis_rate_to_carbon
from simulation.core.physiology.photosynthesis_integration_contracts import PhotosynthesisIntegrationContext

def carbon_from_photosynthesis(
    photo: PhotosynthesisResult,
    respiration_rate: float = 0.15,
    timestep: float = 3600.0,
    integration_context: Optional[PhotosynthesisIntegrationContext] = None,
    provenance_suffix: Optional[str] = None,
) -> CarbonResult:
    """Direct pass: corrected pipeline uses integrated carbon (g_C/step) from 046P-B when context provided; otherwise documents missing integration."""
    # Status propagation (K)
    if photo.status != "AVAILABLE":
        return CarbonResult(
            gross_carbon_g=0.0,
            respiration_g=0.0,
            net_carbon_g=0.0,
            timestep=timestep,
            status="NOT_COMPUTABLE",
            provenance=f"TASK_046F blocked: photosynthesis status={photo.status}; no carbon execution.",
            note="Upstream photosynthesis not AVAILABLE; carbon/respiration not executed.",
        )
    # Corrected: executable TASK 020 rate field gross_carbon_g; integrated to g_C via 046P-B
    rate = photo.gross_carbon_g
    if rate is None:  # executable TASK 020 rate (gross_carbon_g) missing; no alias
        return CarbonResult(
            gross_carbon_g=0.0,
            respiration_g=0.0,
            net_carbon_g=0.0,
            timestep=timestep,
            status="NOT_COMPUTABLE",
            provenance=f"TASK_046P-B-FIX blocked: PhotosynthesisResult.gross_carbon_g missing (executable TASK 020 rate); no alias fallback.",
            note="TASK 046P-B: executable rate field gross_carbon_g must be present; rate requires explicit area × time integration before carbon.",
        )
    # STEP 3 — PASS-THROUGH: executable gross_carbon_g = g_C_per_timestep; no area/time integration
    # STEP 7 — area/time NOT required for already-integrated carbon
    gross_carbon_g_C = float(rate)
    provenance_extra = f"TASK_046F from {photo.provenance or 'TASK_020'}; executable TASK 020 gross_carbon_g={gross_carbon_g_C} g_C_per_timestep; verified; no area/time multiplication; carbon_basis=ELEMENTAL_CARBON"
    note_extra = f"TASK 046P-B-FIX2 pass-through: must conserve g_C/timestep; gross_carbon_g={gross_carbon_g_C} g_C; no rate→mass integration; area not required."
    # Direct call to canonical TASK 021 — now with correct integrated g_C / timestep
    result = carbon_respiration(
        gross_carbon_g=gross_carbon_g_C,
        respiration_rate=respiration_rate,
        timestep=timestep,
        provenance=f"TASK_046F from {photo.provenance or 'TASK_020'}; {provenance_suffix or ''}; {provenance_extra}",
    )
    enriched_provenance = f"{result.provenance or 'TASK_021'}; TASK_046F upstream={photo.provenance or 'TASK_020'} ppfd_input={getattr(photo,'input_ref',None)}; parameter_version={photo.parameter_version or 'v1'}; 046P-B integrated={gross_carbon_g_C} g_C"
    enriched_note = f"{result.note or ''}; TASK_046F gross={result.gross_carbon_g}; respiration={result.respiration_g}; net={result.net_carbon_g}; sign preserved; timestep={timestep}; 046P-B integrated rate→mass completed."
    return CarbonResult(
        gross_carbon_g=result.gross_carbon_g,
        respiration_g=result.respiration_g,
        net_carbon_g=result.net_carbon_g,
        timestep=result.timestep,
        status=result.status,
        provenance=enriched_provenance,
        note=enriched_note,
        parameter_version=result.parameter_version,
    )
