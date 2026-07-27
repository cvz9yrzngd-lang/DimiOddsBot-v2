Application,
    CommandHandler,
    ContextTypes,
)

from database import add_user


class TelegramBot:

    def __init__(self, token):
        self.app = Application.builder().token(token).build()

        self.app.add_handler(
            CommandHandler("start", self.start)
        )

    async def start(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        add_user(update.effective_chat.id)

        await update.message.reply_text(
            "✅ DimiOddsBot v2 е стартиран."
        )

    async def send_alert(self, text):

        from database import get_users
