import asyncio
import logging

from aiogram import Bot, Dispatcher, Router

from config import settings
from db import create_session
from handlers.general import router


logger = logging.getLogger(__name__)


async def init_dispatcher(*routers: Router, **depends) -> Dispatcher:
    logger.info(f'Init bot {settings=}"')

    logger.info(f"Init depends {depends=}")
    dp = Dispatcher(**depends)

    logger.info(f"Init routers {routers}")
    dp.include_routers(*routers)

    return dp


async def main():
    routers = [
        router,
    ]

    depends = {"session": await create_session()}

    bot = Bot(settings.BOT_TOKEN)
    dp = await init_dispatcher(*routers, **depends)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] : %(message)s",
    )

    asyncio.run(main())
