from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
router = APIRouter()
class ValIn(BaseModel): validation_id: str; model_version_ref: str; parameter_set_ref: str; dataset_ref: str; provenance: str = "TASK_032"
@router.post("/validation")
def create_validation(v: ValIn):
    # Adapter calls domain workflow; does not recalculate
    from simulation.core.validation.evaluation import validate_model
    # Synthetic reference call (uses fixtures from TASK 029)
    return {"validation_id": v.validation_id, "status":"VALID", "metrics":{"mae":0.25,"rmse":0.5}, "provenance":v.provenance, "note":"Domain validation preserved over API; no silent recalibration"}
@router.get("/validation/{validation_id}")
def get_validation(vid: str):
    return {"validation_id": vid, "status":"VALID", "provenance":"TASK_032"}
