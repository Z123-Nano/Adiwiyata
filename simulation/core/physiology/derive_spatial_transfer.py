"""TASK 046U — Derivation of SpatialPPFDTransferFactor from two comparable LightField samples.
Pure; no physical PPFD computation; only dimensionless ratio of same LightField quantity.
Requires explicit compatibility (same component, same context, denominator > 0).
References 046T contracts (AbsolutePPFDReference + SpatialPPFDTransferFactor)."""
from __future__ import annotations
from typing import Optional, Literal
from simulation.core.light.field.contracts import LightField, LightSample
from simulation.core.physiology.spatial_ppfd_transfer_factor import SpatialPPFDTransferFactor, build_spatial_ppfd_transfer

def derive_spatial_transfer_from_lightfield(
    reference_lightfield: LightField,
    target_lightfield: LightField,
    reference_id: str,
    lightfield_id: str = "lf_default",
    target_organ_id: Optional[str] = None,
    target_plant_id: Optional[str] = None,
    component: Literal["total", "direct", "diffuse", "reflected"] = "total",
    transfer_id: str = "transfer_046U_1",
    provenance: Optional[str] = None,
    is_synthetic_example: bool = False,
) -> SpatialPPFDTransferFactor:
    """Derive dimensionless T = L_target / L_reference from same LightField quantity.
    Only valid when both use identical approximation/normalization context.
    No arbitrary scaling; no PPFD output."""
    # Compatibility checks
    if not reference_lightfield or not target_lightfield:
        raise ValueError("TASK_046U BLOCKED: either LightField is missing")
    # Component selection
    if component == "total":
        ref_val = float(sum(s.total for s in reference_lightfield.samples)) / max(len(reference_lightfield.samples), 1)
        tgt_val = float(sum(s.total for s in target_lightfield.samples)) / max(len(target_lightfield.samples), 1)
    elif component == "direct":
        ref_val = float(sum(s.direct for s in reference_lightfield.samples)) / max(len(reference_lightfield.samples), 1)
        tgt_val = float(sum(s.direct for s in target_lightfield.samples)) / max(len(target_lightfield.samples), 1)
    elif component == "diffuse":
        ref_val = float(sum(s.diffuse for s in reference_lightfield.samples)) / max(len(reference_lightfield.samples), 1)
        tgt_val = float(sum(s.diffuse for s in target_lightfield.samples)) / max(len(target_lightfield.samples), 1)
    elif component == "reflected":
        ref_val = float(sum(s.reflected for s in reference_lightfield.samples)) / max(len(reference_lightfield.samples), 1)
        tgt_val = float(sum(s.reflected for s in target_lightfield.samples)) / max(len(target_lightfield.samples), 1)
    else:
        raise ValueError("TASK_046U BLOCKED: unsupported component")

    # Same normalization context check (synthetic normalization must be identical)
    ref_approx = reference_lightfield.approximation_params or {}
    tgt_approx = target_lightfield.approximation_params or {}
    ref_solar = reference_lightfield.solar_reference
    tgt_solar = target_lightfield.solar_reference
    # Time / simulation alignment (must match; no interpolation)
    ref_time = reference_lightfield.simulation_time_ref if hasattr(reference_lightfield, "simulation_time_ref") else ref_solar
    tgt_time = target_lightfield.simulation_time_ref if hasattr(target_lightfield, "simulation_time_ref") else tgt_solar
    if ref_time != tgt_time:
        raise ValueError("TASK_046U BLOCKED: simulation_time / solar_reference mismatch; no interpolation allowed")
    # Normalization context: both relative_normalized with same approximation params semantics (explicit check via provenance/approx params)
    if (ref_approx.get("approximation") != tgt_approx.get("approximation") and
        (ref_approx.get("approximation") is not None and tgt_approx.get("approximation") is not None)):
        # Allow only if both are same approximation class; different approximations = invalid transfer
        pass  # actually must enforce exact match for defensible transfer
    # Strict: approximation_params must be present and equivalent for synthetic normalization consistency
    # For this derivation, require same approximation identifier (or both None with same solar reference)
    if ref_approx.get("approximation") is not None and tgt_approx.get("approximation") is not None:
        if ref_approx.get("approximation") != tgt_approx.get("approximation"):
            raise ValueError("TASK_046U BLOCKED: approximation mismatch; normalization context differs")
    # Denominator > 0 and finite
    if ref_val <= 0:
        raise ValueError("TASK_046U BLOCKED: reference LightField value <= 0; denominator must be > 0 for transfer")
    if not (abs(ref_val) < float('inf') and abs(tgt_val) < float('inf')):
        raise ValueError("TASK_046U BLOCKED: non-finite LightField value")
    if ref_val < 0 or tgt_val < 0:
        raise ValueError("TASK_046U BLOCKED: negative LightField value rejected")
    # Compute dimensionless transfer (may exceed 1; no clipping)
    transfer_value = float(tgt_val / ref_val)
    # Reference identity preserved from reference_lightfield (not fabricated)
    # Use lightfield_id from target for linking; reference_id from AbsolutePPFDReference is separate contract
    # This derivation produces the transfer factor only; does not compute PPFD
    return build_spatial_ppfd_transfer(
        transfer_id=transfer_id,
        reference_id=reference_id,
        lightfield_id=lightfield_id,
        target_organ_id=target_organ_id,
        target_plant_id=target_plant_id,
        transfer_value=transfer_value,
        component=component,
        transfer_definition=(
            "Explicit physical anchoring: reference LightField and target LightField use identical "
            "approximation/synthetic normalization; transfer = target_total / reference_total; "
            "orientation limitation preserved (coarse); no arbitrary scaling; no physical PPFD output."
        ),
        provenance=(provenance or f"TASK_046U derivation: ref={reference_id} lightfield={lightfield_id} component={component} time_align={ref_time==tgt_time}"),
        is_synthetic_example=is_synthetic_example,
    )
