"""Phenology transition — TASK 024. Deterministic state machine; explicit graph; no species timing."""
from __future__ import annotations
from datetime import datetime, timezone
from simulation.core.phenology.contracts import PhenologyState, PhenologyTransitionResult, PhenologyTransitionEvent, STAGE_VOCAB

# Default allowed transition graph (explicit; not biological default)
DEFAULT_GRAPH = {
    "seed": ["germination"],
    "germination": ["seedling"],
    "seedling": ["vegetative"],
    "vegetative": ["flowering"],
    "flowering": ["fruiting"],
    "fruiting": ["senescence"],
    "senescence": ["completed"],
    "dormant": ["seedling","vegetative"],
    "completed": [],
}

def transition_phenology(
    state: PhenologyState,
    target_stage: str,
    trigger_type: str = "explicit_stage_event",
    reason: str = None,
    provenance: str = None,
    timestamp: datetime = None,
    allowed_graph: dict = None,
) -> PhenologyTransitionResult:
    allowed = allowed_graph or DEFAULT_GRAPH
    curr = state.current_stage
    # Invalid target vocabulary
    if target_stage not in STAGE_VOCAB:
        return PhenologyTransitionResult(
            plant_id=state.plant_id, previous_stage=curr, current_stage=curr,
            status="INVALID_INPUT", provenance=provenance or "TASK_024; invalid stage vocabulary",
            notes=f"Target stage '{target_stage}' not in vocabulary.",
            is_synthetic_example=state.is_synthetic_example,
        )
    # Self-transition allowed; record event but stage unchanged
    if target_stage == curr:
        event = PhenologyTransitionEvent(
            event_id=f"self-{curr}", plant_id=state.plant_id,
            from_stage=curr, to_stage=curr,
            trigger_type=trigger_type,
            reason=reason or "self-transition",
            provenance=provenance or "TASK_024; self-transition",
            is_synthetic_example=state.is_synthetic_example,
        )
        new_state = state.model_copy(update={
            "current_stage": curr,
            "previous_stage": curr,
            "transition_count": state.transition_count + 1,
            "transition_history": state.transition_history + [event],
            "last_transition_reason": event.reason,
            "provenance": provenance or state.provenance,
            "status": "VALID",
        })
        return PhenologyTransitionResult(
            plant_id=state.plant_id, previous_stage=curr, current_stage=curr,
            event=event, status="VALID",
            provenance=provenance or "TASK_024; self-transition",
            notes="Self-transition allowed; stage unchanged.",
            is_synthetic_example=state.is_synthetic_example,
        )
    # Check allowed transition
    permitted = allowed.get(curr, [])
    if target_stage not in permitted:
        return PhenologyTransitionResult(
            plant_id=state.plant_id, previous_stage=curr, current_stage=curr,
            status="INVALID_INPUT",
            provenance=provenance or "TASK_024; invalid transition",
            notes=f"Transition from '{curr}' to '{target_stage}' not permitted by graph.",
            is_synthetic_example=state.is_synthetic_example,
        )
    event = PhenologyTransitionEvent(
        event_id=f"tx-{curr}-{target_stage}-{timestamp or 't'}",
        plant_id=state.plant_id,
        timestamp=timestamp or datetime.now(timezone.utc),
        from_stage=curr,
        to_stage=target_stage,
        trigger_type=trigger_type,
        reason=reason or f"transition {curr}→{target_stage}",
        provenance=provenance or "TASK_024; explicit transition",
        is_synthetic_example=state.is_synthetic_example,
    )
    new_state = state.model_copy(update={
        "current_stage": target_stage,
        "previous_stage": curr,
        "stage_start_time": timestamp or datetime.now(timezone.utc),
        "transition_count": state.transition_count + 1,
        "transition_history": state.transition_history + [event],
        "last_transition_reason": event.reason,
        "provenance": provenance or state.provenance,
        "status": "VALID",
    })
    return PhenologyTransitionResult(
        plant_id=state.plant_id, previous_stage=curr, current_stage=target_stage,
        event=event, status="VALID",
        provenance=provenance or "TASK_024; transition valid",
        notes="Transition completed; state updated.",
        is_synthetic_example=state.is_synthetic_example,
    )
