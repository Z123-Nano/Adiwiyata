"""Synthetic L-system fixtures — TASK 018. Explicit; synthetic; no biology claimed."""
from simulation.core.lso.contracts import LSystemGrammar, LSystemState, LSystemGenerationRequest, GenerationResult
from simulation.core.lso.rewrite import generate_symbols
from simulation.core.lso.interpreter import interpret_lsystem

SYNTH_GRAMMAR_STRAIGHT = LSystemGrammar(
    grammar_id="grammar-018-straight",
    axiom="F",
    rules={"F": "FF"},
    max_iterations=5,
    max_symbol_count=100,
    segment_length=1.0,
    turn_angle_deg=0.0,
    radius_m=0.01,
    initial_direction=[0.0,0.0,1.0],
    provenance="synthetic_TASK_018; straight axis grammar; not biological",
    is_synthetic_example=True,
    notes="Axiom F, rule F->FF: linear extension only.",
)

SYNTH_GRAMMAR_BRANCH = LSystemGrammar(
    grammar_id="grammar-018-branch",
    axiom="F",
    rules={"F": "F[+F]F[-F]F"},
    max_iterations=3,
    max_symbol_count=500,
    segment_length=1.0,
    turn_angle_deg=90.0,
    radius_m=0.01,
    initial_direction=[0.0,0.0,1.0],
    provenance="synthetic_TASK_018; small recursive branch; not biological",
    is_synthetic_example=True,
    notes="Simple branching grammar for prototype.",
)

# Pre-computed symbolic outputs (verified independently: iteration 0 = axiom; iteration 1 = rule applied)
SYNTH_STATE_0 = LSystemState(grammar_id="grammar-018-straight", symbols="F", iteration=0, provenance="fixture_TASK_018")
SYNTH_STATE_1 = LSystemState(grammar_id="grammar-018-straight", symbols="FF", iteration=1, provenance="fixture_TASK_018")
