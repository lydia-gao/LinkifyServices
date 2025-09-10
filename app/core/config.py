from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    base_url: str = "http://localhost:8000"
    database_url: str
    secret_key: str
    google_client_id: str
    google_client_secret: str
    access_token_expire_minutes: int = 20
    redis_url: str = "redis://localhost:6379/1"

    class Config:
        env_file = ".env"

settings = Settings()

