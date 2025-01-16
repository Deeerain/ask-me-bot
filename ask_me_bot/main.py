import asyncio

from aiogram import Bot, Dispatcher

from .config import settings


async def main():
    bot = Bot(settings.BOT_TOKEN)
    dp = Dispatcher(bot)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
