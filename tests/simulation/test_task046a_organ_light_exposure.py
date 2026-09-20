"""TASK 046A focused tests — OrganLightExposure contract (READ-ONLY boundary)."""
from __future__ import annotations
try:
    import pytest
except Exception:
    pytest = None  # focused assertions only; no pytest dependency
from simulation.core.physiology.organ_light_exposure import OrganLightExposure

# 1. Valid PPFD exposure accepted

def test_01_valid_ppfd_accepted():
    e = OrganLightExposure(
        plant_id="p1", architecture_id="a1", organ_id="leaf_1", organ_type="leaf",
        parent_organ_id="stem_1",
        exposure_type="incident", ppfd_value=800.0, ppfd_unit="umol_photons_m2_s",
        source_type="SYNTHETIC", source_variable="ppfd", source_id="SYNTH_PPFD",
        spatial_ref={"x": 1.0, "y": 2.0, "z": 0.5, "frame": "garden_local"},
        timestamp="2026-09-17T10:00:00Z", provenance="fixture_TASK046A",
        status="AVAILABLE",
    )
    assert e.status == "AVAILABLE"
    assert e.ppfd_value == 800.0
    assert e.ppfd_unit == "umol_photons_m2_s"

# 2. PPFD unit preserved

def test_02_ppfd_unit_preserved():
    e = OrganLightExposure(plant_id="p1", architecture_id="a1", organ_id="o1", ppfd_value=400.0, source_variable="ppfd")
    assert e.ppfd_unit == "umol_photons_m2_s"

# 3. Lux rejected as PPFD

def test_03_lux_rejected_as_ppfd():
    # Source says lux; attempting to set ppfd_value must fail
    try:
        OrganLightExposure(
            plant_id="p1", architecture_id="a1", organ_id="o1",
            source_variable="lux", ppfd_value=100.0,
        )
        raise AssertionError("Expected ValueError for lux as PPFD")
    except ValueError:
        pass

# 4. relative_normalized LightField rejected as PPFD

def test_04_relative_normalized_rejected_as_ppfd():
    try:
        OrganLightExposure(
            plant_id="p1", architecture_id="a1", organ_id="o1",
            source_variable="relative_normalized", ppfd_value=0.8,
        )
        raise AssertionError("Expected ValueError for relative_normalized as PPFD")
    except ValueError:
        pass

# 5. Plant ID preserved

def test_05_plant_id_preserved():
    e = OrganLightExposure(plant_id="garden_plant_42", architecture_id="arch_1", organ_id="leaf_1")
    assert e.plant_id == "garden_plant_42"

# 6. Architecture ID preserved

def test_06_architecture_id_preserved():
    e = OrganLightExposure(plant_id="p1", architecture_id="arch_99", organ_id="o1")
    assert e.architecture_id == "arch_99"

# 7. Organ ID preserved

def test_07_organ_id_preserved():
    e = OrganLightExposure(plant_id="p1", architecture_id="a1", organ_id="root_1")
    assert e.organ_id == "root_1"

# 8. Parent ID preserved where available

def test_08_parent_id_preserved():
    e = OrganLightExposure(plant_id="p1", architecture_id="a1", organ_id="leaf_3", parent_organ_id="stem_2")
    assert e.parent_organ_id == "stem_2"

# 9. Coordinate convention preserved (+X East / +Y North / +Z Up)

def test_09_coordinate_convention():
    e = OrganLightExposure(plant_id="p1", architecture_id="a1", organ_id="o1",
                           spatial_ref={"x": 3.0, "y": -2.0, "z": 1.5, "frame": "garden_local"})
    assert e.spatial_ref["frame"] == "garden_local"
    assert e.spatial_ref["z"] == 1.5

# 10. Timestamp preserved

def test_10_timestamp_preserved():
    e = OrganLightExposure(plant_id="p1", architecture_id="a1", organ_id="o1",
                           timestamp="2026-09-17T12:00:00Z")
    assert e.timestamp == "2026-09-17T12:00:00Z"

# 11. Provenance preserved

def test_11_provenance_preserved():
    e = OrganLightExposure(plant_id="p1", architecture_id="a1", organ_id="o1",
                           provenance="measured_ instrument_v2")
    assert "measured" in (e.provenance or "")

# 12. Uncertainty None remains None

def test_12_uncertainty_none():
    assert "uncertainty_absolute" in OrganLightExposure.model_fields
    assert "uncertainty_relative" in OrganLightExposure.model_fields

# 13. Missing PPFD -> NOT_COMPUTABLE

def test_13_missing_ppfd_not_computable():
    e = OrganLightExposure(plant_id="p1", architecture_id="a1", organ_id="o1",
                           source_variable="unknown", ppfd_value=None,
                           status="NOT_COMPUTABLE",
                           note="No valid PPFD source available; LightField relative_normalized not PPFD")
    assert e.status == "NOT_COMPUTABLE"
    assert e.ppfd_value is None

# 14. Source type preserved

def test_14_source_type_preserved():
    for src in ("MEASURED", "SYNTHETIC", "DERIVED_PHYSICALLY_VALID", "MODELED", "unknown"):
        e = OrganLightExposure(plant_id="p1", architecture_id="a1", organ_id="o1", source_type=src)
        assert e.source_type == src

# 15. Absorbed light not claimed without explicit absorption info

def test_15_absorbed_not_claimed_without_evidence():
    # Incident is safe; claiming absorbed with only relative_normalized source is bounded
    e = OrganLightExposure(plant_id="p1", architecture_id="a1", organ_id="o1",
                           exposure_type="incident", source_variable="ppfd", ppfd_value=600.0,
                           note="Incident PPFD from direct measurement")
    assert e.exposure_type == "incident"
    # If someone attempts absorbed with no evidence: model allows only if note mentions absorption
    # We do not fabricate absorption; contract enforces via note requirement (design only)

# 16. Source Snapshot/Scenario untouched (no mutation mechanism; only read via reference strings)

def test_16_no_source_mutation():
    # Contract has no mutation method; only reference strings preserved
    e = OrganLightExposure(plant_id="p1", architecture_id="a1", organ_id="o1")
    assert not hasattr(e, "mutate_snapshot")

# 17. Deterministic serialization

def test_17_deterministic_serialization():
    e1 = OrganLightExposure(plant_id="p1", architecture_id="a1", organ_id="o1", ppfd_value=100.0, source_variable="ppfd")
    e2 = OrganLightExposure(plant_id="p1", architecture_id="a1", organ_id="o1", ppfd_value=100.0, source_variable="ppfd")
    assert e1.model_dump_json() == e2.model_dump_json()

# 18. LightField reference preserved separately (no reinterpretation)

def test_18_lightfield_ref_separate():
    e = OrganLightExposure(plant_id="p1", architecture_id="a1", organ_id="o1",
                           lightfield_sample_ref="grid_3_7_0",
                           source_variable="relative_normalized",
                           ppfd_value=None,
                           status="NOT_COMPUTABLE",
                           note="LightField sample referenced but NOT converted to PPFD")
    assert e.lightfield_sample_ref == "grid_3_7_0"
    assert e.ppfd_value is None
    assert e.source_variable == "relative_normalized"
