from aiogram import types
from aiogram.dispatcher import FSMContext

from front_bot.loader import dp, bot, executor
from front_bot.keyboards.inline import start_keyboard, start_spiders, shops, back, files_folders
from front_bot.state.user import UserState
from front_bot.request import BotRequest
from front_bot.utils import update_inline_keyboard, clear_button, to_string

fetcher = BotRequest()


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
    shop_id = message.data
    files = fetcher.post(endpoint=f'/api/get_files_by_shop_id?shop_id={shop_id}').json()
    directory_files = {}
    [directory_files.update({folder['file_name']: folder['file_name']}) for folder in files]
    async with state.proxy() as data:
        data['shop_id'] = shop_id
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Выберите файл',
        reply_markup=files_folders(directory_files)
    )
    await UserState.shop.set()


@dp.callback_query_handler(state=UserState.shop)
async def send_file_by_shop_id(message: types.CallbackQuery, state: FSMContext):
    file_name = message.data
    data = await state.get_data()
    shop_id = data['shop_id']
    rq_data = {
        'shop_id': shop_id,
        'file_name': file_name
    }
    file = fetcher.post(endpoint='/api/all_xlsx', data=rq_data).content
    await bot.send_document(
        message.from_user.id,
        (f'{file_name[:-4]}_products.xlsx', file)
    )
    await state.finish()


@dp.callback_query_handler(text='search')
async def get_by_url(message: types.CallbackQuery):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Отправьте ссылку на товар\n'
             'Для того чтобы получить сравнение цены,'
             ' после ссылки поставьте символ | и напишите артикул товара в рф.маркет',
        reply_markup=back()
    )
    await UserState.url.set()


@dp.message_handler(state=UserState.url)
async def send_by_url(message: types.Message):
    url = message.text
    data = {'url': url}
    response_data = fetcher.post(endpoint='/api/price', data=data).json()
    await bot.send_message(
        chat_id=message.from_user.id,
        text=to_string(response_data)
    )


@dp.callback_query_handler(text='start_spider')
async def send_spiders(message: types.CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Выберите магазины которые хотите запустить',
        reply_markup=start_spiders()
    )
    spiders = fetcher.get(endpoint='/api/scrapyd/parsing').json()
    async with state.proxy() as data:
        data['spiders'] = ['□ ' + spider for spider in spiders]

    await UserState.spider.set()


@dp.callback_query_handler(state=UserState.spider)
async def select_and_run_spiders(message: types.CallbackQuery, state: FSMContext):
    if message.data == 'scrapy_start':
        buttons = await state.get_data()
        spiders = clear_button(buttons['spiders'])
        for spider in spiders:
            fetcher.post(endpoint='/api/scrapyd/run', data={'spider': spider})
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
    file = fetcher.send_processing_product(file=file, shop_id=shop_id)
    await bot.send_document(
        message.from_user.id,
        (f'analise_products.xlsx', file)
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)















