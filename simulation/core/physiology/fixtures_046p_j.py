"""TASK 046P-J fixtures — synthetic ConversionResidualContract cases."""
from simulation.core.physiology.conversion_residual_contract import build_conversion_residual_contract

CONTRACT_A = build_conversion_residual_contract("res_A","p1",1.0,1.0,provenance="TASK_046P-J A synthetic",is_synthetic_example=True)
CONTRACT_B = build_conversion_residual_contract("res_B","p1",1.0,0.5,provenance="TASK_046P-J B synthetic",is_synthetic_example=True)
CONTRACT_C = build_conversion_residual_contract("res_C","p1",1.0,0.0,provenance="TASK_046P-J C synthetic",is_synthetic_example=True)
CONTRACT_D = build_conversion_residual_contract("res_D","p1",1.0,0.5,provenance="TASK_046P-J D synthetic surplus distinction",is_synthetic_example=True)
CONTRACT_E = build_conversion_residual_contract("res_E","p1",1.0,0.5,provenance="TASK_046P-J E respiration distinction",is_synthetic_example=True)
CONTRACT_F = build_conversion_residual_contract("res_F","p1",1.0,0.5,provenance="TASK_046P-J F reserve distinction",is_synthetic_example=True)
