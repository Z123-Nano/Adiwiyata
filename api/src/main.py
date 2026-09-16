from fastapi import FastAPI

app = FastAPI(title="Digital Twin Garden API")

@app.get("/")
def root():
    return {"message": "Digital Twin Garden API hello (TASK 001)"}
