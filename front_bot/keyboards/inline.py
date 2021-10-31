from aiogram import types

from front_bot.request import BotRequest

fetcher = BotRequest()


def start_keyboard():
    btn_text = (
        ('🚀 Запустить парсинг', 'start_spider'),
        ('🔎 Поиск по ссылке', 'search'),
        ('🛍 Получить товары магазина', 'shop_file'),
        ('⤒ Загрузить стыковку', 'send_processed'),
    )
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    return keyboard_markup.add(*btn)


def start_spiders():
    spiders = fetcher.get(endpoint="/api/scrapyd/parsing").json()
    btn_text = ((spider, spider) for spider in ['□ ' + spider for spider in spiders])
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    keyboard_markup.add(*btn)
    back_button = types.InlineKeyboardButton('Назад', callback_data='back')
    return keyboard_markup.add(back_button)


def shops():
    shops = fetcher.get(endpoint='/api/shops').json()
    btn_text = ((shop['name'], shop['id']) for shop in shops)
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    keyboard_markup.add(*btn)
    back_button = types.InlineKeyboardButton('Назад', callback_data='back')
    return keyboard_markup.add(back_button)


def files_folders(files: dict):
    btn_text = ((key, value) for key, value in files.items())
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    keyboard_markup.add(*btn)
    back_button = types.InlineKeyboardButton('Назад', callback_data='back')
    return keyboard_markup.add(back_button)


def back():
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    back_button = types.InlineKeyboardButton('Назад', callback_data='back')
    return keyboard_markup.add(back_button)
