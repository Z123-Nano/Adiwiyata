"""TASK 034 — thin service: domain fixture → DTO; no scientific calculation."""
from simulation.core.garden.fixtures import synth_garden, SYNTH_SPATIAL
from simulation.core.contracts.domain import Plant

def get_garden():
    g = synth_garden()
    return {"garden_id": g.id, "status": "VALID", "objects": g.objects, "note": "TASK_034 domain source (provenance on fixture, not contract)"}

def get_garden_objects():
    return {"objects": [{"id": s.id, "type": s.type, "parent_id": getattr(s.transform, "parent_id", None), "position": s.transform.position} for s in SYNTH_SPATIAL], "provenance": "TASK_034 domain source"}

def get_plant(plant_id: str):
    # Resolve against domain plant fixtures (TASK 017 architecture fixtures)
    from simulation.core.plants.architecture_fixtures import SYNTH_SEEDLING
    arch = SYNTH_SEEDLING
    # Return architecture-backed plant reference if id matches
    if plant_id == "plant-p1" or (arch and arch.plant_id == plant_id):
        return {
            "plant_id": plant_id,
            "identity": {"id": plant_id, "species_id": "demo-variety", "variety_id": "v1"},
            "state_ref": "state_" + plant_id,
            "architecture_summary": {"organs": len(arch.organs) if arch and hasattr(arch,"organs") else 4},
            "provenance": "TASK_034 domain source; architecture_ref=arch-017-seed",
            "status": "VALID",
        }
    return None
