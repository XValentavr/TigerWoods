import logging
from golfbot import days_and_month
import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils.callback_data import CallbackData

API_TOKEN = "5102018651:AAEyc4yu6g8W8GEpPRE9i4BAk7HcXr4un2w"
# Configure logging
logging.basicConfig(filename="sample.log", level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
data = {}
# Administrator's chat ID
admins = [669593692, 469236353]
days = days_and_month.create_days()
months = days_and_month.create_month()
typ = "{} ({}, {})"
typs = {}

posts_cb: CallbackData = CallbackData("search", "action", "id", "sum", "quant")


def set_step(chat_id, step):
    with open("golfbot/steps.json", "r") as outfile:
        data_json = json.load(outfile)

    data_json[str(chat_id)] = {"step": step}
    with open("golfbot/steps.json", "w") as outfile:
        json.dump(data_json, outfile)


def get_step(chat_id):
    with open("golfbot/steps.json", "r") as outfile:
        data_json = json.load(outfile)
    return data_json[str(chat_id)]["step"]


@dp.message_handler(commands=["add"])
async def add_train(message):
    from golfbot.add import add_handle
    await add_handle(message, bot, admins, data)


@dp.message_handler(commands=["trainings"])
async def training(message):
    from golfbot.trainings import trainings_handler
    await trainings_handler(message, bot, admins, months, days)


@dp.message_handler(commands=["start"])
async def start_message(message):
    from golfbot.start import start_handle
    await start_handle(message, bot)


@dp.message_handler(content_types=["text"])
async def mes_text(message):
    from golfbot.add_handler_command import add_training_handler
    await add_training_handler(message, bot, data, typs, typ)


@dp.callback_query_handler(posts_cb.filter())
async def json_box(query: types.CallbackQuery, callback_data: dict):
    from golfbot.PayForTraining import pay_for_training
    await pay_for_training(bot, query, callback_data, data)


@dp.message_handler(content_types=["successful_payment"])
async def success(message):
    from golfbot.successfull_payment import handle_successful_payment
    await handle_successful_payment(message, bot, data, months, days)


@dp.pre_checkout_query_handler(lambda shipping_query: True)
async def some_pre_checkout_query_handler(shipping_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(
        shipping_query.id, ok=True, error_message="Помилка. Спробуйте трохи пізніше"
    )


dp.register_pre_checkout_query_handler(
    some_pre_checkout_query_handler, lambda shipping_query: True
)
