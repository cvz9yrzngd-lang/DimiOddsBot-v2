from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from database import add_user, get_users
from keyboards import MAIN_KEYBOARD


class TelegramBot:
    def __init__(self, token):
        self.app = Application.builder().token(token).build()

        self.app.add_handler(
            CommandHandler("start", self.start)
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

    async def send_alert(self, text):
        for chat_id in get_users():
            try:
                await self.app.bot.send_message(
                    chat_id=chat_id,
                    text=text,
                )
            except Exception:
                pass