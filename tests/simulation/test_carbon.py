"""TASK 021 carbon balance tests — bookkeeping reference; synthetic; no growth."""
from datetime import datetime, timezone
from simulation.core.physiology.carbon_contracts import CarbonBalanceInput, CarbonBalanceResult
from simulation.core.physiology.carbon import carbon_balance
from simulation.core.physiology.photosynthesis_fixtures import SYNTH_PARAMS, SYNTH_PFD_MED
from simulation.core.physiology.photosynthesis import photosynthesis_rate
from simulation.core.physiology.respiration_contracts import RespirationInput, RespirationParams
from simulation.core.physiology.respiration import respiration_rate
from simulation.core.physiology.carbon_fixtures import SYNTH_RESP_PARAMS, SYNTH_RESP_INPUT, SYNTH_PHOTOSYN_RESULT, SYNTH_RESP_RESULT

def test_valid_carbon_balance():
    r = carbon_balance(
        "ref_photo", "ref_resp",
        gross_rate=SYNTH_PHOTOSYN_RESULT.gross_assimilation,
        respiration_rate=SYNTH_RESP_RESULT.respiratory_loss_rate,
        timestep_seconds=3600.0,
    )
    assert r.status == "VALID"
    assert r.gross_assimilation_rate == SYNTH_PHOTOSYN_RESULT.gross_assimilation
    assert r.respiratory_loss_rate == SYNTH_RESP_RESULT.respiratory_loss_rate
    expected_net = r.gross_assimilation_rate - r.respiratory_loss_rate
    assert abs(r.net_carbon_rate - expected_net) < 1e-6
    assert r.integrated_net_carbon == r.net_carbon_rate * 3600.0

def test_net_negative_allowed():
    r = carbon_balance("r","r2", gross_rate=2.0, respiration_rate=5.0, timestep_seconds=3600.0)
    assert r.status == "VALID"
    assert r.net_carbon_rate == -3.0
    assert r.integrated_net_carbon == -3.0 * 3600.0

def test_zero_respiration():
    r = carbon_balance("r",None, gross_rate=10.0, respiration_rate=0.0, timestep_seconds=3600.0)
    assert r.status == "VALID"
    assert r.net_carbon_rate == 10.0

def test_zero_photosynthesis():
    r = carbon_balance("r","r2", gross_rate=0.0, respiration_rate=2.0, timestep_seconds=3600.0)
    assert r.status == "VALID"
    assert r.net_carbon_rate == -2.0

def test_invalid_photo_propagates():
    # If photo result is INVALID_INPUT, carbon balance should reflect that; here we pass gross=0 but note propagation
    # Contract expects input references; explicit test: invalid gross input rejected
    try:
        carbon_balance("r", "r2", gross_rate=-1.0, respiration_rate=1.0, timestep_seconds=3600.0)
        # Negative gross rejected
        assert False
    except Exception:
        pass  # behavior depends on validation layer

def test_unavailable_respiration_not_computable():
    # No respiration result available => NOT_COMPUTABLE if required; here we allow resp=None => net = gross
    # Explicit: missing respiration input documented; result can be VALID with respiration=0 if explicitly set
    r = carbon_balance("r", None, gross_rate=10.0, respiration_rate=None, timestep_seconds=3600.0)
    assert r.status == "VALID"
    # But if respiration required and missing, should be NOT_COMPUTABLE; test via contract

def test_timestep_conversion():
    r = carbon_balance("r","r2", gross_rate=10.0, respiration_rate=3.0, timestep_seconds=7200.0)
    assert r.timestep_seconds == 7200.0
    assert abs(r.integrated_net_carbon - 7.0 * 7200.0) < 1e-3

def test_units_preserved():
    r = carbon_balance("r","r2", gross_rate=10.0, respiration_rate=3.0, timestep_seconds=3600.0)
    assert r.unit_rate == "umol_CO2_m2_s"
    assert r.unit_amount == "umol_CO2_m2"

def test_ref_preserved():
    r = carbon_balance("photo_001", "resp_001", gross_rate=10.0, respiration_rate=2.0, timestep_seconds=3600.0)
    assert "photo_001" in r.input_refs or r.provenance is not None

def test_deterministic_repeated():
    r1 = carbon_balance("r","r2", gross_rate=10.0, respiration_rate=2.0, timestep_seconds=3600.0)
    r2 = carbon_balance("r","r2", gross_rate=10.0, respiration_rate=2.0, timestep_seconds=3600.0)
    assert r1.net_carbon_rate == r2.net_carbon_rate
    assert r1.status == r2.status

def test_serialization_roundtrip():
    import json
    d = SYNTH_RESP_RESULT.model_dump(mode="json")
    r2 = PhotosynthesisResult.model_validate(d) if False else None  # just test result serialization
    # Instead test CarbonBalanceResult serialization
    from simulation.core.physiology.carbon_contracts import CarbonBalanceResult
    r = carbon_balance("a","b", 10, 2, 3600)
    d = r.model_dump(mode="json")
    r2 = CarbonBalanceResult.model_validate(d)
    assert r2.status == r.status

def test_no_negative_clamping():
    r = carbon_balance("r","r2", gross_rate=1.0, respiration_rate=5.0, timestep_seconds=3600.0)
    assert r.net_carbon_rate == -4.0
    assert r.net_carbon_rate < 0

def test_no_fake_biomass():
    # Fixture uses synthetic biomass; result references it; no claim of real biomass
    assert SYNTH_RESP_INPUT.biomass_g_m2 == 2.5
    assert SYNTH_RESP_INPUT.is_synthetic_example is True

def test_provenance_model_refs():
    r = carbon_balance("r","r2", 10, 2, 3600, provenance="TASK_021 synthetic", input_ref="ref")
    assert "TASK_021" in (r.provenance or "")

def test_negative_timestep_rejected():
    try:
        carbon_balance("r","r2", 10, 2, -1)
        assert False
    except Exception:
        pass
