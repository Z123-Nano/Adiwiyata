from fastapi import APIRouter
from pydantic import BaseModel
router = APIRouter()
class FIn(BaseModel): source_snapshot_ref: str; target_times: list = []; provenance: str = "TASK_032"; is_synthetic_example: bool = True
@router.post("/forecasts")
def create(f: FIn):
    return {"forecast_id":"f_001","computability_status":"NOT_COMPUTABLE","execution_status":"NOT_COMPUTED","provenance":f.provenance,"note":"Forecast NOT_COMPUTABLE preserved; synthetic only"}
@router.get("/forecasts/{forecast_id}")
def get(fid: str): return {"forecast_id":fid,"computability_status":"NOT_COMPUTABLE","provenance":"TASK_032"}
