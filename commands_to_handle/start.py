from aiogram import types

from golfbot import golf_db
from golfbot.golf_bot import set_step, data, training


async def start_handle(message, bot):
    """
    This module handle start command
    :param message: bot chat identifier
    :param bot: bot API token
    :return:
    """
    if golf_db.is_golf_user(message.chat.id):
        pass
    else:
        golf_db.add_golf_user(
            message.chat.id, message.chat.first_name, message.chat.username
        )
    if len(message.text) > 10:
        await training(message)
    else:
        data[str(f"{message.chat.id}")] = {}
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("Тренування", "Info")
        set_step(message.chat.id, 1)
        await bot.send_message(
            message.chat.id,
            f"""Привіт, <b>{message.chat.first_name}</b>""",
            parse_mode="HTML",
            reply_markup=markup,
        )
