import io
import typing

from aiogram import types
from aiogram.dispatcher import FSMContext

from front_bot.loader import dp, bot, executor
from front_bot.keyboards.inline import start_keyboard, start_spiders, shops, back, files_folders
from front_bot.state.user import UserState
from front_bot.request import Request, Product
from front_bot.utils import update_inline_keyboard, clear_button


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    msg = "Привет я Парсер БОТ вот что я могу"
    await bot.send_message(
        chat_id=message.from_user.id,
        text=msg,
        reply_markup=start_keyboard()
    )
    await state.finish()


@dp.callback_query_handler(text='back', state='*')
async def refresh_state(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='Выберите что вы хотите сделать',
        reply_markup=start_keyboard()
    )
    await state.finish()


@dp.callback_query_handler(text='all_files')
async def get_all_products(message: types.CallbackQuery):
    file = Product.get_xlsx_products()
    await bot.send_document(
        message.from_user.id,
        ('products.xlsx', file)
    )


@dp.callback_query_handler(text='shop_file')
async def get_products_by_shop(message: types.CallbackQuery):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Выберите магазин',
        reply_markup=shops()
    )
    await UserState.folders.set()


@dp.callback_query_handler(state=UserState.folders)
async def send_file_folders(message: types.CallbackQuery, state: FSMContext):
    shop_name = message.data
    files = Product.get_files_folder(shop_name)
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Выберите файл',
        reply_markup=files_folders(files)
    )
    await UserState.shop.set()


@dp.callback_query_handler(state=UserState.shop)
async def send_file_by_shop_id(message: types.CallbackQuery, state: FSMContext):
    file_name = message.data
    file = Product.get_products_by_shop_id(file_name)
    await bot.send_document(
        message.from_user.id,
        (f'{file_name[:-4]}_products.xlsx', file)
    )
    await state.finish()


@dp.callback_query_handler(text='search')
async def get_by_url(message: types.CallbackQuery):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Отправьте ссылку на товар',
        reply_markup=back()
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
async def send_spiders(message: types.CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Выберите магазины которые хотите запустить',
        reply_markup=start_spiders()
    )
    async with state.proxy() as data:
        data['spiders'] = Request().get_spiders()

    await UserState.spider.set()


@dp.callback_query_handler(state=UserState.spider)
async def select_and_run_spiders(message: types.CallbackQuery, state: FSMContext):
    if message.data == 'scrapy_start':
        buttons = await state.get_data()
        spiders = clear_button(buttons['spiders'])
        Request.start_spider(spiders)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f'Парсинг {", ".join(spiders)}, запущен'
        )
        return await state.finish()

    reply_markup = await update_inline_keyboard(message.data, state)
    await bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message.message.message_id,
        reply_markup=reply_markup
    )


@dp.callback_query_handler(text='send_processed')
async def send_processed(message: types.CallbackQuery):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Выберите магазин с которым делаете стыковку',
        reply_markup=shops()
    )

    await UserState.processed.set()


@dp.callback_query_handler(state=UserState.processed)
async def send_processed_file(message: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['shop_id'] = message.data

    await bot.send_message(
        chat_id=message.from_user.id,
        text='Отправьте файл стыковки'
    )

    await UserState.runs.set()


@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=UserState.runs)
async def run_processed(message: types.Message, state: UserState):
    # file = await bot.get_file(message.document.file_id)
    # file: io.BytesIO = await bot.download_file(file.file_path)
    file = await bot.get_file(message.document.file_id)
    file = await bot.download_file(file.file_path)
    state_data = await state.get_data()
    shop_id = state_data['shop_id']
    file = Product.send_processing_product(file=file, shop_id=shop_id)
    await bot.send_document(
        message.from_user.id,
        (f'analise_products.xlsx', file)
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)















