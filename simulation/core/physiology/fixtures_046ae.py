"""TASK 046AE — Synthetic fixtures for two-timestep closed-loop FSPM."""
from simulation.core.contracts.domain import PlantArchitecture, PlantOrgan
from simulation.core.solar.model import SolarPosition
from simulation.core.physiology.absolute_ppfd_reference import AbsolutePPFDReference
from simulation.core.physiology.spatial_ppfd_transfer_factor import SpatialPPFDTransferFactor
from simulation.core.physiology.ppfd_source import PPFDSource
from simulation.core.architecture.growth_delta import ArchitectureGrowthDelta

# Architecture with one organ so delta applies
ORGAN_T = PlantOrgan(id="leaf_1", organ_type="leaf", length_m=0.15, biomass_g_DM=2.0,
    provenance="TASK_046AE synthetic", is_synthetic_example=True)
ARCH_T = PlantArchitecture(
    architecture_id="arch_046AE_t", plant_id="p1", organs=[ORGAN_T],
    provenance="TASK_046AE t synthetic", is_synthetic_example=True)

# Growth delta (positive, valid)
DELTA_T = ArchitectureGrowthDelta(
    result_id="delta_046AE_t", plant_id="p1", architecture_id="arch_046AE_t",
    organ_id="leaf_1", organ_type="leaf",
    previous_length_m=0.15, delta_length_m=0.05, proposed_length_m=0.20,
    previous_biomass_g_DM=2.0, biomass_increment_g_DM=0.5, new_biomass_g_DM=2.5,
    geometry_dimension="length_m", status="AVAILABLE",
    parameter_set_ref="param_046AE_v1", provenance="TASK_046AE synthetic delta", is_synthetic_example=True,
    timestep=3600.0, simulation_time_ref="t_046AE")

# Apply delta -> ARCH_t1 (new object, original unchanged)
from simulation.core.architecture.apply_growth_delta import apply_architecture_growth_delta
ARCH_T1 = apply_architecture_growth_delta(ARCH_T, DELTA_T)

SOLAR_T = SolarPosition(date_iso="2026-09-19", latitude_deg=52.5, longitude_deg=13.4,
    timestamp="2026-09-19T12:00:00Z", azimuth_deg=180.0, altitude_deg=45.0,
    zenith_deg=45.0, above_horizon=True, provenance="TASK_046AE synthetic",
    is_synthetic_example=True)

# Reference + transfer t
REF_T = AbsolutePPFDReference(
    ref_id="ref_046AE_t", ppfd_value=800.0, reference_geometry="GARDEN_REFERENCE_PLANE",
    spectral_domain="PAR_400_700", provenance="TASK_046AE synthetic",
    source_type="SYNTHETIC", is_synthetic_example=True, status="AVAILABLE")
XFER_T = SpatialPPFDTransferFactor(
    transfer_id="xfer_046AE_t", reference_id="ref_046AE_t",
    lightfield_id="lf_046AE_t", target_organ_id="leaf_1",
    transfer_value=0.5, component="total",
    transfer_definition="Explicit anchoring: reference PPFD_ref defined; LightField relative_normalized requires aligned normalization.",
    provenance="TASK_046AE synthetic", is_synthetic_example=True, status="AVAILABLE")

# Reference + transfer t+1 (same absolute ref; changed T due to architecture change)
REF_T1 = AbsolutePPFDReference(
    ref_id="ref_046AE_t1", ppfd_value=800.0, reference_geometry="GARDEN_REFERENCE_PLANE",
    spectral_domain="PAR_400_700", provenance="TASK_046AE synthetic t+1",
    source_type="SYNTHETIC", is_synthetic_example=True, status="AVAILABLE")
XFER_T1 = SpatialPPFDTransferFactor(
    transfer_id="xfer_046AE_t1", reference_id="ref_046AE_t1",
    lightfield_id="lf_046AE_t1", target_organ_id="leaf_1",
    transfer_value=0.45, component="total",
    transfer_definition="Changed architecture yields different transfer; explicit anchoring preserved.",
    provenance="TASK_046AE synthetic t+1", is_synthetic_example=True, status="AVAILABLE")

# Explicit sink demands (synthetic, independent of carbon supply)
from simulation.core.physiology.organ_sink_demand import OrganSinkDemand
SINK_T = OrganSinkDemand(
    demand_id="sink_046AE_t", organ_id="leaf_1", organ_type="leaf", plant_id="p1",
    demand_carbon_g=3.0, potential_demand_g=3.0, demand_type="growth", status="AVAILABLE",
    sink_parameter_set_ref="param_046AE_sink", sink_coefficient_ref=1.0,
    timestep=3600.0, provenance="TASK_046AE synthetic", is_synthetic_example=True)
