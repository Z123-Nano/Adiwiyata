"""Photosynthesis model — TASK 020. Rectangular hyperbola (light-response); documented; synthetic params only.
Equation: A(PPFD) = (alpha * Amax * PPFD) / (alpha * PPFD + Amax)
Source form: standard non-rectangular/rectangular hyperbola light-response approximation (see e.g. classic photosynthesis modeling references); used as structural prototype only.
Not calibrated; not species-specific; parameters synthetic.
Units: PPFD = μmol photons m^-2 s^-1; A = μmol CO2 m^-2 s^-1.
No lux→PPFD; no respiration in equation (separate process deferred).
"""
from __future__ import annotations
from simulation.core.physiology.ppfd_input import PPFDInput
from simulation.core.physiology.photosynthesis_params import PhotosynthesisParams
from simulation.core.physiology.contracts import PhotosynthesisResult

# Parameter provenance documented at module level
PARAM_PROVENANCE = "Synthetic/example parameters for TASK 020 prototype; not calibrated; not species-specific; source: standard light-response form reference (structural prototype only)."

def photosynthesis_rate(pfd: PPFDInput, params: PhotosynthesisParams) -> PhotosynthesisResult:
    """Compute gross assimilation rate from PPFD input using rectangular hyperbola."""
    if pfd.ppfd < 0:
        return PhotosynthesisResult(
            status="INVALID_INPUT",
            gross_assimilation=None,
            limiting_factors=["negative_ppfd"],
            input_ref=pfd.source,
            provenance="TASK_020; invalid PPFD rejected",
            notes="Negative PPFD is physically invalid.",
            is_synthetic_example=pfd.is_synthetic_example,
        )
    # Equation: A = (alpha * Amax * PPFD) / (alpha * PPFD + Amax)
    numerator = params.alpha * params.a_max * pfd.ppfd
    denominator = params.alpha * pfd.ppfd + params.a_max
    # Denominator > 0 because alpha>=0, Amax>=0, PPFD>=0 and not both zero at valid inputs
    if denominator <= 0:
        return PhotosynthesisResult(
            status="INVALID_INPUT",
            gross_assimilation=None,
            limiting_factors=["invalid_parameters"],
            provenance="TASK_020; denominator <= 0",
            notes="Parameter combination invalid.",
        )
    a_gross = numerator / denominator
    # At PPFD=0 => 0; saturation as PPFD->inf => Amax; monotonic increasing for PPFD>=0
    # Limitation: only light modeled; temperature/CO2 not_modelled
    return PhotosynthesisResult(
        status="VALID",
        gross_assimilation=round(a_gross, 6),
        limiting_factors=["light_modeled", "temperature_not_modelled", "co2_not_modelled"],
        input_ref=pfd.source,
        provenance=f"TASK_020; equation=rectangular_hyperbola; params_source={params.source}; {PARAM_PROVENANCE}",
        assumptions=["light-response only; respiration separate process"],
        notes=f"PPFD={pfd.ppfd} μmol photons m^-2 s^-1; Amax={params.a_max}; alpha={params.alpha}.",
        is_synthetic_example=params.is_synthetic_example or pfd.is_synthetic_example,
    )
