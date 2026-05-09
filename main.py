from aiogram import Bot, Dispatcher
from asyncio import run
from configs.config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.menu import router as menu_router
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
async def main():
    """Главная функция запуска бота"""
    bot = Bot(token = BOT_TOKEN)
    print(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(menu_router)

    print("[LOG] Бот запущен")

    await dp.start_polling(bot)

run(main())



# старт - выводит кнопки и приветствие
# кнопки:
#
# {
#     "17-1":"условие задачи",
#     "17-2":"условие задачи"
# }
# from random import randint
# k = f"17-{str(randint(1,10))}"
# text = s[k]
# with open(k) as f:
#     pass