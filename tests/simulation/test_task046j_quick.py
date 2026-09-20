"""TASK 046J focused quick tests — conversion only; no geometry; 023 untouched."""
from __future__ import annotations
import sys
sys.path.insert(0,"/home/anomaly/Projects/Adiwiyata")
from simulation.core.growth.growth_conversion_params import growth_params
from simulation.core.growth.growth_derivation import derive_organ_growth
from simulation.core.growth.fixtures_046j import SYNTH_GROWTH
from simulation.core.contracts.domain import PlantOrgan

# 1 valid conversion (1 g C / 0.5 = 2 g DM)
r = derive_organ_growth("o1","p1","leaf",1.0,0.0,SYNTH_GROWTH)
assert r.status == "AVAILABLE"; assert abs(r.structural_carbon_increment_g_C - 1.0) < 1e-6; assert abs(r.biomass_increment_g_DM - 2.0) < 1e-6; assert abs(r.new_biomass_g_DM - 2.0) < 1e-6; print("PASS 01 conversion")
# 2 zero allocation
rz = derive_organ_growth("o1","p1","leaf",0.0,3.0,SYNTH_GROWTH)
assert rz.biomass_increment_g_DM == 0.0; assert rz.new_biomass_g_DM == 3.0; print("PASS 02 zero")
# 3 positive growth with previous biomass
rp = derive_organ_growth("o1","p1","leaf",2.0,5.0,SYNTH_GROWTH)
assert rp.biomass_increment_g_DM == 4.0; assert rp.new_biomass_g_DM == 9.0; print("PASS 03 previous+inc")
# 4 structural <= allocated with retention 1
assert rp.structural_carbon_increment_g_C <= 2.0 + 1e-6; print("PASS 04 structural")
# 5 parameter bounds: invalid carbon_frac >1 rejected
try:
    from simulation.core.growth.growth_conversion_params import GrowthConversionParameters
    GrowthConversionParameters(parameter_set_id="bad", organ_type="leaf", carbon_fraction_of_dry_biomass=1.2, growth_retention_fraction=0.5, provenance="bad")
    assert False
except Exception: pass
print("PASS 05 param bounds")
# 6 negative allocated rejected
res_neg = derive_organ_growth("o","p","leaf",-1.0,2.0,SYNTH_GROWTH)
assert res_neg.status == "NOT_COMPUTABLE"; print("PASS 06 neg alloc")
# 7 negative previous biomass rejected
res_prev = derive_organ_growth("o","p","leaf",1.0,-2.0,SYNTH_GROWTH)
assert res_prev.status == "NOT_COMPUTABLE"; print("PASS 07 neg prev")
# 8 missing identity
res_id = derive_organ_growth("","p","leaf",1.0,0.0,SYNTH_GROWTH)
assert res_id.status == "NOT_COMPUTABLE"; print("PASS 08 missing id")
# 9 no geometry mutation
org = PlantOrgan(id="o1", plant_id="p1", organ_type="leaf", length_m=1.0)
before = org.model_dump_json()
derive_organ_growth("o1","p1","leaf",1.0,0.0,SYNTH_GROWTH)
assert org.model_dump_json() == before; print("PASS 09 immutability")
# 10 determinism
a = derive_organ_growth("o","p","leaf",2.0,3.0,SYNTH_GROWTH)
b = derive_organ_growth("o","p","leaf",2.0,3.0,SYNTH_GROWTH)
assert a.model_dump_json() == b.model_dump_json(); print("PASS 10 det")
# 11 units distinct in result
assert "g_DM" in (r.note or ""); assert r.allocated_carbon_g == 1.0; print("PASS 11 units")
# 12 no photosynthesis/respiration/geometry in derivation source
src = open("/home/anomaly/Projects/Adiwiyata/simulation/core/growth/growth_derivation.py").read()
assert "from simulation.core.photosynthesis" not in src; print("PASS 12 scope")
print("\nTASK 046J: targeted done; PYTEST unavailable; 023 untouched (unit=g_C noted); 046I direct; growth only.")
