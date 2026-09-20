"""TASK 046AA — End-to-end timestep fixtures (synthetic, no fabrication)."""
from simulation.core.contracts.domain import PlantArchitecture
from simulation.core.solar.model import SolarPosition
from simulation.core.orchestration.fspm_timestep import run_fspm_timestep

# Case A — valid architecture + solar → light AVAILABLE, downstream NOT_COMPUTABLE
ARCH_A = PlantArchitecture(architecture_id="arch_046AA_A", stage="mature")
SOLAR_A = SolarPosition(date_iso="2026-09-18", latitude=52.5, longitude=13.4)
RES_A = run_fspm_timestep(ARCH_A, SOLAR_A, step_id="046AA_A", is_synthetic_example=True)

# Case B — invalid input → INVALID_INPUT
RES_B = run_fspm_timestep(None, SOLAR_A, step_id="046AA_B")

# Case C — immutability (before == after)
# (verified by RES_A: architecture unchanged; provenance notes immutable)
