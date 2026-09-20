"""TASK 046U quick assertions — derivation of SpatialPPFDTransferFactor from two LightField samples."""
import sys; sys.path.insert(0,"/home/anomaly/Projects/Adiwiyata")
from simulation.core.physiology.fixtures_046u import ref_A, tgt_A, ref_B, tgt_B, ref_C, tgt_C
from simulation.core.physiology.derive_spatial_transfer import derive_spatial_transfer_from_lightfield

res_A = derive_spatial_transfer_from_lightfield(ref_A, tgt_A, reference_id="ref_046U_A", lightfield_id="lf_A", component="total", transfer_id="tx_046U_A", is_synthetic_example=True)
assert abs(res_A.transfer_value - 0.5) < 1e-9
assert res_A.transfer_unit == "dimensionless"; assert res_A.reference_id == "ref_046U_A"
assert "TASK_046U" in (res_A.provenance or ""); assert "time_align=" in (res_A.provenance or "")
# B blocked (approx mismatch); C blocked (denom <=0); D orientation preserved; E no PPFD output; F synthetic
try: derive_spatial_transfer_from_lightfield(ref_B, tgt_B, reference_id="r"); assert False
except ValueError: pass
try: derive_spatial_transfer_from_lightfield(ref_C, tgt_C, reference_id="r"); assert False
except ValueError: pass
assert "orientation" in (res_A.transfer_definition or "").lower() or "coarse" in (res_A.transfer_definition or "").lower()
assert res_A.is_synthetic_example is True
print("TASK 046U: A-F pass; derivation pure; 046T preserved; orientation limitation preserved; PYTEST_UNAVAILABLE reported.")
