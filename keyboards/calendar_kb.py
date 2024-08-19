import calendar

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData


class Year(CallbackData, prefix="year"):
    year: int


class Month(CallbackData, prefix="month"):
    year: int
    month: int


class Day(CallbackData, prefix="calendar"):
    day: int
    month: int
    year: int


class Zoom(CallbackData, prefix='zoom'):
    type: str
    year: int

class Next(CallbackData, prefix='next'):
    month: int
    year: int


class Else(CallbackData, prefix="else"):
    text: str


# calendar.monthcalendar(2020, 7)

months = "Январь Февраль Март Апрель Май Июнь Июль Август Сентябрь Октябрь Ноябрь Декабрь".split()
week = "ПН ВТ СР ЧТ ПТ СБ ВС".split()
week2 = "Понедельник Вторник Среда Четверг Пятница Суббота Воскресенье".split()


async def calendar_kb(year: int, month: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=f"{months[month - 1]} {year}",
              callback_data=Zoom(type="month", year=year))

    for day in week:
        kb.button(
            text=day,
            callback_data=Else(text=week2[week.index(day)])
        )

    month_now = calendar.monthcalendar(year, month)

    for line in month_now:
        for day in line:
            if day == 0:
                kb.button(
                    text=' ',
                    callback_data=f'pass:{month_now.index(line)}:{line.index(day)}'
                )
            else:
                kb.button(
                    text=str(day),
                    callback_data=Day(day=day, month=month, year=year)
                )

    if month - 1 < 1:
        month2 = 12
        year2 = year - 1
    else:
        month2 = month - 1
        year2 = year

    kb.button(
        text='️⬅️',
        callback_data=Next(month=month2, year=year2)
    )

    if month + 1 > 12:
        month2 = 1
        year2 += 1
    else:
        month2 = month + 1
        year2 = year

    kb.button(
        text='➡️',
        callback_data=Next(month=month2, year=year2)
    )
    kb.adjust(1, 7)

    return kb.as_markup()


async def months_kb(year):
    kb = InlineKeyboardBuilder()

    kb.button(
        text=f'{year} год',
        callback_data=Zoom(type="year",year=year)
    )

    for month in months:
        kb.button(text=month, callback_data=Month(year=year, month=months.index(month) + 1))

    kb.adjust(1, 3)

    return kb.as_markup()


async def years_kb(main_year: int):
    kb = InlineKeyboardBuilder()

    for year in range(main_year - 4, main_year + 5):
        kb.button(text=str(year), callback_data=Year(year=year))

    kb.adjust(3)
    return kb.as_markup()
