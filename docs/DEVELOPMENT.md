# Development Guide — My Digital Twin Garden

Target OS: Debian Linux.

## Install dependencies

Frontend:
```bash
cd frontend
npm install
```

Python (use a virtualenv):
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or pip install numpy scipy pydantic fastapi pytest
```

API (FastAPI):
```bash
pip install fastapi uvicorn
```

## Run tests
- Python: `pytest` (from repo root or `tests/`)
- Frontend: `npm test` (Vitest, from `frontend/`)

## Development environment
- Frontend dev server: `npm run dev` (Vite, from `frontend/`)
- API: `uvicorn api.src.main:app --reload` (from repo root)
- Simulation package import: `python -c "import simulation; print('ok')"`

## Build check
- `npm run build` (from `frontend/`)

## Notes
- No plant/solar/spatial logic implemented yet (TASK 001); only toolchain verification.
- No CPlantBox/MetaFSPM/GreenLab runtime dependencies.

## Compatibility note — TASK 001-FIX (2026-09-16)
- R3F 8.18 peer dependency requires React >=18 <19 (not React 19).
- Selected: React 18.3.1 + react-dom 18.3.1 + @react-three/fiber 8.18.0 + @react-three/drei 9.122.0 + three 0.160.1.
- Added `frontend/src/r3f-jsx.d.ts` to declare R3F JSX elements until upstream JSX augmentation is available in this build.
- `npm install`, `npm run build`, `tsc --noEmit`, and Vitest all pass.
