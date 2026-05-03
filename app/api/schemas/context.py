from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any

class ContextCreate(BaseModel):
    scope: str
    context_id: str
    version: int
    payload: Dict[str, Any]
    delivered_at: datetime

class ContextUpdateResponse(BaseModel):
    ok: bool
    status: str
