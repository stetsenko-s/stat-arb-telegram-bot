from os import getenv
from dotenv import load_dotenv
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode



load_dotenv()
TOKEN = getenv('TOKEN')

dp = Dispatcher()

async def main() -> None:
    """
    Создаёт бота и запускает получение обновлений.

    Использует TOKEN, загруженный из переменных окружения, и включает
    HTML-разметку по умолчанию. Передаёт бота диспетчеру dp и ожидает
    завершения polling. Вызывается через asyncio.run при запуске файла.

    Args:
        Отсутствуют.

    Returns:
        None: Не возвращает значение при штатном завершении polling.
    """
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
