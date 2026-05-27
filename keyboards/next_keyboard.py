from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

next_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➡️ Следующий раздел",
                callback_data="next_section"
            )
        ]
    ]
)