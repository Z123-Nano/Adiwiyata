"""Nutrient pool / availability — TASK 026. Availability fraction synthetic."""
from __future__ import annotations
from simulation.core.nutrient.contracts import NutrientPoolState

def compute_available(pool: NutrientPoolState) -> NutrientPoolState:
    frac = pool.availability_fraction
    if frac < 0 or frac > 1:
        return pool.model_copy(update={"status":"INVALID_INPUT","notes":"availability fraction out of [0,1]"})
    avail = pool.total_amount_mg * frac
    unavailable = pool.total_amount_mg - avail
    return pool.model_copy(update={
        "available_amount_mg": round(avail, 6),
        "unavailable_amount_mg": round(unavailable, 6),
        "status":"VALID",
        "notes":"Available = total * fraction (synthetic approximation).",
    })
