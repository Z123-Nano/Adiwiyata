"""TASK 046N fixtures — architecture + solar for orchestration test."""
from simulation.core.architecture.fixtures_046m_a import ARCH_3ORG
from simulation.core.light.fixtures_046m import SOLAR_NOON
from simulation.core.contracts.domain import PlantArchitecture
from copy import deepcopy

ARCH_A = ARCH_3ORG
ARCH_B = deepcopy(ARCH_3ORG)
ARCH_B.architecture_id = "arch_n_b"
ARCH_B.organs[0].length_m = 0.8
