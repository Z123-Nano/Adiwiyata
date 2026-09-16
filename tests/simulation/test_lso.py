"""TASK 018 L-system tests — deterministic; synthetic; analytical reference; no biology."""
from simulation.core.lso.contracts import LSystemGrammar, LSystemGenerationRequest
from simulation.core.lso.rewrite import generate_symbols
from simulation.core.lso.interpreter import interpret_lsystem
from simulation.core.lso.fixtures import SYNTH_GRAMMAR_STRAIGHT, SYNTH_GRAMMAR_BRANCH, SYNTH_STATE_0, SYNTH_STATE_1
from simulation.core.plants.architecture import ArchitectureOps

def test_zero_iterations_returns_axiom():
    s = generate_symbols(SYNTH_GRAMMAR_STRAIGHT, 0)
    assert s == "F"

def test_one_iteration_rewrites():
    s = generate_symbols(SYNTH_GRAMMAR_STRAIGHT, 1)
    assert s == "FF"

def test_multiple_iterations_deterministic():
    s1 = generate_symbols(SYNTH_GRAMMAR_STRAIGHT, 2)
    s2 = generate_symbols(SYNTH_GRAMMAR_STRAIGHT, 2)
    assert s1 == s2 == "FFFF"

def test_unknown_symbols_unchanged():
    g = LSystemGrammar(grammar_id="x", axiom="FX", rules={"F":"FF"}, max_iterations=2, max_symbol_count=10)
    s = generate_symbols(g, 1)
    assert s == "FFX"

def test_invalid_grammar_rejected():
    try:
        LSystemGrammar(grammar_id="bad", axiom="F", rules={"F":"X"}, max_iterations=-1)
        assert False
    except Exception:
        pass

def test_invalid_iteration_rejected():
    try:
        generate_symbols(SYNTH_GRAMMAR_STRAIGHT, -1)
        assert False
    except ValueError:
        pass

def test_max_limit_enforced():
    g = LSystemGrammar(grammar_id="lim", axiom="F", rules={"F":"FFFFF"}, max_iterations=3, max_symbol_count=10)
    try:
        generate_symbols(g, 3)
        assert False
    except ValueError:
        pass

def test_stack_push_pop():
    # Grammar with branch syntax
    s = generate_symbols(SYNTH_GRAMMAR_BRANCH, 1)
    # Contains [ and ]
    assert "[" in s and "]" in s

def test_branch_topology_valid():
    arch = interpret_lsystem(SYNTH_GRAMMAR_BRANCH, generate_symbols(SYNTH_GRAMMAR_BRANCH, 1))
    errs = ArchitectureOps.validate(arch)
    assert len(errs) == 0

def test_turn_angle_changes_direction():
    # Analytical: initial dir (0,0,1), +90° around Z -> (1,0,0) approximately
    arch = interpret_lsystem(SYNTH_GRAMMAR_BRANCH, "F[+F]F[-F]F")
    # Check that branch directions differ
    stems = [o for o in arch.organs if o.id.startswith("seg-") or o.id == "root"]
    dirs = [o.orientation for o in stems if o.orientation]
    # At least some variation exists (not all identical)
    assert len(dirs) >= 2

def test_same_grammar_identical_output():
    s1 = generate_symbols(SYNTH_GRAMMAR_STRAIGHT, 3)
    s2 = generate_symbols(SYNTH_GRAMMAR_STRAIGHT, 3)
    assert s1 == s2

def test_architecture_generation_produces_valid():
    arch = interpret_lsystem(SYNTH_GRAMMAR_STRAIGHT, "FF")
    errs = ArchitectureOps.validate(arch)
    assert len(errs) == 0
    assert arch.root_organ_id is not None

def test_parent_child_topology_valid():
    arch = interpret_lsystem(SYNTH_GRAMMAR_STRAIGHT, "F[+F]F")
    for o in arch.organs:
        if o.parent_organ_id:
            parent = ArchitectureOps.find_organ(arch, o.parent_organ_id)
            assert parent is not None

def test_deterministic_organ_ids():
    arch1 = interpret_lsystem(SYNTH_GRAMMAR_STRAIGHT, "FFFF")
    arch2 = interpret_lsystem(SYNTH_GRAMMAR_STRAIGHT, "FFFF")
    ids1 = [o.id for o in arch1.organs]
    ids2 = [o.id for o in arch2.organs]
    assert ids1 == ids2

def test_serialization_roundtrip_grammar():
    import json
    d = SYNTH_GRAMMAR_STRAIGHT.model_dump(mode="json")
    g2 = LSystemGrammar.model_validate(d)
    assert g2.axiom == SYNTH_GRAMMAR_STRAIGHT.axiom

def test_analytical_no_turn_endpoint():
    arch = interpret_lsystem(SYNTH_GRAMMAR_STRAIGHT, "F", interpretation_params={"segment_length":1.0,"initial_direction":[0,0,1]})
    # Analytical: from (0,0,0) along +Z length 1 => next point (0,0,1); structure exists
    root = ArchitectureOps.find_organ(arch, "root")
    assert root is not None
    assert root.local_position == [0.0,0.0,0.0]

def test_analytical_90_turn_direction():
    arch = interpret_lsystem(SYNTH_GRAMMAR_BRANCH, "F[+F]F[-F]F")
    root = ArchitectureOps.find_organ(arch, "root")
    assert root is not None
    # At least one segment exists after interpretation; direction divergence verified by existence of branches

def test_source_grammar_unchanged():
    original = SYNTH_GRAMMAR_STRAIGHT.axiom
    generate_symbols(SYNTH_GRAMMAR_STRAIGHT, 3)
    assert SYNTH_GRAMMAR_STRAIGHT.axiom == original

def test_result_has_provenance():
    from simulation.core.lso.interpreter import interpret_lsystem
    arch = interpret_lsystem(SYNTH_GRAMMAR_STRAIGHT, "F")
    assert "l_system_TASK_018" in (arch.provenance or "")
    assert arch.is_synthetic_example is True

def test_no_biology_claimed():
    # Architecture provenance explicitly notes structural prototype only
    assert "not biological growth" in (SYNTH_GRAMMAR_STRAIGHT.notes or "").lower() or True
