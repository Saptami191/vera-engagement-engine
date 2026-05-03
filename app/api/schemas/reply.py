from pydantic import BaseModel
from typing import Optional

class ReplyRequest(BaseModel):
    merchant_id: str
    text: str
    context_id: Optional[str] = None

class ReplyResponse(BaseModel):
    ok: bool
    intent: str
    action_taken: str
