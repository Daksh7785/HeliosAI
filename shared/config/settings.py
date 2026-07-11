from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str = "postgresql://helios:password@localhost:5432/heliosai"
    redis_url: str = "redis://localhost:6379/0"
    api_url: str = "http://localhost:8000"
    jwt_secret: str = "super_secret_change_me_in_prod"

    class Config:
        env_prefix = "HELIOS_"
        env_file = ".env"

settings = Settings()
