"""TASK 046AC — Two-timestep fixtures (synthetic, deterministic)."""
from simulation.core.contracts.domain import PlantArchitecture
from simulation.core.orchestration.fixtures_046ab import ARCH_AB, SOLAR_AB, SOURCE_A_LEAF1, SOURCE_A_LEAF2
ARCH_T = ARCH_AB  # timestep t
ARCH_T1 = PlantArchitecture(architecture_id="arch_046AC_t1", plant_id="p1",
    provenance="TASK_046AC t+1 from delta", is_synthetic_example=True)
PYEOF
echo fixtures_046ac written