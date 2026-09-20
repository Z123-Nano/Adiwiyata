from fastapi import APIRouter
router = APIRouter()

@router.get("/health")
def health():
    return {
        "status": "ok",
        "api_version": "v1",
        "app": "Digital Twin Garden",
        "scientific_core": "available",
        "note": "TASK 032 adapter boundary — no simulation run",
    }
