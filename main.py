import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, CHECK_INTERVAL
from database import init_db
from monitor import check_matches
from telegram_bot import TelegramBot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def main():

    logging.info("=== BOT START ===")

    init_db()

    bot = TelegramBot(BOT_TOKEN)

    logging.info("Running first odds check...")
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

    logging.info("Scheduler started.")

    await bot.app.initialize()
    await bot.app.start()

    try:

        logging.info("Starting polling...")

        await bot.app.updater.start_polling(
            drop_pending_updates=True
        )

        logging.info("Polling started successfully.")

        while True:
            await asyncio.sleep(3600)

    finally:

        logging.info("Stopping bot...")

        scheduler.shutdown(wait=False)

        await bot.app.updater.stop()
        await bot.app.stop()
        await bot.app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())