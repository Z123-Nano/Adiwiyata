"""TASK 046H-E fixtures — synthetic; clearly labeled; coefficient synthetic."""
from __future__ import annotations
from simulation.core.physiology.sink_params import sink_parameters

# Minimal synthetic parameter — coefficient explicitly not calibrated
SYNTH_SINK_PARAM = sink_parameters(
    parameter_set_id="sink_v1_leaf",
    organ_type="leaf",
    sink_coefficient_g_per_m_per_timestep=2.5,
    structural_proxy_reference="length_m",
    structural_proxy_unit="m",
    provenance="TASK_046H-E synthetic; coefficient not calibrated; proxy=length_m; no biomass contract",
    source_type="SYNTHETIC",
    is_synthetic_example=True,
    note="Synthetic example parameter. Structural proxy limited to length_m.",
)
