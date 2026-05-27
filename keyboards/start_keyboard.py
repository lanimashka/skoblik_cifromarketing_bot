from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✨ Начать анализ")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)