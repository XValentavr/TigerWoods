import ast
import datetime
import string

from aiogram import types

from golfbot import golf_db
from golfbot.golf_bot import posts_cb
from golfbot.golf_bot import days, months, admins


async def pay_for_training(bot, query: types.CallbackQuery, callback_data: dict, data: dict):
    """
    This module allows to pay using liqpay token
    :param bot: bot API token
    :param query: qury handler
    :param callback_data: dict of call
    :param data: dict of data
    :return: None
    """
    callback_data_action = callback_data["action"]
    callback_data_id = callback_data["id"]
    callback_data_sum = callback_data["sum"]
    if callback_data_action == "pay":
        prices = [types.LabeledPrice("Оплата тренування", int(callback_data_sum) * 100)]
        data[str(f"{query.message.chat.id}")] = {}
        data[str(f"{query.message.chat.id}")][
            "payload"
        ] = f"training_{callback_data_id}"
        data[str(f"{query.message.chat.id}")]["id"] = callback_data_id
        await bot.send_invoice(
            query.message.chat.id,
            start_parameter="time-machine-example",
            title="Оплата за тренування",
            description="Оплата за тренування",
            payload=f"training_{callback_data_id}",
            provider_token="635983351:LIVE:i75647872815",
            currency="UAH",
            prices=prices,
            is_flexible=False,
        )
    if callback_data_action == "cancel":
        await bot.delete_message(
            message_id=query.message.message_id, chat_id=query.message.chat.id
        )
        first = ""
        username = ""
        if query.message.chat.first_name:
            first = query.message.chat.first_name

        if query.message.chat.username:
            username = query.message.chat.username
        printable = set(
            string.printable
            + "АаБбВвГгДдЕеЁёЖжЗзІіЇїИиЙйКкЛлМмНнОоПпСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"
        )
        golf_db.cancel_golf_sign(
            callback_data_id,
            query.message.chat.id,
            "".join(filter(lambda x: x in printable, first)),
            username,
        )
        await bot.answer_callback_query(
            query.id, "Ви успішно скасували запис", show_alert=True
        )

    if callback_data_action == "delete":
        await bot.delete_message(
            message_id=query.message.message_id, chat_id=query.message.chat.id
        )
        golf_db.delete_train(callback_data_id)
        await bot.answer_callback_query(query.id, "Видалено", show_alert=False)
    if callback_data_action == "minus":
        golf_db.minus(callback_data_id)
        i = golf_db.golf_train_id(callback_data_id)
        base = """🏐 {}
🗓 {} {} ({}) {} — збір 
📡 {}
    
💵 Передплата {} грн.
    
📋 {} {}"""
        markup = types.InlineKeyboardMarkup()
        if i[9] - len(eval(i[11])) > 0:
            if str(query.message.chat.id) in eval(i[11]):
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
            if str(query.message.chat.id) in eval(i[11]):
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
            callback_data=posts_cb.new(action="location", id=i[0], sum=i[8], quant=0),
        )

        markup.add(b)
        if int(query.message.chat.id) in admins:
            b = types.InlineKeyboardButton(
                text="Видалити ❌",
                callback_data=posts_cb.new(action="delete", id=i[0], sum=i[8], quant=0),
            )

            c = types.InlineKeyboardButton(
                text="-",
                callback_data=posts_cb.new(action="minus", id=i[0], sum=i[8], quant=0),
            )
            x = types.InlineKeyboardButton(
                text="+",
                callback_data=posts_cb.new(action="plus", id=i[0], sum=i[8], quant=0),
            )

            markup.add(b, c, x)
        date = datetime.datetime.strptime(i[2], "%d.%m.%Y")
        users = eval(i[10])
        usrs = ": "
        if users:
            for z, l in enumerate(users):
                k = eval(l)
                if usrs == ": ":
                    usrs += f'<a href="tg://user?id={k["id"]}">{k["name"]}</a> '
                else:
                    usrs += f', <a href="tg://user?id={k["id"]}">{k["name"]}</a>'
            if i[9] - len(eval(i[11])) == 0:
                await bot.edit_message_text(
                    chat_id=query.message.chat.id,
                    message_id=query.message.message_id,
                    text=base.format(
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
                    reply_markup=markup,
                )

            else:
                await bot.edit_message_text(
                    chat_id=query.message.chat.id,
                    message_id=query.message.message_id,
                    text=base.format(
                        i[4],
                        date.day,
                        months[date.month],
                        days[date.weekday()],
                        i[3],
                        i[5],
                        i[8],
                        str(i[9] - len(eval(i[11]))) + " місць",
                        usrs,
                    ),
                    reply_markup=markup,
                )
        else:
            await bot.edit_message_text(
                chat_id=query.message.chat.id,
                message_id=query.message.message_id,
                text=base.format(
                    i[4],
                    date.day,
                    months[date.month],
                    days[date.weekday()],
                    i[3],
                    i[5],
                    i[8],
                    str(i[9] - len(eval(i[11]))) + " місць",
                    "",
                ),
                reply_markup=markup,
            )

    if callback_data_action == "plus":
        golf_db.plus(callback_data_id)
        i = golf_db.golf_train_id(callback_data_id)
        base = """🏐 {}
🗓 {} {} ({}) {} — збір 
📡 {}
    
💵 Передплата {} грн.
    
📋 {} {}"""
        markup = types.InlineKeyboardMarkup()
        if i[9] - len(eval(i[11])) > 0:
            if str(query.message.chat.id) in eval(i[11]):
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
            if str(query.message.chat.id) in eval(i[11]):
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
            callback_data=posts_cb.new(action="location", id=i[0], sum=i[8], quant=0),
        )

        markup.add(b)
        if int(query.message.chat.id) in admins:
            b = types.InlineKeyboardButton(
                text="Видалити ❌",
                callback_data=posts_cb.new(action="delete", id=i[0], sum=i[8], quant=0),
            )

            c = types.InlineKeyboardButton(
                text="-",
                callback_data=posts_cb.new(action="minus", id=i[0], sum=i[8], quant=0),
            )
            x = types.InlineKeyboardButton(
                text="+",
                callback_data=posts_cb.new(action="plus", id=i[0], sum=i[8], quant=0),
            )

            markup.add(b, c, x)
        date = datetime.datetime.strptime(i[2], "%d.%m.%Y")
        users = eval(i[10])
        usrs = ": "
        if users:
            for z, l in enumerate(users):
                k = eval(l)
                if usrs == ": ":
                    usrs += f'<a href="tg://user?id={k["id"]}">{k["name"]}</a> '
                else:
                    usrs += f', <a href="tg://user?id={k["id"]}">{k["name"]}</a>'
            if i[9] - len(ast.literal_eval(i[11])) == 0:
                await bot.edit_message_text(
                    chat_id=query.message.chat.id,
                    message_id=query.message.message_id,
                    text=base.format(
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
                    reply_markup=markup,
                )

            else:
                await bot.edit_message_text(
                    chat_id=query.message.chat.id,
                    message_id=query.message.message_id,
                    text=base.format(
                        i[4],
                        date.day,
                        months[date.month],
                        days[date.weekday()],
                        i[3],
                        i[5],
                        i[8],
                        str(i[9] - len(eval(i[11]))) + " місць",
                        usrs,
                    ),
                    reply_markup=markup,
                )
        else:
            await bot.edit_message_text(
                chat_id=query.message.chat.id,
                message_id=query.message.message_id,
                text=base.format(
                    i[4],
                    date.day,
                    months[date.month],
                    days[date.weekday()],
                    i[3],
                    i[5],
                    i[8],
                    str(i[9] - len(eval(i[11]))) + " місць",
                    "",
                ),
                reply_markup=markup,
            )

    if callback_data_action == "location":
        res = golf_db.golf_train_id(callback_data_id)
        await bot.send_location(query.message.chat.id, float(res[6]), float(res[7]))
