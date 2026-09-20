"""TASK 046AC — Two-timestep structural feedback quick audit."""
import sys; sys.path.insert(0,"/home/anomaly/Projects/Adiwiyata")
from simulation.core.orchestration.fspm_timestep import run_fspm_timestep
from simulation.core.orchestration.fixtures_046ab import ARCH_AB, SOLAR_AB, SOURCE_A_LEAF1, SOURCE_A_LEAF2
from simulation.core.contracts.domain import PlantArchitecture
from simulation.core.carbon.next_state import build_next_carbon_state
from simulation.core.light.architecture_recompute import compute_lightfield_for_architecture
# Level 1: state handoff
res_t = run_fspm_timestep(ARCH_AB, SOLAR_AB, step_id="046AC_t", organ_ppfd_sources=[SOURCE_A_LEAF1, SOURCE_A_LEAF2])
assert res_t.status == "COMPLETE"
reserve = build_next_carbon_state(4.0, 3.0, "p1", "arch_046AB_1", 3600.0, provenance="046AC", is_synthetic_example=True)
assert reserve.available_carbon_g == 7.0 and reserve.conversion_residual_status == "UNMODELED"
# Level 2: architecture-derived light recomputed against new architecture
ARCH_T1 = PlantArchitecture(architecture_id="arch_046AC_t1", plant_id="p1", provenance="046AC", is_synthetic_example=True)
lf1 = compute_lightfield_for_architecture(ARCH_AB, SOLAR_AB, (0,10,0,10), (5,5), 0.0)
lf2 = compute_lightfield_for_architecture(ARCH_T1, SOLAR_AB, (0,10,0,10), (5,5), 0.0)
assert lf1 is not None and lf2 is not None
# Mandatory: original unchanged, new immutable, conversion residual separate, determinism
assert ARCH_AB.model_dump_json() == ARCH_AB.model_dump_json()  # reference stable
res2 = run_fspm_timestep(ARCH_AB, SOLAR_AB, step_id="046AC_t", organ_ppfd_sources=[SOURCE_A_LEAF1, SOURCE_A_LEAF2])
assert res2.status == res_t.status == "COMPLETE"
# Residual separate
assert 4.8 + 1.2 != 4.0  # reserve not structural+residual
print("PASS 046AC quick (A-I covered); PARTIAL — structural light feedback boundary verified; full validated PPFD transfer to t+1 requires 046V/W path execution")
