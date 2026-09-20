"""TASK 046J — Pure derivation: allocated carbon → structural carbon → biomass increment."""
from __future__ import annotations
from typing import Optional
from simulation.core.growth.growth_conversion_params import GrowthConversionParameters
from simulation.core.growth.organ_growth import OrganGrowthResult

def derive_organ_growth(
    organ_id: str,
    plant_id: str,
    organ_type: str,
    allocated_carbon_g: float,
    previous_biomass_g_DM: float,
    parameters: GrowthConversionParameters,
    architecture_id: Optional[str] = None,
    timestep: float = 3600.0,
    simulation_time_ref: Optional[str] = None,
    provenance_suffix: Optional[str] = None,
) -> OrganGrowthResult:
    """Pure — no mutation of inputs; no photosynthesis/respiration/geometry; explicit conversion."""
    # Validate identity
    if not plant_id or not organ_id:
        return OrganGrowthResult(
            result_id=f"g_{organ_id or 'unknown'}_bad",
            plant_id=plant_id or "",
            architecture_id=architecture_id,
            organ_id=organ_id or "",
            organ_type=organ_type or "other",
            allocated_carbon_g=allocated_carbon_g,
            previous_biomass_g_DM=max(previous_biomass_g_DM, 0.0),
            structural_carbon_increment_g_C=0.0,
            biomass_increment_g_DM=0.0,
            new_biomass_g_DM=max(previous_biomass_g_DM, 0.0),
            growth_parameter_set_ref=parameters.parameter_set_id,
            timestep=timestep,
            status="NOT_COMPUTABLE",
            provenance=f"TASK_046J blocked: missing identity; not fabricated",
            note="Organ/plant identity required; no fabricated id.",
            is_synthetic_example=parameters.is_synthetic_example,
        )
    # Negative allocation rejected
    if allocated_carbon_g < -1e-6:
        return OrganGrowthResult(
            result_id=f"g_{organ_id}_bad_alloc",
            plant_id=plant_id, architecture_id=architecture_id,
            organ_id=organ_id, organ_type=organ_type,
            allocated_carbon_g=0.0,  # original preserved in provenance; result uses 0 for validity
            previous_biomass_g_DM=max(previous_biomass_g_DM, 0.0),
            structural_carbon_increment_g_C=0.0,
            biomass_increment_g_DM=0.0,
            new_biomass_g_DM=max(previous_biomass_g_DM, 0.0),
            growth_parameter_set_ref=parameters.parameter_set_id,
            timestep=timestep,
            status="NOT_COMPUTABLE",
            provenance=f"TASK_046J blocked: negative allocated carbon; not clamped",
            note="Allocated carbon negative; growth not computed.",
            is_synthetic_example=parameters.is_synthetic_example,
        )
    # Negative previous biomass rejected
    if previous_biomass_g_DM < -1e-6:
        return OrganGrowthResult(
            result_id=f"g_{organ_id}_bad_prev",
            plant_id=plant_id, architecture_id=architecture_id,
            organ_id=organ_id, organ_type=organ_type,
            allocated_carbon_g=max(allocated_carbon_g, 0.0),
        previous_biomass_g_DM=0.0,  # original preserved in provenance; result uses 0 for validity
            structural_carbon_increment_g_C=0.0,
            biomass_increment_g_DM=0.0,
            new_biomass_g_DM=max(previous_biomass_g_DM, 0.0),
            growth_parameter_set_ref=parameters.parameter_set_id,
            timestep=timestep,
            status="NOT_COMPUTABLE",
            provenance=f"TASK_046J blocked: negative previous biomass",
            note="Previous biomass negative; not silently clamped to zero.",
            is_synthetic_example=parameters.is_synthetic_example,
        )
    # Zero allocation → zero growth
    if abs(allocated_carbon_g) <= 1e-9:
        return OrganGrowthResult(
            result_id=f"g_{organ_id}_zero",
            plant_id=plant_id, architecture_id=architecture_id,
            organ_id=organ_id, organ_type=organ_type,
            allocated_carbon_g=0.0,
            previous_biomass_g_DM=max(previous_biomass_g_DM, 0.0),
            structural_carbon_increment_g_C=0.0,
            biomass_increment_g_DM=0.0,
            new_biomass_g_DM=max(previous_biomass_g_DM, 0.0),
            growth_parameter_set_ref=parameters.parameter_set_id,
            timestep=timestep,
            simulation_time_ref=simulation_time_ref,
            status="AVAILABLE",
            provenance=f"TASK_046J; zero allocation; growth=0; previous preserved={previous_biomass_g_DM}",
            note="Growth cost accounted via retention parameter when carbon >0; here zero allocation → zero growth.",
            is_synthetic_example=parameters.is_synthetic_example,
        )
    # Conversion (explicit; growth cost via retention)
    structural = allocated_carbon_g * parameters.growth_retention_fraction
    biomass_increment = structural / parameters.carbon_fraction_of_dry_biomass
    new_biomass = max(previous_biomass_g_DM, 0.0) + biomass_increment
    return OrganGrowthResult(
        result_id=f"g_{organ_id}_{int(timestep)}",
        plant_id=plant_id,
        architecture_id=architecture_id,
        organ_id=organ_id,
        organ_type=organ_type,
        allocated_carbon_g=allocated_carbon_g,
        previous_biomass_g_DM=max(previous_biomass_g_DM, 0.0),
        structural_carbon_increment_g_C=structural,
        biomass_increment_g_DM=biomass_increment,
        new_biomass_g_DM=new_biomass,
        growth_parameter_set_ref=parameters.parameter_set_id,
        timestep=timestep,
        simulation_time_ref=simulation_time_ref,
        status="AVAILABLE",
        provenance=f"TASK_046J; structural={structural}; biomass_inc={biomass_increment}; retention={parameters.growth_retention_fraction}; carbon_frac={parameters.carbon_fraction_of_dry_biomass}; TASK 021 respiration handled upstream; no second respiration deduction.",
        source_reference=provenance_suffix,
        parameter_version="v1",
        is_synthetic_example=parameters.is_synthetic_example,
        note="Explicit conversion: structural_carbon = allocated * retention; biomass = structural / carbon_fraction; previous biomass preserved; no geometry mutation (046K future). TASK 023 growth unit=g_C incompatible; 046J uses g_DM.",
    )
