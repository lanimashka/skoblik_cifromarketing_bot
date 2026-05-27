import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile
)

from config import BOT_TOKEN

from calculations.numerology import (
    calculate_life_number,
    ENERGY_TEXTS,
    MONEY_TEXTS,
    MARKETING_TEXTS,
    FUTURE_TEXTS
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"


def get_photo(filename: str):
    photo_path = IMAGES_DIR / filename

    if not photo_path.exists():
        raise FileNotFoundError(f"Файл не найден: {photo_path}")

    return FSInputFile(str(photo_path))


start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✨ Начать анализ", callback_data="start_analysis")]
    ]
)

talents_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🌟 Таланты", callback_data="talents_section")]
    ]
)

money_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💸 Деньги и реализация", callback_data="money_section")]
    ]
)

marketing_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📈 Маркетинг по цифрам", callback_data="marketing_section")]
    ]
)

future_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔮 Прогноз на 2026", callback_data="future_section")]
    ]
)

channel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✨ Что еще?", callback_data="channel_section")]
    ]
)

user_data = {}


@dp.message(CommandStart())
async def start(message: Message):
    text = """
Добро пожаловать в пространство цифр, маркетинга, масштабирования и сильной энергии.

Здесь ты сможешь:

✨ узнать свои сильные стороны
✨ понять свои таланты и предназначение
✨ увидеть денежный потенциал
✨ узнать свои точки роста
✨ получить рекомендации для бизнеса и маркетинга
✨ узнать прогноз на 2026 год

Перед началом работы, пожалуйста, ознакомься с документами:

→ Политика конфиденциальности
https://eskoblik.ru/policyskoblik

→ Согласие на обработку персональных данных
https://eskoblik.ru/soglasiepersdann_skoblik

→ Согласие на рассылку
https://eskoblik.ru/soglasyerassylka_skoblik

Нажимая кнопку ниже, ты подтверждаешь согласие с условиями ✨
"""

    await message.answer(text, reply_markup=start_keyboard)


@dp.callback_query(lambda c: c.data == "start_analysis")
async def start_analysis(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "✨ Введи свою дату рождения в формате ДД.ММ.ГГГГ"
    )


@dp.message()
async def get_date(message: Message):
    birth_date = message.text

    try:
        life_number = calculate_life_number(birth_date)

        energy_result = ENERGY_TEXTS[life_number]
        money_result = MONEY_TEXTS[life_number]
        marketing_result = MARKETING_TEXTS[life_number]
        future_result = FUTURE_TEXTS[life_number]

    except Exception:
        await message.answer(
            "❌ Пожалуйста, введи дату в формате ДД.ММ.ГГГГ"
        )
        return

    user_data[message.from_user.id] = {
        "energy": energy_result,
        "money": money_result,
        "marketing": marketing_result,
        "future": future_result
    }

    await message.answer(
        f"""
✨ Твоя дата рождения: {birth_date}

🔮 Анализ уже рассчитывается...

Это может занять несколько секунд 🚀
"""
    )

    await asyncio.sleep(1)

    energy_text = f"""
🌟 Кто ты по энергии

{energy_result}

✨ Это только начало твоего разбора
"""

    await message.answer_photo(
        photo=get_photo("energy.jpg"),
        caption=energy_text,
        reply_markup=talents_keyboard
    )


@dp.callback_query(lambda c: c.data == "talents_section")
async def talents_section(callback: CallbackQuery):
    await callback.answer()

    talents_text = """
🌟 Таланты

У тебя очень сильный потенциал влияния через идеи, знания и личную подачу.

Ты человек, который способен не просто делать что-то для себя, а реально менять мышление и состояние других людей.

Ты умеешь:
— вдохновлять людей
— видеть возможности раньше других
— чувствовать тренды
— создавать сильные идеи
— превращать хаос в систему

Особенно сильно твоя энергия раскрывается через:
— личный бренд
— публичность
— контент
— обучение
— наставничество
— создание собственных проектов

✨ Одна из твоих главных задач — перестать занижать свой масштаб.
"""

    await callback.message.answer_photo(
        photo=get_photo("talents.jpg"),
        caption=talents_text,
        reply_markup=money_keyboard
    )


@dp.callback_query(lambda c: c.data == "money_section")
async def money_section(callback: CallbackQuery):
    await callback.answer()

    money_text = f"""
💸 Деньги и реализация

{user_data[callback.from_user.id]["money"]}

✨ Твои цифры показывают сильный потенциал финансового роста
"""

    await callback.message.answer_photo(
        photo=get_photo("money.jpg"),
        caption=money_text,
        reply_markup=marketing_keyboard
    )


@dp.callback_query(lambda c: c.data == "marketing_section")
async def marketing_section(callback: CallbackQuery):
    await callback.answer()

    marketing_text = f"""
📈 Маркетинг по твоим цифрам

{user_data[callback.from_user.id]["marketing"]}

🚀 Именно такая стратегия будет раскрываться у тебя сильнее всего
"""

    await callback.message.answer_photo(
        photo=get_photo("marketing.jpg"),
        caption=marketing_text,
        reply_markup=future_keyboard
    )


@dp.callback_query(lambda c: c.data == "future_section")
async def future_section(callback: CallbackQuery):
    await callback.answer()

    future_text = f"""
🔮 Прогноз на 2026 год

{user_data[callback.from_user.id]["future"]}

✨ Этот период может очень сильно изменить твой уровень жизни
"""

    await callback.message.answer_photo(
        photo=get_photo("future.jpg"),
        caption=future_text,
        reply_markup=channel_keyboard
    )


@dp.callback_query(lambda c: c.data == "channel_section")
async def channel_section(callback: CallbackQuery):
    await callback.answer()

    channel_text = """
💜 Если тебе откликнулся этот разбор — буду рада видеть тебя в Telegram-канале Екатерины Скоблик 🚀

https://t.me/skoblikmarketing

Там тебя ждут:
— маркетинг
— нейросети
— продвижение
— продажи
— Reels
— сильные разборы
— полезные инструменты
— рабочие схемы и стратегии

Это пространство для тех, кто хочет расти, масштабироваться и идти в сильное проявление ✨

И да… это будет лучшая благодарность за разбор 💜
"""

    await callback.message.answer_photo(
        photo=get_photo("thanks.jpg"),
        caption=channel_text
    )

    await callback.message.answer(
        """
✨ Буду рада твоим отметкам в сторис и социальных сетях.

Отмечай меня и мои блоги — мне будет очень приятно видеть твои впечатления от разбора и твои результаты 🚀💜
"""
    )


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())