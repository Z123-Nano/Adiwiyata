"""TASK 046Y fixtures — audit of integrated carbon boundary (g_C_per_timestep)."""
from simulation.core.photosynthesis.photosynthesis import PhotosynthesisResult

# A — synthetic integrated carbon (known value, known timestep)
RESULT_A = PhotosynthesisResult(
    gross_carbon_g=12.5,
    ppfd_input=500.0,
    unit="g_C_per_timestep",
    timestep=3600.0,
    status="AVAILABLE",
    provenance="TASK_046Y synthetic A integrated",
    is_synthetic_example=True,
    note="Audit: integrated g_C for 3600s timestep; rate not required",
)
# B — zero integrated carbon
RESULT_B = PhotosynthesisResult(
    gross_carbon_g=0.0,
    ppfd_input=0.0,
    unit="g_C_per_timestep",
    timestep=3600.0,
    status="AVAILABLE",
    provenance="TASK_046Y synthetic B zero",
    is_synthetic_example=True,
)
# C — non-zero with different timestep (timestep preserved, value scaled by contract, not by us)
RESULT_C = PhotosynthesisResult(
    gross_carbon_g=6.25,
    ppfd_input=250.0,
    unit="g_C_per_timestep",
    timestep=1800.0,
    status="AVAILABLE",
    provenance="TASK_046Y synthetic C timestep_1800",
    is_synthetic_example=True,
)
