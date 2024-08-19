from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


async def menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.button(
        text="До",
        callback_data="do"
    )

    kb.button(
        text="Узнать расстояние",
        callback_data="distance"
    )

    kb.adjust(1)
    return kb.as_markup()


async def back() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.button(
        text="🔙Назад",
        callback_data="menu"
    )

    return kb.as_markup()
