from datetime import datetime
from typing import Tuple, Optional
from app.state.models import MerchantState

def should_suppress(
    merchant_id: str,
    signal_name: str,
    merchant_state: MerchantState
) -> Tuple[bool, Optional[str]]:
    
    # 1. Opt-out
    if merchant_state.opted_out:
        return True, "merchant_opted_out"
    
    # 2. Global suppression window
    if merchant_state.suppression_until and merchant_state.suppression_until > datetime.utcnow():
        return True, "active_suppression_window"
    
    # 3. Duplicate recent campaign
    last_messages = merchant_state.last_messages[-5:] # Check last 5
    for msg in last_messages:
        if msg.get("suppression_key") == signal_name:
            # Check if sent in last 24 hours (simplified)
            # sent_at = datetime.fromisoformat(msg.get("sent_at"))
            # if (datetime.utcnow() - sent_at).days < 1:
            return True, "duplicate_recent_campaign"
            
    # 4. Excessive ignored messages
    if merchant_state.ignored_count > 3:
        return True, "excessive_ignored_messages"
        
    return False, None
