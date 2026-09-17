"""TASK 020 fixtures — explicit synthetic; not calibration."""
from simulation.core.photosynthesis.photosynthesis import PhotosynthesisParameters

SYNTH_PHOTO_PARAMS = PhotosynthesisParameters(
    alpha=0.05,
    pmax=12.0,
    provenance="synthetic_example_TASK_020; not calibrated; parameter version v1",
    source="fixture",
)

# Valid PPFD fixture (synthetic, clearly labeled — not measured garden PPFD)
SYNTH_PPFD = 800.0  # umol/m2/s — synthetic fixture
