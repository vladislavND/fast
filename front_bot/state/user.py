from aiogram.dispatcher.filters.state import State, StatesGroup
from scrapy.utils import spider


class UserState(StatesGroup):

    url = State()
    spider = State()
    shop = State()
    runs = State()
    processed = State()