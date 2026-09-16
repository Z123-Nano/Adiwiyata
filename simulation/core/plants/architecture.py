"""PlantArchitecture operations — TASK 017 (infrastructure; no growth/L-system/physics)."""
from __future__ import annotations
from typing import Optional, List
from simulation.core.contracts.domain import PlantArchitecture, PlantOrgan

class ArchitectureOps:
    @staticmethod
    def validate(arch: PlantArchitecture) -> list[str]:
        errors = []
        ids = {o.id for o in arch.organs}
        if len(ids) != len(arch.organs):
            errors.append("duplicate organ ids")
        for o in arch.organs:
            if o.length_m is not None and o.length_m < 0:
                errors.append(f"negative length: {o.id}")
            if o.radius_m is not None and o.radius_m < 0:
                errors.append(f"negative radius: {o.id}")
            if o.parent_organ_id is not None and o.parent_organ_id not in ids:
                errors.append(f"invalid parent: {o.id} -> {o.parent_organ_id}")
        # cycle detection
        visited = set()
        def dfs(node_id, path):
            if node_id in path:
                errors.append(f"cycle at {node_id}")
                return
            path = path | {node_id}
            for o in arch.organs:
                if o.parent_organ_id == node_id:
                    dfs(o.id, path)
        root = arch.root_organ_id or (arch.organs[0].id if arch.organs else None)
        if root:
            dfs(root, set())
        # root consistency
        for o in arch.organs:
            if o.id == root and o.parent_organ_id is not None:
                errors.append("root has parent")
        return errors

    @staticmethod
    def add_organ(arch: PlantArchitecture, organ: PlantOrgan) -> PlantArchitecture:
        # Deep-copy boundary via serialization (Pydantic)
        arch = PlantArchitecture.model_validate(arch.model_dump(mode="json"))
        if any(o.id == organ.id for o in arch.organs):
            raise ValueError("duplicate organ id")
        archiv = PlantOrgan.model_validate(organ.model_dump(mode="json"))
        arch.organs.append(archiv)
        # If parent set and exists, update parent children
        if archiv.parent_organ_id:
            for p in arch.organs:
                if p.id == archiv.parent_organ_id and archiv.id not in p.children_ids:
                    p.children_ids.append(archiv.id)
        return arch

    @staticmethod
    def remove_organ(arch: PlantArchitecture, organ_id: str, detach_children: bool = False) -> PlantArchitecture:
        arch = PlantArchitecture.model_validate(arch.model_dump(mode="json"))
        target = next((o for o in arch.organs if o.id == organ_id), None)
        if target is None:
            raise ValueError("organ not found")
        if target.children_ids and not detach_children:
            raise ValueError("organ has children; set detach_children=True")
        # Remove from parent's children
        if target.parent_organ_id:
            for p in arch.organs:
                if p.id == target.parent_organ_id and organ_id in p.children_ids:
                    p.children_ids.remove(organ_id)
        # If detach_children, reattach descendants to parent (simplified: just remove children refs; deeper reattach deferred)
        if detach_children:
            for child_id in target.children_ids:
                for c in arch.organs:
                    if c.id == child_id:
                        c.parent_organ_id = target.parent_organ_id
                        if target.parent_organ_id:
                            for pp in arch.organs:
                                if pp.id == target.parent_organ_id and child_id not in pp.children_ids:
                                    pp.children_ids.append(child_id)
        arch.organs = [o for o in arch.organs if o.id != organ_id]
        if arch.root_organ_id == organ_id and arch.organs:
            arch.root_organ_id = arch.organs[0].id
        return arch

    @staticmethod
    def find_organ(arch: PlantArchitecture, organ_id: str) -> Optional[PlantOrgan]:
        for o in arch.organs:
            if o.id == organ_id:
                return o
        return None

    @staticmethod
    def get_children(arch: PlantArchitecture, organ_id: str) -> List[PlantOrgan]:
        return [o for o in arch.organs if o.parent_organ_id == organ_id]

    @staticmethod
    def get_parent(arch: PlantArchitecture, organ_id: str) -> Optional[PlantOrgan]:
        o = ArchitectureOps.find_organ(arch, organ_id)
        if o is None or o.parent_organ_id is None:
            return None
        return ArchitectureOps.find_organ(arch, o.parent_organ_id)

    @staticmethod
    def get_root(arch: PlantArchitecture) -> Optional[PlantOrgan]:
        root_id = arch.root_organ_id or (arch.organs[0].id if arch.organs else None)
        if root_id is None:
            return None
        return ArchitectureOps.find_organ(arch, root_id)
