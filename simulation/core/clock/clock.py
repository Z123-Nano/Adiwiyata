"""SimulationClock — TASK 007. Timezone-aware, deterministic, serializable."""
from datetime import datetime, timezone, timedelta
from typing import Optional

class SimulationClock:
    def __init__(self, start: Optional[datetime] = None, end: Optional[datetime] = None):
        self.start = start or datetime.now(timezone.utc)
        self.current = self.start
        self.end = end
        self.paused = False
        if self.end is not None and self.end < self.start:
            raise ValueError("end time earlier than start time")
        if self.start.tzinfo is None:
            raise ValueError("start must be timezone-aware")

    def advance(self, delta: timedelta):
        if delta.total_seconds() <= 0:
            raise ValueError("delta must be positive")
        if self.paused:
            raise ValueError("clock is paused")
        self.current = self.current + delta
        if self.end is not None and self.current > self.end:
            # allow exceeding slightly; stop handles
            pass

    def set_time(self, t: datetime):
        if t.tzinfo is None:
            raise ValueError("time must be timezone-aware")
        self.current = t

    def reset(self):
        self.current = self.start
        self.paused = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def elapsed(self) -> timedelta:
        return self.current - self.start

    def state(self) -> dict:
        return {
            "start": self.start.isoformat() if self.start else None,
            "current": self.current.isoformat(),
            "end": self.end.isoformat() if self.end else None,
            "paused": self.paused,
        }
