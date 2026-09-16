"""SimulationScheduler — TASK 007. Generic, no science."""
from datetime import timedelta
from typing import List, Callable, Optional
from simulation.core.clock.clock import SimulationClock

class ScheduledProcess:
    def __init__(self, id: str, timestep_minutes: float, priority: int = 0, enabled: bool = True):
        if timestep_minutes <= 0:
            raise ValueError("timestep must be positive")
        self.id = id
        self.timestep = timedelta(minutes=timestep_minutes)
        self.priority = priority
        self.enabled = enabled
        self.next_run = None

    def update_next(self, clock_current):
        # Simplified: next = last_run + timestep; initialize at start
        from datetime import timedelta
        if self.next_run is None:
            self.next_run = clock_current
        else:
            self.next_run = self.next_run + self.timestep

class SimulationScheduler:
    def __init__(self, clock: SimulationClock):
        self.clock = clock
        self.processes: List[ScheduledProcess] = []

    def register(self, p: ScheduledProcess):
        p.update_next(self.clock.current)
        self.processes.append(p)

    def disable(self, pid: str):
        for p in self.processes:
            if p.id == pid:
                p.enabled = False

    def enable(self, pid: str):
        for p in self.processes:
            if p.id == pid:
                p.enabled = True

    def due_processes(self):
        due = [p for p in self.processes if p.enabled and p.next_run is not None and p.next_run <= self.clock.current]
        due.sort(key=lambda p: (p.priority, p.id))
        return due

    def step(self, duration_minutes: float, callbacks: Optional[dict] = None):
        if duration_minutes <= 0:
            raise ValueError("duration must be positive")
        self.clock.advance(timedelta(minutes=duration_minutes))
        due = self.due_processes()
        for p in due:
            # Execute deterministic priority-ordered; callback optional
            if callbacks and p.id in callbacks:
                callbacks[p.id]()
            p.update_next(self.clock.current)
        return due

    def run_until(self, target_minutes_from_start: float):
        if target_minutes_from_start < 0:
            raise ValueError("target must be non-negative")
        target = self.clock.start + timedelta(minutes=target_minutes_from_start)
        while self.clock.current < target and (self.clock.end is None or self.clock.current < self.clock.end):
            # Step by smallest process timestep or 1 minute default
            min_step = min((p.timestep.total_seconds()/60 for p in self.processes if p.enabled), default=1.0)
            step_size = min(min_step, (target - self.clock.current).total_seconds()/60)
            if step_size <= 0:
                break
            self.step(step_size)

    def state(self) -> dict:
        return {
            "clock": self.clock.state(),
            "processes": [{"id": p.id, "timestep_min": p.timestep.total_seconds()/60, "priority": p.priority, "enabled": p.enabled, "next_run": p.next_run.isoformat() if p.next_run else None} for p in self.processes],
        }
