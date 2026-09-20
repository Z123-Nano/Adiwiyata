"""TASK 046K — Pure derivation: realized biomass → architecture growth delta (proposal only)."""
from __future__ import annotations
from typing import Optional
from simulation.core.growth.growth_conversion_params import GrowthConversionParameters
from simulation.core.architecture.growth_delta import ArchitectureGrowthDelta
from simulation.core.growth.organ_growth import OrganGrowthResult

def derive_architecture_growth_delta(
    organ_id: str,
    plant_id: str,
    organ_type: str,
    previous_length_m: float,
    growth_result: OrganGrowthResult,
    parameters: GrowthConversionParameters,
    architecture_id: Optional[str] = None,
    timestep: float = 3600.0,
    simulation_time_ref: Optional[str] = None,
    provenance_suffix: Optional[str] = None,
) -> ArchitectureGrowthDelta:
    """Pure — consumes 046J growth result; proposes geometry delta; does NOT mutate PlantOrgan."""
    # Identity required
    if not plant_id or not organ_id:
        return ArchitectureGrowthDelta(
            result_id=f"delta_{organ_id or ''}_bad_id", plant_id=plant_id or "",
            architecture_id=architecture_id, organ_id=organ_id or "", organ_type=organ_type or "other",
            previous_biomass_g_DM=max(getattr(growth_result,"previous_biomass_g_DM",0.0),0.0),
            biomass_increment_g_DM=0.0, new_biomass_g_DM=max(getattr(growth_result,"previous_biomass_g_DM",0.0),0.0),
            geometry_dimension="length_m", previous_length_m=max(previous_length_m,0.0), delta_length_m=0.0, proposed_length_m=max(previous_length_m,0.0),
            relation_type="none", parameter_set_ref=getattr(parameters,"parameter_set_id","none"), timestep=timestep,
            status="NOT_COMPUTABLE",
            provenance="TASK_046K blocked: missing identity; no fabricated id.",
            note="Organ/plant identity required.",
            is_synthetic_example=getattr(parameters,"is_synthetic_example",False),
        )
    # Negative previous length rejected
    if previous_length_m < -1e-6:
        return ArchitectureGrowthDelta(
            result_id=f"delta_{organ_id}_bad_len", plant_id=plant_id, architecture_id=architecture_id,
            organ_id=organ_id, organ_type=organ_type,
            previous_biomass_g_DM=getattr(growth_result,"previous_biomass_g_DM",0.0) or 0.0,
            biomass_increment_g_DM=0.0, new_biomass_g_DM=max(getattr(growth_result,"previous_biomass_g_DM",0.0) or 0.0,0.0),
            geometry_dimension="length_m", previous_length_m=max(previous_length_m,0.0),
            delta_length_m=0.0, proposed_length_m=max(previous_length_m,0.0),
            relation_type="none", parameter_set_ref=getattr(parameters,"parameter_set_id","none"), timestep=timestep,
            status="NOT_COMPUTABLE",
            provenance="TASK_046K blocked: negative previous_length_m; not clamped.",
            note="Invalid geometry input.",
            is_synthetic_example=getattr(parameters,"is_synthetic_example",False),
        )
    # Negative biomass increment rejected
    biomass_inc = float(getattr(growth_result,"biomass_increment_g_DM",0.0) or 0.0)
    if biomass_inc < -1e-6:
        return ArchitectureGrowthDelta(
            result_id=f"delta_{organ_id}_bad_biomass", plant_id=plant_id, architecture_id=architecture_id,
            organ_id=organ_id, organ_type=organ_type,
            previous_biomass_g_DM=float(getattr(growth_result,"previous_biomass_g_DM",0.0) or 0.0),
            biomass_increment_g_DM=biomass_inc,
            new_biomass_g_DM=float(getattr(growth_result,"previous_biomass_g_DM",0.0) or 0.0) + biomass_inc,
            geometry_dimension="length_m", previous_length_m=max(previous_length_m,0.0),
            delta_length_m=0.0, proposed_length_m=max(previous_length_m,0.0),
            relation_type="none", parameter_set_ref=getattr(parameters,"parameter_set_id","none"), timestep=timestep,
            status="NOT_COMPUTABLE",
            provenance="TASK_046K blocked: negative biomass increment; shrinkage not modeled.",
            note="Negative growth rejected; no shrinkage model.",
            is_synthetic_example=getattr(parameters,"is_synthetic_example",False),
        )
    # Parameter check
    if parameters.relation_type != "specific_length_linear" or parameters.specific_length_m_per_g_DM <= 0:
        return ArchitectureGrowthDelta(
            result_id=f"delta_{organ_id}_bad_param", plant_id=plant_id, architecture_id=architecture_id,
            organ_id=organ_id, organ_type=organ_type,
            previous_biomass_g_DM=float(getattr(growth_result,"previous_biomass_g_DM",0.0) or 0.0),
            biomass_increment_g_DM=biomass_inc,
            new_biomass_g_DM=float(getattr(growth_result,"previous_biomass_g_DM",0.0) or 0.0) + biomass_inc,
            geometry_dimension="length_m", previous_length_m=max(previous_length_m,0.0),
            delta_length_m=0.0, proposed_length_m=max(previous_length_m,0.0),
            relation_type=getattr(parameters,"relation_type","none"),
            parameter_set_ref=getattr(parameters,"parameter_set_id","none"), timestep=timestep,
            status="NOT_COMPUTABLE",
            provenance="TASK_046K blocked: unsupported or invalid growth parameter",
            note="Only specific_length_linear with positive coeff supported.",
            is_synthetic_example=getattr(parameters,"is_synthetic_example",False),
        )
    # Derivation (linear specific-length; explicit)
    delta = biomass_inc * parameters.specific_length_m_per_g_DM
    proposed = max(previous_length_m, 0.0) + delta
    prev_bio = float(getattr(growth_result,"previous_biomass_g_DM",0.0) or 0.0)
    new_bio = prev_bio + biomass_inc
    return ArchitectureGrowthDelta(
        result_id=f"delta_{organ_id}_{int(timestep)}",
        plant_id=plant_id,
        architecture_id=architecture_id,
        organ_id=organ_id,
        organ_type=organ_type,
        previous_biomass_g_DM=prev_bio,
        biomass_increment_g_DM=biomass_inc,
        new_biomass_g_DM=new_bio,
        geometry_dimension="length_m",
        previous_length_m=max(previous_length_m, 0.0),
        delta_length_m=delta,
        proposed_length_m=proposed,
        relation_type="specific_length_linear",
        parameter_set_ref=parameters.parameter_set_id,
        timestep=timestep,
        simulation_time_ref=simulation_time_ref,
        status="AVAILABLE",
        provenance=f"TASK_046K; delta={delta}; prev_len={previous_length_m}; param={parameters.parameter_set_id}; 046J biomass source; 023 unit=g_C noted; synthetic param.",
        source_reference=provenance_suffix,
        parameter_version="v1",
        is_synthetic_example=getattr(parameters,"is_synthetic_example",False),
        note="Proposal only; PlantOrgan not mutated; geometry update belongs to future application layer (046K+); synthetic specific_length parameter.",
    )
