from fastapi import APIRouter
router = APIRouter()
@router.get("/models")
def list_models(): return {"models":[{"version":"v1","provenance":"TASK_032","status":"VALID"}],"note":"Read-only lineage"}
@router.get("/parameters")
def list_params(): return {"parameter_sets":[{"id":"base_1","version":"base","provenance":"TASK_032","status":"VALID","note":"Calibrated variants separate (TASK 028)"}]}
