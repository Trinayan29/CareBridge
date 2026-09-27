import os
from dotenv import load_dotenv

load_dotenv()


def _as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Settings:
    APP_NAME = os.getenv("APP_NAME", "CareBridge API")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DEBUG = _as_bool(os.getenv("DEBUG", "true"))
    DATABASE_URL = os.getenv("DATABASE_URL")

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "change-this-in-production"
    )
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    BOB_API_KEY = os.getenv("BOB_API_KEY")
    BOB_API_URL = os.getenv(
        "BOB_API_URL",
        "https://api.us-east.bob.ibm.com/inference/v1/chat/completions"
    )

    BOB_MODEL = os.getenv("BOB_MODEL", "premium")


settings = Settings()