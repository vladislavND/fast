import os

from aiogram.types import BotCommand

# from dotenv import load_dotenv
# load_dotenv()

BOT_TOKEN = '1956949762:AAGG7SOeIPPqJc22OEX-uP3bbKALrCBfqMA'

commands = [
        BotCommand(command="/send", description="Подать объявление"),
        BotCommand(command='/filter', description="Добавить или удалить фильтр"),
        BotCommand(command="/search", description="Найти авто по вашему фильтру"),
        BotCommand(command="/settings", description="Перейти в настройки вашего профиля"),
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/help", description="Получить справку о методах")
    ]