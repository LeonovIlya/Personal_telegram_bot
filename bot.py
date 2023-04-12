import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
from ai.handler import register_handlers_ai
from auth.handler import register_handlers_auth
from notebook.handler import register_handlers_notebook
from reminder.handler import register_handlers_reminder
from weather.handler import register_handlers_weather

from reminder.handler import check_records


logger = logging.getLogger(__name__)


async def main(loop) -> None:
    logging.basicConfig(filename='bot_log.log',
                        filemode='a',
                        level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(name)s - %("
                               "message)s", )
    logger.info("Starting bot")
    bot = Bot(token=config.BOT_TOKEN)
    try:
        logger.info(await bot.get_me())
    finally:
        await (await bot.get_session()).close()
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_ai(dp)
    register_handlers_auth(dp)
    register_handlers_notebook(dp)
    register_handlers_reminder(dp)
    register_handlers_weather(dp)

    await dp.start_polling()


async def check_reminders() -> None:
    while True:
        await check_records()
        await asyncio.sleep(60)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(check_reminders())
    loop.run_until_complete(main(loop))
    loop.run_forever()
