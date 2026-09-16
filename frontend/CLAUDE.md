# Frontend — My Digital Twin Garden

## Responsibility
Visualization and interaction only. No scientific computation inside React render loops.

## Rules
- Use R3F / Drei for 3D; Zustand for UI state.
- Scientific logic lives in `simulation/`; frontend consumes domain output.
- Do NOT compute photosynthesis, growth, shadow, or solar position in components.

## Tests
- `npm test` (Vitest)
