"""Synthetic phenology fixtures — TASK 024. Synthetic stages; labeled; no species timing."""
from datetime import datetime, timezone
from simulation.core.phenology.contracts import PhenologyState, PhenologyTransitionEvent

SYNTH_SEED = PhenologyState(
    plant_id="p1", current_stage="seed", previous_stage=None,
    stage_start_time=datetime(2026,6,1,8,0,0,tzinfo=timezone.utc),
    provenance="TASK_024 synthetic; initial", is_synthetic_example=True)
SYNTH_GERM = PhenologyState(
    plant_id="p1", current_stage="germination", previous_stage="seed",
    stage_start_time=datetime(2026,6,2,8,0,0,tzinfo=timezone.utc),
    transition_count=1,
    transition_history=[PhenologyTransitionEvent(event_id="e1", plant_id="p1", from_stage="seed", to_stage="germination", trigger_type="explicit_stage_event", provenance="TASK_024 synthetic")],
    provenance="TASK_024 synthetic; transitional", is_synthetic_example=True)
SYNTH_VEG = PhenologyState(
    plant_id="p1", current_stage="vegetative",
    provenance="TASK_024 synthetic; vegetative", is_synthetic_example=True)
