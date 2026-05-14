from aiogram import Bot, Dispatcher
from asyncio import run
from configs.config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.menu import router as menu_router


async def main():
    """Главная функция запуска бота"""
    bot = Bot(token = BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(menu_router)

    print("[LOG] Бот запущен")

    await dp.start_polling(bot)

run(main())
