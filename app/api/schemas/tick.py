from pydantic import BaseModel
from typing import List, Optional
from app.state.models import EngagementAction

class TickResponse(BaseModel):
    actions: List[EngagementAction]
