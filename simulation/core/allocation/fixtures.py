"""Synthetic fixtures — TASK 022. Allocation only; synthetic demands; no growth."""
from simulation.core.allocation.contracts import CarbonSource, CarbonSink, SourceSinkAllocationRequest

SYNTH_SOURCE_10 = CarbonSource(
    source_id="src-10", plant_id="p1", available_carbon=10.0,
    timestep_seconds=3600.0, provenance="TASK_022 synthetic; full demand", is_synthetic_example=True)
SYNTH_SOURCE_5 = CarbonSource(
    source_id="src-5", plant_id="p1", available_carbon=5.0,
    timestep_seconds=3600.0, provenance="TASK_022 synthetic; limiting", is_synthetic_example=True)
SYNTH_SOURCE_NEG = CarbonSource(
    source_id="src-neg", plant_id="p1", available_carbon=-3.0,
    timestep_seconds=3600.0, provenance="TASK_022 synthetic; deficit", is_synthetic_example=True)
SYNTH_SOURCE_0 = CarbonSource(
    source_id="src-0", plant_id="p1", available_carbon=0.0,
    timestep_seconds=3600.0, provenance="TASK_022 synthetic; zero", is_synthetic_example=True)

SYNTH_SINK_STEM = CarbonSink(sink_id="stem", plant_id="p1", organ_id="stem-1", sink_type="stem", demand=5.0, provenance="TASK_022 synthetic", is_synthetic_example=True)
SYNTH_SINK_ROOT = CarbonSink(sink_id="root", plant_id="p1", organ_id="root-1", sink_type="root", demand=3.0, provenance="TASK_022 synthetic", is_synthetic_example=True)
SYNTH_SINK_LEAF = CarbonSink(sink_id="leaf", plant_id="p1", organ_id="leaf-1", sink_type="leaf", demand=2.0, provenance="TASK_022 synthetic", is_synthetic_example=True)
SYNTH_SINK_ZERO = CarbonSink(sink_id="zero", plant_id="p1", sink_type="other", demand=0.0, provenance="TASK_022 synthetic; zero demand", is_synthetic_example=True)
SYNTH_SINK_NEG = CarbonSink(sink_id="bad", plant_id="p1", sink_type="other", demand=-1.0, provenance="TASK_022 synthetic; invalid", is_synthetic_example=True)
SYNTH_SINK_NOD = CarbonSink(sink_id="nodemand", plant_id="p1", sink_type="other", demand=None, provenance="TASK_022 synthetic; unavailable", is_synthetic_example=True)

def SYNTH_REQ(source, sinks, policy="proportional_demand", provenance="TASK_022 synthetic"):
    return SourceSinkAllocationRequest(
        source=source, sinks=sinks, allocation_policy=policy,
        provenance=provenance, is_synthetic_example=True)
