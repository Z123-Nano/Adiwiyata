"""TASK 032 — FastAPI boundary (adapter, not second domain)."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from simulation.api.routers import health, garden, plants, lightfield, measurement, observation, snapshot, scenario, prediction, forecast, validation, calibration, models, clock, simulation_step

app = FastAPI(title="Digital Twin Garden API", version="v1", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(garden.router, prefix="/api/v1", tags=["garden"])
app.include_router(plants.router, prefix="/api/v1", tags=["plants"])
app.include_router(lightfield.router, prefix="/api/v1", tags=["lightfield"])
app.include_router(measurement.router, prefix="/api/v1", tags=["measurement"])
app.include_router(observation.router, prefix="/api/v1", tags=["observation"])
app.include_router(snapshot.router, prefix="/api/v1", tags=["snapshot"])
app.include_router(scenario.router, prefix="/api/v1", tags=["scenario"])
app.include_router(prediction.router, prefix="/api/v1", tags=["prediction"])
app.include_router(forecast.router, prefix="/api/v1", tags=["forecast"])
app.include_router(validation.router, prefix="/api/v1", tags=["validation"])
app.include_router(calibration.router, prefix="/api/v1", tags=["calibration"])
app.include_router(models.router, prefix="/api/v1", tags=["models"])
app.include_router(clock.router, prefix="/api/v1", tags=["simulation"])
app.include_router(simulation_step.router, prefix="/api/v1", tags=["simulation"])
