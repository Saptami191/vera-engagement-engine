from typing import Dict, Any

TEMPLATES = {
    "search_visibility_spike": {
        "text": "{search_visibility_change}% more users searched nearby this week. Want to promote your {offer_title} tonight?",
        "cta": "Reply YES to launch tonight"
    },

    "weekly_order_drop": {
        "text": "Orders dropped {weekly_orders_change_abs}% this week. Want to reactivate your {offer_title} today?",
        "cta": "Reply YES to relaunch"
    },

    "inactive_offer_available": {
        "text": "Your {offer_title} is inactive right now. Want to promote it to nearby customers tonight?",
        "cta": "Reply YES to promote"
    }
}

def render_message(signal_name: str, context_data: Dict[str, Any]) -> Dict[str, str]:
    template = TEMPLATES.get(signal_name)

    if not template:
        return {
            "message": "New customer demand detected nearby. Want to act on it today?",
            "cta": "Reply YES to explore"
        }

    safe_context = context_data.copy()

    if "weekly_orders_change" in safe_context:
        safe_context["weekly_orders_change_abs"] = abs(
            safe_context["weekly_orders_change"]
        )

    try:
        message = template["text"].format(**safe_context)

        return {
            "message": message,
            "cta": template["cta"]
        }

    except KeyError as e:
        return {
            "message": f"New demand detected in your area. Want to promote your offers today?",
            "cta": "Reply YES to launch"
        }