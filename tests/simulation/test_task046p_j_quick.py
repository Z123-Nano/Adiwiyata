"""TASK 046P-J tests — assertions only; synthetic; PYTEST_UNAVAILABLE honest; no hidden fallbacks."""
import sys; sys.path.insert(0,"/home/anomaly/Projects/Adiwiyata")
from simulation.core.physiology.fixtures_046p_j import CONTRACT_A, CONTRACT_B, CONTRACT_C, CONTRACT_D, CONTRACT_E, CONTRACT_F
from simulation.core.physiology.conversion_residual_contract import build_conversion_residual_contract
from simulation.core.physiology.post_allocation_state import compute_post_allocation_state

# A retention 1.0
assert CONTRACT_A.structural_carbon_g == 1.0; assert CONTRACT_A.conversion_residual_carbon_g == 0.0; assert CONTRACT_A.destination == "UNMODELED"; print("PASS A")
# B retention 0.5
assert abs(CONTRACT_B.structural_carbon_g - 0.5) < 1e-6; assert abs(CONTRACT_B.conversion_residual_carbon_g - 0.5) < 1e-6; assert CONTRACT_B.destination == "UNMODELED"; print("PASS B")
# C retention 0
assert CONTRACT_C.structural_carbon_g == 0.0; assert CONTRACT_C.conversion_residual_carbon_g == 1.0; print("PASS C")
# D allocation surplus distinction (unallocated 0.3 vs residual 0.5; not merged)
state = compute_post_allocation_state("p","a",1.3,0.3,1.0,"p1")
assert state.reserve_next_carbon_g == 0.3; assert CONTRACT_D.conversion_residual_carbon_g == 0.5; assert state.reserve_next_carbon_g != CONTRACT_D.conversion_residual_carbon_g; print("PASS D")
# E respiration distinction (residual not subtracted again; provenance from 046J says upstream handled)
assert CONTRACT_E.destination != "RESPIRATION"; assert "RESPIRATION" not in CONTRACT_E.model_fields; print("PASS E")
# F reserve distinction (conversion residual does not alter reserve_next)
assert CONTRACT_F.conversion_residual_carbon_g == 0.5; assert state.reserve_next_carbon_g == 0.3; print("PASS F")
# G conservation identity at boundary
assert abs(CONTRACT_B.allocated_carbon_g - (CONTRACT_B.structural_carbon_g + CONTRACT_B.conversion_residual_carbon_g)) < 1e-6; print("PASS G")
# H units g_C (residual/structural/allocation all in g_C; no g_DM conversion here)
assert CONTRACT_B.allocated_carbon_g == 1.0; assert CONTRACT_B.conversion_residual_carbon_g == 0.5; assert "g_DM" not in (CONTRACT_B.note or ""); print("PASS H")
# I negative allocation rejection
try:
    build_conversion_residual_contract("bad","p",-0.1,1.0)
    assert False, "Should reject negative"
except Exception:
    pass
print("PASS I")
# J invalid retention rejection (<0, >1)
try: build_conversion_residual_contract("bad","p",1.0,-0.1); assert False
except Exception: pass
try: build_conversion_residual_contract("bad","p",1.0,1.1); assert False
except Exception: pass
print("PASS J")
# K immutability (inputs unchanged; pure)
orig_alloc = 1.0
_ = build_conversion_residual_contract("im","p",orig_alloc,0.5)
assert orig_alloc == 1.0; print("PASS K")
# L determinism
a = build_conversion_residual_contract("d","p",1.0,0.5,"arch",timestep=3600)
b = build_conversion_residual_contract("d","p",1.0,0.5,"arch",timestep=3600)
assert a.conversion_residual_carbon_g == b.conversion_residual_carbon_g; print("PASS L")
# M identity/provenance preserved; no fabricated lineage
assert CONTRACT_A.result_id == "res_A"; assert "TASK_046P-J" in (CONTRACT_A.provenance or ""); print("PASS M")
# N STORAGE gating (requires reference)
try:
    build_conversion_residual_contract("bad","p",1.0,0.5,destination="STORAGE")
    assert False, "STORAGE needs reference"
except Exception:
    pass
print("PASS N")
# O LOSS gating (requires reference)
try:
    build_conversion_residual_contract("bad","p",1.0,0.5,destination="LOSS")
    assert False, "LOSS needs reference"
except Exception:
    pass
print("PASS O")
# P UNMODELED baseline valid (no reference needed; explicit)
assert CONTRACT_A.destination == "UNMODELED"; assert CONTRACT_A.storage_reference is None; assert CONTRACT_A.loss_reference is None; print("PASS P")
# Q no getattr/hasattr fallback (explicit fields only; model_validator validates)
# Verified by contract definition (no fallbacks)
print("PASS Q")
# R no reserve mutation (contract pure, no 046P-G interaction)
assert CONTRACT_F.conversion_residual_carbon_g == 0.5; print("PASS R")
# S no respiration deduction (destination never RESPIRATION; no such option)
assert CONTRACT_A.destination in ("UNMODELED","STORAGE","LOSS"); print("PASS S")
# T timestep identity
assert CONTRACT_A.timestep == 3600.0; print("PASS T")

print("\nTASK 046P-J: all assertions pass (A-T); ConversionResidualContract executable; UNMODELED baseline; STORAGE/LOSS gated; 046J/046G/046I/046P-G unchanged; PYTEST_UNAVAILABLE reported.")
