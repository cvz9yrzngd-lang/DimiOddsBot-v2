import logging

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from database import (
    add_user,
    add_league,
    get_users,
    get_leagues,
)

from odds_api import get_soccer_leagues


MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        ["📋 Мачове"],
        ["➕ Добави лига"],
    ],
    resize_keyboard=True,
)


class TelegramBot:

    def __init__(self, token):

        self.app = Application.builder().token(token).build()

        self.app.add_handler(CommandHandler("start", self.start))

        self.app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                self.handle_message,
            )
        )

        self.app.add_handler(
            CallbackQueryHandler(self.callback_handler)
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        add_user(update.effective_chat.id)

        logging.info(
            "CHAT ID SAVED: %s",
            update.effective_chat.id,
        )

        await update.message.reply_text(
            "✅ DimiOddsBot е стартиран.",
            reply_markup=MAIN_KEYBOARD,
        )

    async def handle_message(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        text = update.message.text

        if text == "➕ Добави лига":

            leagues = get_soccer_leagues()

            if not leagues:

                await update.message.reply_text(
                    "❌ Не успях да заредя лигите."
                )
                return

            keyboard = [
                [
                    InlineKeyboardButton(
                        league["name"],
                        callback_data=league["key"],
                    )
                ]
                for league in leagues
            ]

            await update.message.reply_text(
                "⚽ Избери лига:",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )

            return

        if text == "📋 Мачове":

            leagues = get_leagues()

            if not leagues:

                await update.message.reply_text(
                    "Няма избрани лиги."
                )

                return

            message = "📋 Следени лиги\n\n"

            for league in leagues:
                message += f"• {league['league_name']}\n"

            await update.message.reply_text(message)

    async def callback_handler(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        query = update.callback_query
        await query.answer()

        leagues = get_soccer_leagues()

        selected = next(
            (
                league
                for league in leagues
                if league["key"] == query.data
            ),
            None,
        )

        if selected is None:

            await query.edit_message_text(
                "❌ Лигата не беше намерена."
            )

            return

        for league in get_leagues():

            if league["league_key"] == selected["key"]:

                await query.edit_message_text(
                    f"ℹ️ {selected['name']} вече се следи."
                )

                return

        add_league(
            selected["key"],
            selected["name"],
        )

        await query.edit_message_text(
            f"✅ Добавена лига:\n\n{selected['name']}"
        )

    async def send_alert(self, text):

        users = get_users()

        logging.info("USERS IN DATABASE: %s", users)

        for chat_id in users:

            try:

                logging.info(
                    "Sending message to %s",
                    chat_id,
                )

                await self.app.bot.send_message(
                    chat_id=chat_id,
                    text=text,
                )

                logging.info("Message sent successfully.")

            except Exception as e:

                logging.exception(e)