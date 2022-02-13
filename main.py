from aiogram.utils import executor

from golfbot.golf_bot import dp

executor.start_polling(dp, skip_updates=True)
