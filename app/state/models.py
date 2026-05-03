from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, JSON, Column
from pydantic import BaseModel

class ContextRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    scope: str = Field(index=True)
    context_id: str = Field(index=True)
    version: int
    payload: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    delivered_at: datetime
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MerchantState(SQLModel, table=True):
    merchant_id: str = Field(primary_key=True)
    last_messages: List[Dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))
    ignored_count: int = 0
    reply_rate: float = 0.0
    last_campaign_type: Optional[str] = None
    suppression_until: Optional[datetime] = None
    negative_reply_count: int = 0
    positive_reply_count: int = 0
    opted_out: bool = False
    extra_metadata: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

class EngagementAction(BaseModel):
    merchant_id: str
    message: str
    cta: str
    send_as: str
    suppression_key: str
    priority_score: float
    rationale: List[str]
    extra_metadata: Dict[str, Any] = {}
