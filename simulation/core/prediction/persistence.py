"""Prediction persistence — JSON; deterministic; no DB."""
from __future__ import annotations
import json
from pathlib import Path
from typing import List, Optional
from simulation.core.prediction.contracts import Prediction, PredictionRequest

class PredictionRecord:
    def __init__(self, predictions: Optional[List[Prediction]] = None):
        self.predictions = predictions or []
    def add(self, p: Prediction) -> None:
        self.predictions.append(Prediction.model_validate(p.model_dump(mode="json")))
    def to_json(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps([p.model_dump(mode="json") for p in self.predictions], indent=2, default=str))
    @classmethod
    def from_json(cls, path: str | Path) -> "PredictionRecord":
        data = json.loads(Path(path).read_text())
        return cls(predictions=[Prediction.model_validate(item) for item in data])

def save_prediction(p: Prediction, path: str | Path) -> None:
    PredictionRecord([p]).to_json(path)

def load_prediction(path: str | Path) -> Prediction:
    return PredictionRecord.from_json(path).predictions[0]
