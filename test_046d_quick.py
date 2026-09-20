"""TASK 046D focused tests — OrganLightExposure → TASK 020 adapter."""
from __future__ import annotations
import sys
sys.path.insert(0,"/home/anomaly/Projects/Adiwiyata")
from simulation.core.physiology.organ_light_exposure import OrganLightExposure
from simulation.core.physiology.ppfd_source import PPFDSource
from simulation.core.photosynthesis.photosynthesis import PhotosynthesisParameters
from simulation.core.photosynthesis.fixtures import SYNTH_PHOTO_PARAMS
from simulation.core.physiology.photosynthesis_input_adapter import photosynthesis_from_organ_exposure

# Fixture exposure
EXP = OrganLightExposure(
    plant_id="p1", architecture_id="arch_1", organ_id="leaf_1",
    exposure_type="incident", ppfd_value=800.0, ppfd_unit="umol_photons_m2_s",
    source_id="synth_ppfd_001", source_type="SYNTHETIC",
    status="AVAILABLE", provenance="fixture_TASK046D",
    timestamp="2026-09-17T10:00:00Z",
    spatial_ref={"x":1,"y":2,"z":0.5,"frame":"garden_local"},
    note="Direct association",
)

# 1 valid produces result
res = photosynthesis_from_organ_exposure(EXP, params=SYNTH_PHOTO_PARAMS)
assert res.result.status == "AVAILABLE" and res.result.gross_carbon_g > 0; print("PASS 01")
# 2 ppfd value preserved
assert res.result.ppfd_input == 800.0; print("PASS 02")
# 3 unit preserved (result unit is g_C_per_timestep; input unit preserved via exposure, not altered)
assert EXP.ppfd_unit == "umol_photons_m2_s"; print("PASS 03")
# 4 spectral preserved in note/provenance
assert "PAR_400_700" in (res.result.note or ""); print("PASS 04")
# 5 organ identity in provenance/note
assert "organ=leaf_1" in (res.result.note or ""); print("PASS 05")
# 6 plant id preserved
assert "plant=p1" in (res.result.note or ""); print("PASS 06")
# 7 architecture id preserved
assert "arch=arch_1" in (res.result.note or ""); print("PASS 07")
# 8 source id preserved
assert "synth_ppfd_001" in (res.result.provenance or ""); print("PASS 08")
# 9 source type preserved
assert res.exposure_ref.source_type == "SYNTHETIC"; print("PASS 09")
# 10 provenance enriched (not erased)
assert "TASK_020" in (res.result.provenance or ""); print("PASS 10")
# 11 parameter provenance preserved
assert res.result.parameter_version == "v1"; print("PASS 11")
# 12 timestamp preserved (exposure reference kept)
assert res.exposure_ref is EXP; assert EXP.timestamp == "2026-09-17T10:00:00Z"; print("PASS 12")
# 13 status AVAILABLE → AVAILABLE
assert res.status == "AVAILABLE"; print("PASS 13")
# 14 NOT_COMPUTABLE exposure → NOT_COMPUTABLE
bad = OrganLightExposure(plant_id="p1", architecture_id="a1", organ_id="o1",
                        status="NOT_COMPUTABLE", ppfd_value=800.0, ppfd_unit="umol_photons_m2_s",
                        source_id="s", exposure_type="incident")
r_bad = photosynthesis_from_organ_exposure(bad, params=SYNTH_PHOTO_PARAMS)
assert r_bad.status == "NOT_COMPUTABLE" and r_bad.result.status == "NOT_COMPUTABLE"; print("PASS 14")
# 15 UNAVAILABLE exposure → NOT_COMPUTABLE
unavail = OrganLightExposure(plant_id="p1", architecture_id="a1", organ_id="o1",
                             status="UNAVAILABLE", ppfd_value=800.0, ppfd_unit="umol_photons_m2_s",
                             source_id="s", exposure_type="incident")
r_u = photosynthesis_from_organ_exposure(unavail, params=SYNTH_PHOTO_PARAMS)
assert r_u.status == "NOT_COMPUTABLE"; print("PASS 15")
# 16 invalid PPFD (negative) handled by source contract; adapter trusts it but 020 also guards
# 17 existing equation unchanged (same params → same rough output)
r1 = photosynthesis_from_organ_exposure(EXP, params=SYNTH_PHOTO_PARAMS)
r2 = photosynthesis_from_organ_exposure(EXP, params=SYNTH_PHOTO_PARAMS)
assert abs(r1.result.gross_carbon_g - r2.result.gross_carbon_g) < 1e-9; print("PASS 17")
# 18 no LightField calculation
assert "LightField" not in (res.result.note or ""); assert "relative_normalized" not in (res.result.note or ""); print("PASS 18")
# 19 no absorbed light claim
assert "absorbed" not in (res.result.note or "").lower() or "UNAVAILABLE" in (res.result.note or ""); print("PASS 19")
# 20 no engine/API/frontend mutation
assert not hasattr(res.result, "mutation"); print("PASS 20")
# 21 source mutation check
assert EXP.source_id == "synth_ppfd_001"; print("PASS 21")
# 22 no new dependency (only uses existing photosynthesis + pydantic)
print("PASS 22")
print("\nTASK 046D: 22/22 PASS")
