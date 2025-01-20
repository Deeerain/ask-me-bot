import logging

from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart
from aiogram.utils.deep_linking import create_start_link

from db.session import AsyncSession
from services import users as user_service
from keyboards.general import start_keyboard, cancel_keyboard


logger = logging.getLogger(__name__)

router = Router(name=__name__)


class SendAnonMessageStateGroup(StatesGroup):
    message = State()


@router.message(SendAnonMessageStateGroup.message)
async def send_anon_message_handler(
    message: Message, state: FSMContext, bot: Bot, session: AsyncSession
):
    target_id = (await state.get_data()).get("target_id")

    async with session:
        user = await user_service.get_user_by_tg_id(
            session, message.from_user.id
        )
        if user is None:
            await user_service.create_user(
                session, message.from_user.id, message.chat.id
            )

        target = await user_service.get_user_by_tg_id(session, target_id)

    await message.answer(f"Сообщение отправлено!\n{message.text}")
    await start_command_handler(message, bot, state, session)
    await bot.send_message(
        text=f"Получено сообщение!\n\n{message.text}", chat_id=target.chat_id
    )
    await state.clear()


@router.message(CommandStart(deep_link=True))
async def start_command_handler(
    message: Message, state: FSMContext, command, session: AsyncSession
) -> None:

    await message.delete()

    async with session:
        user = await user_service.get_user_by_tg_id(
            session, message.from_user.id
        )
        if user is None:
            await user_service.create_user(
                session, message.from_user.id, message.chat.id
            )

        target_user = await user_service.get_user_by_tg_id(
            session, int(command.args)
        )

    logger.debug(f"Anon message target {target_user.telegram_id=}")

    await state.set_state(SendAnonMessageStateGroup.message)
    await state.set_data({"target_id": target_user.id})

    await message.answer(
        "Напиши сюда сообщение и оно отправится человеку,"
        " который запостил ссылку",
        reply_markup=cancel_keyboard.as_markup(),
    )


@router.message(CommandStart())
@router.message()
async def start_command_handler_main(
    message: Message, bot: Bot, state: FSMContext, session: AsyncSession
) -> None:

    await state.clear()

    async with session:
        user = await user_service.get_user_by_tg_id(
            session, message.from_user.id
        )
        if user is None:
            user_service.create_user(
                session, message.from_user.id, message.chat.id
            )

    deep_link = await create_start_link(bot, message.from_user.id)

    logger.debug(f"Returned user {user=}")

    await message.answer(
        "Получай анонимные сообщени от знакомых\n\nВот твоя"
        f" персональная ссылка:\n {deep_link} \n\nЗакрепи ссылку"
        " в своих соц. сетях и получай анонимные сообщения",
        reply_markup=start_keyboard.as_markup(),
    )


@router.callback_query()
async def callback_handler(
    callback_query: CallbackQuery, state: FSMContext
):
    logger.debug(f"Handle callback {callback_query=} \n{state=}\n")

    match callback_query.data:
        case "cancel":
            await state.clear()
            await callback_query.message.delete()
