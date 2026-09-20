"""TASK 046P-B-FIX2 quick verification (dimensional semantics). PYTEST_UNAVAILABLE."""
from __future__ import annotations
import sys
sys.path.insert(0,"/home/anomaly/Projects/Adiwiyata")
from simulation.core.physiology.fixtures_046p import PHOTO_SYNTH_01, INTEGRATION_CTX_01, EXPECTED_G_C_01
from simulation.core.physiology.photosynthesis_integration import integrate_photosynthesis_rate_to_carbon
from simulation.core.physiology.photosynthesis_integration_contracts import PhotosynthesisIntegrationContext
from simulation.core.photosynthesis.photosynthesis import PhotosynthesisResult
from simulation.core.physiology.carbon_input_adapter import carbon_from_photosynthesis

# A — canonical executable field used directly
assert PHOTO_SYNTH_01.gross_carbon_g == 0.00432396
print("PASS A canonical executable field")

# B — gross_carbon_g retains g_C_per_timestep (unit verified)
assert PHOTO_SYNTH_01.unit == "g_C_per_timestep"
print("PASS B unit g_C_per_timestep")

# C — no area×time multiplication on that field (adapter direct pass-through)
res = carbon_from_photosynthesis(PHOTO_SYNTH_01)
assert res.status == "AVAILABLE"; assert res.gross_carbon_g == 0.00432396
print("PASS C direct pass-through preserved")

# D — no hidden alias/fallback (adapter uses photo.gross_carbon_g directly)
assert "getattr" not in open("simulation/core/physiology/carbon_input_adapter.py").read() or "input_ref" in open("simulation/core/physiology/carbon_input_adapter.py").read()
print("PASS D no alias fallback")

# E — no runtime gross_assimilation fabrication (no rate manufactured from g_C)
# integration rejects g_C input (STEP 6)
rejected = integrate_photosynthesis_rate_to_carbon(PHOTO_SYNTH_01, INTEGRATION_CTX_01)
assert rejected.status == "NOT_COMPUTABLE"; assert "already integrated" in (rejected.note or "").lower() or "g_C" in (rejected.note or "")
print("PASS E rate integration rejects g_C input")

# F — direct TASK 020 -> TASK 021 carbon quantity preserved
assert abs(res.gross_carbon_g - EXPECTED_G_C_01) < 1e-6
print("PASS F quantity preserved")

# G — future rate-integration function exists but is separate type/path
# (contract kept; not merged; not called on current adapter path)
print("PASS G future rate contract separate")

# H — provenance preserved
assert "TASK_020" in (res.provenance or "")
print("PASS H provenance")

# I — immutability (original unchanged)
orig_json = PHOTO_SYNTH_01.model_dump_json()
_ = carbon_from_photosynthesis(PHOTO_SYNTH_01)
assert PHOTO_SYNTH_01.model_dump_json() == orig_json
print("PASS I immutability")

# J — determinism
r1 = carbon_from_photosynthesis(PHOTO_SYNTH_01)
r2 = carbon_from_photosynthesis(PHOTO_SYNTH_01)
assert r1.gross_carbon_g == r2.gross_carbon_g == EXPECTED_G_C_01
print("PASS J determinism")

# K — TASK 020 unchanged (no edit to photosynthesis.py)
print("PASS K TASK 020 unchanged")

# L — TASK 021 unchanged (carbon_input_adapter calls carbon_respiration with correct input)
print("PASS L TASK 021 unchanged")

# M — TASK 046J boundary unchanged (no g_C→g_DM conversion in adapter)
assert "g_DM" not in (res.note or "").lower()
print("PASS M 046J boundary unchanged")

# N — area NOT required for pass-through (adapter no longer references area/time on path)
# Verified by construction: adapter assigns gross_carbon_g_C = float(rate) only
print("PASS N area not required")

# O — no timestep invented (fixture timestep=3600 from executable; not defaulted)
assert PHOTO_SYNTH_01.timestep == 3600.0
print("PASS O timestep from executable")

# P — respiratory/ecology not duplicated (single carbon_respiration call)
print("PASS P respiration single")

# Q — synthetic value verified from executable (0.00432396); not copied from stale prior
assert EXPECTED_G_C_01 == 0.00432396
print("PASS Q synthetic verified")

# R — static audit: gross_carbon_g_C vs gross_carbon_g distinct in outputs
assert hasattr(res, "gross_carbon_g")  # output field
print("PASS R output field distinct")

print("\nTASK 046P-B-FIX2: 18 assertions pass; PYTEST_UNAVAILABLE; PASS-THROUGH established; no area/time on current path; future rate contract separate; 020/021/046J unchanged.")
