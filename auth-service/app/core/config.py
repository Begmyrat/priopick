from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database connection string
    DATABASE_URL: str

    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    ENVIRONMENT: str = "development"

    class Config:
        # Tell Pydantic where to find the .env file
        env_file = ".env"

settings = Settings()