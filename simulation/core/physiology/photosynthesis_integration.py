"""TASK 046P-B — Pure integration: photosynthesis rate → carbon mass.
Explicit area × time; explicit carbon mass conversion (12.011); no inference.
Reads executable TASK 020 rate field gross_carbon_g; distinguishes rate from integrated gross_carbon_g_C."""
from __future__ import annotations
from typing import Optional
from simulation.core.photosynthesis.photosynthesis import PhotosynthesisResult
from simulation.core.physiology.photosynthesis_integration_contracts import (
    PhotosynthesisIntegrationContext, IntegratedPhotosyntheticCarbon,
)

def integrate_photosynthesis_rate_to_carbon(
    photo: PhotosynthesisResult,
    context: PhotosynthesisIntegrationContext,
    result_id: Optional[str] = None,
) -> IntegratedPhotosyntheticCarbon:
    # STEP 6 — future rate-integration: reject if input is already integrated g_C
    if getattr(photo, "unit", None) == "g_C_per_timestep" or (hasattr(photo, "gross_carbon_g") and photo.gross_carbon_g > 0 and getattr(photo, "ppfd_input",None) is None):
        return IntegratedPhotosyntheticCarbon(
            result_id=result_id or "int_rejected",
            organ_id=context.organ_id,
            gross_assimilation_rate_umol_co2_m2_s=0.0,
            organ_photosynthetic_area_m2=context.organ_photosynthetic_area_m2,
            elapsed_seconds=context.elapsed_seconds,
            gross_co2_amount_umol=0.0, carbon_molar_mass_g_per_mol=context.carbon_molar_mass_g_per_mol,
            gross_carbon_g_C=0.0, carbon_basis="ELEMENTAL_CARBON", timestep=context.elapsed_seconds,
            status="NOT_COMPUTABLE",
            provenance="TASK_046P-B-FIX2 blocked: input is already integrated g_C_per_timestep (gross_carbon_g); rate integration not applicable.",
            note="Rate-integration requires actual rate input (µmol/m²/s), not g_C/timestep. Separate future contract only.",
            is_synthetic_example=context.is_synthetic_example,
        )
    """Pure derivation: rate [umol/m2/s] × area [m2] × time [s] = umol CO2 → g_C."""
    # Step 5 — validate area
    if context.organ_photosynthetic_area_m2 <= 0 or not isinstance(context.organ_photosynthetic_area_m2, (int, float)):
        import math
        if math.isnan(context.organ_photosynthetic_area_m2) or math.isinf(context.organ_photosynthetic_area_m2) or context.organ_photosynthetic_area_m2 <= 0:
            return IntegratedPhotosyntheticCarbon(
                result_id=result_id or f"int_{context.organ_id}",
                organ_id=context.organ_id, gross_assimilation_rate_umol_co2_m2_s=0.0,
                organ_photosynthetic_area_m2=context.organ_photosynthetic_area_m2,
                elapsed_seconds=context.elapsed_seconds,
                gross_co2_amount_umol=0.0, carbon_molar_mass_g_per_mol=context.carbon_molar_mass_g_per_mol,
                gross_carbon_g_C=0.0, carbon_basis="ELEMENTAL_CARBON", timestep=context.elapsed_seconds,
                status="NOT_COMPUTABLE",
                provenance="TASK_046P-B blocked: area must be >0 and finite; no inference.",
                note="Invalid area input.",
                is_synthetic_example=context.is_synthetic_example,
            )
    # Step 6 — validate elapsed time
    if context.elapsed_seconds <= 0 or not isinstance(context.elapsed_seconds, (int, float)):
        import math
        if math.isnan(context.elapsed_seconds) or math.isinf(context.elapsed_seconds) or context.elapsed_seconds <= 0:
            return IntegratedPhotosyntheticCarbon(
                result_id=result_id or f"int_{context.organ_id}",
                organ_id=context.organ_id,
                gross_assimilation_rate_umol_co2_m2_s=photo.gross_carbon_g,
                organ_photosynthetic_area_m2=context.organ_photosynthetic_area_m2,
                elapsed_seconds=context.elapsed_seconds,
                gross_co2_amount_umol=0.0, carbon_molar_mass_g_per_mol=context.carbon_molar_mass_g_per_mol,
                gross_carbon_g_C=0.0, carbon_basis="ELEMENTAL_CARBON", timestep=context.elapsed_seconds,
                status="NOT_COMPUTABLE",
                provenance="TASK_046P-B blocked: elapsed_seconds must be >0 and finite.",
                note="Invalid timestep input.",
                is_synthetic_example=context.is_synthetic_example,
            )
    # Step 7 — validate photosynthesis rate (canonical field)
    rate = photo.gross_carbon_g
    if rate is None:
        return IntegratedPhotosyntheticCarbon(
            result_id=result_id or f"int_{context.organ_id}",
            organ_id=context.organ_id,
            gross_assimilation_rate_umol_co2_m2_s=0.0,
            organ_photosynthetic_area_m2=context.organ_photosynthetic_area_m2,
            elapsed_seconds=context.elapsed_seconds,
            gross_co2_amount_umol=0.0, carbon_molar_mass_g_per_mol=context.carbon_molar_mass_g_per_mol,
            gross_carbon_g_C=0.0, carbon_basis="ELEMENTAL_CARBON", timestep=context.elapsed_seconds,
            status="NOT_COMPUTABLE",
            provenance="TASK_046P-B blocked: gross_carbon_g missing from PhotosynthesisResult (model rate field); adapter field mismatch documented.",
            note="PhotosynthesisResult.gross_carbon_g required (executable TASK 020 rate field).",
            is_synthetic_example=context.is_synthetic_example,
        )
    if rate is None:
        return IntegratedPhotosyntheticCarbon(
            result_id=result_id or f"int_{context.organ_id}",
            organ_id=context.organ_id,
            gross_assimilation_rate_umol_co2_m2_s=0.0,
            organ_photosynthetic_area_m2=context.organ_photosynthetic_area_m2,
            elapsed_seconds=context.elapsed_seconds,
            gross_co2_amount_umol=0.0, carbon_molar_mass_g_per_mol=context.carbon_molar_mass_g_per_mol,
            gross_carbon_g_C=0.0, carbon_basis="ELEMENTAL_CARBON", timestep=context.elapsed_seconds,
            status="NOT_COMPUTABLE",
            provenance="TASK_046P-B-FIX blocked: gross_carbon_g (executable TASK 020 rate) is None.",
            note="Executable TASK 020 rate field gross_carbon_g missing; no fallback alias.",
            is_synthetic_example=context.is_synthetic_example,
        )
    try:
        rate_f = float(rate)
    except Exception:
        rate_f = 0.0
    import math
    if not math.isfinite(rate_f) or rate_f < 0:
        return IntegratedPhotosyntheticCarbon(
            result_id=result_id or f"int_{context.organ_id}",
            organ_id=context.organ_id,
            gross_assimilation_rate_umol_co2_m2_s=rate_f,
            organ_photosynthetic_area_m2=context.organ_photosynthetic_area_m2,
            elapsed_seconds=context.elapsed_seconds,
            gross_co2_amount_umol=0.0, carbon_molar_mass_g_per_mol=context.carbon_molar_mass_g_per_mol,
            gross_carbon_g_C=0.0, carbon_basis="ELEMENTAL_CARBON", timestep=context.elapsed_seconds,
            status="NOT_COMPUTABLE",
            provenance="TASK_046P-B blocked: rate not finite/non-negative.",
            note="Invalid photosynthesis rate.",
            is_synthetic_example=context.is_synthetic_example,
        )
    # Step 8 — dimensional conversion (explicit, documented)
    co2_amount_umol = rate_f * float(context.organ_photosynthetic_area_m2) * float(context.elapsed_seconds)
    carbon_mass_g = co2_amount_umol * float(context.carbon_molar_mass_g_per_mol) * 1e-6
    # Explicit basis documentation
    return IntegratedPhotosyntheticCarbon(
        result_id=result_id or f"int_{context.organ_id}_{int(context.elapsed_seconds)}",
        organ_id=context.organ_id,
        gross_assimilation_rate_umol_co2_m2_s=round(rate_f, 6),
        organ_photosynthetic_area_m2=float(context.organ_photosynthetic_area_m2),
        elapsed_seconds=float(context.elapsed_seconds),
        gross_co2_amount_umol=round(co2_amount_umol, 6),
        carbon_molar_mass_g_per_mol=float(context.carbon_molar_mass_g_per_mol),
        gross_carbon_g_C=round(carbon_mass_g, 6),
        carbon_basis="ELEMENTAL_CARBON",
        timestep=float(context.elapsed_seconds),
        status="AVAILABLE",
        provenance=f"TASK_046P-B; rate_x_area_x_time; carbon_molar_mass={context.carbon_molar_mass_g_per_mol}; basis=ELEMENTAL_CARBON; area_explicit; no_inference; input_ref={getattr(photo,'input_ref','unknown')}",
        note=f"Rate={rate_f} umol/m2/s; area={context.organ_photosynthetic_area_m2} m2; time={context.elapsed_seconds} s; CO2={co2_amount_umol} umol; C={carbon_mass_g} g_C/step; no g_CO2 used.",
        is_synthetic_example=context.is_synthetic_example,
    )
