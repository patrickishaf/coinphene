from telebot.async_telebot import AsyncTeleBot
from db import init_db
from bot import bot as mybot
# from api import run_server
import asyncio
from common.logging import init_file_logging


async def run_app(app: AsyncTeleBot):
    init_db()
    init_file_logging()
    print("bot polling...")
    await app.infinity_polling()


if __name__ == '__main__':
    asyncio.run(run_app(mybot))
