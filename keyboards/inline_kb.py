from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

key_en = InlineKeyboardButton('English 🇬🇧', callback_data='en')
key_ru = InlineKeyboardButton('Русский 🇷🇺', callback_data='ru')
key_ua = InlineKeyboardButton('Українська 🇺🇦', callback_data='ua')
language_kb = InlineKeyboardMarkup(row_width=1).add(key_en, key_ru, key_ua)

def get_video_audio_kb(language, yid, main_message_id):
    if language == 'EN':
        key_video = InlineKeyboardButton('🔴 Download Video', callback_data=f'video {yid} {main_message_id}')
        key_audio = InlineKeyboardButton('⚪️ Download Audio', callback_data=f'audio {yid} {main_message_id}')
    elif language == 'RU':
        key_video = InlineKeyboardButton('🔴 Скачать Видео', callback_data=f'video {yid} {main_message_id}')
        key_audio = InlineKeyboardButton('⚪️ Скачать Аудио', callback_data=f'audio {yid} {main_message_id}')
    else:
        key_video = InlineKeyboardButton('🔴 Завантажити Відео', callback_data=f'video {yid} {main_message_id}')
        key_audio = InlineKeyboardButton('⚪️ Завантажити Аудіо', callback_data=f'audio {yid} {main_message_id}')
    return InlineKeyboardMarkup(row_width=1).row(key_video, key_audio)
