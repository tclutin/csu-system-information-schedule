import httpx

from config.config import settings


class MessageService:
    def __init__(self):
        pass

    async def send(self, tgchat_id: int, message: str):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage?chat_id={tgchat_id}&text={message}")
                response.raise_for_status()
                body = response.json()
                return body
            except Exception:
                raise ValueError("TELEGRAM_SERVICE: я чуток откис, ты там это.. держись")