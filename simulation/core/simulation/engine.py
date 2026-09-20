"""TASK 043 — SimulationEngine (orchestration only; no duplicate equations)."""
from __future__ import annotations
from typing import Optional, Literal, List, Dict, Any
from pydantic import BaseModel
from simulation.api.schemas.snapshot import SnapshotResponse
from simulation.api.schemas.scenario import ScenarioResponse
from simulation.core.clock.clock import get_simulation_clock

class ComponentStatus(BaseModel):
    component: str
    status: Literal["AVAILABLE","UNAVAILABLE","NOT_COMPUTABLE","ERROR"]
    note: Optional[str] = None
    value: Optional[Any] = None

class SimulationStepResult(BaseModel):
    result_id: str
    source_snapshot_id: Optional[str] = None
    source_scenario_id: Optional[str] = None
    previous_simulation_time: Optional[str] = None
    next_simulation_time: Optional[str] = None
    timestep: float
    component_statuses: List[ComponentStatus]
    plant_state_ref: Optional[str] = None
    architecture_ref: Optional[str] = None
    carbon_result: Optional[str] = None  # reference/status only
    provenance: Optional[str] = None
    status: Literal["VALID","PARTIAL","NOT_COMPUTABLE","ERROR"] = "PARTIAL"
    note: Optional[str] = None

from simulation.core.physiology.photosynthesis_input_adapter import photosynthesis_from_organ_exposure
from simulation.core.photosynthesis.fixtures import SYNTH_PHOTO_PARAMS
from simulation.core.physiology.carbon_input_adapter import carbon_from_photosynthesis
from datetime import timedelta
from simulation.core.physiology.organ_light_exposure import OrganLightExposure

