import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.db.orm import AsyncOrm
from bot.db.engine import async_session
from bot.handlers import admin_handlers, user_handlers, pagination_handlers, calculator_handlers, help_hanlders
from bot.middleware.database import DataBaseSession

from config.config_reader import config

storage = MemoryStorage()


bot = Bot(token=config.bot_token.get_secret_value())


async def on_startup(bot):
    await AsyncOrm.create_db()

async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding="utf-8",
        handlers=[
            logging.FileHandler('logs.log', mode='a', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    dp = Dispatcher(storage=storage)
    
    dp.startup.register(on_startup)

    dp.update.middleware(DataBaseSession(session_pool=async_session))

    dp.include_routers(
        admin_handlers.router,
        user_handlers.router,
        pagination_handlers.router,
        calculator_handlers.router,
        help_hanlders.router
        )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


