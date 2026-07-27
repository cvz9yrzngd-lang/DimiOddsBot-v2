from telegram import ReplyKeyboardMarkup

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        ["📋 Мачове", "➕ Добави"],
        ["❌ Изтрий", "🗑 Изчисти"]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)