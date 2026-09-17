"""Synthetic validation fixtures — TASK 029. Independent observations; synthetic predictions; labeled."""
from simulation.core.validation.contracts import ValidationDataset, MetricCriterion

SYNTH_VAL_DS = ValidationDataset(
    dataset_id="val_synth_01",
    role="validation",
    observation_refs=["obs_v1","obs_v2","obs_v3","obs_v4"],
    variable="gross_rate",
    unit="umol_CO2_m2_s",
    provenance="TASK_029 synthetic; independent of calibration ds",
    is_synthetic_example=True,
)

# Synthetic independent observations (not derived from calibration)
SYNTH_OBS_VALUES = [1.0, 2.0, 3.0, 4.0]
# Synthetic predictions (slightly off: 1,2,3,5 => bias 0.25, MAE 0.25, RMSE 0.5)
SYNTH_PRED_VALUES = [1.0, 2.0, 3.0, 5.0]
# Synthetic PASS case (close match)
SYNTH_PRED_PASS = [1.01, 2.02, 2.99, 4.01]
# Synthetic FAIL case (large error)
SYNTH_PRED_FAIL = [10.0, 10.0, 10.0, 10.0]
# Constant observed => correlation undefined
SYNTH_OBS_CONSTANT = [2.0, 2.0, 2.0, 2.0]
SYNTH_PRED_CONST = [1.9, 2.1, 2.0, 2.2]

SYNTH_CRITERION_MAE = MetricCriterion(metric_name="mae", max_allowed_error=0.5, unit="umol_CO2_m2_s", provenance="TASK_029 synthetic", is_synthetic_example=True)
