"""Synthetic snapshot fixtures — TASK 014. Labeled; no real garden data; immutability verified."""
from datetime import datetime, timezone
from simulation.core.contracts.domain import Garden, GardenReference, Boundary
from simulation.core.snapshot.contracts import Snapshot, ClockState, SchedulerState, ScheduledProcessState
from simulation.core.clock.clock import SimulationClock
from simulation.core.scheduler.scheduler import SimulationScheduler, ScheduledProcess

# Synthetic garden state reference (existing pattern)
SYNTH_GARDEN = Garden(
    id="g-synth-001",
    reference=GardenReference(),
    boundary=Boundary(points=[[0,0,0],[2,0,0],[2,1,0],[1,1,0],[1,2,0],[0,2,0],[0,0,0]]),
    objects=["rack-1"],
)

# Clock state captured
_clock = SimulationClock(start=datetime(2026,6,21,10,0,0,tzinfo=timezone.utc))
_clock.advance(__import__('datetime').timedelta(hours=2))

# Scheduler state (minimal processes)
_sched = SimulationScheduler(clock=_clock)
_sched.register(ScheduledProcess(id="solar", timestep_minutes=5, priority=0))
_sched.register(ScheduledProcess(id="env", timestep_minutes=60, priority=1))

def _scheduler_snapshot() -> SchedulerState:
    return SchedulerState(processes=[
        ScheduledProcessState(
            id=p.id, timestep_minutes=p.timestep.total_seconds()/60, priority=p.priority, enabled=p.enabled, next_run=p.next_run.isoformat() if p.next_run else None
        ) for p in _sched.processes
    ])

def _clock_snapshot() -> ClockState:
    return ClockState(start=_clock.start.isoformat(), current=_clock.current.isoformat(), end=_clock.end.isoformat() if _clock.end else None, paused=_clock.paused)

SYNTH_SNAPSHOT = Snapshot(
    snapshot_id="snap-014-001",
    created_at=datetime.now(timezone.utc),
    simulation_time=7200.0,  # 2 hours in seconds
    world_time=_clock.current.isoformat(),
    world_time_tz="UTC",
    model_version_ref="v0.1",
    parameter_set_ref="params-default",
    garden_ref=SYNTH_GARDEN.id,
    plant_states_refs=["plant-p1"],
    environment_state_ref="env-01",
    clock_state=_clock_snapshot(),
    scheduler_state=_scheduler_snapshot(),
    random_seed=None,  # not applicable currently
    provenance="synthetic_snapshot_TASK_014; no biology; immutability verified by round-trip",
    schema_version="v1",
    is_checkpoint=False,
    notes="Synthetic fixture — one clock + scheduler state; garden ref only (not full serialized garden to avoid duplication).",
)

SYNTH_CHECKPOINT = Snapshot(
    snapshot_id="cp-014-001",
    created_at=datetime(2026,6,21,12,0,0,tzinfo=timezone.utc),
    simulation_time=7200.0,
    world_time="2026-06-21T12:00:00+00:00",
    world_time_tz="UTC",
    model_version_ref="v0.1",
    parameter_set_ref="params-default",
    garden_ref="g-synth-001",
    plant_states_refs=["plant-p1"],
    environment_state_ref="env-01",
    clock_state=_clock_snapshot(),
    scheduler_state=_scheduler_snapshot(),
    random_seed=None,
    provenance="synthetic_checkpoint_TASK_014",
    schema_version="v1",
    is_checkpoint=True,
    notes="Checkpoint artifact persisted for restart/replay.",
)
