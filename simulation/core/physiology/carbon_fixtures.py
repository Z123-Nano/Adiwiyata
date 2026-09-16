"""Synthetic carbon fixtures — TASK 021. Synthetic biomass; synthetic photosynthesis; labeled."""
from datetime import datetime, timezone
from simulation.core.physiology.photosynthesis_fixtures import SYNTH_PARAMS, SYNTH_PFD_MED
from simulation.core.physiology.photosynthesis import photosynthesis_rate
from simulation.core.physiology.respiration_contracts import RespirationInput, RespirationParams
from simulation.core.physiology.respiration import respiration_rate
from simulation.core.physiology.fixtures import SYNTH_STATE

# Synthetic biomass for respiration (explicit test example — not real)
SYNTH_BIOMASS_G_M2 = 2.5  # synthetic test fixture only

SYNTH_RESP_PARAMS = RespirationParams(
    name="synthetic_maintenance",
    maintenance_rate_per_biomass=1.2,  # μmol CO2 g^-1 s^-1 — synthetic placeholder; not calibrated
    source="synthetic_example",
    provenance="TASK_021 synthetic; maintenance coefficient placeholder; not species-specific",
    is_synthetic_example=True,
)

SYNTH_RESP_INPUT = RespirationInput(
    biomass_g_m2=SYNTH_BIOMASS_G_M2,
    temperature_c=25.0,
    organ_id="leaf-1",
    plant_id="plant-p1",
    timestamp=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc),
    provenance="synthetic_TASK_021",
    is_synthetic_example=True,
)

SYNTH_PHOTOSYN_RESULT = photosynthesis_rate(SYNTH_PFD_MED, SYNTH_PARAMS)
SYNTH_RESP_RESULT = respiration_rate(SYNTH_RESP_INPUT, SYNTH_RESP_PARAMS)
