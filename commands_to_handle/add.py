"""
This module works with add command
"""
import datetime

import pytz
from aiogram import types

from golfbot.golf_bot import set_step


async def add_handle(message, bot, admins: list, data: dict):
    """
    This function allows to add new training if user is admin
    :param message: message chaat id
    :param bot: bot API token
    :param admins: lists of admins
    :param data: admins information
    :return: None
    """
    if message.chat.id in admins:
        ll = []
        data["add"] = {}
        set_step(message.chat.id, "add_1")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(9):
            ll.append(
                (
                        datetime.datetime.now(pytz.timezone("Europe/Kiev"))
                        + datetime.timedelta(i)
                ).strftime("%d.%m.%Y")
            )
            if len(ll) == 3:
                markup.row(ll[0], ll[1], ll[2])
                ll = []
        await bot.send_message(
            message.chat.id,
            f"""Виберіть дату тренування:""",
            parse_mode="HTML",
            reply_markup=markup,
        )
    else:
        await bot.send_message(
            message.chat.id, f"""Ви не адміністратор""", parse_mode="HTML"
        )
