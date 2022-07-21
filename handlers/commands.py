from aiogram import types
from aiogram.dispatcher import Dispatcher
from tools.bot_tools import bot, db, read_config
from keyboards.inline_kb import language_kb

users = db.users
messages = read_config()

async def start(message: types.Message):
    uid = message.from_user.id
    if users.count_documents({'_id': uid}) == 0:
        users.insert_one({'_id': uid,
                          'LANGUAGE': 'EN',
                          'VIDEO DOWNLOADING NOW': [],
                          'VIDEO DOWNLOADS': 0,
                          'VIDEO BYTES DOWNLOADED': 0,
                          'AUDIO DOWNLOADING NOW': [],
                          'AUDIO DOWNLOADS': 0,
                          'AUDIO BYTES DOWNLOADED': 0})

    text = messages['WELCOME'][users.find_one({'_id': uid})['LANGUAGE']]
    text += messages['TO START'][users.find_one({'_id': uid})['LANGUAGE']]
    text += messages['FORMATS']
    await bot.send_message(uid, text, parse_mode='Markdown')

async def language(message: types.Message):
    uid = message.from_user.id
    language = users.find_one({'_id': uid})['LANGUAGE']
    text = messages['LANGUAGE'][language]
    await bot.send_message(uid, text, parse_mode='Markdown', reply_markup=language_kb)


async def stats(message: types.Message):
    uid = message.from_user.id
    video_amount = users.find_one({'_id': uid})['VIDEO DOWNLOADS']
    audio_amount = users.find_one({'_id': uid})['AUDIO DOWNLOADS']
    text = messages['STATS'][users.find_one({'_id': uid})['LANGUAGE']].format(video_amount, audio_amount)
    await bot.send_message(uid, text, parse_mode='Markdown')




def command_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(language, commands='language')
    dp.register_message_handler(stats,  commands='stats')