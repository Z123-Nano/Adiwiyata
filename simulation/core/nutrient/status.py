"""Plant nutrient status — TASK 026. Simplified; synthetic thresholds; not tissue diagnosis."""
from __future__ import annotations
from simulation.core.nutrient.contracts import PlantNutrientStatus

def derive_nutrient_status(
    plant_id: str,
    N_available: float = 0.0, N_cap: float = 100.0,
    P_available: float = 0.0, P_cap: float = 20.0,
    K_available: float = 0.0, K_cap: float = 100.0,
    provenance: str = None,
) -> PlantNutrientStatus:
    def ind(av, cap):
        r = av / cap if cap > 0 else 0
        return "adequate" if r >= 0.8 else ("limited" if r >= 0.4 else "deficient")
    return PlantNutrientStatus(
        plant_id=plant_id,
        N_status=ind(N_available, N_cap),
        P_status=ind(P_available, P_cap),
        K_status=ind(K_available, K_cap),
        provenance=provenance or "TASK_026; synthetic thresholds",
        notes="Simplified modeled status; not tissue nutrient concentration or diagnostic agronomic status.",
        is_synthetic_example=True,
    )
