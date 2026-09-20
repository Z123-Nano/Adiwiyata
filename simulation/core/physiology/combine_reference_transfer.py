"""TASK 046V — Combine AbsolutePPFDReference + validated SpatialPPFDTransferFactor → absolute incident PPFD (PPFDSource-compatible).
Pure adapter; no absorbed PAR; no photosynthesis; no geometry invention; no interpolation; synthetic fixtures labeled.
Uses existing contracts (046T, 046O boundary preserved)."""
from __future__ import annotations
from typing import Optional, Literal
from simulation.core.physiology.absolute_ppfd_reference import AbsolutePPFDReference
from simulation.core.physiology.spatial_ppfd_transfer_factor import SpatialPPFDTransferFactor
from simulation.core.physiology.ppfd_source import PPFDSource

def combine_reference_transfer_to_ppfd_source(
    reference: AbsolutePPFDReference,
    transfer: SpatialPPFDTransferFactor,
    target_organ_id: Optional[str] = None,
    target_location: Optional[dict] = None,
    reference_geometry_compatible: bool = True,
    reference_geometry_compatibility_note: Optional[str] = None,
    provenance_suffix: Optional[str] = None,
    is_synthetic_example: bool = False,
) -> PPFDSource:
    """Physical combination: PPFD_target = ppfd_ref × T.
    Returns PPFDSource (incident only) with explicit provenance; NOT_COMPUTABLE if invalid.
    No arbitrary conversion; unit preserved umol_photons_m2_s."""
    # 1. Reference identity must match transfer's reference_id
    if not reference.ref_id or not transfer.reference_id or reference.ref_id != transfer.reference_id:
        return PPFDSource(
            source_id="derived_error_046V", quantity_kind="PPFD", value=0.0, unit="umol_photons_m2_s", spectral_band="PAR_400_700", source_type="DERIVED_PHYSICALLY_VALID" if not is_synthetic_example else "SYNTHETIC",
            status="NOT_COMPUTABLE",
            provenance=(provenance_suffix or "TASK_046V") + ": reference_id mismatch (ref="+str(reference.ref_id)+" transfer_ref="+str(transfer.reference_id)+")",
            note="Reference identity mismatch; transfer denominator does not refer to this AbsolutePPFDReference.",
            source_variable="ppfd",
            is_synthetic_example=is_synthetic_example,
        )
    # 2. Unit preservation
    if reference.unit != "umol_photons_m2_s":
        return PPFDSource(
            source_id="derived_error_046V", quantity_kind="PPFD", value=0.0, unit="umol_photons_m2_s", spectral_band="PAR_400_700", source_type="SYNTHETIC", status="NOT_COMPUTABLE",
            provenance=(provenance_suffix or "TASK_046V") + ": reference unit not umol_photons_m2_s",
            note="Unit must be umol_photons_m2_s (PAR 400-700).",
            
        )
    # 3. Spectral domain (reference defines PAR; transfer must conceptually align; contract-level check)
    if reference.spectral_domain != "PAR_400_700" and reference.spectral_domain != "EPAR_400_750":
        return PPFDSource(
            source_id="derived_error_046V", quantity_kind="PPFD", value=0.0, unit="umol_photons_m2_s", spectral_band="PAR_400_700", source_type="SYNTHETIC", status="NOT_COMPUTABLE",
            provenance=(provenance_suffix or "TASK_046V") + ": spectral domain unsupported",
            note="Spectral domain must be PAR 400-700.",
            
        )
    # 4. Time alignment (exact; no interpolation)
    ref_time = reference.simulation_time_ref
    xfer_time = transfer.simulation_time_ref
    if ref_time != xfer_time:
        return PPFDSource(
            source_id="derived_error_046V", quantity_kind="PPFD", value=0.0, unit="umol_photons_m2_s", spectral_band="PAR_400_700", source_type="SYNTHETIC", status="NOT_COMPUTABLE",
            provenance=(provenance_suffix or "TASK_046V") + f": time mismatch (ref={ref_time} transfer={xfer_time})",
            note="Simulation time must match exactly; no interpolation.",
            
        )
    # 5. Reference geometry compatibility (explicit; no silent swap)
    if not reference_geometry_compatible:
        return PPFDSource(
            source_id="derived_error_046V", quantity_kind="PPFD", value=0.0, unit="umol_photons_m2_s", spectral_band="PAR_400_700", source_type="SYNTHETIC", status="NOT_COMPUTABLE",
            provenance=(provenance_suffix or "TASK_046V") + ": geometry incompatible (ref="+str(reference.reference_geometry)+")",
            note=(reference_geometry_compatibility_note or "Reference geometry not compatible with target; no silent mapping.") + " Orientation / local-reflection limitations preserved.",
            
        )
    # 6. Reference value: finite, non-negative (zero allowed; negative/inf/nan reject)
    ppfd_ref = float(reference.ppfd_value)
    if ppfd_ref < 0:
        return PPFDSource(
            source_id="derived_error_046V", quantity_kind="PPFD", value=0.0, unit="umol_photons_m2_s", spectral_band="PAR_400_700", source_type="SYNTHETIC", status="ERROR",
            provenance=(provenance_suffix or "TASK_046V") + ": negative reference PPFD",
            note="Absolute reference PPFD must be non-negative.",
            
        )
    if not (abs(ppfd_ref) < float('inf')):
        return PPFDSource(
            source_id="derived_error_046V", quantity_kind="PPFD", value=0.0, unit="umol_photons_m2_s", spectral_band="PAR_400_700", source_type="SYNTHETIC", status="ERROR",
            provenance=(provenance_suffix or "TASK_046V") + ": non-finite reference",
            note="Reference PPFD must be finite.",
            
        )
    # 7. Transfer validation
    t_val = float(transfer.transfer_value)
    if t_val < 0:
        return PPFDSource(
            source_id="derived_error_046V", quantity_kind="PPFD", value=0.0, unit="umol_photons_m2_s", spectral_band="PAR_400_700", source_type="SYNTHETIC", status="ERROR",
            provenance=(provenance_suffix or "TASK_046V") + ": negative transfer",
            note="Spatial transfer factor must be non-negative.",
            
        )
    if not (abs(t_val) < float('inf')):
        return PPFDSource(
            source_id="derived_error_046V", quantity_kind="PPFD", value=0.0, unit="umol_photons_m2_s", spectral_band="PAR_400_700", source_type="SYNTHETIC", status="ERROR",
            provenance=(provenance_suffix or "TASK_046V") + ": non-finite transfer",
            note="Transfer factor must be finite.",
            
        )
    # 8. Component alignment (baseline total; per-component deferred)
    if transfer.component != "total":
        # Allow with explicit note that component-specific output deferred
        note_comp = (f"Component={transfer.component}; baseline output uses total reference × total transfer; "
                     f"per-component derivation deferred (not supported by current contracts).")
    else:
        note_comp = "Total incident PPFD; direct/diffuse/reflected components deferred."
    # 9. Compute (zero ref produces zero target; no epsilon fabrication)
    result_ppfd = float(ppfd_ref * t_val)
    # 10. Uncertainty preservation (metadata, not propagated)
    unc_note = None
    if reference.uncertainty is not None and transfer.provenance is not None:
        unc_note = f"Reference uncertainty={reference.uncertainty}; transfer provenance={transfer.provenance}; propagation deferred."
    # 11. Build PPFDSource (incident only — no absorbed claim)
    source = PPFDSource(
        source_id=("derived_" + reference.ref_id + "_" + transfer.transfer_id + ("_" + str(target_organ_id) if target_organ_id else "")),
        quantity_kind="PPFD",
        value=result_ppfd if (abs(result_ppfd) < float('inf')) else 0.0,
        unit="umol_photons_m2_s",
        spectral_band=reference.spectral_domain if reference.spectral_domain in ("PAR_400_700","EPAR_400_750") else "PAR_400_700",
        source_type="SYNTHETIC" if is_synthetic_example else "DERIVED_PHYSICALLY_VALID",
        timestamp=reference.timestamp,
        spatial_ref=target_location if target_location else (reference.reference_position if reference.reference_position else {"x":None,"y":None,"z":None,"frame":"garden_local","note":"+X East / +Y North / +Z Up"}),
        derivation_source_ids=[reference.ref_id, transfer.transfer_id],
        derivation_method="AbsolutePPFDReference × SpatialPPFDTransferFactor (TASK_046V); incident only; no absorption model.",
        provenance=(
            f"TASK_046V: ref_id={reference.ref_id} ppfd_ref={ppfd_ref} × transfer_id={transfer.transfer_id} T={t_val} "
            f"time_align={ref_time==xfer_time} component={transfer.component} synthetic={is_synthetic_example}" +
            (f" | {unc_note}" if unc_note else "") +
            (f" | provenance_suffix={provenance_suffix}" if provenance_suffix else "")
        ),
        note=(
            f"Incident organ PPFD derived from AbsolutePPFDReference × SpatialPPFDTransferFactor. "
            f"{note_comp} "
            f"Reference geometry={reference.reference_geometry}; orientation/optics limitations preserved (coarse). "
            f"No absorbed PAR / APAR / optical model applied. No lux / W/m² / µmol/J conversion."
        ),
        is_synthetic_example=is_synthetic_example,
        status="AVAILABLE" if (abs(result_ppfd) < float('inf')) else "ERROR",
    )
    return source
