"""TASK 046P-B-FIX2 fixtures — executable TASK 020 output: gross_carbon_g = g_C/timestep."""
from __future__ import annotations
from simulation.core.photosynthesis.photosynthesis import PhotosynthesisResult
from simulation.core.physiology.photosynthesis_integration_contracts import PhotosynthesisIntegrationContext

PHOTO_SYNTH_01 = PhotosynthesisResult(
    result_id="photo-syn-01",
    gross_carbon_g=0.00432396,  # executable synthetic output; g_C/timestep (verified)
    ppfd_input=500.0,
    unit="g_C_per_timestep",
    timestep=3600.0,
    status="AVAILABLE",
    provenance="TASK_020 synthetic; gross_carbon_g verified as g_C_per_timestep.",
    parameter_version="v1",
    note="Synthetic TASK 020 output; already integrated; no area/time multiplication.",
    is_synthetic_example=True,
    input_ref="fixture_046p_01",
)

# Future rate-integration context (STEP 6 separate; NOT used on current path)
INTEGRATION_CTX_01 = PhotosynthesisIntegrationContext(
    organ_id="leaf_1",
    organ_photosynthetic_area_m2=0.01,
    elapsed_seconds=3600.0,
    carbon_molar_mass_g_per_mol=12.011,
    carbon_basis="ELEMENTAL_CARBON",
    source="TASK_046P-B-FIX2 future rate contract (not current path)",
    provenance="Explicit; only for future actual rate input; rejected if g_C/timestep input.",
    parameter_version="v1",
    is_synthetic_example=True,
)

EXPECTED_G_C_01 = 0.00432396  # verified from executable semantics; no multiplication
INTEGRATION_CTX_BAD_AREA = PhotosynthesisIntegrationContext(
    organ_id="leaf_bad", organ_photosynthetic_area_m2=0.0, elapsed_seconds=3600.0,
    source="TASK_046P-B-FIX2 synthetic (invalid future only)", is_synthetic_example=True,
)
