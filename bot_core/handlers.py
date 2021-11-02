from aiogram import Dispatcher, types


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_cmd_handler, commands=["start"])


async def start_cmd_handler(message: types.Message):
    await message.answer(
        "Select cryptocurrency. Make sure you type it as short version in brackets as it appears on the list.")
    # TODO кнопочный выбор самых популярных? Или вывод списка всех возможных монет, чтобы пользователь ввел в ответ ETH?
    await message.answer("Bitcoin (BTC) Ethereum (ETH) Shiba Inu (SHIB) Dogecoin (DOGE)")
