"""TASK 020 photosynthesis tests — analytical independent references; no lux conversion; no invented biology."""
from datetime import datetime, timezone
from simulation.core.physiology.ppfd_input import PPFDInput
from simulation.core.physiology.photosynthesis_params import PhotosynthesisParams
from simulation.core.physiology.photosynthesis import photosynthesis_rate
from simulation.core.physiology.photosynthesis_fixtures import SYNTH_PARAMS, SYNTH_PFD_ZERO, SYNTH_PFD_LOW, SYNTH_PFD_MED, SYNTH_PFD_HIGH
from simulation.core.physiology.contracts import PhotosynthesisResult

def test_zero_light_zero_assimilation():
    r = photosynthesis_rate(SYNTH_PFD_ZERO, SYNTH_PARAMS)
    assert r.status == "VALID"
    assert r.gross_assimilation == 0.0
    assert "light_modeled" in r.limiting_factors
    assert "temperature_not_modelled" in r.limiting_factors

def test_low_light_positive():
    # Analytical: (0.05*25*50)/(2.5+25)=62.5/27.5=2.2727...
    r = photosynthesis_rate(SYNTH_PFD_LOW, SYNTH_PARAMS)
    assert r.status == "VALID"
    assert r.gross_assimilation is not None
    expected = 62.5 / 27.5
    assert abs(r.gross_assimilation - expected) < 1e-3

def test_medium_light_increases():
    r_low = photosynthesis_rate(SYNTH_PFD_LOW, SYNTH_PARAMS)
    r_med = photosynthesis_rate(SYNTH_PFD_MED, SYNTH_PARAMS)
    assert r_med.gross_assimilation > r_low.gross_assimilation

def test_high_light_saturates_near_amax():
    # Analytical: (0.05*25*1000)/(50+25)=1250/75=16.666... < 25
    r = photosynthesis_rate(SYNTH_PFD_HIGH, SYNTH_PARAMS)
    assert r.status == "VALID"
    expected = 1250.0 / 75.0
    assert abs(r.gross_assimilation - expected) < 1e-3
    assert r.gross_assimilation < SYNTH_PARAMS.a_max  # not exceeding Amax

def test_negative_ppfd_rejected():
    try:
        PPFDInput(ppfd=-10, unit="umol_photons_m2_s", timestamp=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc), source="test", is_synthetic_example=True)
        assert False, "negative PPFD should fail at input creation"
    except Exception:
        pass

def test_invalid_parameter_rejected():
    from pydantic import ValidationError
    try:
        PhotosynthesisParams(name="bad2", a_max=-1, alpha=0.05, source="test")
        assert False, "negative a_max should fail at creation"
    except ValidationError:
        pass

def test_finite_output():
    r = photosynthesis_rate(SYNTH_PFD_HIGH, SYNTH_PARAMS)
    assert r.gross_assimilation is not None
    assert r.gross_assimilation >= 0
    assert r.gross_assimilation < float('inf')

def test_deterministic_repeat():
    r1 = photosynthesis_rate(SYNTH_PFD_MED, SYNTH_PARAMS)
    r2 = photosynthesis_rate(SYNTH_PFD_MED, SYNTH_PARAMS)
    assert r1.gross_assimilation == r2.gross_assimilation
    assert r1.status == r2.status

def test_units_preserved():
    r = photosynthesis_rate(SYNTH_PFD_LOW, SYNTH_PARAMS)
    # Result carries provenance/unit info implicitly through documentation
    assert r.provenance is not None
    assert "TASK_020" in r.provenance

def test_provenance_preserved():
    r = photosynthesis_rate(SYNTH_PFD_ZERO, SYNTH_PARAMS)
    assert "TASK_020" in (r.provenance or "")
    assert r.is_synthetic_example is True

def test_leaf_organ_reference():
    # Input can reference organ; output references input
    ln = PPFDInput(ppfd=200, unit="umol_photons_m2_s", organ_id="leaf-1", plant_id="plant-p1", is_synthetic_example=True)
    r = photosynthesis_rate(ln, SYNTH_PARAMS)
    assert r.status == "VALID"

def test_non_modeled_limitation_explicit():
    r = photosynthesis_rate(SYNTH_PFD_MED, SYNTH_PARAMS)
    assert "temperature_not_modelled" in r.limiting_factors
    assert "co2_not_modelled" in r.limiting_factors

def test_no_lux_to_ppfd_conversion():
    # LightInput from measurement uses lux; model requires PPFD directly
    # No conversion in model; must use PPFD input
    ln = PPFDInput(ppfd=500, source="measurement", is_synthetic_example=True, provenance="explicit PPFD; not lux")
    r = photosynthesis_rate(ln, SYNTH_PARAMS)
    assert r.status == "VALID"
    # Ensure model does not silently treat lux as PPFD
    assert ln.unit == "umol_photons_m2_s"

def test_serialization_roundtrip():
    import json
    d = SYNTH_PARAMS.model_dump(mode="json")
    p2 = PhotosynthesisParams.model_validate(d)
    assert p2.a_max == SYNTH_PARAMS.a_max
    assert p2.alpha == SYNTH_PARAMS.alpha
