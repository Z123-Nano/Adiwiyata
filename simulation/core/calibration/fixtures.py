"""Synthetic calibration fixtures — TASK 028. Synthetic observations from y = alpha*x with true alpha=0.05; labeled."""
from simulation.core.calibration.contracts import CalibrationDataset

# Synthetic observations for scalar calibration (true alpha = 0.05)
SYNTH_CALIB_DATASET = CalibrationDataset(
    dataset_id="synth_alpha_05",
    observation_refs=["obs_1","obs_2","obs_3"],
    variable="gross_rate",
    unit="umol_CO2_m2_s",
    source_provenance="TASK_028 synthetic; deterministic observations from y=alpha*x; alpha_true=0.05",
    inclusion_status="calibration",
    is_synthetic_example=True,
)

# Synthetic observation pairs (x=PFD, y=gross_rate) computed from alpha=0.05
SYNTH_OBS = [
    {"x": 250, "y": 12.5},   # 0.05 * 250
    {"x": 500, "y": 25.0},
    {"x": 1000, "y": 50.0},
    {"x": 1250, "y": 62.5},
]
