from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from os import getenv
from json import load
from tools.mongodb_tools import DataBase
from userbot.userbot import check_session

BOT_ID = getenv('BOT_ID')
bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot)
db = DataBase()

async def on_startup(_):
    general_check()
    print('[BOT] Bot has been started.')

def general_check():
    if db.check_connections():
        print('[DATABASE] Connected successfully.')
    else:
        print('[DATABASE] Connection is failed.')
    if check_session():
        print('[USERBOT] Userbot is working')
    else:
        print('[USERBOT] Userbot is not working')

def read_config():
    with open('E:\\Programming\\Python\\PyCharmProjects\\Downloader_BOT\\config.json', 'r', encoding='utf-8') as f:
        return load(f)

async def is_url(message: types.Message):
    try:
        message['entities'][0]['type']
    except IndexError:
        return False
    else:
        return True