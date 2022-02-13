"""
This moodule create funcion to add trainin
"""
import datetime

from aiogram import types

from golfbot.trainings import trainings_handler
from golfbot import golf_db
from golfbot.golf_bot import get_step, set_step
from golfbot.golf_bot import days, months, admins


async def add_training_handler(message, bot, data: dict, typs: dict, typ: str):
    """
    This module handle add command to add new trainings
    :param message: message bot chat
    :param bot: bot API token
    :param data: dict of data
    :param typs: dict
    :param typ: dict
    :return:
    """
    if get_step(message.chat.id) == "add_1":
        data["add"]["date"] = message.text
        markup = types.ReplyKeyboardRemove()
        set_step(message.chat.id, "add_2")
        await bot.send_message(
            message.chat.id,
            f"""Введіть час в форматі ГГ:ХХ """,
            parse_mode="HTML",
            reply_markup=markup,
        )
    elif get_step(message.chat.id) == "add_2":
        data["add"]["time"] = message.text
        set_step(message.chat.id, "add_3_1")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("Тренування", "Двосторонка")
        await bot.send_message(
            message.chat.id,
            f"""Виберіть або введіть тип тренування""",
            parse_mode="HTML",
            reply_markup=markup,
        )
    elif get_step(message.chat.id) == "add_3_1":
        typs["1"] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("Пляж", "Зал")
        set_step(message.chat.id, "add_3_2")
        await bot.send_message(
            message.chat.id,
            f"""Виберіть або введіть місце тренування""",
            parse_mode="HTML",
            reply_markup=markup,
        )
    elif get_step(message.chat.id) == "add_3_2":
        typs["2"] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("Пісок", "Паркет")
        set_step(message.chat.id, "add_3")
        await bot.send_message(
            message.chat.id,
            f"""Виберіть або введіть тип покриття""",
            parse_mode="HTML",
            reply_markup=markup,
        )
    elif get_step(message.chat.id) == "add_3":
        typs["3"] = message.text
        data["add"]["type"] = typ.format(typs["1"], typs["2"], typs["3"])
        set_step(message.chat.id, "add_4")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(
            "Kozyn GC",
            "Equides",
            "Golfstream",
        )
        await bot.send_message(
            message.chat.id,
            f"""Виберіть або введіть місце тренування""",
            parse_mode="HTML",
            reply_markup=markup,
        )
    elif get_step(message.chat.id) == "add_4":
        if message.text == "Kozyn GC":
            data["add"]["place"] = "Kozyn GC"
            data["add"]["latitude"] = "50.499389"
            data["add"]["longitude"] = "30.545220"
        elif message.text == "Equides":
            data["add"]["place"] = "Equides"
            data["add"]["latitude"] = "50.437975"
            data["add"]["longitude"] = "30.147740"
        elif message.text == "Golfstream":
            data["add"]["place"] = "Golfstream"
            data["add"]["latitude"] = "50.450811"
            data["add"]["longitude"] = "30.577949"

        set_step(message.chat.id, "add_5")
        await bot.send_message(
            message.chat.id, f"""Введіть ціну за тренування""", parse_mode="HTML"
        )
    elif get_step(message.chat.id) == "add_5":
        data["add"]["price"] = message.text
        set_step(message.chat.id, "add_6")
        await bot.send_message(
            message.chat.id, f"""Введіть к-ть місць""", parse_mode="HTML"
        )
    elif get_step(message.chat.id) == "add_6":
        data["add"]["quant"] = message.text
        golf_db.add_golf_train(
            datetime.datetime.strptime(
                f"{data['add']['date']} {data['add']['time']}", "%d.%m.%Y %H:%M"
            ).strftime("%Y-%m-%d %H:%M"),
            data["add"]["date"],
            data["add"]["time"],
            data["add"]["type"],
            data["add"]["place"],
            data["add"]["latitude"],
            data["add"]["longitude"],
            data["add"]["price"],
            data["add"]["quant"],
        )
        set_step(message.chat.id, 1)
        await bot.send_message(message.chat.id, f"""Додано /start""", parse_mode="HTML")

    elif message.text == "Тренування":
        await trainings_handler(message, bot, admins, months, days)

    elif message.text == "Info":
        await bot.send_message(
            message.chat.id,
            f"""<b>Тренування</b>
        - Для того, щоб подивитися список тренувань потрібно натиснути кнопку або написати слово "тренування".
        - В повідомленнях ви отримаєте перелік доступних тренувань.
        - Для оплати місця потрібно натиснути  кнопку "Зареєструватися".
        - Після чого, бот попросить провести оплату. У разі успішної оплати, місце буде заброньовано за вами. 
        - Щоб скасувати бронювання - натисніть відповідну кнопку.
        - Проводити операції по оплаті тренування можна в боті не виходячи з Телеграм

        Бот для запису на тренування з гри в Гольф.

        Контакти:
        Демков Денис 
        Email: denis@demkov.me
        Mob: +380981540900""",
            parse_mode="HTML",
        )
