"""Prediction execution boundary — TASK 016. No scientific forecasting; status explicit."""
from __future__ import annotations
from datetime import datetime, timezone
from simulation.core.prediction.contracts import Prediction, PredictionRequest
from simulation.core.snapshot.contracts import Snapshot

def create_prediction(
    request: PredictionRequest,
    source_snapshot_ref_or_object: str | Snapshot,
) -> Prediction:
    """Create prediction infrastructure; do NOT invent biological outputs."""
    # Validate consistency: snapshot exists, scenario ref consistent (if present)
    if not request.source_snapshot_ref:
        raise ValueError("source_snapshot_ref required")
    # If scenario_ref provided, must reference scenario derived from same snapshot (not enforced fully at this layer)
    # No clock advancement; no scheduler step
    return Prediction(
        prediction_id=f"pred-{request.request_id}",
        request_ref=request.request_id,
        source_snapshot_ref=request.source_snapshot_ref,
        scenario_ref=request.scenario_ref,
        target_time=request.target_time,
        created_at=request.created_at,
        model_version_ref=request.model_version_ref,
        parameter_set_ref=request.parameter_set_ref,
        status="NOT_COMPUTABLE",
        output_ref=None,
        assumptions=["biological forecasting not implemented"],
        uncertainty_status="not_modelled",
        provenance=request.provenance or "prediction_TASK_016",
        schema_version="v1",
        notes="Forecasting model unavailable — infrastructure only. No fabricated outputs.",
        is_synthetic_example=request.is_synthetic_example,
    )
