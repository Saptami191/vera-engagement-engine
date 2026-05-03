from typing import Dict, Any
from app.composer.templates import render_message

def render_action_content(signal_name: str, metadata: Dict[str, Any]) -> Dict[str, str]:
    """
    Renders the final message and CTA based on the signal and metadata.
    """
    return render_message(signal_name, metadata)
