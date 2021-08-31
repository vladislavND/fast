from aiogram import types
from aiogram.dispatcher import FSMContext

from front_bot.loader import dp, bot, executor
from front_bot.keyboards.inline import start_keyboard, start_spiders
from front_bot.state.user import UserState
from front_bot.request import Request


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    msg = "Привет я Парсер БОТ вот что я могу"
    await bot.send_message(
        chat_id=message.from_user.id,
        text=msg,
        reply_markup=start_keyboard()
    )
    await state.finish()


@dp.callback_query_handler(text='search')
async def get_by_url(message: types.CallbackQuery):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Отправьте ссылку на товар',
    )
    await UserState.url.set()


@dp.message_handler(state=UserState.url)
async def send_by_url(message: types.Message):
    url = message.text
    request = Request()
    msg = request.get_price(url)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=msg
    )


@dp.callback_query_handler(text='start_spider')
async def start_spider(message: types.CallbackQuery):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Выберите Магазин для запуска парсинга',
        reply_markup=start_spiders()
    )
    await UserState.spider.set()


@dp.callback_query_handler(state=UserState.spider)
async def spider_run(message: types.CallbackQuery, state: FSMContext):
    spider = message.data
    request = Request()
    request.start_spider(spider)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f'Парсинг, {spider} запущен'
    )
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)















