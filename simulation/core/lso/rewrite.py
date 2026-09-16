"""L-System rewrite — deterministic simultaneous replacement; limits enforced."""
from __future__ import annotations
from simulation.core.lso.contracts import LSystemGrammar

def generate_symbols(grammar: LSystemGrammar, iterations: int) -> str:
    if iterations < 0:
        raise ValueError("iterations must be >= 0")
    if iterations > grammar.max_iterations:
        raise ValueError(f"iterations {iterations} exceeds max {grammar.max_iterations}")
    symbols = grammar.axiom
    for i in range(iterations):
        new = []
        for ch in symbols:
            new.append(grammar.rules.get(ch, ch))
        symbols = "".join(new)
        if len(symbols) > grammar.max_symbol_count:
            raise ValueError(f"symbol count {len(symbols)} exceeds max {grammar.max_symbol_count}")
    return symbols
