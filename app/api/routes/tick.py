from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.state.store import get_session
from app.state.models import ContextRecord, MerchantState, EngagementAction
from app.api.schemas.tick import TickResponse
from app.engine.signal_extractor import extract_signals
from app.engine.prioritizer import prioritize_actions
from app.engine.suppression import should_suppress
from typing import List

router = APIRouter()

@router.post("/tick", response_model=TickResponse)
async def process_tick(db: AsyncSession = Depends(get_session)):
    # 1. Collect all merchants (simplified: get unique merchant_ids from contexts)
    # In a real app, this would be from a Merchant table.
    print("TICK STARTED")
    query = select(ContextRecord.context_id).where(ContextRecord.scope == "merchant").distinct()
    result = await db.execute(query)
    merchant_ids = result.scalars().all()
    print("MERCHANT IDS:", merchant_ids)
    
    all_candidate_actions: List[EngagementAction] = []
    
    for m_id in merchant_ids:
        # 2. Get state
        stmt = select(MerchantState).where(MerchantState.merchant_id == m_id)
        res = await db.execute(stmt)
        m_state = res.scalars().first()
        
        if not m_state:
            m_state = MerchantState(merchant_id=m_id)
            db.add(m_state)
            await db.commit()
            await db.refresh(m_state)
            
        # 3. Get recent contexts
        ctx_stmt = select(ContextRecord).where(ContextRecord.context_id == m_id).order_by(ContextRecord.version.desc())
        ctx_res = await db.execute(ctx_stmt)
        contexts = ctx_res.scalars().all()
        print("CONTEXTS:", contexts)
        
        # 4. Extract signals
        signals = extract_signals(m_id, contexts)
        print("SIGNALS:", signals)
        
        # 5. Prioritize actions
        category = contexts[0].payload.get("identity", {}).get("category", "restaurant") if contexts else "restaurant"
        actions = prioritize_actions(m_id, signals, m_state, category)
        print("ACTIONS:", actions)
        
        # 6. Apply suppression
        for action in actions:
            is_suppressed, reason = should_suppress(m_id, action.suppression_key, m_state)
            if not is_suppressed:
                all_candidate_actions.append(action)
                
    # 7. Global prioritization & cap to 20
    all_candidate_actions.sort(key=lambda x: x.priority_score, reverse=True)
    top_actions = all_candidate_actions[:20]
    
    return TickResponse(actions=top_actions)
