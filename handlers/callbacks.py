from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import NetworkError, InvalidQueryID, MessageToDeleteNotFound
from tools.bot_tools import bot, db, read_config
from userbot.userbot import USERBOT_ID
from tools.yt_tools import download_audio, download_video, get_audio_path, get_video_path
from os import remove
from time import sleep
from http.client import IncompleteRead

users = db.users
audio_docs = db.audio_docs
video_docs = db.video_docs
messages = read_config()

async def language(callback: types.CallbackQuery):
    uid = callback.from_user.id
    message_id = callback.message.message_id
    if callback.data == 'en':
        users.update_one({'_id': uid}, {'$set': {'LANGUAGE': 'EN'}})
    elif callback.data == 'ru':
        users.update_one({'_id': uid}, {'$set': {'LANGUAGE': 'RU'}})
    else:
        users.update_one({'_id': uid}, {'$set': {'LANGUAGE': 'UA'}})
    await bot.delete_message(chat_id=uid, message_id=message_id)

    text = messages['WELCOME'][users.find_one({'_id': uid})['LANGUAGE']]
    text += messages['TO START'][users.find_one({'_id': uid})['LANGUAGE']]
    text += messages['FORMATS']
    await bot.send_message(uid, text, parse_mode="Markdown")


async def video(callback: types.CallbackQuery):
    yid = callback.data.split(' ')[1]
    uid = callback.from_user.id
    message_id = callback.data.split(' ')[2]
    language = users.find_one({'_id': uid})['LANGUAGE']

    # if doc id of youtube link is in database
    if video_docs.count_documents({'_id': yid}) == 1:
        video_doc_id = video_docs.find_one({'_id': yid})['VIDEO DOC_ID']
        if video_doc_id is not None:
            text = messages['DOWNLOADED'][language]
            await bot.send_document(uid, document=video_doc_id, caption=text, reply_to_message_id=message_id)
            sleep(0.1)
            try:
                await callback.answer()
            except InvalidQueryID:
                pass
            await bot.delete_message(chat_id=uid, message_id=callback.message.message_id)

    else:
        # if document loading now, user cant download it repeatedly
        if db.is_video_downloading_now(yid, uid):
            try:
                await callback.answer()
            except InvalidQueryID:
                pass

            await bot.delete_message(chat_id=uid, message_id=callback.message.message_id)
            text = messages['VIDEO DOWNLOADING NOW'][language]
            await bot.send_message(uid, text=text, reply_to_message_id=message_id)


        else:
            try:
                await callback.answer()
            except InvalidQueryID:
                pass
            try:
                await bot.delete_message(chat_id=uid, message_id=callback.message.message_id)
            except MessageToDeleteNotFound:
                pass
            text = messages['PLEASE WAIT VIDEO'][language]
            bot_message = await bot.send_message(uid, text=text, reply_to_message_id=message_id)

            db.add_video_downloading_now(yid, uid)
            path = await get_video_path(uid, yid)
            # download starts here
            try:
                await download_video(uid, yid)
            except IncompleteRead:
                text = messages['VIDEO INCOMPLETE READ'][language]
                await bot.delete_message(chat_id=uid, message_id=bot_message.message_id)
                await bot.send_message(uid, text=text, reply_to_message_id=message_id, parse_mode="Markdown")
                db.del_video_downloading_now(yid, uid)
                remove(path)

            else:
                text = messages['DOWNLOADED'][language]
                try:
                    # bot try to send document
                    bot_document = await bot.send_document(uid, open(path, 'rb'), caption=text,
                                                           reply_to_message_id=message_id)
                    # some documents telegram send like document, or audio
                    try:
                        video_docs.insert_one({'_id': yid, 'VIDEO DOC_ID': bot_document.document.file_id})
                    except AttributeError:
                        video_docs.insert_one({'_id': yid, 'VIDEO DOC_ID': bot_document.video.file_id})

                # when documents >50mb -> send command to userbot
                except NetworkError:
                    await bot.send_message(chat_id=USERBOT_ID,
                                           text=f'/v {bot_message.message_id} {message_id} {yid} {uid} {path}')

                else:
                    # when document was sent
                    sleep(0.1)
                    await bot.delete_message(chat_id=uid, message_id=bot_message.message_id)
                    db.del_video_downloading_now(yid, uid)
                    remove(path)
















async def audio(callback: types.CallbackQuery):
    yid = callback.data.split(' ')[1]
    uid = callback.from_user.id
    message_id = callback.data.split(' ')[2]
    language = users.find_one({'_id': uid})['LANGUAGE']

    #if doc id of youtube link is in database
    if audio_docs.count_documents({'_id': yid}) == 1:
        audio_doc_id = audio_docs.find_one({'_id': yid})['AUDIO DOC_ID']
        if audio_doc_id is not None:
            text = messages['DOWNLOADED'][language]
            await bot.send_document(uid, document=audio_doc_id, caption=text, reply_to_message_id=message_id)
            sleep(0.1)
            try:
                await callback.answer()
            except InvalidQueryID:
                pass
            await bot.delete_message(chat_id=uid, message_id=callback.message.message_id)
    else:
        # if document loading now, user cant download it repeatedly
        if db.is_audio_downloading_now(yid, uid):
            try:
                await callback.answer()
            except InvalidQueryID:
                pass
            await bot.delete_message(chat_id=uid, message_id=callback.message.message_id)
            text = messages['AUDIO DOWNLOADING NOW'][language]
            await bot.send_message(uid, text=text, reply_to_message_id=message_id)

        else:
            try:
                await callback.answer()
            except InvalidQueryID:
                pass
            try:
                await bot.delete_message(chat_id=uid, message_id=callback.message.message_id)
            except MessageToDeleteNotFound:
                pass
            text = messages['PLEASE WAIT AUDIO'][language]
            bot_message = await bot.send_message(uid, text=text, reply_to_message_id=message_id)

            db.add_audio_downloading_now(yid, uid)

            # download starts here
            path = await get_audio_path(uid, yid)
            try:
                await download_audio(uid, yid)
            except IncompleteRead:
                text = messages['VIDEO INCOMPLETE READ'][language]
                await bot.delete_message(chat_id=uid, message_id=bot_message.message_id)
                await bot.send_message(uid, text=text, reply_to_message_id=message_id, parse_mode="Markdown")
                db.del_audio_downloading_now(yid, uid)
                remove(path)

            else:
                text = messages['DOWNLOADED'][language]
                try:
                    # bot try to send document
                    bot_document = await bot.send_document(uid, open(path, 'rb'), caption=text,
                                                           reply_to_message_id=message_id)
                    # some documents telegram send like document, or audio
                    try:
                        audio_docs.insert_one({'_id': yid, 'AUDIO DOC_ID': bot_document.document.file_id})
                    except AttributeError:
                        audio_docs.insert_one({'_id': yid, 'AUDIO DOC_ID':  bot_document.audio.file_id})

                # when documents >50mb -> send command to userbot
                except NetworkError:
                    await bot.send_message(chat_id=USERBOT_ID,
                                           text=f'/a {bot_message.message_id} {message_id} {yid} {uid} {path}')

                else:
                    # when document was sent
                    sleep(0.1)
                    await bot.delete_message(chat_id=uid, message_id=bot_message.message_id)
                    db.del_audio_downloading_now(yid, uid)
                    remove(path)





def callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(language, text=['en', 'ru', 'ua'])
    dp.register_callback_query_handler(video, lambda callback: callback.data.startswith('video'))
    dp.register_callback_query_handler(audio, lambda callback: callback.data.startswith('audio'))
