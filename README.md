# My Digital Twin Garden

A local-first, scientifically grounded spatial-temporal digital twin of a real garden with a Functional-Structural Plant Model (FSPM).

Status: FOUNDATION v0.1 — repository/tooling bootstrap (TASK 001 complete). Not a game; visualization is output, not source of biological truth.

## Repository structure
- `frontend/` — React + TypeScript + Vite + R3F + Zustand
- `api/` — FastAPI
- `simulation/` — Python scientific core (NumPy, SciPy, Pydantic/dataclasses)
- `data/` — project files + DuckDB when useful
- `tests/` — pytest, Vitest
- `docs/` — ARCHITECTURE.md, DEVELOPMENT.md
- `scripts/` — helpers

## How they relate
Frontend renders domain state; API is the boundary; simulation core computes independently of R3F/Three.js.

## Start
```bash
# Frontend
cd frontend && npm install && npm run dev

# Python / API
python -m venv .venv && source .venv/bin/activate
pip install numpy scipy pydantic fastapi pytest
pytest

# API
uvicorn api.src.main:app --reload
```

## References only (not runtime dependencies)
MetaFSPM, CPlantBox, GreenLab — inform architecture, not required at install.

See `CLAUDE.md` and `CLAUDE_MASTER_SPEC.md` for full specification.
