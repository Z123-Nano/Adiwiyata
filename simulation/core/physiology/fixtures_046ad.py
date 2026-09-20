"""TASK 046AD — Synthetic fixtures for architecture→PPFD integration."""
from simulation.core.contracts.domain import PlantArchitecture
from simulation.core.solar.model import SolarPosition
from simulation.core.physiology.absolute_ppfd_reference import AbsolutePPFDReference
from simulation.core.physiology.spatial_ppfd_transfer_factor import SpatialPPFDTransferFactor
from simulation.core.physiology.ppfd_source import PPFDSource

ARCH_T = PlantArchitecture(architecture_id="arch_046AD_t", plant_id="p1",
    provenance="TASK_046AD t synthetic", is_synthetic_example=True)
ARCH_T1 = PlantArchitecture(architecture_id="arch_046AD_t1", plant_id="p1",
    provenance="TASK_046AD t+1 synthetic", is_synthetic_example=True)
SOLAR_T = SolarPosition(date_iso="2026-09-19", latitude_deg=52.5, longitude_deg=13.4,
    timestamp="2026-09-19T12:00:00Z", azimuth_deg=180.0, altitude_deg=45.0,
    zenith_deg=45.0, above_horizon=True, provenance="TASK_046AD synthetic",
    is_synthetic_example=True)

REF_T = AbsolutePPFDReference(
    ref_id="ref_046AD_t", ppfd_value=800.0, reference_geometry="GARDEN_REFERENCE_PLANE",
    spectral_domain="PAR_400_700", provenance="TASK_046AD synthetic",
    source_type="SYNTHETIC", is_synthetic_example=True, status="AVAILABLE")

REF_T1 = AbsolutePPFDReference(
    ref_id="ref_046AD_t1", ppfd_value=800.0, reference_geometry="GARDEN_REFERENCE_PLANE",
    spectral_domain="PAR_400_700", provenance="TASK_046AD synthetic t+1",
    source_type="SYNTHETIC", is_synthetic_example=True, status="AVAILABLE")

XFER_T = SpatialPPFDTransferFactor(
    transfer_id="xfer_046AD_t", reference_id="ref_046AD_t",
    lightfield_id="lf_046AD_t", target_organ_id="leaf_1",
    transfer_value=0.5, component="total",
    transfer_definition="Explicit anchoring: reference PPFD_ref defined; LightField relative_normalized requires aligned normalization; orientation limitations preserved.",
    provenance="TASK_046AD synthetic", is_synthetic_example=True, status="AVAILABLE")

XFER_T1 = SpatialPPFDTransferFactor(
    transfer_id="xfer_046AD_t1", reference_id="ref_046AD_t1",
    lightfield_id="lf_046AD_t1", target_organ_id="leaf_1",
    transfer_value=0.45,
    transfer_definition="Explicit anchoring: reference PPFD_ref defined; changed architecture yields different T.",
    provenance="TASK_046AD synthetic t+1", is_synthetic_example=True, status="AVAILABLE")
