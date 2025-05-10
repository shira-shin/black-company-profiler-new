# server/models.py

from typing import Optional, Dict
from pydantic import BaseModel

class ProfileRequest(BaseModel):
    company: str
    statsDataId: Optional[str] = None
    preset: str = 'default'

class ProfileResponse(BaseModel):
    company: str
    score: float
    rank: str
    comment: str
    breakdown: Dict[str, float]
