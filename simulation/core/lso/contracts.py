"""L-System contracts — TASK 018 (formal rewriting prototype; not biological growth)."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Dict

class LSystemGrammar(BaseModel):
    grammar_id: str
    axiom: str
    rules: Dict[str, str] = Field(default_factory=dict)  # symbol -> replacement
    max_iterations: int = Field(default=10, ge=0)
    max_symbol_count: int = Field(default=10000, ge=1)
    turn_angle_deg: float = 25.0
    segment_length: float = 1.0
    radius_m: float = 0.01
    initial_direction: List[float] = Field(default_factory=lambda: [0.0, 0.0, 1.0])
    schema_version: Literal["v1"] = "v1"
    provenance: Optional[str] = None
    is_synthetic_example: bool = False
    notes: Optional[str] = None

class LSystemState(BaseModel):
    grammar_id: str
    symbols: str
    iteration: int = 0
    provenance: Optional[str] = None
    schema_version: Literal["v1"] = "v1"

class LSystemGenerationRequest(BaseModel):
    grammar_ref: str  # grammar id or serialized
    iterations: int = Field(..., ge=0)
    deterministic_settings: Optional[dict] = None
    interpretation_params: Optional[dict] = None
    provenance: Optional[str] = None
    is_synthetic_example: bool = False

class GenerationResult(BaseModel):
    grammar_ref: str
    symbols: str
    iteration: int
    architecture_ref: Optional[str] = None
    provenance: Optional[str] = None
    status: Literal["COMPLETED","LIMIT_EXCEEDED","FAILED"] = "COMPLETED"
    notes: Optional[str] = None
    schema_version: Literal["v1"] = "v1"
    is_synthetic_example: bool = False
