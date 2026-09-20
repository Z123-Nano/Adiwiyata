"""TASK 046P-H fixtures — synthetic 046J audit cases (labeled)."""
from simulation.core.growth.growth_conversion_params import growth_params
from simulation.core.growth.growth_derivation import derive_organ_growth

# A retention=1.0
PARAM_A = growth_params("pA", "leaf", growth_retention_fraction=1.0, carbon_fraction_of_dry_biomass=0.5, provenance="TASK_046P-H A synthetic", is_synthetic_example=True)
# B retention=0.5
PARAM_B = growth_params("pB", "leaf", growth_retention_fraction=0.5, carbon_fraction_of_dry_biomass=0.5, provenance="TASK_046P-H B synthetic", is_synthetic_example=True)
# C retention=0
PARAM_C = growth_params("pC", "leaf", growth_retention_fraction=0.0, carbon_fraction_of_dry_biomass=0.5, provenance="TASK_046P-H C synthetic", is_synthetic_example=True)

RES_A = derive_organ_growth("o1","p1","leaf",1.0,0.0,PARAM_A,timestep=3600)
RES_B = derive_organ_growth("o2","p1","leaf",1.0,0.0,PARAM_B,timestep=3600)
RES_C = derive_organ_growth("o3","p1","leaf",1.0,0.0,PARAM_C,timestep=3600)
