import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, CHECK_INTERVAL
from database import init_db
from monitor import check_matches
from telegram_bot import TelegramBot


async def main():

    init_db()

    bot = TelegramBot(BOT_TOKEN)

    # Първа проверка веднага след стартиране
    await check_matches(bot)

    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        check_matches,
        "interval",
        seconds=CHECK_INTERVAL,
        args=[bot],
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()

    await bot.app.initialize()
    await bot.app.start()
    await bot.app.updater.start_polling()

    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        scheduler.shutdown()

        await bot.app.updater.stop()
        await bot.app.stop()
        await bot.app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())