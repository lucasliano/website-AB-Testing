from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Information loaded from the docker-compose.yml file
    FASTAPI_NAME: str
    DB_URL: str

    # Cookie names
    COOKIE_SESSION_NAME: str = "session_id"
    COOKIE_VARIANT_NAME: str = "ab_variant"

    # Default BaseSettings structure should include a Config Class
    class Config:
        # If I find any environment variables that are NOT declared in the Settings model, ignore them. Do not raise an error.
        extra = "ignore"

settings = Settings()