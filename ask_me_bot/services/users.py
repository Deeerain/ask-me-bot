import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from models.users import User


logger = logging.getLogger(__name__.capitalize())


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    try:
        return await session.get_one(User, user_id)
    except NoResultFound:
        return None


async def get_user_by_chat_id(
    session: AsyncSession, chat_id: int
) -> User | None:
    try:
        return await session.get_one(User, chat_id=chat_id)
    except NoResultFound:
        return None


async def get_user_by_tg_id(
    session: AsyncSession, telegram_id: int
) -> User | None:
    try:
        return await session.get_one(User, telegram_id == telegram_id)
    except NoResultFound:
        return None


async def get_or_create_user_by_tg_id(
    session: AsyncSession, telegram_id: int
) -> User:

    user = await get_user_by_tg_id(session, telegram_id=telegram_id)

    if user is None:
        user = await create_user(session, telegram_id)

    return user


async def create_user(
    session: AsyncSession, telegram_id: int, chat_id: int
) -> User:
    user = User(telegram_id=telegram_id, chat_id=chat_id)

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
