try:
    from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover - fallback for Pydantic v1
    from pydantic import BaseSettings

    SettingsConfigDict = dict


class Settings(BaseSettings):
    APP_NAME: str = "CareBridge API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    if SettingsConfigDict is not dict:
        model_config = SettingsConfigDict(
            env_file=".env",
            extra="ignore",
        )
    else:
        class Config:
            env_file = ".env"
            extra = "ignore"


settings = Settings()