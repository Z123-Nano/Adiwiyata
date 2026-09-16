"""Synthetic photosynthesis fixtures — TASK 020. Synthetic PPFD; synthetic params; labeled."""
from datetime import datetime, timezone
from simulation.core.physiology.ppfd_input import PPFDInput
from simulation.core.physiology.photosynthesis_params import PhotosynthesisParams

SYNTH_PARAMS = PhotosynthesisParams(
    name="synthetic_example_leaf",
    a_max=25.0,  # μmol CO2 m^-2 s^-1 — synthetic placeholder
    alpha=0.05,  # mol CO2 / mol photons — synthetic placeholder
    rd_ref=None,  # respiration separate; not in equation
    source="synthetic_example",
    provenance="TASK_020 synthetic placeholder; not calibrated; not species-specific; source form: standard light-response reference",
    uncertainty="not_modelled",
    notes="Parameters for prototype only. Not validated against real leaf data.",
    is_synthetic_example=True,
)

SYNTH_PFD_ZERO = PPFDInput(ppfd=0.0, unit="umol_photons_m2_s", timestamp=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc), source="synthetic", provenance="TASK_020 synthetic zero PPFD", is_synthetic_example=True)
SYNTH_PFD_LOW = PPFDInput(ppfd=50.0, unit="umol_photons_m2_s", timestamp=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc), source="synthetic", provenance="TASK_020 synthetic low PPFD", is_synthetic_example=True)
SYNTH_PFD_MED = PPFDInput(ppfd=200.0, unit="umol_photons_m2_s", timestamp=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc), source="synthetic", provenance="TASK_020 synthetic medium PPFD", is_synthetic_example=True)
SYNTH_PFD_HIGH = PPFDInput(ppfd=1000.0, unit="umol_photons_m2_s", timestamp=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc), source="synthetic", provenance="TASK_020 synthetic high PPFD", is_synthetic_example=True)
