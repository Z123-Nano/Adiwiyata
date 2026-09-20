"""TASK 046V fixtures — synthetic AbsolutePPFDReference + SpatialPPFDTransferFactor → PPFDSource."""
from simulation.core.physiology.absolute_ppfd_reference import build_absolute_ppfd_reference
from simulation.core.physiology.spatial_ppfd_transfer_factor import build_spatial_ppfd_transfer
from simulation.core.physiology.combine_reference_transfer import combine_reference_transfer_to_ppfd_source

REF_A = build_absolute_ppfd_reference("ref_A_046V", 1000.0, reference_geometry="GARDEN_REFERENCE_PLANE", source_type="MEASURED", provenance="TASK_046V A measured", is_synthetic_example=False)
TRANSFER_A = build_spatial_ppfd_transfer("tx_A_046V", "ref_A_046V", lightfield_id="lf_A", transfer_value=0.5, component="total", provenance="TASK_046V A", is_synthetic_example=True)
# B — T=1.5
TRANSFER_B = build_spatial_ppfd_transfer("tx_B_046V", "ref_A_046V", lightfield_id="lf_B", transfer_value=1.5, component="total", provenance="TASK_046V B", is_synthetic_example=True)
# C — reference = 0, T=0.5
REF_C = build_absolute_ppfd_reference("ref_C_046V", 0.0, reference_geometry="OPEN_SKY", source_type="SYNTHETIC", provenance="TASK_046V C synthetic zero", is_synthetic_example=True)
TRANSFER_C = build_spatial_ppfd_transfer("tx_C_046V", "ref_C_046V", lightfield_id="lf_C", transfer_value=0.5, provenance="TASK_046V C", is_synthetic_example=True)
# D — T=0
TRANSFER_D = build_spatial_ppfd_transfer("tx_D_046V", "ref_A_046V", lightfield_id="lf_D", transfer_value=0.0, provenance="TASK_046V D", is_synthetic_example=True)
# E — negative reference (should produce NOT_COMPUTABLE via adapter; but reference contract blocks negative; use synthetic negative only if allowed — ref validator rejects, so skip direct; handled by adapter if called with invalid)
# K — geometry mismatch (explicit incompatible; adapter requires reference_geometry_compatible=False)
REF_K = build_absolute_ppfd_reference("ref_K_046V", 500.0, reference_geometry="ABOVE_CANOPY", provenance="TASK_046V K", is_synthetic_example=True)
TRANSFER_K = build_spatial_ppfd_transfer("tx_K_046V", "ref_K_046V", lightfield_id="lf_K", transfer_value=0.8, provenance="TASK_046V K", is_synthetic_example=True)
# M — target organ preserved
# N — provenance preserved (check result.provenance)
# O — synthetic labeling preserved (REF_A is measured, fixtures synthetic labeled)
# P — uncertainty preserved (REF_A no uncertainty; can add)
REF_U = build_absolute_ppfd_reference("ref_U_046V", 800.0, uncertainty=40.0, provenance="TASK_046V U", is_synthetic_example=True)
TRANSFER_U = build_spatial_ppfd_transfer("tx_U_046V", "ref_U_046V", lightfield_id="lf_U", transfer_value=0.6, provenance="TASK_046V U", is_synthetic_example=True)
