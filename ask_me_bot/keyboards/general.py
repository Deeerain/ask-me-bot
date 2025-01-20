from aiogram.utils.keyboard import InlineKeyboardBuilder


start_keyboard = InlineKeyboardBuilder()
start_keyboard.button(text="Изменить ссылку", callback_data="change_link")


cancel_keyboard = InlineKeyboardBuilder()
cancel_keyboard.button(text="Отмена", callback_data="cancel")
