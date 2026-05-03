from datetime import datetime, timedelta
from app.state.models import MerchantState

def handle_reply_logic(merchant_state: MerchantState, intent: str):
    if intent == "positive":
        merchant_state.positive_reply_count += 1
        merchant_state.ignored_count = 0
        # Maybe set a follow-up window or boost reply rate
        merchant_state.reply_rate = (merchant_state.reply_rate + 1.0) / 2.0
        
    elif intent == "negative":
        merchant_state.negative_reply_count += 1
        # Suppress for 3 days
        merchant_state.suppression_until = datetime.utcnow() + timedelta(days=3)
        
    elif intent == "stop":
        merchant_state.opted_out = True
        
    elif intent == "objection_price":
        merchant_state.negative_reply_count += 1
        # Metadata to suggest low-cost campaigns next time
        merchant_state.extra_metadata["price_sensitive"] = True
        
    elif intent == "already_running_campaign":
        # Suppress similar campaigns for a week
        merchant_state.suppression_until = datetime.utcnow() + timedelta(days=7)
        
    elif intent == "confused":
        merchant_state.extra_metadata["needs_simpler_cta"] = True

    return merchant_state
