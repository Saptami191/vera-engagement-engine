from typing import List, Dict, Any
from app.state.models import ContextRecord
from pydantic import BaseModel

class Signal(BaseModel):
    name: str
    strength: float
    description: str
    metadata: Dict[str, Any] = {}

def extract_signals(merchant_id: str, contexts: List[ContextRecord]) -> List[Signal]:
    signals = []

    merged_payload = {}

    for ctx in contexts:
        merged_payload.update(ctx.payload)

    performance = merged_payload.get("performance", {})
    offers = merged_payload.get("offers", [])

    # SEARCH SPIKE
    search_change = performance.get("search_visibility_change", 0)

    if search_change >= 20:
        signals.append(
            Signal(
                name="search_visibility_spike",
                strength=min(1.0, search_change / 100),
                description=f"Search visibility increased by {search_change}%.",
                metadata={
                    "search_visibility_change": search_change
                }
            )
        )

    # ORDER DROP
    order_change = performance.get("weekly_orders_change", 0)

    if order_change <= -10:
        signals.append(
            Signal(
                name="weekly_order_drop",
                strength=min(1.0, abs(order_change) / 100),
                description=f"Orders dropped by {abs(order_change)}% this week.",
                metadata={
                    "weekly_orders_change": order_change
                }
            )
        )

    # INACTIVE OFFERS
    inactive_offers = [
        o for o in offers
        if not o.get("active", True)
    ]

    if inactive_offers:
        signals.append(
            Signal(
                name="inactive_offer_available",
                strength=0.6,
                description="You have inactive offers ready to promote.",
                metadata={
                    "offer_title": inactive_offers[0].get("title")
                }
            )
        )

    return signals
