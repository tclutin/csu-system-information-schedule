import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    database_url: str = os.getenv("DATABASE_URL")

    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN")

settings = Settings()
