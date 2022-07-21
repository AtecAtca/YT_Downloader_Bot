from aiogram import types
from pytube import YouTube
from pytube.exceptions import LiveStreamError, RegexMatchError, VideoUnavailable
from string import punctuation



async def is_correct_url(message: types.Message):
    try:
        yt = YouTube(message.text).streams
    except LiveStreamError:
        return 'LiveStreamError'
    except RegexMatchError:
        return 'RegexMatchError'
    except VideoUnavailable:
        return 'VideoUnavailable'
    else:
        return 'VideoAvailable'

async def get_yid(message: types.Message):
    return YouTube(message.text).video_id

async def download_audio(uid, yid):
    path = f'E:\\Programming\\Python\\PyCharmProjects\\Downloader_BOT\\data\\{uid}\\audios'
    yt = YouTube(f'https://youtu.be/{yid}')
    title = yt.title.translate(str.maketrans(' ', '_', punctuation))
    audio = yt.streams.filter(only_audio=True).desc().first()
    audio.download(output_path=path, filename=f'{title}.mp3')

async def get_audio_path(uid, yid):
    path = f'E:\\Programming\\Python\\PyCharmProjects\\Downloader_BOT\\data\\{uid}\\audios'
    yt = YouTube(f'https://youtu.be/{yid}')
    title = yt.title.translate(str.maketrans(' ', '_', punctuation))
    return f'{path}\\{title}.mp3'

async def download_video(uid, yid):
    path = f'E:\\Programming\\Python\\PyCharmProjects\\Downloader_BOT\\data\\{uid}\\videos'
    yt = YouTube(f'https://youtu.be/{yid}')
    title = yt.title.translate(str.maketrans(' ', '_', punctuation))
    video = yt.streams.filter(progressive=True).desc().first()
    video.download(output_path=path, filename=f'{title}.mp4')


async def get_video_path(uid, yid):
    path = f'E:\\Programming\\Python\\PyCharmProjects\\Downloader_BOT\\data\\{uid}\\videos'
    yt = YouTube(f'https://youtu.be/{yid}')
    title = yt.title.translate(str.maketrans(' ', '_', punctuation))
    return f'{path}\\{title}.mp4'