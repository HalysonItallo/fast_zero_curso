from pydantic_settings import BaseSettings, SettingsConfigDict

INSTALLED_APPS = [
    "fast_zero.users",
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
