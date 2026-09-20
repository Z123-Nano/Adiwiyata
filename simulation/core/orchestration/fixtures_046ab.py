"""TASK 046AB — Synthetic fixtures: explicit PPFD → orchestrator integration."""
from simulation.core.physiology.ppfd_source import PPFDSource
from simulation.core.contracts.domain import PlantArchitecture
from simulation.core.solar.model import SolarPosition

# Plant / architecture
ARCH_AB = PlantArchitecture(
    architecture_id="arch_046AB_1", plant_id="p1",
    provenance="TASK_046AB synthetic", is_synthetic_example=True,
)
SOLAR_AB = SolarPosition(
    date_iso="2026-09-18", latitude_deg=52.5, longitude_deg=13.4,
    timestamp="2026-09-18T12:00:00Z", azimuth_deg=180.0, altitude_deg=45.0,
    zenith_deg=45.0, above_horizon=True, provenance="TASK_046AB synthetic",
    is_synthetic_example=True,
)

# Case A — two organs with different PPFD (explicit sources)
SOURCE_A_LEAF1 = PPFDSource(
    source_id="ppfd_046AB_leaf1",
    quantity_kind="PPFD", value=400.0, unit="umol_photons_m2_s",
    spectral_band="PAR_400_700", source_type="MODELED", timestamp="2026-09-18T12:00:00Z",
    provenance="TASK_046AB A synthetic modeled", is_synthetic_example=True,
    status="AVAILABLE",
)
SOURCE_A_LEAF2 = PPFDSource(
    source_id="ppfd_046AB_leaf2",
    quantity_kind="PPFD", value=200.0, unit="umol_photons_m2_s",
    spectral_band="PAR_400_700", source_type="MODELED", timestamp="2026-09-18T12:00:00Z",
    provenance="TASK_046AB A synthetic modeled", is_synthetic_example=True,
    status="AVAILABLE",
)

# Case B — same sources, just different values (already in A; reused)
# Case C — zero PPFD explicitly
SOURCE_C_ZERO = PPFDSource(
    source_id="ppfd_046AB_zero",
    quantity_kind="PPFD", value=0.0, unit="umol_photons_m2_s",
    spectral_band="PAR_400_700", source_type="MEASURED", timestamp="2026-09-18T12:00:00Z",
    provenance="TASK_046AB C zero explicit", is_synthetic_example=True,
    status="AVAILABLE",
)

# Case D — missing source for required organ (absence = not in list)
# (tested by calling with only leaf1, omitting leaf2 — not here; used in test)
