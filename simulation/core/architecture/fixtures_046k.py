"""TASK 046K fixtures — synthetic, labeled."""
from simulation.core.architecture.growth_params import architecture_growth_params
SYNTH_ARCH = architecture_growth_params(
    parameter_set_id="arch_v1_leaf",
    organ_type="leaf",
    specific_length_m_per_g_DM=0.02,
    provenance="TASK_046K synthetic; minimal specific-length bridge; not calibrated; 023 g_C noted",
    is_synthetic_example=True,
    note="Synthetic: 0.02 m/g_DM; linear relation.",
)
