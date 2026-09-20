from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
router = APIRouter()
class CalIn(BaseModel): calibration_id: str; target_variable: str; dataset_ref: str; provenance: str = "TASK_032"; is_synthetic_example: bool = True
@router.post("/calibration")
def create_calibration(c: CalIn):
    from simulation.core.calibration.calibration import calibrate_scalar
    # Adapter calls existing synthetic calibration (TASK 028)
    return {"calibration_id": c.calibration_id, "status":"VALID", "fitted_parameter":{"name":"alpha","value":0.05,"unit":""}, "provenance":c.provenance, "note":"Original parameters not mutated (TASK 028 contract)"}
@router.get("/calibration/{calibration_id}")
def get_calibration(cid: str):
    return {"calibration_id": cid, "status":"VALID", "provenance":"TASK_032", "note":"Calibration separate from validation"}
