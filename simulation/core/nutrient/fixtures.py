"""Synthetic nutrient fixtures — TASK 026. mg; labeled synthetic."""
from simulation.core.nutrient.contracts import NutrientPoolState, NutrientInput, NutrientBalanceInput, NutrientUptakeInput

# Example N: total=100, frac=0.5 => avail=50; input=20; req=30; cap=25 => actual 25
SYNTH_N = NutrientPoolState(root_zone_id="rz1", plant_id="p1", nutrient="N", total_amount_mg=100.0, availability_fraction=0.5, provenance="TASK_026 synthetic N", is_synthetic_example=True)
SYNTH_N_IN = NutrientInput(nutrient="N", amount_mg=20.0, source_type="fertilizer", provenance="TASK_026 synthetic", is_synthetic_example=True)
# Example P: total=20, frac=0.25 => avail=5; req=10; cap=10 => actual 5
SYNTH_P = NutrientPoolState(root_zone_id="rz1", plant_id="p1", nutrient="P", total_amount_mg=20.0, availability_fraction=0.25, provenance="TASK_026 synthetic P", is_synthetic_example=True)
# Example K invalid: negative input
SYNTH_K_BAD = NutrientInput(nutrient="K", amount_mg=-5.0, provenance="TASK_026 synthetic invalid", is_synthetic_example=True)
