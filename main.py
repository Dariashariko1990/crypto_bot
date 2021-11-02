import asyncio
import logging
from logging.config import dictConfig

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils import executor
from aiogram_calendar import dialog_cal_callback, DialogCalendar

from bot_core import handlers

from settings import LOGGING, BOT_API_TOKEN, BOT_STORAGE

logger = logging.getLogger("main")


async def main():
    dictConfig(LOGGING)

    if BOT_STORAGE:
        pass
        # TODO: Set connector to db
    else:
        storage = MemoryStorage()
    # инициализируем бота
    bot = Bot(token=BOT_API_TOKEN)
    dp = Dispatcher(bot, storage=storage)

    class SetBacktest(StatesGroup):
        waiting_for_end_date = State()

    # вопрос как лучше реализовывать это/в каком месте регистрировать/добавлять клавиатуру и handlers callback
    # при выносе callback_query_handler в handlers не работает правильно, message_handler работает.

    @dp.message_handler(commands=["backtest"], state="*")
    async def start_backtest_handler(message: Message):
        await message.answer("Select and set date range window to be backtested: ",
                             reply_markup=await DialogCalendar().start_calendar())

    #states не работает в callback query handler/ как вызывать следующую фуннкцию выбора end data?
    @dp.callback_query_handler(dialog_cal_callback.filter())
    async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: dict):
        selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
        if selected:
            start_date = date.strftime("%d/%m/%Y")
            # await SetBacktest.waiting_for_end_date.set() попытка  установить state
            await callback_query.message.answer(
                f'You selected start date: {start_date}.'
            )
            # TODO: save start date in db

    @dp.message_handler(state=SetBacktest.waiting_for_end_date) # и использовать его в качестве фильтра
    async def select_end_date_handler(message: Message, state: FSMContext):
        await message.answer("Set date range window to be backtested. Select end date: ")

    handlers.register_handlers(dp)

    try:
        await executor.start_polling(dp, skip_updates=True)
    finally:
        await dp.storage.close()
        await dp.start_polling()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
