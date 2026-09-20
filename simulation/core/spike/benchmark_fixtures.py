"""TASK 031 benchmark fixtures — synthetic, deterministic, labeled.
Cases A-D per spec. No real botanical claims.
"""
from simulation.core.contracts.domain import PlantArchitecture, PlantOrgan
from pydantic import BaseModel, Field; from typing import List, Optional, Literal

def _make_organ(i: int, plant_id: str, parent_id: Optional[str], pos: list, typ: str, length: float = 0.05, radius: float = 0.005) -> PlantOrgan:
    return PlantOrgan(
        id=f"o-{plant_id}-{i}", plant_id=plant_id, organ_type=typ,
        parent_organ_id=parent_id, local_position=pos,
        orientation=[0.0, 0.0, 1.0], length_m=length, radius_m=radius,
        status="synthetic", provenance="TASK_031 benchmark", is_synthetic_example=True,
    )

def bench_small() -> PlantArchitecture:
    # ~100 organs: simple branched tree of depth ~3
    p = "p-small"
    organs = [_make_organ(0, p, None, [0,0,0], "root", 0.05, 0.005)]
    # 4 branches × 6 levels = 24 stems + 72 leaves ≈ 100
    for b in range(4):
        stem = _make_organ(1+b, p, "o-p-small-0", [0.1*b, 0, 0.05], "stem", 0.08, 0.003)
        organs.append(stem)
        for l in range(6):
            leaf = _make_organ(5+b*6+l, p, stem.id, [0.02*b, 0, 0.08+0.05*l], "leaf", 0.03, 0.001)
            organs.append(leaf)
    return PlantArchitecture(architecture_id="arch-"+p, plant_id=p, organs=organs, provenance="TASK_031 A small ~100", is_synthetic_example=True)

def bench_medium() -> PlantArchitecture:
    # ~1,000 organs: 10 branches × 10 levels × 10 leaves ≈ 100 + 900
    p = "p-medium"
    organs = [_make_organ(0, p, None, [0,0,0], "root", 0.05, 0.005)]
    for b in range(10):
        s = _make_organ(1+b, p, "o-p-medium-0", [0.05*b, 0, 0.05], "stem", 0.08, 0.003)
        organs.append(s)
        for l in range(10):
            sub = _make_organ(11+b*10+l, p, s.id, [0.02*b, 0, 0.08+0.05*l], "branch", 0.06, 0.002)
            organs.append(sub)
            for ll in range(9):
                leaf = _make_organ(111+b*10*10+10*10*0 + ll, p, sub.id, [0.01*b, 0, 0.1+0.02*ll], "leaf", 0.03, 0.001)
                organs.append(leaf)
    return PlantArchitecture(architecture_id="arch-"+p, plant_id=p, organs=organs, provenance="TASK_031 B medium ~1000", is_synthetic_example=True)

def bench_large() -> PlantArchitecture:
    # ~10,000: 10 plants-equivalent merged into 1 architecture handle (benchmark only)
    # Use deterministic repetition of a 100-organ unit × 100 = 10,000; ids deterministic
    p = "p-large"
    organs: list = []
    for block in range(100):
        base = 100*block
        root = _make_organ(base, p, None, [0, 0, block*0.01], "root", 0.05, 0.005); organs.append(root)
        for b in range(4):
            s = _make_organ(base+1+b, p, root.id, [0.1*b, 0, 0.05+block*0.01], "stem", 0.08, 0.003); organs.append(s)
            for l in range(24):
                organs.append(_make_organ(base+5+b*24+l, p, s.id, [0,0,0.08+0.03*l], "leaf", 0.03, 0.001))
    return PlantArchitecture(architecture_id="arch-"+p, plant_id=p, organs=organs, provenance="TASK_031 C large ~10000", is_synthetic_example=True)

def bench_multi_plant() -> list[PlantArchitecture]:
    # ~100 plants, reasonable organ count each (~10) → ~1000 total
    plants = []
    for pi in range(100):
        p = f"p-m-{pi}"
        root = _make_organ(0, p, None, [pi*0.1, 0, 0], "root", 0.05, 0.005)
        s = _make_organ(1, p, root.id, [0,0,0.05], "stem", 0.08, 0.003)
        plants.append(PlantArchitecture(architecture_id="arch-"+p, plant_id=p, organs=[root, s, _make_organ(2, p, s.id, [0.02,0,0.08], "leaf", 0.03, 0.001)], provenance="TASK_031 D multi ~100 plants", is_synthetic_example=True))
    return plants

# Adapter conversion: domain → render-only (no scientific duplication)
def to_render_data(arch):
    return {"plant_id": arch.plant_id, "organs": [{"organ_id": o.id, "plant_id": o.plant_id or arch.plant_id, "render_identity": o.id} for o in arch.organs], "provenance": "TASK_031"}
