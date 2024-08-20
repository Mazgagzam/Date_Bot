from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram import Router

from keyboards.other_kb import menu_kb
from middleware.register import Register

router = Router()
router.message.middleware(Register())


@router.message(Command('start'), StateFilter(None))
async def start(message: Message, user):
    await message.answer(
        f"Привет {user.name}!\nЯ могу рассчитать расстояние между днями. Чтобы продолжить напиши /menu")


@router.message(Command("menu"), StateFilter(None))
async def start(message: Message):
    await message.answer(
        text="Меню",
        reply_markup=await menu_kb()
    )


@router.message()
async def else_message(message: Message):
    await message.delete()