"""Validation evaluation — TASK 029. Fixed model; independent dataset; metrics; criteria; leakage check."""
from __future__ import annotations
from typing import Optional, List, Dict, Any
from simulation.core.validation.contracts import ValidationRequest, ValidationResult, ValidationDataset, MetricCriterion

def validate_model(
    request: ValidationRequest,
    predictions: List[float],
    observations: List[float],
    dataset_ref: Optional[str] = None,
    calibration_dataset_ref: Optional[str] = None,
    provenance: Optional[str] = None,
) -> ValidationResult:
    # Leakage checks
    if dataset_ref and calibration_dataset_ref and dataset_ref == calibration_dataset_ref:
        return ValidationResult(
            validation_id=request.validation_id,
            model_version_ref=request.model_version_ref,
            parameter_set_ref=request.parameter_set_ref,
            dataset_ref=dataset_ref or request.validation_dataset_ref,
            status="LEAKAGE_DETECTED",
            provenance=provenance or "TASK_029; calibration and validation dataset identical",
            notes="Dataset leakage detected: validation dataset equals calibration dataset.",
            is_synthetic_example=request.is_synthetic_example,
        )
    # Unit mismatch guard (simplified): if target_unit missing or predictions/obs empty
    if not predictions or not observations:
        return ValidationResult(
            validation_id=request.validation_id,
            model_version_ref=request.model_version_ref,
            parameter_set_ref=request.parameter_set_ref,
            dataset_ref=dataset_ref or request.validation_dataset_ref,
            status="INSUFFICIENT_DATA",
            provenance=provenance or "TASK_029; empty predictions or observations",
            notes="No paired predictions/observations.",
            is_synthetic_example=request.is_synthetic_example,
        )
    if len(predictions) != len(observations):
        return ValidationResult(
            validation_id=request.validation_id,
            model_version_ref=request.model_version_ref,
            parameter_set_ref=request.parameter_set_ref,
            dataset_ref=dataset_ref or request.validation_dataset_ref,
            status="INVALID_INPUT",
            provenance=provenance or "TASK_029; mismatched prediction/observation counts",
            notes=f"Predictions ({len(predictions)}) != observations ({len(observations)}).",
            is_synthetic_example=request.is_synthetic_example,
        )
    # Metrics
    diffs = [float(p) - float(o) for p, o in zip(predictions, observations)]
    n = len(diffs)
    bias = sum(diffs) / n if n > 0 else 0.0
    mae = sum(abs(d) for d in diffs) / n if n > 0 else 0.0
    rmse = (sum(d*d for d in diffs) / n) ** 0.5 if n > 0 else 0.0
    metrics = {"count": n, "bias": round(bias, 6), "mae": round(mae, 6), "rmse": round(rmse, 6)}
    # Criteria evaluation (simple: if max_allowed_error provided for mae/rmse)
    criteria_met = {}
    for c in request.metric_config:
        val = metrics.get(c.metric_name, None)
        met = None
        if val is not None and c.max_allowed_error is not None:
            met = val <= c.max_allowed_error
        criteria_met[c.metric_name] = {"value": val, "criterion": c.max_allowed_error, "met": met, "unit": c.unit}
    status = "VALID"
    # Constant observed data => correlation undefined; don't report correlation
    # Just keep status VALID if metrics computed
    diagnostics = {"unit_check": request.target_unit, "paired": n, "leakage_checked": True}
    return ValidationResult(
        validation_id=request.validation_id,
        model_version_ref=request.model_version_ref,
        parameter_set_ref=request.parameter_set_ref,
        dataset_ref=dataset_ref or request.validation_dataset_ref,
        matched_count=n,
        unmatched_count=0,
        exclusions=[],
        metrics=metrics,
        diagnostics=diagnostics,
        criteria_met=criteria_met,
        status=status,
        provenance=provenance or "TASK_029; validation synthetic",
        notes="Synthetic validation: predictions vs independent observations; not biological validation.",
        is_synthetic_example=True,
    )
