"""TASK 046J fixtures — synthetic, labeled."""
from simulation.core.growth.growth_conversion_params import growth_params
SYNTH_GROWTH = growth_params(
    parameter_set_id="growth_v1_leaf",
    organ_type="leaf",
    growth_retention_fraction=1.0,
    carbon_fraction_of_dry_biomass=0.5,
    provenance="TASK_046J synthetic; not calibrated; TASK 023 unit=g_C incompatible with g_DM",
    source_type="SYNTHETIC",
    is_synthetic_example=True,
    note="Synthetic: retention=1, carbon_frac=0.5 → biomass = 2× allocated.",
)
