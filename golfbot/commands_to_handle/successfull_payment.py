import datetime
import string

from aiogram import types

from commands_to_handle import payment_for_trainings
from golfbot import golf_db
from golfbot.golf_bot import posts_cb


async def handle_successful_payment(message, bot, data: dict, months: dict, days: dict):
    if (
            message.successful_payment.invoice_payload
            == data[str(f"{message.chat.id}")]["payload"]
    ):
        first = ""
        username = ""
        if message.chat.first_name:
            first = message.chat.first_name

        if message.chat.username:
            username = message.chat.username

        printable = set(
            string.printable
            + "АаБбВвГгДдЕеЁёЖжЗзІіЇїИиЙйКкЛлМмНнОоПпСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"
        )
        name = "".join(filter(lambda x: x in printable, first))
        golf_db.golf_sign(
            data[str(f"{message.chat.id}")]["id"], message.chat.id, name, username
        )
        await bot.send_message(
            message.chat.id, f"""ви успішно записані на тренування""", parse_mode="HTML"
        )
        await bot.send_message(
            -1001126968735,
            f"""<a href="tg://user?id={message.chat.id}">{message.chat.first_name + ' ' + message.chat.last_name}</a> успішно записався на тренування""",
            parse_mode="HTML",
        )
        await payment_for_trainings.training_id(message, data[str(f"{message.chat.id}")]["id"], bot)
        base = """🏐 {}
🗓 {} {} ({}) {} — збір 
📡 {}
💵 Передплата {} грн.
📋 {} {}"""
        i = golf_db.golf_train_id(data[str(f"{message.chat.id}")]["id"])
        markup = types.InlineKeyboardMarkup()
        if i[9] - len(eval(i[11])) > 0:
            b = types.InlineKeyboardButton(
                text="Зареєструватися", url="https://t.me/Sportgolf_bot?start=golf"
            )
            markup.add(b)

        b = types.InlineKeyboardButton(
            text="Показати розташування",
            callback_data=posts_cb.new(action="location", id=i[0], sum=i[8], quant=0),
        )

        markup.add(b)
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
                await bot.send_message(
                    -1001126968735,
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
                    -1001126968735,
                    base.format(
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
                    parse_mode="HTML",
                    reply_markup=markup,
                    disable_web_page_preview=True,
                )
        else:
            await bot.send_message(
                -1001126968735,
                base.format(
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
                parse_mode="HTML",
                reply_markup=markup,
                disable_web_page_preview=True,
            )
