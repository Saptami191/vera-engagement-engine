import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/v1"

async def run_demo():
    print("--- Vera Engagement Engine Demo ---")
    
    async with httpx.AsyncClient() as client:
        # 1. Health check
        resp = await client.get(f"{BASE_URL}/healthz")
        print(f"Healthz: {resp.json()}")
        
        # 2. Add Context
        context_payload = {
            "scope": "merchant",
            "context_id": "m_001_demo",
            "version": 1,
            "payload": {
                "identity": {"category": "restaurant", "name": "Vera Pizza"},
                "performance": {
                    "nearby_searches": 450,
                    "order_trend": -0.18
                },
                "offers": [
                    {"id": "o1", "name": "₹99 Lunch Combo", "redemption_rate": 0.02}
                ]
            },
            "delivered_at": datetime.utcnow().isoformat() + "Z"
        }
        resp = await client.post(f"{BASE_URL}/context", json=context_payload)
        print(f"Update Context: {resp.json()}")
        
        # 3. Process Tick
        resp = await client.post(f"{BASE_URL}/tick")
        actions = resp.json().get("actions", [])
        print(f"Tick generated {len(actions)} actions.")
        for action in actions:
            print(f"\n[ACTION] Priority: {action['priority_score']}")
            print(f"Message: {action['message']}")
            print(f"Rationale: {action['rationale']}")
            
        # 4. Handle Reply
        reply_payload = {
            "merchant_id": "m_001_demo",
            "text": "this sounds expensive"
        }
        resp = await client.post(f"{BASE_URL}/reply", json=reply_payload)
        print(f"\nReply Handling: {resp.json()}")

if __name__ == "__main__":
    print("Ensure the server is running (uvicorn main:app) before running this demo.")
    # In a real scenario, we'd start the server here, but for now we just show the code.
    # asyncio.run(run_demo())
