from aiogram.types import CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from datetime import datetime, timedelta

from get_distance import get_distance
from middleware.register import Register
from keyboards.other_kb import menu_kb, back
from keyboards.calendar_kb import calendar_kb
from states.state import GetDates

router = Router()
router.callback_query.filter(StateFilter(None))
router.callback_query.middleware(Register())


@router.callback_query(F.data == "menu")
async def menu_callback(call: CallbackQuery):
    await call.message.edit_text(
        text="Меню",
        reply_markup=await menu_kb()
    )


@router.callback_query(F.data == "do")
async def until_dates(call: CallbackQuery):
    now = datetime.now()
    now += timedelta(hours=5)

    new_year = datetime(2025, 1, 1)
    winter = datetime(2024, 12, 1)
    spring = datetime(2025, 3, 1)
    summer = datetime(2025, 6, 1)

    await call.message.edit_text(
        text=f"❄️До зимы {(winter-now).days} дней(день)\n"
             f"🎄До нового года {(new_year-now).days} дней(день)\n"
             f"🌸До весны {(spring-now).days} дней(день)\n"
             f"🌞До лета {(summer-now).days} дней(день)",
        reply_markup=await back()
    )


@router.callback_query(F.data == "distance")
async def distance_callback(call: CallbackQuery, state: FSMContext):
    date = datetime.now()
    await call.message.edit_text(
        text="Выберете день",
        reply_markup=await calendar_kb(date.year, date.month)
    )

    await state.set_state(GetDates.date1)