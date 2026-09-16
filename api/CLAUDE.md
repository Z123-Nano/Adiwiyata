# API — My Digital Twin Garden

## Responsibility
FastAPI boundary between frontend and scientific simulation core.

## Rules
- Stateless endpoints; simulation state managed by Python core.
- No plant/solar logic here — delegate to `simulation/`.

## Tests
- `pytest` under `tests/api/`
