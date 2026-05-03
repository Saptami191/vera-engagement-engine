CATEGORY_RULES = {
    "dentist": {
        "tone": "clinical",
        "cta_style": "simple",
        "avoid": ["aggressive hype"],
        "default_cta": "Reply YES to book a consultation"
    },
    "salon": {
        "tone": "visual",
        "cta_style": "promotional",
        "default_cta": "Reply YES to claim this offer"
    },
    "restaurant": {
        "tone": "urgent",
        "cta_style": "offer-driven",
        "default_cta": "Reply YES to order now"
    },
    "gym": {
        "tone": "performance",
        "cta_style": "challenge",
        "default_cta": "Reply YES to start your challenge"
    },
    "pharmacy": {
        "tone": "utility-first",
        "cta_style": "trust-oriented",
        "default_cta": "Reply YES to order refill"
    }
}

SIGNAL_WEIGHTS = {
    "trigger_strength": 0.35,
    "engagement_probability": 0.25,
    "urgency": 0.20,
    "merchant_responsiveness": 0.20
}

INTENT_MAP = {
    "positive": "positive",
    "negative": "negative",
    "stop": "stop",
    "confused": "confused",
    "already_running_campaign": "already_running_campaign",
    "objection_price": "objection_price",
    "objection_timing": "objection_timing",
    "off_topic": "off_topic",
    "hostile": "hostile"
}
