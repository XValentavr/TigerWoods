"""
This module show all posible trainings
"""
import datetime

from aiogram import types

from golfbot import golf_db
from golfbot.golf_bot import posts_cb


async def trainings_handler(message, bot, admins: list, months: dict, days: dict):
    """
    This function show all trainings that is in database. If not trainings, then show None
    :param message: bot message chat id
    :param bot: bot API token
    :param admins: list of admins
    :param months: dic of month
    :param days: dict of days
    :return: None
    """
    base = """🏐 {}
🗓 {} {} ({}) {} — збір
📡 {}
    
💵 Передплата {} грн.
    
📋 {} {}"""

    trains = golf_db.golf_train()
    if trains:
        for i in trains:
            markup = types.InlineKeyboardMarkup()
            if i[9] - len(eval(i[11])) > 0:
                if message.chat.id == -1001126968735:
                    b = types.InlineKeyboardButton(
                        text="Зареєструватися",
                        url="https://t.me/Sportgolf_bot?start=golf",
                    )
                    markup.add(b)
                else:
                    if message.chat.id in eval(i[11]):
                        c = types.InlineKeyboardButton(
                            text="Скасувати запис",
                            callback_data=posts_cb.new(
                                action="cancel", id=i[0], sum=0, quant=0
                            ),
                        )
                        markup.add(c)
                    else:
                        b = types.InlineKeyboardButton(
                            text="Зареєструватися",
                            callback_data=posts_cb.new(
                                action="pay", id=i[0], sum=i[8], quant=0
                            ),
                        )

                        markup.add(b)
            else:
                if message.chat.id in eval(i[11]):
                    c = types.InlineKeyboardButton(
                        text="Скасувати запис",
                        callback_data=posts_cb.new(
                            action="cancel", id=i[0], sum=0, quant=0
                        ),
                    )
                    markup.add(c)
                else:
                    b = types.InlineKeyboardButton(
                        text="Місць немає!",
                        callback_data=posts_cb.new(
                            action="111111111", id=i[0], sum=i[8], quant=0
                        ),
                    )
                    markup.add(b)
            b = types.InlineKeyboardButton(
                text="Показати розташування",
                callback_data=posts_cb.new(
                    action="location", id=i[0], sum=i[8], quant=0
                ),
            )

            markup.add(b)
            if int(message.chat.id) in admins:
                b = types.InlineKeyboardButton(
                    text="Видалити ❌",
                    callback_data=posts_cb.new(
                        action="delete", id=i[0], sum=i[8], quant=0
                    ),
                )

                c = types.InlineKeyboardButton(
                    text="-",
                    callback_data=posts_cb.new(
                        action="minus", id=i[0], sum=i[8], quant=0
                    ),
                )
                x = types.InlineKeyboardButton(
                    text="+",
                    callback_data=posts_cb.new(
                        action="plus", id=i[0], sum=i[8], quant=0
                    ),
                )
                markup.add(b, c, x)

            date = datetime.datetime.strptime(i[2], "%d.%m.%Y")
            users = eval(i[10])
            usrs = ": "
            if users:
                for z, l in enumerate(users):
                    k = eval(l)
                    if usrs == ": ":
                        usrs += f"""<a href="tg://user?id={k['id']}">{k['name']}</a> """
                    else:
                        usrs += (
                            f""", <a href="tg://user?id={k['id']}">{k['name']}</a>"""
                        )

                if i[9] - len(users) == 0:
                    await bot.send_message(
                        message.chat.id,
                        base.format(
                            i[4],
                            date.day,
                            months[date.month],
                            days[date.weekday()],
                            i[3],
                            i[5],
                            i[8],
                            "Місць немає",
                            usrs,
                        ),
                        parse_mode="HTML",
                        reply_markup=markup,
                        disable_web_page_preview=True,
                    )
                else:
                    await bot.send_message(
                        message.chat.id,
                        base.format(
                            i[4],
                            date.day,
                            months[date.month],
                            days[date.weekday()],
                            i[3],
                            i[5],
                            i[8],
                            str(i[9] - len(users)) + " місць",
                            usrs,
                        ),
                        parse_mode="HTML",
                        reply_markup=markup,
                        disable_web_page_preview=True,
                    )

            else:
                await bot.send_message(
                    message.chat.id,
                    base.format(
                        i[4],
                        date.day,
                        months[date.month],
                        days[date.weekday()],
                        i[3],
                        i[5],
                        i[8],
                        str(i[9] - len(users)) + " місць",
                        "",
                    ),
                    parse_mode="HTML",
                    reply_markup=markup,
                    disable_web_page_preview=True,
                )
    else:
        await bot.send_message(
            message.chat.id, f"""Немає тренувань""", parse_mode="HTML"
        )
