from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "RF Analyzer"
    SECRET_KEY: str = "change-me"
    DB_URL: str = "sqlite:///./rf_site.db"

    COOKIE_SESSION_NAME: str = "session_id"
    COOKIE_VARIANT_NAME: str = "ab_variant"

    class Config:
        env_file = ".env"

settings = Settings()
