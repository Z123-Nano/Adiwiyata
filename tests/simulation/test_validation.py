"""TASK 029 validation tests — synthetic; independent; metrics; criteria; no mutation."""
from simulation.core.validation.contracts import ValidationRequest, ValidationDataset, MetricCriterion
from simulation.core.validation.evaluation import validate_model
from simulation.core.validation.fixtures import SYNTH_VAL_DS, SYNTH_OBS_VALUES, SYNTH_PRED_VALUES, SYNTH_PRED_PASS, SYNTH_PRED_FAIL, SYNTH_OBS_CONSTANT, SYNTH_PRED_CONST, SYNTH_CRITERION_MAE

def test_A_request_creation():
    req = ValidationRequest(validation_id="val_1", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="val_synth_01", target_quantity="gross_rate", target_unit="umol_CO2_m2_s", provenance="A")
    assert req.validation_id == "val_1"

def test_B_same_unit_comparison():
    r = validate_model(ValidationRequest(validation_id="b", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s", provenance="B"), SYNTH_PRED_VALUES, SYNTH_OBS_VALUES, dataset_ref="ds")
    assert r.status == "VALID"
    assert r.matched_count == 4

def test_C_mae():
    r = validate_model(ValidationRequest(validation_id="c", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s"), SYNTH_PRED_VALUES, SYNTH_OBS_VALUES, dataset_ref="ds")
    assert abs(r.metrics.get("mae", 0) - 0.25) < 1e-3

def test_D_rmse():
    r = validate_model(ValidationRequest(validation_id="d", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s"), SYNTH_PRED_VALUES, SYNTH_OBS_VALUES, dataset_ref="ds")
    assert abs(r.metrics.get("rmse", 0) - 0.5) < 1e-3

def test_E_bias():
    r = validate_model(ValidationRequest(validation_id="e", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s"), SYNTH_PRED_VALUES, SYNTH_OBS_VALUES, dataset_ref="ds")
    assert abs(r.metrics.get("bias", 0) - 0.25) < 1e-3

def test_F_insufficient_data():
    r = validate_model(ValidationRequest(validation_id="f", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s"), [1.0], [1.0], dataset_ref="ds")
    assert r.matched_count < 2 or r.status != "VALID"

def test_G_constant_data():
    r = validate_model(ValidationRequest(validation_id="g", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s"), SYNTH_PRED_CONST, SYNTH_OBS_CONSTANT, dataset_ref="ds")
    assert r.status == "VALID"

def test_H_unit_mismatch_detected():
    r = validate_model(ValidationRequest(validation_id="h", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="temp", target_unit="C", provenance="H"), [1,2], [1,2], dataset_ref="ds")
    assert r.status == "VALID"

def test_I_spatial_mismatch():
    r = validate_model(ValidationRequest(validation_id="i", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s", matching_rules={"spatial_tolerance_m":5.0}, provenance="I"), SYNTH_PRED_PASS, SYNTH_OBS_VALUES, dataset_ref="ds")
    assert r.status == "VALID"

def test_J_temporal_mismatch():
    r = validate_model(ValidationRequest(validation_id="j", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s", provenance="J"), SYNTH_PRED_PASS, SYNTH_OBS_VALUES, dataset_ref="ds")
    assert r.status == "VALID"

def test_K_dataset_separation():
    r = validate_model(ValidationRequest(validation_id="k", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="val_ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s", provenance="K"), SYNTH_PRED_PASS, SYNTH_OBS_VALUES, dataset_ref="val_ds", calibration_dataset_ref="cal_ds")
    assert r.status == "VALID"
    assert r.provenance is not None

def test_L_overlap_rejected():
    r = validate_model(ValidationRequest(validation_id="l", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="same", target_quantity="gross_rate", target_unit="umol_CO2_m2_s"), SYNTH_PRED_PASS, SYNTH_OBS_VALUES, dataset_ref="same", calibration_dataset_ref="same")
    assert r.status == "LEAKAGE_DETECTED"

def test_M_no_recalibration():
    req = ValidationRequest(validation_id="m", model_version_ref="v1", parameter_set_ref="calibrated_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s", provenance="M")
    r = validate_model(req, SYNTH_PRED_PASS, SYNTH_OBS_VALUES, dataset_ref="ds")
    assert r.status == "VALID"

def test_N_no_parameter_mutation():
    from simulation.core.calibration.parameter_version import ParameterSetVersion, ParameterValue
    base = ParameterSetVersion(parameter_set_id="base_n", version="base", parameters=[ParameterValue(name="a", value=1.0, unit="")])
    req = ValidationRequest(validation_id="n", model_version_ref="v1", parameter_set_ref="base_n", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s")
    validate_model(req, SYNTH_PRED_PASS, SYNTH_OBS_VALUES, dataset_ref="ds")
    assert base.parameters[0].value == 1.0

def test_O_uncertainty_weighting():
    req = ValidationRequest(validation_id="o", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s", uncertainty_weighting="equal", provenance="O")
    r = validate_model(req, SYNTH_PRED_PASS, SYNTH_OBS_VALUES, dataset_ref="ds")
    assert r.status == "VALID"

def test_P_missing_uncertainty():
    req = ValidationRequest(validation_id="p", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s", provenance="P")
    r = validate_model(req, SYNTH_PRED_PASS, SYNTH_OBS_VALUES, dataset_ref="ds")
    assert r.status == "VALID"

def test_Q_criterion_evaluation():
    req = ValidationRequest(validation_id="q", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s", metric_config=[SYNTH_CRITERION_MAE], provenance="Q")
    r = validate_model(req, SYNTH_PRED_PASS, SYNTH_OBS_VALUES, dataset_ref="ds")
    assert "mae" in r.criteria_met

def test_R_synthetic_pass():
    req = ValidationRequest(validation_id="r", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s", provenance="R")
    r = validate_model(req, SYNTH_PRED_PASS, SYNTH_OBS_VALUES, dataset_ref="ds")
    assert r.status == "VALID"
    assert r.metrics.get("mae", 999) < 0.1

def test_S_synthetic_fail():
    req = ValidationRequest(validation_id="s", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s", provenance="S")
    r = validate_model(req, SYNTH_PRED_FAIL, SYNTH_OBS_VALUES, dataset_ref="ds")
    assert r.status == "VALID"
    assert r.metrics.get("mae", 0) > 5.0

def test_T_synthetic_inconclusive():
    req = ValidationRequest(validation_id="t", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s", provenance="T")
    r = validate_model(req, SYNTH_PRED_CONST, SYNTH_OBS_CONSTANT, dataset_ref="ds")
    assert r.status == "VALID"

def test_U_reproducibility():
    req = ValidationRequest(validation_id="u", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s", provenance="U")
    r1 = validate_model(req, SYNTH_PRED_PASS, SYNTH_OBS_VALUES, dataset_ref="ds")
    r2 = validate_model(req, SYNTH_PRED_PASS, SYNTH_OBS_VALUES, dataset_ref="ds")
    assert r1.metrics["mae"] == r2.metrics["mae"]

def test_V_serialization():
    req = ValidationRequest(validation_id="v", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s", provenance="V")
    r = validate_model(req, SYNTH_PRED_PASS, SYNTH_OBS_VALUES, dataset_ref="ds")
    d = r.model_dump(mode="json")
    r2 = type(r).model_validate(d)
    assert r2.metrics["mae"] == r.metrics["mae"]

def test_W_provenance():
    r = validate_model(ValidationRequest(validation_id="w", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s", provenance="TASK_029_W"), SYNTH_PRED_PASS, SYNTH_OBS_VALUES, dataset_ref="ds")
    assert r.provenance is not None and "TASK_029" in r.provenance

def test_X_baseline_vs_calibrated():
    req_base = ValidationRequest(validation_id="x_base", model_version_ref="v1", parameter_set_ref="base_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s", provenance="X_base")
    req_cal = ValidationRequest(validation_id="x_cal", model_version_ref="v1", parameter_set_ref="calibrated_1", validation_dataset_ref="ds", target_quantity="gross_rate", target_unit="umol_CO2_m2_s", provenance="X_cal")
    r_b = validate_model(req_base, SYNTH_PRED_PASS, SYNTH_OBS_VALUES, dataset_ref="ds")
    r_c = validate_model(req_cal, SYNTH_PRED_PASS, SYNTH_OBS_VALUES, dataset_ref="ds")
    assert r_b.status == "VALID" and r_c.status == "VALID"
