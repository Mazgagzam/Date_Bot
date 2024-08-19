import asyncio, logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy

from handlers import handler
from handlers import calendar_callback
from handlers import callback

logging.basicConfig(level=logging.INFO)


async def main():
    dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.USER_IN_CHAT)
    TOKEN = "5896262614:AAGIGElR8aK_imHyTvXTWvX1xIVpud7P2_0"  # "5340042795:AAEqEsQr3qcDctstc-Ui982oggyiQT2jB_g" "5896262614:AAGIGElR8aK_imHyTvXTWvX1xIVpud7P2_0"
    bot = Bot(TOKEN, parse_mode="html")
  #  await bot.send_video(2028784660, "BAACAglAAxkBAAIU_GSTL-dC4S9oHYNo5KSZK30ah3DCAAJ1NAACc3CYSK3g6dmS0fyNLwQ")

    dp.include_router(handler.router)
    dp.include_router(callback.router)
    dp.include_router(calendar_callback.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
