"""Synthetic water fixtures — TASK 025. Liters; labeled synthetic."""
from datetime import datetime, timezone
from simulation.core.water.contracts import RootZoneState, WaterInput, WaterBalanceInput, RootUptakeInput, PlantWaterStatus

SYNTH_ZONE = RootZoneState(
    root_zone_id="rz-1", plant_id="p1", storage_l=2.0, capacity_l=10.0,
    available_water_l=2.0, unavailable_floor_l=0.5,
    timestamp=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc),
    provenance="TASK_025 synthetic; case A base", is_synthetic_example=True)
SYNTH_IN_IRR = WaterInput(amount_l=5.0, source_type="irrigation", provenance="TASK_025 synthetic", is_synthetic_example=True)
SYNTH_BAL_A = WaterBalanceInput(initial_state=SYNTH_ZONE, inputs=[SYNTH_IN_IRR], uptake_l=3.0, provenance="TASK_025 synthetic A", is_synthetic_example=True)
SYNTH_UPTAKE = RootUptakeInput(
    plant_id="p1", root_organ_id="root-1", available_water_l=2.0,
    requested_uptake_l=5.0, uptake_capacity_l=4.0, provenance="TASK_025 synthetic C", is_synthetic_example=True)
SYNTH_STATUS = PlantWaterStatus(plant_id="p1", status_indicator="limited", relative_available=0.2, provenance="TASK_025 synthetic", is_synthetic_example=True)
