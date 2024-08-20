import asyncio
from datetime import datetime, timedelta

from aiogram import Bot
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db import db

bot = Bot("5896262614:AAGIGElR8aK_imHyTvXTWvX1xIVpud7P2_0", parse_mode="html")

scheduler = AsyncIOScheduler(timezone=pytz.timezone("Asia/Almaty"))

summer = datetime(2025, 6, 1)  # news[0]
new_year = datetime(2025, 1, 1)  # news[3]
winter = datetime(2024, 12, 1)  # news[1]
spring = datetime(2025, 3, 1)  # news[2]

summer_id = -1001986872768
new_year_id = -1001986872768
winter_id = -1001986872768
spring_id = -1001986872768


async def send_summer(people: list):
    print("sum", people)
    now = datetime.now() + timedelta(hours=6)
    text = f"🌞До лета осталось {(summer - now).days} дней(день)"

    await bot.send_message(summer_id, text=text)

    for id in people:
        await bot.send_message(id, text=text)


async def send_new_year(people: list):
    print("new", people)
    now = datetime.now() + timedelta(hours=6)
    text = f"🎄До нового года {(new_year - now).days} дней(день)\n"

    await bot.send_message(new_year_id, text=text)

    for id in people:
        await bot.send_message(id, text=text)


async def send_winter(people: list):
    print(people)
    now = datetime.now() + timedelta(hours=6)
    text = f"❄️До зимы {(winter - now).days} дней(день)\n"

    await bot.send_message(winter_id, text=text)

    for id in people:
        await bot.send_message(id, text=text)


async def send_spring(people: list):
    print("spring", people)
    now = datetime.now() + timedelta(hours=6)
    text = f"🌸До весны {(spring - now).days} дней(день)\n"

    await bot.send_message(spring_id, text=text)

    for id in people:
        await bot.send_message(id, text=text)


async def send_newsletter():
    people = db.execute("SELECT * FROM users")

    # db.append_line("users", "news")

    summer_people = []
    winter_people = []
    spring_people = []
    new_year_people = []

    for person in people:
        news = list(map(int, person[3].split()))

        if news[0]:
            summer_people.append(person[0])
        if news[1]:
            winter_people.append(person[0])
        if news[2]:
            spring_people.append(person[0])
        if news[3]:
            new_year_people.append(person[0])

    await send_summer(summer_people)
    await send_spring(spring_people)
    await send_winter(winter_people)
    await send_new_year(new_year_people)

if __name__ == "__main__":
    scheduler.add_job(send_newsletter, 'cron', hour=0, minute=0, end_date='2029-10-13')

    scheduler.start()

    asyncio.get_event_loop().run_forever()