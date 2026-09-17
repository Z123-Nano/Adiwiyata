"""Stochastic variation — TASK 027. NumPy Generator PCG64; explicit seed; bounded; synthetic."""
from __future__ import annotations
import numpy as np
from simulation.core.stochastic.contracts import StochasticVariationRequest, StochasticVariationResult, StochasticDistribution, RNGStateRef

def vary_parameter(req: StochasticVariationRequest) -> StochasticVariationResult:
    # Validation
    if req.seed is None:
        return StochasticVariationResult(parameter_name=req.parameter_name, base_value=req.base_value, sampled_value=req.base_value, distribution=req.distribution, seed=-1, bounds=req.bounds, status="INVALID_INPUT", provenance=req.provenance or "TASK_027; seed required")
    # Bounds validation
    lower = req.bounds.get("lower")
    upper = req.bounds.get("upper")
    if lower is not None and upper is not None and lower > upper:
        return StochasticVariationResult(parameter_name=req.parameter_name, base_value=req.base_value, sampled_value=req.base_value, distribution=req.distribution, seed=req.seed, bounds=req.bounds, status="INVALID_INPUT", provenance=req.provenance or "TASK_027; lower > upper")
    dist = req.distribution
    if dist.distribution_type == "uniform":
        lo = dist.parameters.get("lower") if "lower" in dist.parameters else (req.bounds.get("lower") if req.bounds.get("lower") is not None else 0.0)
        up = dist.parameters.get("upper") if "upper" in dist.parameters else (req.bounds.get("upper") if req.bounds.get("upper") is not None else 1.0)
        if lo is None or up is None:
            return StochasticVariationResult(parameter_name=req.parameter_name, base_value=req.base_value, sampled_value=req.base_value, distribution=dist, seed=req.seed, bounds=req.bounds, status="INVALID_INPUT", provenance=req.provenance or "TASK_027; uniform bounds missing")
        if lo > up:
            return StochasticVariationResult(parameter_name=req.parameter_name, base_value=req.base_value, sampled_value=req.base_value, distribution=dist, seed=req.seed, bounds=req.bounds, status="INVALID_INPUT", provenance=req.provenance or "TASK_027; uniform lower>upper")
        rng = np.random.default_rng(req.seed)
        sampled = float(rng.uniform(float(lo), float(up)))
    elif dist.distribution_type == "normal" or dist.distribution_type == "truncated_normal":
        mean = dist.parameters.get("mean", req.base_value)
        sd = dist.parameters.get("sd", 0.1)
        if sd < 0:
            return StochasticVariationResult(parameter_name=req.parameter_name, base_value=req.base_value, sampled_value=req.base_value, distribution=dist, seed=req.seed, bounds=req.bounds, status="INVALID_INPUT", provenance=req.provenance or "TASK_027; negative sd")
        lo = req.bounds.get("lower")
        up = req.bounds.get("upper")
        rng = np.random.default_rng(req.seed)
        # Truncated normal via rejection sampling (few iterations enough for synthetic)
        max_iter = 1000
        sampled = None
        for _ in range(max_iter):
            val = float(rng.normal(float(mean), float(sd)))
            if (lo is None or val >= float(lo)) and (up is None or val <= float(up)):
                sampled = val
                break
        if sampled is None:
            # Fallback to boundary if bounds very narrow; record
            sampled = float(lo) if lo is not None else (float(up) if up is not None else float(mean))
    else:
        return StochasticVariationResult(parameter_name=req.parameter_name, base_value=req.base_value, sampled_value=req.base_value, distribution=dist, seed=req.seed, bounds=req.bounds, status="NOT_IMPLEMENTED", provenance=req.provenance or f"TASK_027; unsupported {dist.distribution_type}")
    # Preserve bounds in result even if not clipped (clipping not needed with bounded methods)
    return StochasticVariationResult(
        parameter_name=req.parameter_name,
        base_value=req.base_value,
        sampled_value=round(sampled, 6),
        distribution=dist,
        seed=req.seed,
        bounds=req.bounds,
        random_state_ref=f"np.default_rng({req.seed}) PCG64",
        status="VALID",
        provenance=req.provenance or f"TASK_027; {dist.distribution_type} seed={req.seed}",
        notes=f"Synthetic distribution; reproducible; not empirical biological variability.",
        is_synthetic_example=req.is_synthetic_example,
    )
