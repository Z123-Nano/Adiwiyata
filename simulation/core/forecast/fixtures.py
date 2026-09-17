"""Synthetic forecast fixtures — TASK 030. Synthetic snapshot/ref; labeled."""
from simulation.core.forecast.contracts import ForecastRequest, ForecastTarget, ModelCandidate, ModelComparisonRequest

SYNTH_SNAPSHOT_REF = "snap_001"
SYNTH_SCENARIO_REF = "scen_baseline"
SYNTH_REQ = ForecastRequest(
    forecast_id="fcast_1", source_snapshot_ref=SYNTH_SNAPSHOT_REF, scenario_ref=SYNTH_SCENARIO_REF,
    model_version_ref="v1", parameter_set_ref="base_1", target_times=[1.0, 3.0],
    targets=[ForecastTarget(variable="gross_rate", unit="umol_CO2_m2_s")],
    provenance="TASK_030 synthetic; baseline scenario", is_synthetic_example=True)
SYNTH_REQ_SCENARIO = ForecastRequest(
    forecast_id="fcast_2", source_snapshot_ref=SYNTH_SNAPSHOT_REF, scenario_ref="scen_alt",
    model_version_ref="v1", parameter_set_ref="calibrated_1", target_times=[2.0],
    targets=[ForecastTarget(variable="gross_rate", unit="umol_CO2_m2_s")],
    provenance="TASK_030 synthetic; alternate scenario", is_synthetic_example=True)

SYNTH_CANDIDATE_A = ModelCandidate(candidate_id="cA", model_version_ref="v1", parameter_set_ref="base_1", description="base model", provenance="TASK_030", is_synthetic_example=True)
SYNTH_CANDIDATE_B = ModelCandidate(candidate_id="cB", model_version_ref="v1", parameter_set_ref="calibrated_1", description="calibrated model", provenance="TASK_030", is_synthetic_example=True)
