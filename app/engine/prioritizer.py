from typing import List
from app.state.models import EngagementAction, MerchantState
from app.engine.signal_extractor import Signal
from app.engine.scoring import calculate_priority_score
from app.composer.templates import render_message
from app.core.constants import CATEGORY_RULES

def prioritize_actions(
    merchant_id: str,
    signals: List[Signal],
    merchant_state: MerchantState,
    merchant_category: str
) -> List[EngagementAction]:
    actions = []
    
    # Sort signals by strength for initial selection
    signals.sort(key=lambda x: x.strength, reverse=True)
    
    # Category specific rules
    cat_rules = CATEGORY_RULES.get(merchant_category, {})
    
    for signal in signals:
        score = calculate_priority_score(signal, merchant_state)
        
        # Prepare context for rendering
        render_ctx = {
            "category": merchant_category,
            "offer_name": "special deal", # Default, should come from context
            **signal.metadata
        }
        
        # Override drop percentage for display
        if "drop_percentage" in render_ctx:
            render_ctx["drop_percentage"] = int(render_ctx["drop_percentage"] * 100)
            
        rendered = render_message(signal.name, render_ctx)
        
        actions.append(EngagementAction(
            merchant_id=merchant_id,
            message=rendered["message"],
            cta=rendered["cta"],
            send_as="vera_growth_assistant",
            suppression_key=signal.name,
            priority_score=score,
            rationale=[signal.name],
            extra_metadata=signal.metadata
        ))
        
    # Final sort by priority score
    actions.sort(key=lambda x: x.priority_score, reverse=True)
    
    return actions
