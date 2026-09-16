"""Scheduler / clock tests — TASK 007. No science."""
from datetime import datetime, timezone, timedelta
from simulation.core.clock.clock import SimulationClock
from simulation.core.scheduler.scheduler import SimulationScheduler, ScheduledProcess

def test_clock_init():
    c = SimulationClock()
    assert c.current.tzinfo is not None
    assert c.paused is False

def test_clock_advance():
    c = SimulationClock()
    c.advance(timedelta(minutes=30))
    assert (c.current - c.start).total_seconds() == 1800

def test_clock_reset():
    c = SimulationClock()
    c.advance(timedelta(minutes=10))
    c.reset()
    assert c.current == c.start

def test_pause_resume():
    c = SimulationClock()
    c.pause()
    assert c.paused
    c.resume()
    assert not c.paused

def test_invalid_negative_delta():
    try:
        SimulationClock().advance(timedelta(minutes=-1))
        assert False, "should raise"
    except ValueError:
        pass

def test_invalid_end_before_start():
    try:
        SimulationClock(start=datetime.now(timezone.utc), end=datetime(2020,1,1,tzinfo=timezone.utc))
        assert False
    except ValueError:
        pass

def test_scheduler_single():
    c = SimulationClock()
    s = SimulationScheduler(c)
    p = ScheduledProcess(id="solar", timestep_minutes=5)
    s.register(p)
    s.step(10)
    assert p.next_run > c.start

def test_scheduler_multiple_timesteps():
    c = SimulationClock()
    s = SimulationScheduler(c)
    s.register(ScheduledProcess(id="solar", timestep_minutes=5))
    s.register(ScheduledProcess(id="env", timestep_minutes=60))
    s.step(10)
    due = s.due_processes()
    # solar due every 5 min; env not yet
    ids = {p.id for p in due}
    assert "solar" in ids
    assert "env" not in ids

def test_priority_order():
    c = SimulationClock()
    s = SimulationScheduler(c)
    s.register(ScheduledProcess(id="light", timestep_minutes=10, priority=2))
    s.register(ScheduledProcess(id="solar", timestep_minutes=10, priority=1))
    s.step(10)
    due = s.due_processes()
    assert [p.id for p in due] == ["solar", "light"]

def test_run_until():
    c = SimulationClock()
    s = SimulationScheduler(c)
    s.register(ScheduledProcess(id="a", timestep_minutes=1))
    s.run_until(5)
    assert (c.current - c.start).total_seconds() >= 300

def test_disable_enable():
    c = SimulationClock()
    s = SimulationScheduler(c)
    p = ScheduledProcess(id="x", timestep_minutes=1)
    s.register(p)
    s.disable("x")
    s.step(1)
    assert len(s.due_processes()) == 0

def test_state_serializable():
    c = SimulationClock()
    s = SimulationScheduler(c)
    s.register(ScheduledProcess(id="a", timestep_minutes=5))
    state = s.state()
    assert "clock" in state and "processes" in state
    assert isinstance(state["processes"], list)
