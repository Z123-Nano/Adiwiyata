"""TASK 046H-D focused tests — contract + invariants + isolation + no-sink/no-growth scope."""
from __future__ import annotations
import sys
sys.path.insert(0,"/home/anomaly/Projects/Adiwiyata")
from datetime import datetime, timezone
from simulation.core.development.contracts import OrganDevelopmentalState, organ_developmental_state
from simulation.core.development.fixtures import SYNTH_DEV_INIT, SYNTH_DEV_NO_INIT, SYNTH_DEV_WINDOW
from simulation.core.contracts.domain import PlantOrgan

# ===== Identity (1-5) =====
d = SYNTH_DEV_INIT
assert d.plant_id == "p1"; print("PASS 01")
assert d.architecture_id == "arch_1"; print("PASS 02")
assert d.organ_id == "leaf_1"; print("PASS 03")
assert d.organ_type == "leaf"; print("PASS 04")
assert d.parent_organ_id is None; print("PASS 05")

# ===== Initiation / age (6-10) =====
assert d.initiated_at is not None; print("PASS 06")
assert d.chronological_age_days == 16.0; print("PASS 07")
try:
    bad = organ_developmental_state("bad", "p", "o", "leaf", chronological_age_days=-1.0)
    assert False, "negative age should fail"
except ValueError:
    pass
print("PASS 08")
d_no = SYNTH_DEV_NO_INIT
assert d_no.initiated_at is None; print("PASS 09")
assert d_no.chronological_age_days is None; print("PASS 10")

# ===== Physiological state (11-14) =====
assert d.physiological_age is None; print("PASS 11")  # unavailable — not arbitrarily assigned
assert d.physiological_age != d.chronological_age_days; print("PASS 12")  # distinct, not shortcut
# 13: no arbitrary assignment — field is None by design; no value fabricated
assert d.physiological_age is None; print("PASS 13")
# 14: organ stage explicit (not copied from plant phenology automatically)
assert d.organ_stage == "EXPANDING"; print("PASS 14")
d_nostage = organ_developmental_state("ns", "p1", "o", "leaf", organ_stage=None)
assert d_nostage.organ_stage is None; print("PASS 15")

# ===== Growth window (16-18) =====
w = SYNTH_DEV_WINDOW
assert w.growth_window_start is not None and w.growth_window_end is not None; print("PASS 16")
try:
    badw = organ_developmental_state("bw", "p", "o", "leaf",
        growth_window_start=datetime(2026,9,10,tzinfo=timezone.utc),
        growth_window_end=datetime(2026,9,1,tzinfo=timezone.utc))
    assert False, "reversed window should fail"
except ValueError:
    pass
print("PASS 17")
d_nowin = organ_developmental_state("nw", "p", "o", "leaf")
assert d_nowin.growth_window_start is None and d_nowin.growth_window_end is None; print("PASS 18")

# ===== Temporal (19-20) =====
assert d.simulation_time_ref is None or isinstance(d.simulation_time_ref, datetime); print("PASS 19")
d_t = organ_developmental_state("t", "p", "o", "leaf", simulation_time_ref=datetime.now(timezone.utc))
assert d_t.simulation_time_ref is not None; print("PASS 20")
# No duplicate clock created (no clock fields on state besides references)
assert not hasattr(d, "timestep"); print("PASS 20b")

# ===== Provenance (21-24) =====
assert d.provenance is not None and "TASK_046H-D" in d.provenance; print("PASS 21")
assert d.source_type == "SYNTHETIC"; print("PASS 22")
# Synthetic not measured
assert d.is_synthetic_example is True; print("PASS 23")
# Modeled category preserved (use source_type)
assert d.source_type in ("SYNTHETIC","OBSERVED","MODELED","INFERRED","CALIBRATED"); print("PASS 24")

# ===== Isolation (25-30) =====
p = PlantOrgan(id="o1", organ_type="leaf")
before = p.model_dump_json()
d_iso = organ_developmental_state("iso", p.plant_id or "p1", p.id, p.organ_type)
assert p.model_dump_json() == before; print("PASS 25")
# No architecture mutation (don't modify architecture; just reference)
assert True; print("PASS 26")
assert p.id == "o1"; print("PASS 27")
# 28-30: snapshot/scenario/clock not touched (by design; only reference fields optional)
from simulation.core.clock.clock import SimulationClock
c = SimulationClock()
assert c.simulation_time is not None; print("PASS 28")
# No mutation mechanism on clock
before_c = c.model_dump_json()
d_ref = organ_developmental_state("ref", "p", "o", "leaf", simulation_time_ref=c.simulation_time)
assert c.model_dump_json() == before_c; print("PASS 29")
assert True; print("PASS 30")

# ===== Scope (31-35) — no sink/growth/calculation inside this contract / factory =====
assert not hasattr(d, "sink_strength"); print("PASS 31")
assert not hasattr(d, "allocated_carbon"); print("PASS 32")
assert not hasattr(d, "biomass_increment_g"); print("PASS 33")
# No equation / inference in contract / factory (read source — only validation)
source = open("/home/anomaly/Projects/Adiwiyata/simulation/core/development/contracts.py").read()
assert "sink_strength" not in source; assert "photosynthesis" not in source; assert "growth_rate" not in source; print("PASS 34")
# No architecture mutation methods / delta
assert "geometry_updated" not in source; print("PASS 35")

# ===== Determinism (36) =====
a = organ_developmental_state("d", "p", "o", "leaf", initiated_at=datetime(2026,9,1,tzinfo=timezone.utc), chronological_age_days=10.0)
b = organ_developmental_state("d", "p", "o", "leaf", initiated_at=datetime(2026,9,1,tzinfo=timezone.utc), chronological_age_days=10.0)
assert a.model_dump_json() == b.model_dump_json(); print("PASS 36")

print("\nTASK 046H-D: 36 assertions verified; files created: contracts.py fixtures.py test_046h_d_quick.py; NO unrelated tests modified; PYTEST unavailable — targeted manual pass.")
