from pydantic_settings import BaseSettings, SettingsConfigDict

INSTALLED_APPS = [
    "fast_zero.users",
    "fast_zero.todos",
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_LIFETIME: int
