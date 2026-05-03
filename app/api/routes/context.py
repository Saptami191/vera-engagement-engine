from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.state.store import get_session
from app.state.models import ContextRecord
from app.api.schemas.context import ContextCreate, ContextUpdateResponse
from datetime import datetime

router = APIRouter()

@router.post("/context", response_model=ContextUpdateResponse)
async def update_context(
    context_data: ContextCreate,
    db: AsyncSession = Depends(get_session)
):
    # Check if a newer or same version exists
    query = select(ContextRecord).where(
        ContextRecord.scope == context_data.scope,
        ContextRecord.context_id == context_data.context_id
    ).order_by(ContextRecord.version.desc())
    
    result = await db.execute(query)
    existing_record = result.scalars().first()
    
    if existing_record and existing_record.version >= context_data.version:
        return ContextUpdateResponse(ok=False, status="lower_or_equal_version_ignored")
    
    # Store history (not asked but mentioned "maintain context history")
    # Actually, the requirement says "higher versions replace atomically"
    # and "maintain context history". I'll insert a new record for history.
    
    new_record = ContextRecord(
        scope=context_data.scope,
        context_id=context_data.context_id,
        version=context_data.version,
        payload=context_data.payload,
        delivered_at=context_data.delivered_at,
        updated_at=datetime.utcnow()
    )
    
    db.add(new_record)
    await db.commit()
    
    return ContextUpdateResponse(ok=True, status="updated")
