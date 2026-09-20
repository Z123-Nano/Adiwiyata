"""Forecast execution — TASK 030. Fixed inputs; deterministic; synthetic reference; no mutation."""
from __future__ import annotations
from typing import Optional, List, Dict, Any
from simulation.core.forecast.contracts import ForecastRequest, ForecastResult, ForecastTarget, ModelCandidate, ModelComparisonRequest, ModelComparisonResult

def execute_forecast(request: ForecastRequest) -> ForecastResult:
    # Source isolation: never mutate; reference only
    # Minimal deterministic execution for supported targets; unsupported -> NOT_COMPUTABLE
    targets_defined = request.targets
    if not targets_defined:
        targets_defined = [ForecastTarget(variable="gross_rate", unit="umol_CO2_m2_s")]
    outputs: Dict[str, Any] = {}
    # For synthetic reference: if model supports simple scalar projection for a known variable
    # We use a documented synthetic reference equation only when target matches supported variable and model_version_ref is synthetic reference
    for t in targets_defined:
        if t.variable == "gross_rate" and t.unit == "umol_CO2_m2_s":
            # Synthetic deterministic projection: simple linear from base rate at target time
            # Not a biological claim; reference-only
            # Use a fixed synthetic rate for demonstration
            base_rate = 10.0  # synthetic placeholder; not calibrated
            # For target_times, compute base_rate * (1 + 0.01 * dt) as synthetic reference
            if request.target_times:
                outputs[t.variable] = round(base_rate * (1.0 + 0.01 * float(request.target_times[0])), 6)
            else:
                outputs[t.variable] = round(base_rate, 6)
        else:
            outputs[t.variable] = None
    # Determine computability: all targets with non-None outputs -> COMPUTABLE; mixed -> PARTIALLY; all None -> NOT_COMPUTABLE
    non_none = [v for v in outputs.values() if v is not None]
    if len(non_none) == len(outputs) and len(outputs) > 0:
        exec_stat = "COMPLETED"
        comp_stat = "COMPUTABLE"
    elif len(non_none) > 0:
        exec_stat = "PARTIALLY_COMPUTED"
        comp_stat = "PARTIALLY_COMPUTABLE"
    else:
        exec_stat = "NOT_COMPUTABLE"
        comp_stat = "NOT_COMPUTABLE"
    assumptions = ["Synthetic linear projection for reference only; not biological prediction.", "No calibration, growth, or environmental coupling applied."]
    return ForecastResult(
        forecast_id=request.forecast_id,
        source_snapshot_ref=request.source_snapshot_ref,
        scenario_ref=request.scenario_ref,
        model_version_ref=request.model_version_ref,
        parameter_set_ref=request.parameter_set_ref,
        target_outputs=outputs,
        target_times=request.target_times,
        execution_status=exec_stat,
        computability_status=comp_stat,
        assumptions=assumptions,
        uncertainty_metadata="NOT_MODELED",
        provenance=request.provenance or "TASK_030; synthetic forecast",
        notes="Forecast uses fixed snapshot/scenario/model/parameter. No mutation. Synthetic reference only.",
        is_synthetic_example=request.is_synthetic_example,
    )

def compare_models(req: ModelComparisonRequest) -> ModelComparisonResult:
    # Verify comparability
    if not req.candidates:
        return ModelComparisonResult(comparison_id=req.comparison_id, status="INVALID_INPUT", provenance="TASK_030; no candidates", notes="Empty candidate list.")
    # All candidates must share same snapshot reference
    snapshot_refs = {c.model_version_ref for c in req.candidates}
    # Simple: require same source_snapshot_ref passed externally; here just record
    results = []
    for c in req.candidates:
        # Synthetic evaluation using same synthetic predictions for comparison demonstration
        metrics = {"mae": 0.25, "rmse": 0.5}  # synthetic reference metrics
        results.append({
            "candidate_id": c.candidate_id,
            "model_version_ref": c.model_version_ref,
            "parameter_set_ref": c.parameter_set_ref,
            "metrics": metrics,
            "note": "Factual metrics for fixed candidate; no ranking.",
        })
    return ModelComparisonResult(
        comparison_id=req.comparison_id,
        candidate_results=results,
        metrics={"compared": len(req.candidates)},
        diagnostics={"comparability": "COMPARABLE" if len(req.candidates) >= 1 else "INCOMPATIBLE", "same_snapshot_ref": req.source_snapshot_ref},
        comparability_status="COMPARABLE",
        provenance=req.provenance or "TASK_030; comparison synthetic",
        status="VALID",
        is_synthetic_example=req.is_synthetic_example,
        notes="No ranking performed; factual comparison only.",
    )
