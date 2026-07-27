from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from database import add_user, get_users, get_leagues
from keyboards import MAIN_KEYBOARD
from odds_api import get_soccer_leagues


class TelegramBot:
    def __init__(self, token):
        self.app = Application.builder().token(token).build()

        self.app.add_handler(
            CommandHandler("start", self.start)
        )

        self.app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                self.handle_message,
            )
        )

    async def start(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):
        add_user(update.effective_chat.id)

        await update.message.reply_text(
            "✅ DimiOddsBot v2 е стартиран.",
            reply_markup=MAIN_KEYBOARD,
        )

    async def handle_message(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):
        text = update.message.text

        if text == "📋 Мачове":

            leagues = get_leagues()

            if not leagues:
                await update.message.reply_text(
                    "Няма добавени лиги."
                )
                return

            message = "📋 Следени лиги:\n\n"

            for league in leagues:
                message += f"• {league['league_name']}\n"

            await update.message.reply_text(message)
            return

        if text == "➕ Добави":

            leagues = get_soccer_leagues()

            if not leagues:
                await update.message.reply_text(
                    "Не успях да заредя лигите."
                )
                return

            message = "⚽ Налични лиги:\n\n"

            for league in leagues:
                message += (
                    f"{league['key']}\n"
                    f"{league['name']}\n\n"
                )

            await update.message.reply_text(message)
            return

        if text == "❌ Изтрий":
            await update.message.reply_text(
                "Функцията ще бъде добавена в следващата стъпка."
            )
            return

        if text == "🗑 Изчисти":
            await update.message.reply_text(
                "Функцията ще бъде добавена в следващата стъпка."
            )
            return

    async def send_alert(self, text):
        for chat_id in get_users():
            try:
                await self.app.bot.send_message(
                    chat_id=chat_id,
                    text=text,
                )
            except Exception:
                pass