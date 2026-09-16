"""Synthetic prediction fixtures — TASK 016. Labeled; no biological values."""
from datetime import datetime, timezone
from simulation.core.prediction.contracts import Prediction, PredictionRequest
from simulation.core.snapshot.fixtures import SYNTH_SNAPSHOT

SYNTH_REQUEST = PredictionRequest(
    request_id="req-016-001",
    source_snapshot_ref=SYNTH_SNAPSHOT.snapshot_id,
    target_time=datetime(2026,6,22,12,0,0,tzinfo=timezone.utc),
    model_version_ref="v0.1",
    parameter_set_ref="params-default",
    deterministic_settings={"random_seed": 42},
    created_at=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc),
    provenance="synthetic_request_TASK_016; no forecasting model yet",
    is_synthetic_example=True,
)

SYNTH_PREDICTION = Prediction(
    prediction_id="pred-016-001",
    request_ref="req-016-001",
    source_snapshot_ref=SYNTH_SNAPSHOT.snapshot_id,
    target_time=datetime(2026,6,22,12,0,0,tzinfo=timezone.utc),
    created_at=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc),
    model_version_ref="v0.1",
    parameter_set_ref="params-default",
    status="NOT_COMPUTABLE",
    output_ref=None,
    assumptions=["biological forecasting model not yet implemented"],
    uncertainty_status="not_modelled",
    provenance="synthetic_prediction_TASK_016; structurally honest — no fabricated growth/yield/biomass",
    schema_version="v1",
    notes="Prediction infrastructure only. Future-state output requires plant-growth/physiology model (TASK 017+). No invented values.",
    is_synthetic_example=True,
)