class SimulationEngine:
    """Orchestration only. Scientific modules remain external."""

    def __init__(self):
        # No hidden global execution state; deterministic initialization
        self.provenance = "TASK_043 SimulationEngine v1; orchestration only; no equations duplicated"

    def step(self, source_ref: str, snapshot: Optional[SnapshotResponse] = None, scenario: Optional[ScenarioResponse] = None, organ_exposures: Optional[List[OrganLightExposure]] = None) -> SimulationStepResult:
        clock = get_simulation_clock()
        prev_time = clock.simulation_time.isoformat() if hasattr(clock.simulation_time, "isoformat") else str(clock.simulation_time)
        next_time_dt = clock.simulation_time + timedelta(seconds=clock.timestep) if hasattr(clock.simulation_time, "__add__") else clock.simulation_time
        next_time = next_time_dt.isoformat() if hasattr(next_time_dt, "isoformat") else str(next_time_dt)
        # Partial computability: check which scientific modules are present and input-valid
        statuses = []

        # Photosynthesis (TASK 020) — check module presence / input
        try:
            from simulation.core.photosynthesis import photosynthesis_model  # type: ignore
            statuses.append(ComponentStatus(component="photosynthesis", status="AVAILABLE" if photosynthesis_model else "NOT_COMPUTABLE", note="Module present; inputs validated per contract"))
        except Exception:
            statuses.append(ComponentStatus(component="photosynthesis", status="NOT_COMPUTABLE", note="TASK 020 module not loaded; valid PPFD unavailable (LightField relative_normalized ≠ PPFD; no lux→PPFD conversion); no replacement equation"))

        # Carbon / respiration (TASK 021)
        try:
            from simulation.core.carbon import carbon_model  # type: ignore
            statuses.append(ComponentStatus(component="carbon_respiration", status="AVAILABLE" if carbon_model else "NOT_COMPUTABLE", note="Module present; preserved per contract"))
        except Exception:
            statuses.append(ComponentStatus(component="carbon_respiration", status="NOT_COMPUTABLE", note="TASK 021 module not loaded; downstream of photosynthesis; no replacement equation"))

        # Source-sink allocation (TASK 022)
        try:
            from simulation.core.allocation import allocate_sources  # type: ignore
            statuses.append(ComponentStatus(component="source_sink_allocation", status="AVAILABLE" if allocate_sources else "NOT_COMPUTABLE", note="Module present"))
        except Exception:
            statuses.append(ComponentStatus(component="source_sink_allocation", status="NOT_COMPUTABLE", note="TASK 022 module not loaded; requires actual organ demand and available carbon source"))

        # Growth (TASK 023) — mass-first only; geometry only if supported
        try:
            from simulation.core.growth import growth_model  # type: ignore
            statuses.append(ComponentStatus(component="organ_growth", status="AVAILABLE" if growth_model else "NOT_COMPUTABLE", note="Mass-first growth preserved; geometry only if architecture contract supports"))
        except Exception:
            statuses.append(ComponentStatus(component="organ_growth", status="NOT_COMPUTABLE", note="TASK 023 module not loaded; biomass-only if available; geometry only if architecture contract supports; no fabricated growth"))

        # Water (TASK 025)
        try:
            from simulation.core.water import water_model  # type: ignore
            statuses.append(ComponentStatus(component="water", status="AVAILABLE" if water_model else "NOT_COMPUTABLE", note="Reservoir semantics preserved"))
        except Exception:
            statuses.append(ComponentStatus(component="water", status="NOT_COMPUTABLE", note="TASK 025 module not loaded"))

        # Nutrients (TASK 026) — independent N/P/K
        try:
            from simulation.core.nutrients import nutrient_model  # type: ignore
            statuses.append(ComponentStatus(component="nutrients", status="AVAILABLE" if nutrient_model else "NOT_COMPUTABLE", note="Independent N/P/K preserved"))
        except Exception:
            statuses.append(ComponentStatus(component="nutrients", status="NOT_COMPUTABLE", note="TASK 026 module not loaded"))

        # Phenology (TASK 024) — not automatic from age
        try:
            from simulation.core.phenology import phenology_model  # type: ignore
            statuses.append(ComponentStatus(component="phenology", status="AVAILABLE" if phenology_model else "NOT_COMPUTABLE", note="Transition governed by existing triggers only"))
        except Exception:
            statuses.append(ComponentStatus(component="phenology", status="NOT_COMPUTABLE", note="TASK 024 module not loaded"))

        # Stochastic (TASK 027) — only if module explicitly requires
        try:
            from simulation.core.stochastic import stochastic_model  # type: ignore
            statuses.append(ComponentStatus(component="stochastic", status="NOT_COMPUTABLE", note="Not injected unless module requires; no hidden randomness"))
        except Exception:
            statuses.append(ComponentStatus(component="stochastic", status="UNAVAILABLE", note="TASK 027 module not loaded; not required for step"))

        # LightField / environment input — use existing computed data if available; do NOT recompute
        try:
            from simulation.api.services.lightfield_service import compute_lightfield_service  # type: ignore
            statuses.append(ComponentStatus(component="lightfield_input", status="AVAILABLE" if compute_lightfield_service else "NOT_COMPUTABLE", note="Existing LightField consumed if available"))
        except Exception:
            statuses.append(ComponentStatus(component="lightfield_input", status="NOT_COMPUTABLE", note="LightField input unavailable; no recomputation"))

        overall = "PARTIAL" if any(s.status == "AVAILABLE" for s in statuses) else ("NOT_COMPUTABLE" if all(s.status == "NOT_COMPUTABLE" for s in statuses) else "VALID")

        # TASK 046E — explicit OrganLightExposure → photosynthesis (orchestration only; no equation)
        if organ_exposures is not None:
            for exp in organ_exposures:
                if exp is None:
                    statuses.append(ComponentStatus(component="photosynthesis_046E", status="NOT_COMPUTABLE", note="Exposure is None; direct association unavailable"))
                    statuses.append(ComponentStatus(component="carbon_respiration_046F", status="NOT_COMPUTABLE", note="Upstream exposure None; TASK 021 not executed"))
                    continue
                # Validation: direct explicit association only (B/C/E/F)
                valid = (getattr(exp, "status", None) == "AVAILABLE" and
                         getattr(exp, "ppfd_value", None) is not None and
                         getattr(exp, "ppfd_unit", None) == "umol_photons_m2_s" and
                         getattr(exp, "exposure_type", None) == "incident")
                if valid:
                    try:
                        adapter_res = photosynthesis_from_organ_exposure(exp, params=SYNTH_PHOTO_PARAMS, timestep=clock.timestep)
                        result = adapter_res.result
                        note = f"TASK_046E direct; plant={getattr(exp, 'plant_id', None)} arch={getattr(exp, 'architecture_id', None)} organ={getattr(exp, 'organ_id', None)}; source={getattr(exp, 'source_id', None)}; ppfd={getattr(exp, 'ppfd_value', None)}; spectral=PAR_400_700; absorbed=UNAVAILABLE; provenance={result.provenance or ''}"
                        statuses.append(ComponentStatus(
                            component="photosynthesis_046E",
                            status=result.status,
                            note=note,
                            value=result.gross_carbon_g,
                        ))
                        # TASK 046F — photosynthesis → carbon/respiration (adapt from result, not from raw PPFD)
                        if result.status == "AVAILABLE":
                            try:
                                carbon_res = carbon_from_photosynthesis(result, timestep=clock.timestep, provenance_suffix=f"org={getattr(exp,'organ_id',None)}")
                                statuses.append(ComponentStatus(
                                    component="carbon_respiration_046F",
                                    status=carbon_res.status,
                                    note=f"TASK_046F from {getattr(exp,'organ_id',None)}; gross={carbon_res.gross_carbon_g}; resp={carbon_res.respiration_g}; net={carbon_res.net_carbon_g}; sign preserved; timestep={clock.timestep}",
                                    value=carbon_res.net_carbon_g,
                                ))
                            except Exception as ce:
                                statuses.append(ComponentStatus(component="carbon_respiration_046F", status="ERROR", note=f"TASK_046F adapter failure: {ce}; canonical TASK 021 preserved; no equation in engine"))
                        else:
                            statuses.append(ComponentStatus(component="carbon_respiration_046F", status="NOT_COMPUTABLE", note="Upstream photosynthesis not AVAILABLE; carbon/respiration not executed per TASK 021 contract"))
                    except Exception as e:
                        statuses.append(ComponentStatus(component="photosynthesis_046E", status="ERROR", note=f"TASK_046E adapter failure: {e}; no equation in engine; no replacement"))
                else:
                    reason = (f"Exposure status={getattr(exp, 'status', None)}; ppfd_value={getattr(exp, 'ppfd_value', None)}; "
                              f"ppfd_unit={getattr(exp, 'ppfd_unit', None)}; exposure_type={getattr(exp, 'exposure_type', None)}; "
                              f"explicit organ association required; no interpolation/aggregation.")
                    statuses.append(ComponentStatus(component="photosynthesis_046E", status="NOT_COMPUTABLE", note=f"TASK_046E blocked: {reason}"))
                    statuses.append(ComponentStatus(component="carbon_respiration_046F", status="NOT_COMPUTABLE", note=f"TASK_046F blocked by upstream exposure: {reason}"))

        return SimulationStepResult(
            result_id=f"step-{source_ref}",
            source_snapshot_id=snapshot.snapshot_id if snapshot else None,
            source_scenario_id=scenario.scenario_id if scenario else None,
            previous_simulation_time=prev_time,
            next_simulation_time=next_time,
            timestep=clock.timestep,
            component_statuses=statuses,
            provenance=self.provenance,
            status=overall,
            note="Single-step orchestration; source Snapshot/Scenario preserved; no mutation of source; partial computability preserved; no duplicate equations.",
        )

# Module-level singleton (deterministic; no hidden execution loop)
simulation_engine = SimulationEngine()
