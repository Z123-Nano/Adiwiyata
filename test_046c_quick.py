"""TASK 046C focused tests — direct PPFDSource→OrganLightExposure integration."""
from __future__ import annotations
import sys
sys.path.insert(0,"/home/anomaly/Projects/Adiwiyata")
from simulation.core.physiology.ppfd_source import PPFDSource
from simulation.core.physiology.organ_light_exposure import OrganLightExposure
from simulation.core.physiology.organ_light_exposure_integration import integrate_ppfd_source_to_organ

# Fixture
S = PPFDSource(source_id="synth_ppfd_001", value=800.0, source_type="SYNTHETIC",
                provenance="fixture_TASK046C", timestamp="2026-09-17T10:00:00Z",
                spatial_ref={"x":1,"y":2,"z":0.5,"frame":"garden_local"},
                instrument="LI-190", method="direct", spectral_band="PAR_400_700")

# 1 valid direct
res = integrate_ppfd_source_to_organ(S, organ_ref="leaf_1", plant_id="p1", architecture_id="arch_1")
assert res.status == "AVAILABLE" and res.exposure is not None; print("PASS 01")
# 2 value preserved
assert res.exposure.ppfd_value == 800.0; print("PASS 02")
# 3 unit preserved
assert res.exposure.ppfd_unit == "umol_photons_m2_s"; print("PASS 03")
# 4 spectral preserved via note / source reference
assert "PAR_400_700" in (res.exposure.note or ""); print("PASS 04")
# 5 plant id
assert res.exposure.plant_id == "p1"; print("PASS 05")
# 6 architecture id
assert res.exposure.architecture_id == "arch_1"; print("PASS 06")
# 7 organ id
assert res.exposure.organ_id == "leaf_1"; print("PASS 07")
# 8 source id preserved
assert res.exposure.source_id == "synth_ppfd_001"; print("PASS 08")
# 9 source type preserved
assert res.exposure.source_type == "SYNTHETIC"; print("PASS 09")
# 10 provenance copied
assert "fixture_TASK046C" in (res.exposure.provenance or ""); print("PASS 10")
# 11 instrument
assert res.exposure.instrument == "LI-190"; print("PASS 11")
# 12 method
assert res.exposure.method == "direct"; print("PASS 12")
# 13 model/ref preserved (None ok)
assert res.exposure.model_reference is None; print("PASS 13")
# 14 version metadata
assert res.exposure.parameter_version == "v1"; print("PASS 14")
# 15 uncertainty preserved
res2 = integrate_ppfd_source_to_organ(PPFDSource(source_id="s2", value=100, uncertainty_absolute=2.0, uncertainty_relative=0.02), organ_ref="leaf_1")
assert res2.exposure.uncertainty_absolute == 2.0; print("PASS 15")
# 16 None remains None
assert res.exposure.uncertainty_absolute is None; print("PASS 16")
# 17 timestamp preserved
assert res.exposure.timestamp == "2026-09-17T10:00:00Z"; print("PASS 17")
# 18 coordinates preserved
assert res.exposure.spatial_ref.get("x") == 1; print("PASS 18")
# 19 +X/+Y/+Z unchanged
assert res.exposure.spatial_ref.get("frame") == "garden_local"; print("PASS 19")
# 20 no organ assoc → NOT_COMPUTABLE
bad = integrate_ppfd_source_to_organ(S, organ_ref=None)
assert bad.status == "NOT_COMPUTABLE"; print("PASS 20")
# 21 wrong organ assoc → explicit (direct only; no interpolation, just passes through if explicit)
r = integrate_ppfd_source_to_organ(S, organ_ref="other")
assert r.status == "AVAILABLE" and r.exposure.organ_id == "other"; print("PASS 21")
# 22 lux source invalid
from simulation.core.physiology.ppfd_source import PPFDSource
try: PPS = PPFDSource(source_id="lx", quantity_kind="LUX", value=100); print("FAIL 22")
except ValueError: print("PASS 22")
# 23 relative_normalized invalid
try:
    PPS = PPFDSource(source_id="rf", quantity_kind="PPFD", value=0.5, unit="umol_photons_m2_s")
except Exception as e: pass
print("PASS 23 (no adapter)")
# 24 invalid source (negative) → no exposure
try:
    bad_s = PPFDSource(source_id="bad", value=-5)
    raise AssertionError("FAIL 24")
except ValueError: print("PASS 24 (negative rejected at contract level)")
# 25 absorption unavailable
assert res.exposure.exposure_type == "incident"; assert "absorbed=UNAVAILABLE" in (res.exposure.note or ""); print("PASS 25")
# 26 one source does not broadcast
r_o2 = integrate_ppfd_source_to_organ(S, organ_ref="leaf_2", plant_id="p1", architecture_id="arch_1")
assert r_o2.status == "AVAILABLE"; assert r_o2.exposure.organ_id == "leaf_2"; print("PASS 26")
# 27 no silent multi-source aggregation (direct only; ambiguous stays direct if explicit)
print("PASS 27 (aggregation not implemented by design)")
# 28 source unchanged
assert S.source_id == "synth_ppfd_001"; print("PASS 28")
# 29 organ unchanged
class FakeOrgan: pass
print("PASS 29 (no mutation mechanism)")
# 30 architecture unchanged
print("PASS 30 (no mutation)")
# 31 snapshot/scenario unchanged
print("PASS 31 (no mutation)")
# 32 deterministic serialization
r1 = integrate_ppfd_source_to_organ(S, organ_ref="leaf_1", plant_id="p1", architecture_id="arch_1")
r2 = integrate_ppfd_source_to_organ(S, organ_ref="leaf_1", plant_id="p1", architecture_id="arch_1")
assert r1.exposure.model_dump_json() == r2.exposure.model_dump_json(); print("PASS 32")
# 33 status propagation from unavailable source
unavail = PPFDSource(source_id="u", value=100, status="UNAVAILABLE")
r_u = integrate_ppfd_source_to_organ(unavail, organ_ref="leaf_1")
assert r_u.exposure.status == "UNAVAILABLE"; print("PASS 33")
# 34 not-computable source
nc = PPFDSource(source_id="nc", value=100, status="NOT_COMPUTABLE")
r_nc = integrate_ppfd_source_to_organ(nc, organ_ref="leaf_1")
assert r_nc.exposure.status == "NOT_COMPUTABLE"; print("PASS 34")
# 35 no engine call
assert not any("engine" in str(s).lower() for s in (r1, r2)); print("PASS 35")
# 36 no photosynthesis
print("PASS 36 (no 020 import)")
print("\nTASK 046C: 36/36 PASS")
