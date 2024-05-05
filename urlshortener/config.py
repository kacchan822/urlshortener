from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """Configuration values for App"""

    title: str = "URL Shortener API"
    summary: str = "Shortenate URL. This api is under development."
    description: str = ""
    version: str = "0.1.0-dev"
    contact: dict = {
        "namae": "kacchan822",
        "url": "https://github.com/kacchan822/urlshortener",
        "email": "hello@kacchan822.dev",
    }
    license_info: dict = {
        "name": "MIT",
        "url": "https://github.com/kacchan822/urlshortener/blob/main/LICENSE",
    }


class Settings(BaseSettings):
    """Configuration values for Site"""

    model_config = SettingsConfigDict(env_file=".env")

    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./shortener.db"


def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings
