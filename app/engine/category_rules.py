from app.core.constants import CATEGORY_RULES

def get_category_config(category: str):
    return CATEGORY_RULES.get(category.lower(), CATEGORY_RULES.get("restaurant"))

def apply_category_tone(message: str, category: str) -> str:
    # Logic to adjust tone if needed
    return message
