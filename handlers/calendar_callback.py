from datetime import datetime

from aiogram.types import CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from get_distance import get_distance
from states.state import GetDates
from middleware.register import Register
from keyboards.other_kb import back
from keyboards.calendar_kb import months_kb, calendar_kb, Zoom, Next, Else, years_kb
from keyboards.calendar_kb import Year, Month, Day

router = Router()
router.callback_query.middleware(Register())


@router.callback_query(Next.filter())
async def next_callback(call: CallbackQuery, callback_data: Next):
    await call.message.edit_reply_markup(reply_markup=await calendar_kb(callback_data.year, callback_data.month))


@router.callback_query(Day.filter(), GetDates.date1)
async def day1_callback(call: CallbackQuery, callback_data: Day, state: FSMContext):
    date = datetime.now()
    date1 = datetime(callback_data.year, callback_data.month, callback_data.day)

    await call.message.edit_text(
        text=f"Первая датa: {date1.strftime('%d.%m.%Y')}\nВыберете вторую дату",
        reply_markup=await calendar_kb(date.year, date.month)
    )

    await state.update_data(date1=date1)
    await state.set_state(GetDates.date2)


@router.callback_query(Day.filter(), GetDates.date2)
async def day2_callback(call: CallbackQuery, callback_data: Day, state: FSMContext):
    date1 = (await state.get_data())["date1"]
    date2 = datetime(callback_data.year, callback_data.month, callback_data.day)

    date1, date2 = max(date1, date2), min(date1, date2)
    date = await get_distance(date1, date2)

    date_str = f"{f'{date.years} год(лет) ' if date.years != 0 else ''}{f'{date.months} месяц(месяцев) ' if date.months != 0 else ''}{f'{date.days} день(дней)' if date.days != 0 else ''}"

    await call.message.edit_text(
        text=f"Расстояние между {date2.strftime('%d.%m.%Y')} и {date1.strftime('%d.%m.%Y')}\n{date_str}",
        reply_markup=await back()
    )

    await state.clear()


@router.callback_query(Year.filter())
@router.callback_query(Zoom.filter(F.type == "month"))
async def zoom_month_callback(call: CallbackQuery, callback_data: Zoom):
    await call.message.edit_text(text="Выберете месяц",
                                 reply_markup=await months_kb(callback_data.year))


@router.callback_query(Zoom.filter(F.type == "year"))
async def zoom_year_callback(call: CallbackQuery, callback_data: Zoom):
    await call.message.edit_text(text="Выберете год",
                                 reply_markup=await years_kb(callback_data.year))


@router.callback_query(Month.filter())
async def month_callback(call: CallbackQuery, callback_data: Month):
    await call.message.edit_text(text="Выберете день",
                                 reply_markup=await calendar_kb(callback_data.year, callback_data.month))


@router.callback_query(Else.filter())
async def else_callback(call: CallbackQuery, callback_data: Else):
    await call.answer(text=callback_data.text, show_alert=True)


@router.callback_query(lambda call: call.data[:4] == 'pass')
async def pass_callback(call: CallbackQuery):
    await call.answer(text="Пусто")
