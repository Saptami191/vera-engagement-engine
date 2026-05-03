from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.state.store import get_session
from app.state.models import MerchantState
from app.api.schemas.reply import ReplyRequest, ReplyResponse
from app.replay.intent_classifier import classify_intent
from app.engine.reply_handler import handle_reply_logic

router = APIRouter()

@router.post("/reply", response_model=ReplyResponse)
async def handle_reply(
    reply: ReplyRequest,
    db: AsyncSession = Depends(get_session)
):
    # 1. Get merchant state
    stmt = select(MerchantState).where(MerchantState.merchant_id == reply.merchant_id)
    result = await db.execute(stmt)
    m_state = result.scalars().first()
    
    if not m_state:
        raise HTTPException(status_code=404, detail="Merchant state not found")
        
    # 2. Classify intent
    intent = classify_intent(reply.text)
    
    # 3. Handle logic
    m_state = handle_reply_logic(m_state, intent)
    
    # 4. Save state
    db.add(m_state)
    await db.commit()
    
    return ReplyResponse(
        ok=True,
        intent=intent,
        action_taken=f"State updated for intent: {intent}"
    )
