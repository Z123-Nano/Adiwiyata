"""TASK 046H-D fixtures — synthetic examples labeled; no calibration; no inference from geometry."""
from __future__ import annotations
from datetime import datetime, timezone
from simulation.core.development.contracts import OrganDevelopmentalState, organ_developmental_state

# Real-pattern synthetic with initiation + chronological age available
SYNTH_DEV_INIT = organ_developmental_state(
    organ_developmental_state_id="dev_1",
    plant_id="p1",
    architecture_id="arch_1",
    organ_id="leaf_1",
    organ_type="leaf",
    initiated_at=datetime(2026, 9, 1, 12, 0, 0, tzinfo=timezone.utc),
    chronological_age_days=16.0,
    physiological_age=None,  # unavailable — no domain definition
    organ_stage="EXPANDING",
    growth_window_start=None,  # unavailable until model defined
    growth_window_end=None,
    provenance="TASK_046H-D synthetic; initiated+age available; physiological_age unavailable; growth_window unavailable",
    source_type="SYNTHETIC",
    is_synthetic_example=True,
)

# Missing initiation — chronological age unavailable
SYNTH_DEV_NO_INIT = organ_developmental_state(
    organ_developmental_state_id="dev_2",
    plant_id="p1",
    architecture_id="arch_1",
    organ_id="stem_1",
    organ_type="stem",
    initiated_at=None,
    chronological_age_days=None,
    physiological_age=None,
    organ_stage=None,
    provenance="TASK_046H-D synthetic; initiation unknown; chronological_age unavailable; stage unavailable",
    source_type="SYNTHETIC",
    is_synthetic_example=True,
    note="No initiation; age uncomputable; stage unassigned.",
)

# With growth window (both defined — valid order)
SYNTH_DEV_WINDOW = organ_developmental_state(
    organ_developmental_state_id="dev_3",
    plant_id="p2",
    architecture_id="arch_2",
    organ_id="root_1",
    organ_type="root",
    initiated_at=datetime(2026, 8, 1, 12, 0, 0, tzinfo=timezone.utc),
    chronological_age_days=47.0,
    growth_window_start=datetime(2026, 8, 10, 12, 0, 0, tzinfo=timezone.utc),
    growth_window_end=datetime(2026, 10, 1, 12, 0, 0, tzinfo=timezone.utc),
    provenance="TASK_046H-D synthetic; valid window order",
    source_type="SYNTHETIC",
    is_synthetic_example=True,
)
