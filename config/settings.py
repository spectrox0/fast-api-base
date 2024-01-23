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
    # Defaults value for env variables if not found the .env file
    db_name: str = "upwork_sample"
    db_password: str = "test"
    db_host: str = "localhost"
    db_port: str = "8000"
    db_driver: str = "postgresql+asyncpg"
    db_user: str = "postgres"
    jwt_secret_key: str = "secret"
    jwt_algorithm: str = "HS256"


settings = Settings()
