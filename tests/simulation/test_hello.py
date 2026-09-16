def test_hello():
    from simulation.core.engine.hello import hello
    assert hello() == "simulation core loaded (no domain logic yet)"
