from pyrogram import Client, filters
from os import getenv, remove, listdir




PATH = listdir('E:\\Programming\\Python\\PyCharmProjects\\Downloader_BOT\\userbot')
BOT_ID = getenv('BOT_ID')
USERBOT_ID = getenv('USERBOT_ID')
API_ID = getenv('API_ID')
API_HASH = getenv('API_HASH')
SESSION = 'session'
PHONE = '+380934693192'
PASSWORD = 'Zipopo123'
app = Client(SESSION, api_id=API_ID, api_hash=API_HASH)

def check_session():
    if f'{SESSION}.session' and f'{SESSION}.session-journal' in PATH:
        return True
    else:
        return False



@app.on_message(filters.private | filters.regex('/v'))
def check(app, message):
    v, bot_message, main_message, yid, uid, path = message.text.split(' ')
    for i in message.text.split(' '):
        print(i)
    try:
        app.send_document(BOT_ID, path, caption=f'{v} {bot_message} {main_message} {yid} {uid}')
    except ValueError:
        pass
    else:
        remove(path)


@app.on_message(filters.private | filters.regex('/a'))
def check(app, message):
    a, bot_message, main_message, yid, uid, path = message.text.split(' ')
    for i in message.text.split(' '):
        print(i)
    try:
        app.send_document(BOT_ID, path, caption=f'{a} {bot_message} {main_message} {yid} {uid}')
    except ValueError:
        pass
    else:
        remove(path)

if __name__ == '__main__':
    app.run()