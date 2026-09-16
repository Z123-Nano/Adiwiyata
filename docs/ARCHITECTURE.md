# My Digital Twin Garden — Architecture

Status: FOUNDATION v0.1 (TASK 001).

## Purpose
Local-first, scientifically grounded spatial-temporal digital twin of a real garden. Not a game; visualization is output, not source of biological truth.

## Repository structure
- `frontend/` — React + R3F visualization and interaction (Zustand state)
- `api/` — FastAPI boundary
- `simulation/` — Python scientific core (independent of frontend)
- `data/` — human-readable project files; DuckDB for analytics when needed
- `tests/` — `tests/simulation/`, `tests/api/`, `tests/frontend/`
- `docs/` — specification, architecture, development guides
- `scripts/` — helper scripts

## Component relationships
Frontend <-> API <-> Simulation core + Data layer
- R3F never calculates scientific growth or solar geometry.
- Simulation clock -> scheduler -> model updates -> domain state -> frontend rendering.

## Stack (per CLAUDE.md / master spec)
- Frontend: React, TypeScript, Vite, R3F, Three.js, Drei, Zustand
- Core: Python, NumPy, SciPy, Pydantic/dataclasses
- API: FastAPI
- Data: project files + DuckDB (when useful)
- Testing: pytest, Vitest

## Boundaries
- Scientific logic independent from React/R3F.
- Plant physiology, solar model, garden spatial model not yet implemented (TASK 002+).
- References MetaFSPM, CPlantBox, GreenLab are research only — not runtime dependencies.
Contracts added: simulation/core/contracts/domain.py (Pydantic) and frontend/src/contracts/domain.ts. No architecture change to stack.
