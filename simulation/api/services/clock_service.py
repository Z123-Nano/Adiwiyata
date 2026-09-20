"""TASK 042 — Clock service reads actual TASK 007 domain instance."""
from simulation.api.schemas.clock import ClockResponse
from simulation.core.clock.clock import get_simulation_clock

def clock_service():
    clock = get_simulation_clock()
    return ClockResponse(
        simulation_time=clock.simulation_time.isoformat() if hasattr(clock.simulation_time, "isoformat") else str(clock.simulation_time),
        world_time=clock.world_time.isoformat() if hasattr(clock.world_time, "isoformat") else str(clock.world_time),
        observation_time=clock.observation_time.isoformat() if hasattr(clock.observation_time, "isoformat") else str(clock.observation_time),
        timestep=clock.timestep,
        timestep_mode=clock.timestep_mode,
        timezone=clock.timezone,
        plant_age="UNAVAILABLE (TASK 007 domain does not define plant age; not derived in React)",
        forecast_target="UNAVAILABLE (forecast contract not loaded / not computed)",
        scheduler_status=clock.scheduler.status,
        clock_status=clock.clock_status,
        provenance=f"TASK_042; source = TASK 007 SimulationClock v{clock.version}; deterministic; provenance={clock.provenance}",
        version=clock.version,
        note="Domain-backed; no browser-time substitution; no mutation endpoint.",
    )
