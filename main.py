import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_reader import config
from handlers import user_handlers,pagination_handlers,calculator_handlers,help_hanlders

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())

async def main():
    dp = Dispatcher(storage=storage)
    dp.include_router(user_handlers.router)
    dp.include_router(pagination_handlers.router)
    dp.include_router(calculator_handlers.router)
    dp.include_router(help_hanlders.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


