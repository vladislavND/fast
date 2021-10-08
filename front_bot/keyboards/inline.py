from aiogram import types

from front_bot.request import Request, Product


def start_keyboard():
    btn_text = (
        ('Запустить парсинг', 'start_spider'),
        ('Поиск по ссылке', 'search'),
        ('Получить все товары', 'all_files'),
        ('Получить товары магазина', 'shop_file'),
        ('Загрузить стыковку', 'send_processed'),
        # ('Личный кабинет', 'cabinet')
    )
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    return keyboard_markup.add(*btn)


def start_spiders():
    spiders = Request().get_spiders()
    btn_text = ((spider, spider) for spider in spiders)
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    keyboard_markup.add(*btn)
    back_button = types.InlineKeyboardButton('Назад', callback_data='back')
    return keyboard_markup.add(back_button)


def shops():
    shops = Product.get_shops()
    btn_text = ((shop['name'], shop['name']) for shop in shops)
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    keyboard_markup.add(*btn)
    back_button = types.InlineKeyboardButton('Назад', callback_data='back')
    return keyboard_markup.add(back_button)


def back():
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    back_button = types.InlineKeyboardButton('Назад', callback_data='back')
    return keyboard_markup.add(back_button)
