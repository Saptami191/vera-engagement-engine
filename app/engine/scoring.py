from app.core.constants import SIGNAL_WEIGHTS
from app.engine.signal_extractor import Signal
from app.state.models import MerchantState

def calculate_priority_score(
    signal: Signal,
    merchant_state: MerchantState
) -> float:
    # priority_score = ( trigger_strength * 0.35 + engagement_probability * 0.25 + 
    #                  urgency * 0.20 + merchant_responsiveness * 0.20 )
    
    trigger_strength = signal.strength
    
    # Simple heuristics for engagement probability and urgency
    engagement_probability = merchant_state.reply_rate if merchant_state.reply_rate > 0 else 0.5
    
    # Urgency depends on signal type
    urgency_map = {
        "local_search_spike": 0.8,
        "severe_order_drop": 0.9,
        "unused_offer_inventory": 0.4
    }
    urgency = urgency_map.get(signal.name, 0.5)
    
    # Merchant responsiveness
    responsiveness = 0.5
    if merchant_state.positive_reply_count > 0:
        responsiveness += 0.1 * merchant_state.positive_reply_count
    if merchant_state.negative_reply_count > 0:
        responsiveness -= 0.1 * merchant_state.negative_reply_count
    responsiveness = max(0.1, min(1.0, responsiveness))
    
    score = (
        trigger_strength * SIGNAL_WEIGHTS["trigger_strength"] +
        engagement_probability * SIGNAL_WEIGHTS["engagement_probability"] +
        urgency * SIGNAL_WEIGHTS["urgency"] +
        responsiveness * SIGNAL_WEIGHTS["merchant_responsiveness"]
    )
    
    return round(score * 10, 2) # Scale to 0-10
