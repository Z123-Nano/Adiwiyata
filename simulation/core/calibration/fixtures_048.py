"""TASK 048 — Synthetic calibration-readiness fixtures (no real data, no fitting)."""
from simulation.core.photosynthesis.photosynthesis import PhotosynthesisParameters
from simulation.core.growth.growth_conversion_params import GrowthConversionParameters, growth_params
from simulation.core.physiology.sink_params import SinkParameterSet, sink_parameters

# Active parameter baseline (synthetic; labeled)
PHOTO_BASE = PhotosynthesisParameters(alpha=0.05, pmax=20.0, version="v1", provenance="TASK_048 synthetic baseline", source="SYNTHETIC")

GROWTH_BASE = growth_params("param_leaf_048", "leaf", growth_retention_fraction=0.8, carbon_fraction_of_dry_biomass=0.45, provenance="TASK_048 synthetic; not calibrated", source_type="SYNTHETIC")

SINK_BASE = sink_parameters("param_sink_048", "leaf", sink_coefficient_g_per_m_per_timestep=0.12, provenance="TASK_048 synthetic; not calibrated", source_type="SYNTHETIC")

# Synthetic ground-truth scenarios (for identifiability test — not real calibration)
SCENARIO_A = {"label":"baseline", "alpha":0.05, "pmax":20.0, "retention":0.8, "sink":0.12, "ppfd":400.0}
SCENARIO_A_PLUS_ALPHA = {"label":"+10% alpha", "alpha":0.055, "pmax":20.0, "retention":0.8, "sink":0.12, "ppfd":400.0}
SCENARIO_A_MINUS_ALPHA = {"label":"-10% alpha", "alpha":0.045, "pmax":20.0, "retention":0.8, "sink":0.12, "ppfd":400.0}
SCENARIO_A_PLUS_PMAX = {"label":"+10% pmax", "alpha":0.05, "pmax":22.0, "retention":0.8, "sink":0.12, "ppfd":400.0}
SCENARIO_A_MINUS_PMAX = {"label":"-10% pmax", "alpha":0.05, "pmax":18.0, "retention":0.8, "sink":0.12, "ppfd":400.0}
