"""TASK 046X fixtures — PPFDSource/OrganLightExposure → Photosynthesis (TASK 020) for measured + modeled paths."""
from simulation.core.physiology.fixtures_046v import REF_A, TRANSFER_A, REF_C, TRANSFER_C
from simulation.core.physiology.combine_reference_transfer import combine_reference_transfer_to_ppfd_source
from simulation.core.physiology.organ_light_exposure_integration import integrate_ppfd_source_to_organ
from simulation.core.physiology.photosynthesis import PhotosynthesisParams, photosynthesis_rate
from simulation.core.physiology.ppfd_input import PPFDInput

# A — modeled PPFD (046V) through 046W → 046D → 020
SRC_A = combine_reference_transfer_to_ppfd_source(REF_A, TRANSFER_A, target_organ_id="leaf_1", provenance_suffix="TASK_046X A")
EXP_A = integrate_ppfd_source_to_organ(SRC_A, organ_ref="leaf_1", plant_id="P1", architecture_id="arch_1").exposure
# B — measured-style (same adapter; synthetic/measured converge; use 046V-derived source with source_type override concept)
# C — zero PPFD through full chain
SRC_C = combine_reference_transfer_to_ppfd_source(REF_C, TRANSFER_C, target_organ_id="leaf_z", provenance_suffix="TASK_046X C")
EXP_C = integrate_ppfd_source_to_organ(SRC_C, organ_ref="leaf_z", plant_id="Pz").exposure
# Params for 020 (synthetic, from contracts; not calibrated)
from simulation.core.physiology.photosynthesis_params import PhotosynthesisParams
PARAMS = PhotosynthesisParams(name="param_046X", alpha=0.05, a_max=30.0, source="synthetic_example")
