import asyncio
from datetime import datetime, timedelta

import pytz
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import settings
from database.model import Notification
from database.postgres import postgres_client
from services.message_service import MessageService


async def fetch_and_send_notifications():
    async for session in postgres_client.session_getter():
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute

        current_day_of_week = now.weekday()
        week_number = now.isocalendar()[1]
        print(current_hour, current_minute)
        current_week_parity = 'odd' if week_number % 2 != 0 else 'even'

        repeating_stmt = select(Notification).where(
            Notification.is_repeating == True,
            func.extract('hour', Notification.time) == current_hour,
            func.extract('minute', Notification.time) == current_minute,
            (Notification.day_of_week == current_day_of_week) | (Notification.day_of_week.is_(None)),
            (Notification.week_parity == current_week_parity) | (Notification.week_parity.is_(None))
        )

        one_time_stmt = select(Notification).where(
            Notification.is_repeating == False,
            func.date_trunc('minute', Notification.date) == func.date_trunc('minute', now)
        )

        # Execute both queries
        repeating_result = await session.execute(repeating_stmt)
        one_time_result = await session.execute(one_time_stmt)

        notifications = repeating_result.scalars().all() + one_time_result.scalars().all()
        print(notifications)

        message_service = MessageService()
        for notification in notifications:
            await message_service.send(notification.tgchat_id, notification.message)


async def main():
    while True:
        now = datetime.now()
        next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)

        sleep_seconds = (next_minute - now).total_seconds()
        print(f"Спим {sleep_seconds} секунд до {next_minute}")

        await asyncio.sleep(sleep_seconds)
        await fetch_and_send_notifications()


if __name__ == "__main__":
    print(settings.telegram_bot_token)
    asyncio.run(main())
