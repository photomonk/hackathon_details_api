from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    gemini_api_key: str
    gemini_model: str = "gemini-1.5-flash"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()