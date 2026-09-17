"""Synthetic growth fixtures — TASK 023. Synthetic efficiency/density; labeled; not calibrated."""
from simulation.core.growth.contracts import OrganGrowthInput, GrowthParam

SYNTH_EFF = GrowthParam(name="carbon_to_biomass_efficiency", value=0.5, unit="g_umol-1", provenance="TASK_023 synthetic; not species-calibrated", is_synthetic_example=True, uncertainty_note="placeholder efficiency")
SYNTH_DENS = GrowthParam(name="tissue_density_g_m3", value=500.0, unit="g_m-3", provenance="TASK_023 synthetic; generic placeholder", is_synthetic_example=True, uncertainty_note="not measured")
SYNTH_GEOM = GrowthParam(name="derive_geometry", value=1.0, unit="bool_flag", provenance="TASK_023 synthetic; enable geometry derivation", is_synthetic_example=True)

SYNTH_INPUT_10 = OrganGrowthInput(
    organ_id="stem-1", organ_type="stem", allocated_carbon=10.0,
    current_organ_state={"length_m": 1.0, "radius_m": 0.05},
    growth_params=[SYNTH_EFF], provenance="TASK_023 synthetic; mass-only", is_synthetic_example=True)
SYNTH_INPUT_0 = OrganGrowthInput(
    organ_id="leaf-1", organ_type="leaf", allocated_carbon=0.0,
    current_organ_state={"length_m": 0.5, "radius_m": 0.02},
    growth_params=[SYNTH_EFF], provenance="TASK_023 synthetic; zero", is_synthetic_example=True)
SYNTH_INPUT_NEG = OrganGrowthInput(
    organ_id="stem-bad", organ_type="stem", allocated_carbon=-4.0,
    current_organ_state={"length_m": 1.0}, provenance="TASK_023 synthetic; invalid", is_synthetic_example=True)
SYNTH_INPUT_GEOM = OrganGrowthInput(
    organ_id="branch-1", organ_type="branch", allocated_carbon=4.0,
    current_organ_state={"length_m": 2.0, "radius_m": 0.1},
    growth_params=[SYNTH_EFF, SYNTH_DENS, SYNTH_GEOM], provenance="TASK_023 synthetic; geometry derived", is_synthetic_example=True)
