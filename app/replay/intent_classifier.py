# No imports needed for builtin str

def classify_intent(text: str) -> str:
    text = text.lower().strip()
    
    if any(word in text for word in ["yes", "ok", "sure", "do it", "start", "launch"]):
        return "positive"
    
    if any(word in text for word in ["stop", "unsubscribe", "no more", "quit"]):
        return "stop"
    
    if any(word in text for word in ["no", "not now", "later", "busy"]):
        return "negative"
        
    if any(word in text for word in ["expensive", "cost", "price", "too much"]):
        return "objection_price"
        
    if any(word in text for word in ["what", "how", "don't understand", "help"]):
        return "confused"
        
    if any(word in text for word in ["already", "running", "active"]):
        return "already_running_campaign"
        
    return "off_topic"
