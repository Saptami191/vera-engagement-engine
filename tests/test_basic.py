import pytest
from app.replay.intent_classifier import classify_intent
from app.engine.signal_extractor import extract_signals, Signal
from app.state.models import ContextRecord
from datetime import datetime

def test_intent_classification():
    assert classify_intent("yes please") == "positive"
    assert classify_intent("stop") == "stop"
    assert classify_intent("too expensive") == "objection_price"
    assert classify_intent("already running this") == "already_running_campaign"

def test_signal_extraction():
    ctx = ContextRecord(
        scope="merchant",
        context_id="m1",
        version=1,
        payload={
            "performance": {
                "nearby_searches": 300,
                "order_trend": -0.20
            }
        },
        delivered_at=datetime.utcnow()
    )
    signals = extract_signals("m1", [ctx])
    signal_names = [s.name for s in signals]
    assert "local_search_spike" in signal_names
    assert "severe_order_drop" in signal_names
