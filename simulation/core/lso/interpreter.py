"""L-System turtle interpreter — minimal deterministic; produces PlantArchitecture."""
from __future__ import annotations
import math
from typing import List, Optional, Tuple
from simulation.core.contracts.domain import PlantArchitecture, PlantOrgan
from simulation.core.plants.architecture import ArchitectureOps
from simulation.core.lso.contracts import LSystemGrammar

def _normalize(v: List[float]) -> List[float]:
    mag = math.sqrt(sum(x*x for x in v))
    return [x/mag for x in v] if mag > 0 else [0.0,0.0,0.0]

def _rotate(dir_vec: List[float], angle_deg: float, axis: List[float]) -> List[float]:
    # Simple Rodrigues rotation around axis (documented; minimal)
    ax = _normalize(axis)
    d = _normalize(dir_vec)
    theta = math.radians(angle_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    # Project d onto axis
    proj = [d[i]*ax[i] for i in range(3)]
    d_parallel = [proj[i]*ax[i] for i in range(3)]
    d_perp = [d[i]-d_parallel[i] for i in range(3)]
    # Cross product ax x d_perp
    cx = ax[1]*d_perp[2]-ax[2]*d_perp[1]
    cy = ax[2]*d_perp[0]-ax[0]*d_perp[2]
    cz = ax[0]*d_perp[1]-ax[1]*d_perp[0]
    # Rotate parallel unchanged; rotate perp
    new_perp = [d_perp[i]*cos_t + [cx,cy,cz][i]*sin_t for i in range(3)]
    res = [d_parallel[i]+new_perp[i] for i in range(3)]
    return _normalize(res)

def interpret_lsystem(grammar: LSystemGrammar, symbols: str, interpretation_params: Optional[dict] = None) -> PlantArchitecture:
    params = interpretation_params or {}
    segment_length = params.get("segment_length", grammar.segment_length)
    turn_angle = params.get("turn_angle_deg", grammar.turn_angle_deg)
    radius = params.get("radius_m", grammar.radius_m)
    initial_dir = params.get("initial_direction", grammar.initial_direction)
    axis = params.get("turn_axis", [0.0, 0.0, 1.0])  # rotate around up/Z
    # Turtle state
    pos = [0.0, 0.0, 0.0]
    direction = _normalize(initial_dir)
    parent_stack = ["root"]  # stack of parent organ ids
    current_parent = "root"
    organs = []
    organ_index = 0
    def new_organ(oid: str, parent_id: Optional[str], pos_local: List[float], dir_local: List[float]):
        nonlocal organ_index
        organ_index += 1
        organs.append(PlantOrgan(
            id=oid,
            plant_id=params.get("plant_id", "plant-lso"),
            organ_type="axis" if organ_index == 1 else "axis",
            parent_organ_id=parent_id,
            children_ids=[],
            local_position=pos_local,
            orientation=dir_local,
            length_m=segment_length,
            radius_m=radius,
            status="l_system_generated",
            schema_version="v1",
            provenance="l_system_TASK_018; structural prototype; not biological growth",
            is_synthetic_example=True,
        ))
    # Root at initial pos
    new_organ("root", None, [0.0,0.0,0.0], _normalize(initial_dir))
    current_parent = "root"
    for ch in symbols:
        if ch == "F":
            # Extend segment from current pos along direction
            # Organ starts at current pos; length along direction
            new_pos = [pos[i] + direction[i]*segment_length for i in range(3)]
            oid = f"seg-{organ_index+1}"
            new_organ(oid, current_parent, list(pos), list(direction))
            # Update parent chain: new segment becomes current parent for next linear segment
            # For branch, parent restored by stack.
            current_parent = oid
            pos = new_pos
        elif ch == "+":
            direction = _rotate(direction, turn_angle, axis)
        elif ch == "-":
            direction = _rotate(direction, -turn_angle, axis)
        elif ch == "[":
            parent_stack.append(current_parent)
        elif ch == "]":
            if len(parent_stack) > 1:
                current_parent = parent_stack.pop()
            else:
                current_parent = parent_stack[-1]  # keep root
        else:
            # Unknown symbol unchanged; no structural action
            pass
    # Build architecture
    # Update children references
    for o in organs:
        for p in organs:
            if p.id == o.parent_organ_id and o.id not in p.children_ids:
                p.children_ids.append(o.id)
    root_id = "root"
    arch = PlantArchitecture(
        architecture_id=params.get("architecture_id", "arch-lso-001"),
        plant_id=params.get("plant_id", "plant-lso"),
        root_organ_id=root_id,
        coordinate_frame="plant_local",
        local_origin=[0.0,0.0,0.0],
        organs=organs,
        provenance="l_system_TASK_018; synthetic structural prototype; not validated biological growth",
        schema_version="v1",
        is_synthetic_example=True,
        notes="L-system interpreter output. Grammar: formal rewriting only.",
    )
    return arch
