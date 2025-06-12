from pydantic import BaseModel
from typing import Any

class diagnosis_IA(BaseModel):
    resultado: str
    resultado_json: Any 