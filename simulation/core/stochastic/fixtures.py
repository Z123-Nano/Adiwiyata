"""Synthetic stochastic fixtures — TASK 027. Synthetic; labeled; not biological."""
from simulation.core.stochastic.contracts import StochasticDistribution, StochasticVariationRequest

def SYNTH_UNIFORM_REQ(base=1.0, seed=42):
    return StochasticVariationRequest(
        parameter_name="growth_efficiency",
        base_value=base,
        distribution=StochasticDistribution(distribution_type="uniform", parameters={"lower":0.9,"upper":1.1}, provenance="TASK_027 synthetic"),
        seed=seed, bounds={"lower":0.9,"upper":1.1}, provenance="TASK_027 synthetic", is_synthetic_example=True)

def SYNTH_TRUNC_REQ(base=1.0, seed=7):
    return StochasticVariationRequest(
        parameter_name="availability_fraction",
        base_value=base,
        distribution=StochasticDistribution(distribution_type="truncated_normal", parameters={"mean":1.0,"sd":0.05}, provenance="TASK_027 synthetic"),
        seed=seed, bounds={"lower":0.8,"upper":1.2}, provenance="TASK_027 synthetic", is_synthetic_example=True)
