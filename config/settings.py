from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration settings for the application.
    """

    model_config = SettingsConfigDict(
        # Priority of env
        env_file=(".env.production", ".env", ".env.local", ".env.development"),
        env_file_encoding="utf-8",
    )
    db_name: str = "upwork_sample"
    db_password: str = "test"
    db_host: str = "localhost"
    db_port: str = "8000"
    db_driver: str = "postgresql+asyncpg"


settings = Settings()
