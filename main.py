import asyncio, logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy

from dotenv import dotenv_values

from handlers import handler
from handlers import calendar_callback
from handlers import callback

logging.basicConfig(level=logging.INFO)

config = dotenv_values()
TOKEN = config["TOKEN"]


async def main():
    dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.USER_IN_CHAT)
    bot = Bot(TOKEN, parse_mode="html")

    dp.include_router(handler.router)
    dp.include_router(callback.router)
    dp.include_router(calendar_callback.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())