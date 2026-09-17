"""Calibration demonstration — TASK 028. Synthetic scalar parameter only; deterministic; no biological claim."""
from __future__ import annotations
from typing import Optional, List, Dict
import numpy as np
from scipy.optimize import minimize
from simulation.core.calibration.contracts import CalibrationRequest, CalibrationResult, FittedParameter

def calibrate_scalar(
    request: CalibrationRequest,
    observations: Dict[str, List[float]],
    objective: str = "sum_sq_residuals",
) -> CalibrationResult:
    if not request.target_parameter_names or len(request.target_parameter_names) != 1:
        return CalibrationResult(
            calibration_id=request.calibration_id,
            model_version_ref=request.model_version_ref,
            base_parameter_set_ref=request.base_parameter_set_ref,
            status="NOT_IDENTIFIABLE", observations_used=0, objective_value=0.0,
            provenance=request.provenance or "TASK_028; scalar calibration requires exactly one target parameter",
            notes="Single-parameter scalar demonstration only.",
            is_synthetic_example=request.is_synthetic_example,
        )
    param_name = request.target_parameter_names[0]
    var_data = observations.get(param_name, [])
    if not var_data or len(var_data) < 2:
        return CalibrationResult(
            calibration_id=request.calibration_id,
            model_version_ref=request.model_version_ref,
            base_parameter_set_ref=request.base_parameter_set_ref,
            status="INSUFFICIENT_DATA", observations_used=0, objective_value=0.0,
            provenance=request.provenance or "TASK_028; insufficient observations"
        )
    xs = []
    ys = []
    for item in var_data:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            xs.append(float(item[0]))
            ys.append(float(item[1]))
        elif isinstance(item, dict) and "x" in item and "y" in item:
            xs.append(float(item["x"]))
            ys.append(float(item["y"]))
    if len(xs) < 2:
        return CalibrationResult(
            calibration_id=request.calibration_id,
            model_version_ref=request.model_version_ref,
            base_parameter_set_ref=request.base_parameter_set_ref,
            status="INSUFFICIENT_DATA", observations_used=0, objective_value=0.0,
            provenance=request.provenance or "TASK_028; observation pairs insufficient"
        )
    xs = np.array(xs)
    ys = np.array(ys)
    bounds_dict = request.bounds.get(param_name) if request.bounds else None
    if bounds_dict is None:
        bounds_dict = [0.01, 0.1]
    lo, up = float(bounds_dict[0]), float(bounds_dict[1])
    def obj(alpha):
        pred = alpha[0] * xs
        return float(np.sum((ys - pred) ** 2))
    x0 = np.array([(lo + up) / 2.0])
    res = minimize(obj, x0, method="L-BFGS-B", bounds=[(lo, up)], options={"maxiter":100, "ftol":1e-9})
    fitted_alpha = float(res.x[0])
    converged = res.success
    at_bound = (abs(fitted_alpha - lo) < 1e-6) or (abs(fitted_alpha - up) < 1e-6)
    status = "CONVERGED" if converged else "NOT_CONVERGED"
    notes = f"Parameter at bound (lo={lo}, up={up}); fitted={fitted_alpha}." if at_bound else "Synthetic scalar calibration completed; not biological validation."
    fitted_param = FittedParameter(
        parameter_name=param_name,
        base_value=lo if bounds_dict else 0.05,
        fitted_value=round(fitted_alpha, 6),
        unit="dimensionless_synthetic",
        bounds=[lo, up],
        method_ref=str(request.method),
        objective_value=round(float(res.fun), 6),
        status=status,
        provenance=request.provenance or "TASK_028; synthetic scalar calibration",
        is_synthetic_example=True,
    )
    return CalibrationResult(
        calibration_id=request.calibration_id,
        model_version_ref=request.model_version_ref,
        base_parameter_set_ref=request.base_parameter_set_ref,
        calibrated_parameter_set_ref=f"calibrated_{request.calibration_id}",
        fitted_parameters=[fitted_param],
        objective_value=round(float(res.fun), 6),
        diagnostics={"optimizer":"L-BFGS-B","iterations":int(res.nit) if hasattr(res,"nit") else None,"converged":converged,"at_bound":at_bound,"residual_norm":float(np.linalg.norm(ys - fitted_alpha*xs))},
        observations_used=len(xs),
        exclusions=[],
        status=status,
        provenance=request.provenance or f"TASK_028; synthetic calibration seed={request.seed}",
        timestamp=None,
        notes=notes,
        is_synthetic_example=True,
    )
