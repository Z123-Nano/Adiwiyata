"""TASK 046W fixtures — synthetic PPFDSource → OrganLightExposure via existing integrate_ppfd_source_to_organ."""
from simulation.core.physiology.fixtures_046v import REF_A, TRANSFER_A, REF_C, TRANSFER_C
from simulation.core.physiology.combine_reference_transfer import combine_reference_transfer_to_ppfd_source
from simulation.core.physiology.organ_light_exposure_integration import integrate_ppfd_source_to_organ

# A — modeled PPFD (046V) → exposure; valid
SRC_A = combine_reference_transfer_to_ppfd_source(REF_A, TRANSFER_A, target_organ_id="leaf_1", provenance_suffix="TASK_046W A")
# B — measured-style (use same source with source_type override to MEASURED for path test)
# C — zero
SRC_C = combine_reference_transfer_to_ppfd_source(REF_C, TRANSFER_C, target_organ_id="leaf_z", provenance_suffix="TASK_046W C")
# D — identity mismatch source (use SRC_A with different organ_ref to test adapter behavior)
