"""Stochastic framework contracts — TASK 027. Explicit; reproducible; bounded; synthetic."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any, List

class StochasticDistribution(BaseModel):
    distribution_type: Literal["uniform","truncated_normal","normal"] = "uniform"
    parameters: Dict[str, float] = Field(default_factory=dict)  # mean, sd, lower, upper
    bounds: Dict[str, float] = Field(default_factory=dict)   # lower/upper
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class StochasticVariationRequest(BaseModel):
    parameter_name: str
    base_value: float
    distribution: StochasticDistribution
    seed: int
    bounds: Dict[str, float] = Field(default_factory=dict)
    context_ref: Optional[str] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class StochasticVariationResult(BaseModel):
    parameter_name: str
    base_value: float
    sampled_value: float
    distribution: StochasticDistribution
    seed: int
    bounds: Dict[str, float]
    random_state_ref: Optional[str] = None
    status: Literal["VALID","INVALID_INPUT","NOT_IMPLEMENTED","NOT_COMPUTABLE","INCONCLUSIVE"] = "VALID"
    provenance: Optional[str] = None
    notes: Optional[str] = None
    is_synthetic_example: bool = False
    schema_version: Literal["v1"] = "v1"

class RNGStateRef(BaseModel):
    generator_type: str = "numpy.Generator + PCG64"
    seed: int
    version_ref: Optional[str] = None
    provenance: Optional[str] = None
    schema_version: Literal["v1"] = "v1"
