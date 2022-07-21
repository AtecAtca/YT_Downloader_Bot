from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import WrongFileIdentifier, InvalidHTTPUrlContent
from tools.bot_tools import bot, db, read_config, is_url
from tools.yt_tools import is_correct_url, get_yid
from userbot.userbot import USERBOT_ID
from keyboards.inline_kb import get_video_audio_kb
from time import sleep

users = db.users
audio_docs = db.audio_docs
video_docs = db.video_docs
messages = read_config()


async def take_from_userbot(message):
    doc_id = message.document.file_id
    type, bot_message, main_message, yid, uid = message.caption.split(' ')
    uid = int(uid)
    language = users.find_one({'_id': uid})['LANGUAGE']
    text = messages['DOWNLOADED'][language]

    await bot.send_document(uid, document=doc_id , caption=text, reply_to_message_id=main_message)
    sleep(0.1)
    await bot.delete_message(chat_id=uid, message_id=bot_message)
    if type ==  '/a':
        audio_docs.insert_one({'_id': yid, 'AUDIO DOC_ID': doc_id})
        db.del_audio_downloading_now(yid, uid)
    elif type == '/v':
        video_docs.insert_one({'_id': yid, 'VIDEO DOC_ID': doc_id})
        db.del_video_downloading_now(yid, uid)



async def link(message: types.Message):
    uid = message.from_user.id
    message_id = message.message_id
    language = users.find_one({'_id': uid})['LANGUAGE']

    if await is_url(message):
        match await is_correct_url(message):
            case 'VideoAvailable':
                yid = await get_yid(message)
                audio_video_kb = get_video_audio_kb(language=language, yid=yid, main_message_id=message_id)
                try:
                    await bot.send_photo(chat_id=uid, reply_markup=audio_video_kb,
                                         reply_to_message_id=message_id,
                                         photo=f'https://i.ytimg.com/vi/{yid}/maxresdefault.jpg')
                except WrongFileIdentifier:
                    await bot.send_photo(chat_id=uid, reply_markup=audio_video_kb,
                                         reply_to_message_id=message_id,
                                         photo=f'https://i.ytimg.com/vi/{yid}/hqdefault.jpg')
                except InvalidHTTPUrlContent:
                    text = messages['CHOOSE'][language]
                    await bot.send_message(chat_id=uid, reply_markup=audio_video_kb, reply_to_message_id=message_id,
                                           text=text)

            case 'VideoUnavailable':
                text = messages['VIDEO UNAVAILABLE'][language]
                text += messages['FORMATS']
                await bot.send_message(uid, text, parse_mode='Markdown')
            case 'RegexMatchError':
                text = messages['WRONG INPUT'][language]
                text += messages['FORMATS']
                await bot.send_message(uid, text, parse_mode='Markdown')
            case 'LiveStreamError':
                text = messages['LIVESTREAM'][language]
                text += messages['FORMATS']
                await bot.send_message(uid, text, parse_mode='Markdown')
    else:
        text = messages['WRONG INPUT'][language]
        text += messages['FORMATS']
        await bot.send_message(uid, text, parse_mode='Markdown')



def message_handlers(dp: Dispatcher):
    dp.register_message_handler(take_from_userbot, content_types=['document'])
    dp.register_message_handler(take_from_userbot, lambda message: message.from_user.id == USERBOT_ID)
    dp.register_message_handler(link, content_types=['text'])


