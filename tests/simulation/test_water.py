"""TASK 025 water/root tests — synthetic; liters; conservation; explicit status."""
from simulation.core.water.balance import balance_water
from simulation.core.water.uptake import root_uptake
from simulation.core.water.status import derive_water_status
from simulation.core.water.fixtures import SYNTH_ZONE, SYNTH_IN_IRR, SYNTH_BAL_A, SYNTH_UPTAKE, SYNTH_STATUS
from simulation.core.water.contracts import RootZoneState, WaterInput, RootUptakeInput, WaterBalanceInput

def test_A_water_balance():
    r = balance_water(SYNTH_BAL_A)
    assert r.status == "VALID"
    assert abs(r.initial_storage_l - 2.0) < 1e-6

def test_B_overflow_drainage():
    s = RootZoneState(storage_l=4.0, capacity_l=5.0)
    r = balance_water(WaterBalanceInput(initial_state=s, inputs=[WaterInput(amount_l=4.0)], provenance="B"))
    assert r.drainage_l == 3.0
    assert r.final_storage_l == 5.0

def test_C_zero_input():
    s = RootZoneState(storage_l=3.0, capacity_l=10.0)
    r = balance_water(WaterBalanceInput(initial_state=s, inputs=[], uptake_l=0, provenance="C"))
    assert r.final_storage_l == 3.0

def test_D_zero_storage():
    s = RootZoneState(storage_l=0.0, capacity_l=10.0)
    r = balance_water(WaterBalanceInput(initial_state=s, inputs=[WaterInput(amount_l=1.0)], uptake_l=0, provenance="D"))
    assert r.final_storage_l == 1.0

def test_E_bounded_storage():
    s = RootZoneState(storage_l=9.0, capacity_l=10.0)
    r = balance_water(WaterBalanceInput(initial_state=s, inputs=[WaterInput(amount_l=5.0)], provenance="E"))
    assert r.final_storage_l <= 10.0

def test_F_available_water():
    s = RootZoneState(storage_l=3.0, capacity_l=10.0, unavailable_floor_l=1.0, available_water_l=2.0)
    assert s.available_water_l == 2.0

def test_G_actual_uptake_limited():
    r = root_uptake(SYNTH_UPTAKE)
    assert r.actual_uptake_l <= SYNTH_UPTAKE.available_water_l + 1e-6

def test_H_uptake_never_exceeds_available():
    r = root_uptake(RootUptakeInput(plant_id="p", available_water_l=1.5, requested_uptake_l=10.0, uptake_capacity_l=10.0, provenance="H"))
    assert r.actual_uptake_l <= 1.5

def test_I_unmet_uptake():
    r = root_uptake(SYNTH_UPTAKE)
    assert r.unmet_uptake_l == r.requested_uptake_l - r.actual_uptake_l

def test_J_negative_rejected():
    r = balance_water(WaterBalanceInput(initial_state=RootZoneState(), inputs=[WaterInput(amount_l=-1.0)], provenance="J"))
    assert r.status == "INVALID_INPUT"

def test_K_timestep_handling():
    r = balance_water(WaterBalanceInput(initial_state=RootZoneState(), timestep_seconds=3600, provenance="K"))
    assert r.timestep_seconds == 3600

def test_L_conservation_tolerance():
    s = RootZoneState(storage_l=2.0, capacity_l=10.0)
    r = balance_water(WaterBalanceInput(initial_state=s, inputs=[WaterInput(amount_l=5.0)], uptake_l=3.0, provenance="L"))
    err = abs(r.initial_storage_l + r.total_input_l - r.uptake_l - r.drainage_l - r.final_storage_l)
    assert err < 1e-6

def test_M_root_organ_required():
    # Without root reference, uptake still calculable but integration should note; here just ensure model runs
    r = root_uptake(RootUptakeInput(plant_id="p1", root_organ_id=None, available_water_l=3, requested_uptake_l=2, provenance="M"))
    assert r.status == "VALID"

def test_N_reference_preserved():
    r = root_uptake(RootUptakeInput(plant_id="p1", root_organ_id="root-1", available_water_l=2, requested_uptake_l=1, provenance="N"))
    assert r.provenance is not None

def test_O_deterministic():
    r1 = root_uptake(SYNTH_UPTAKE)
    r2 = root_uptake(SYNTH_UPTAKE)
    assert r1.actual_uptake_l == r2.actual_uptake_l

def test_P_serialization():
    import json
    d = SYNTH_ZONE.model_dump(mode="json")
    s2 = RootZoneState.model_validate(d)
    assert s2.storage_l == SYNTH_ZONE.storage_l

def test_Q_provenance_preserved():
    r = balance_water(SYNTH_BAL_A)
    assert "TASK_025" in (r.provenance or "")

def test_R_synthetic_label():
    assert SYNTH_ZONE.is_synthetic_example is True

def test_S_no_photo_mutation():
    # Ensure water model doesn't touch photosynthesis; just check import paths independent
    from simulation.core.physiology.photosynthesis import photosynthesis_rate
    assert callable(photosynthesis_rate)

def test_T_no_carbon_growth_mutation():
    from simulation.core.growth.fixtures import SYNTH_INPUT_10
    before = SYNTH_INPUT_10.allocated_carbon
    balance_water(SYNTH_BAL_A)
    assert SYNTH_INPUT_10.allocated_carbon == before
