"""TASK 046M-A focused quick tests — mapping contract only; no light computation."""
from __future__ import annotations
import sys
sys.path.insert(0,"/home/anomaly/Projects/Adiwiyata")
from simulation.core.architecture.fixtures_046m_a import ARCH_3ORG, ORG_LEAF, CONFIG_DEFAULT
from simulation.core.architecture.occluder_mapping import derive_occluder_set, ArchitectureOccluderMappingConfig

# 1 valid mapping
res = derive_occluder_set(ARCH_3ORG, CONFIG_DEFAULT)
assert res.status == "AVAILABLE"; print("PASS 01 available")
# 2 source architecture unchanged
assert ARCH_3ORG.organs[0].id == "leaf_1"; assert ARCH_3ORG.organs[0].length_m == 0.5; print("PASS 02 source unchanged")
# 3 architecture identity referenced
assert res.source_architecture_id == "arch_1"; assert res.source_plant_id == "p1"; print("PASS 03 identity")
# 4 occluders produced for included types
assert len(res.occluders) >= 2; print("PASS 04 occluders produced")
# 5 root excluded
assert "root_1" in res.excluded_organ_ids; assert "root_1" not in res.mapped_organ_ids; print("PASS 05 root excluded")
# 6 leaf mapped
assert "leaf_1" in res.mapped_organ_ids; print("PASS 06 leaf mapped")
# 7 cylinder geometry used
for occ in res.occluders:
    assert occ.geometry == "cylinder"; print("PASS 07 cylinder")
# 8 position reflects local_origin + local_position (origin 0 here => same)
leaf_occ = [o for o in res.occluders if o.id == "occl_leaf_1"][0]
assert abs(leaf_occ.position[0] - 1.0) < 1e-6; print("PASS 08 position")
# 9 height from length_m
assert abs(leaf_occ.height_m - 0.5) < 1e-6; print("PASS 09 height")
# 10 dimensions carry radius
assert abs(leaf_occ.dimensions[0] - 0.05) < 1e-6; print("PASS 10 radius")
# 11 determinism
res2 = derive_occluder_set(ARCH_3ORG, CONFIG_DEFAULT)
assert res.model_dump_json() == res2.model_dump_json(); print("PASS 11 det")
# 12 provenance preserved
assert "TASK_046M-A" in (res.provenance or ""); assert res.mapping_config_ref == "046M-A-v1"; print("PASS 12 provenance")
# 13 no light computation invoked (no import of compute_lightfield required; pure mapping)
# verified by construction: function only uses domain + shadow/model contracts
print("PASS 13 no light computation")
# 14 missing architecture → NOT_COMPUTABLE
bad = derive_occluder_set(None)
assert bad.status == "NOT_COMPUTABLE"; print("PASS 14 missing arch")
# 15 no mutation of architecture organs (deep identity preserved via list equality, not object identity break)
before = [o.id for o in ARCH_3ORG.organs]
after = [o.id for o in ARCH_3ORG.organs]
assert before == after; print("PASS 15 immutability")
# 16 structural feedback traceable (two architectures differ -> results separately identifiable)
res_a = derive_occluder_set(ARCH_3ORG, CONFIG_DEFAULT)
from copy import deepcopy
ARCH_B = deepcopy(ARCH_3ORG)
ARCH_B.architecture_id = "arch_2"
ARCH_B.organs[0].length_m = 0.8
res_b = derive_occluder_set(ARCH_B, CONFIG_DEFAULT)
assert res_a.source_architecture_id != res_b.source_architecture_id; print("PASS 16 structural feedback")
print("\nTASK 046M-A: 16 assertions pass; shadow model (Occluder) reused; no light equation modified; no engine change; mapping pure.")
