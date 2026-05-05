from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Opus Docs"
    debug: bool = False
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        extra = "forbid"