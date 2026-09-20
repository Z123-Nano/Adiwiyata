from datetime import datetime, timezone
"""TASK 046AF — Three-step synthetic sequence (clock-coupled, environment-explicit)."""
from simulation.core.contracts.domain import PlantArchitecture, PlantOrgan
from simulation.core.solar.model import SolarPosition
from simulation.core.physiology.absolute_ppfd_reference import AbsolutePPFDReference
from simulation.core.physiology.spatial_ppfd_transfer_factor import SpatialPPFDTransferFactor
from simulation.core.clock.clock import SimulationClock, get_simulation_clock, reset_clock
from simulation.core.architecture.growth_delta import ArchitectureGrowthDelta
from simulation.core.architecture.apply_growth_delta import apply_architecture_growth_delta

# Initial architecture with organ
ORGAN_0 = PlantOrgan(id="leaf_1", organ_type="leaf", length_m=0.15, biomass_g_DM=2.0,
    provenance="TASK_046AF synthetic", is_synthetic_example=True)
ARCH_0 = PlantArchitecture(
    architecture_id="arch_046AF_0", plant_id="p1", organs=[ORGAN_0],
    provenance="TASK_046AF t0 synthetic", is_synthetic_example=True)

SOLAR_0 = SolarPosition(date_iso="2026-09-19", latitude_deg=52.5, longitude_deg=13.4,
    timestamp="2026-09-19T12:00:00Z", azimuth_deg=180.0, altitude_deg=45.0,
    zenith_deg=45.0, above_horizon=True, provenance="TASK_046AF synthetic",
    is_synthetic_example=True)

# Explicit references — changing environment per timestep (800 → 650 → 500)
REF_0 = AbsolutePPFDReference(ref_id="ref_046AF_0", ppfd_value=800.0, reference_geometry="GARDEN_REFERENCE_PLANE",
    spectral_domain="PAR_400_700", provenance="TASK_046AF env_t0", source_type="SYNTHETIC", is_synthetic_example=True, status="AVAILABLE")
REF_1 = AbsolutePPFDReference(ref_id="ref_046AF_1", ppfd_value=650.0, reference_geometry="GARDEN_REFERENCE_PLANE",
    spectral_domain="PAR_400_700", provenance="TASK_046AF env_t1", source_type="SYNTHETIC", is_synthetic_example=True, status="AVAILABLE")
REF_2 = AbsolutePPFDReference(ref_id="ref_046AF_2", ppfd_value=500.0, reference_geometry="GARDEN_REFERENCE_PLANE",
    spectral_domain="PAR_400_700", provenance="TASK_046AF env_t2", source_type="SYNTHETIC", is_synthetic_example=True, status="AVAILABLE")

# Deltas to evolve architecture across steps (positive, valid)
DELTA_0 = ArchitectureGrowthDelta(result_id="delta_046AF_0", plant_id="p1", architecture_id="arch_046AF_0",
    organ_id="leaf_1", organ_type="leaf", previous_length_m=0.15, delta_length_m=0.05, proposed_length_m=0.20,
    previous_biomass_g_DM=2.0, biomass_increment_g_DM=0.5, new_biomass_g_DM=2.5,
    geometry_dimension="length_m", status="AVAILABLE", parameter_set_ref="param_046AF_v1",
    provenance="TASK_046AF delta_t0", is_synthetic_example=True, timestep=3600.0, simulation_time_ref="t0_046AF")
DELTA_1 = ArchitectureGrowthDelta(result_id="delta_046AF_1", plant_id="p1", architecture_id="arch_046AF_0",
    organ_id="leaf_1", organ_type="leaf", previous_length_m=0.20, delta_length_m=0.05, proposed_length_m=0.25,
    previous_biomass_g_DM=2.5, biomass_increment_g_DM=0.5, new_biomass_g_DM=3.0,
    geometry_dimension="length_m", status="AVAILABLE", parameter_set_ref="param_046AF_v1",
    provenance="TASK_046AF delta_t1", is_synthetic_example=True, timestep=3600.0, simulation_time_ref="t1_046AF")

ARCH_1 = apply_architecture_growth_delta(ARCH_0, DELTA_0)
ARCH_2 = apply_architecture_growth_delta(ARCH_1, DELTA_1)

# Transfers — architecture-derived; different per step (structure + env context)
XFER_0 = SpatialPPFDTransferFactor(transfer_id="xfer_046AF_0", reference_id="ref_046AF_0",
    lightfield_id="lf_046AF_0", target_organ_id="leaf_1", transfer_value=0.50, component="total",
    transfer_definition="Explicit anchoring; ref 800; T=0.50.", provenance="TASK_046AF t0", is_synthetic_example=True, status="AVAILABLE")
XFER_1 = SpatialPPFDTransferFactor(transfer_id="xfer_046AF_1", reference_id="ref_046AF_1",
    lightfield_id="lf_046AF_1", target_organ_id="leaf_1", transfer_value=0.46, component="total",
    transfer_definition="Explicit anchoring; ref 650; changed architecture; T=0.46.", provenance="TASK_046AF t1", is_synthetic_example=True, status="AVAILABLE")
XFER_2 = SpatialPPFDTransferFactor(transfer_id="xfer_046AF_2", reference_id="ref_046AF_2",
    lightfield_id="lf_046AF_2", target_organ_id="leaf_1", transfer_value=0.42, component="total",
    transfer_definition="Explicit anchoring; ref 500; changed architecture; T=0.42.", provenance="TASK_046AF t2", is_synthetic_example=True, status="AVAILABLE")

# Clock instances (explicit per step, not wall-clock)
CLOCK_0 = SimulationClock(simulation_time=datetime(2026,9,19,12,0,0,tzinfo=timezone.utc), timestep=3600.0, provenance="TASK_046AF clock_t0")
CLOCK_1 = SimulationClock(simulation_time=datetime(2026,9,19,13,0,0,tzinfo=timezone.utc), timestep=3600.0, provenance="TASK_046AF clock_t1")
CLOCK_2 = SimulationClock(simulation_time=datetime(2026,9,19,14,0,0,tzinfo=timezone.utc), timestep=3600.0, provenance="TASK_046AF clock_t2")
