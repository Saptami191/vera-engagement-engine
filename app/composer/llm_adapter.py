from typing import str, Any, Dict
from app.core.config import settings

class LLMAdapter:
    """
    Abstraction for OpenAI-compatible LLM.
    Ensures deterministic behavior with temperature=0.
    """
    def __init__(self):
        self.model = settings.LLM_MODEL
        self.temperature = settings.LLM_TEMPERATURE # Forced to 0.0 in config
        
    async def generate_response(self, prompt: str, system_prompt: str = "") -> str:
        # In a real implementation, this would call OpenAI API
        # For now, we remain deterministic via templates or simple logic
        return "Deterministic response from LLM placeholder."

llm = LLMAdapter()
