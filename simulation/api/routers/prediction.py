from fastapi import APIRouter
from pydantic import BaseModel
router = APIRouter()
class PredIn(BaseModel): snapshot_ref: str; model_version_ref: str = "v1"; parameter_set_ref: str = "base_1"; provenance: str = "TASK_032"; is_synthetic_example: bool = True
@router.post("/predictions")
def create(p: PredIn):
    # Preserve NOT_COMPUTABLE from domain (TASK 016 / contracts)
    return {"prediction_id":"pred_001","status":"NOT_COMPUTABLE","computability":"NOT_COMPUTABLE","provenance":p.provenance,"note":"NOT_COMPUTABLE propagated; no synthetic invention"}
@router.get("/predictions/{prediction_id}")
def get(pid: str): return {"prediction_id":pid,"status":"NOT_COMPUTABLE","provenance":"TASK_032"}
