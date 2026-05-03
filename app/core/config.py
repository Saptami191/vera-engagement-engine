from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "vera-compose-engine"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/v1"
    
    DATABASE_URL: str = "sqlite+aiosqlite:///./vera.db"
    
    # LLM Configuration
    OPENAI_API_KEY: str = "sk-placeholder"
    LLM_MODEL: str = "gpt-4-turbo"
    LLM_TEMPERATURE: float = 0.0
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    SUPPORTED_SCOPES: List[str] = ["merchant", "customer", "trigger"]
    
    # Data Paths
    SEED_DATA_PATH: str = "app/data/seeds"
    EXPANDED_DATA_PATH: str = "app/data/expanded"
    
    class Config:
        env_file = ".env"

settings = Settings()
