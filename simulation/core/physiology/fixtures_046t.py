"""TASK 046T fixtures — synthetic AbsolutePPFDReference + SpatialPPFDTransferFactor."""
from simulation.core.physiology.absolute_ppfd_reference import build_absolute_ppfd_reference
from simulation.core.physiology.spatial_ppfd_transfer_factor import build_spatial_ppfd_transfer

# A — valid positive reference (measured-like)
REF_A = build_absolute_ppfd_reference("ref_A", 1200.0, reference_geometry="GARDEN_REFERENCE_PLANE", reference_geometry_note="Horizontal reference plane at z=0.5m, open garden", provenance="TASK_046T synthetic A measured", source_type="MEASURED", is_synthetic_example=True)
# B — valid synthetic reference (for calibration/anchoring)
REF_B = build_absolute_ppfd_reference("ref_B", 850.0, reference_geometry="ABOVE_CANOPY", provenance="TASK_046T synthetic B synthetic", source_type="SYNTHETIC", is_synthetic_example=True)
# C — zero reference (boundary case; denominator zero — transfer invalid; reference itself valid at 0)
REF_C = build_absolute_ppfd_reference("ref_C", 0.0, reference_geometry="OPEN_SKY", provenance="TASK_046T synthetic C zero", source_type="SYNTHETIC", is_synthetic_example=True)
# D — transfer with valid reference (total, synthetic example)
TRANSFER_D = build_spatial_ppfd_transfer("tx_D", "ref_A", lightfield_id="lf_046M_1", transfer_value=0.75, component="total", transfer_definition="Explicit anchoring: PPFD_ref=1200 at garden plane; LightField relative_normalized aligned to same condition; coarse_orientation_aware documented; no arbitrary multiplier.", provenance="TASK_046T synthetic D", is_synthetic_example=True)
# E — transfer with zero denominator reference (ref_C at 0 — must be rejected at use, not at reference; reference valid at 0, transfer invalid because denom=0)
TRANSFER_E = build_spatial_ppfd_transfer("tx_E", "ref_C", lightfield_id="lf_046M_1", transfer_value=0.0, component="total", transfer_definition="Explicit anchoring with zero-denom reference; invalid for transfer.", provenance="TASK_046T synthetic E", is_synthetic_example=True)
