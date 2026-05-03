# Vera Engagement Engine

A production-ready, deterministic AI engagement engine built for the magicpin Vera AI Challenge.

## Features
- **Deterministic Messaging**: Temperature=0 and rule-based templates ensure consistent outputs.
- **Stateful Decision Engine**: Tracks merchant performance, reply history, and suppression windows.
- **Signal Extraction**: Automatically identifies opportunities like local search spikes and order drops.
- **Priority Scoring**: Uses a weighted formula to rank engagement opportunities.
- **Suppression Logic**: Prevents spam and respects merchant preferences/replies.
- **Category-Aware**: Adapts tone and CTA style based on merchant category (Dentist, Salon, etc.).

## Tech Stack
- Python 3.11+
- FastAPI
- SQLModel (SQLite)
- Docker

## Getting Started

### Local Development
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

### Using Docker
1. Build the image:
   ```bash
   docker build -t vera-engine .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 vera-engine
   ```

## API Endpoints

- `GET /v1/healthz`: Health check.
- `GET /v1/metadata`: System metadata.
- `POST /v1/context`: Update merchant/trigger context.
- `POST /v1/tick`: Evaluate and generate engagement actions.
- `POST /v1/reply`: Handle merchant/customer replies.

## Example Flow

1. **Context Update**:
   ```json
   POST /v1/context
   {
     "scope": "merchant",
     "context_id": "m_001",
     "version": 1,
     "payload": {
       "identity": {"category": "restaurant"},
       "performance": {"nearby_searches": 250, "order_trend": -0.15}
     },
     "delivered_at": "2026-05-03T10:00:00Z"
   }
   ```

2. **Tick**:
   ```json
   POST /v1/tick
   ```
   *Returns actions prioritized by urgency and relevance.*

3. **Reply**:
   ```json
   POST /v1/reply
   {
     "merchant_id": "m_001",
     "text": "stop messaging"
   }
   ```
   *Updates state to opt-out the merchant.*
