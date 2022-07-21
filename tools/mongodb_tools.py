from pymongo import MongoClient
from pymongo.errors import OperationFailure
from os import getenv

class DataBase():
    def __init__(self):
        self.user = getenv('DB_USER')
        self.password = getenv('DB_PASSWORD')
        self.url = f'mongodb+srv://{self.user}:{self.password}@cluster0.ewr9jm1.mongodb.net/?retryWrites=true&w=majority'
        self.cluster = MongoClient(self.url)
        self.users = self.cluster.database.youdownloader_bot
        self.audio_docs = self.cluster.database.audio_documents
        self.video_docs = self.cluster.database.video_documents

    def check_connections(self):
        try:
            self.users.find_one()
            self.audio_docs.find_one()
            self.video_docs.find_one()
        except OperationFailure:
            return False
        else:
            return True

    def is_audio_downloading_now(self, yid, uid):
        if yid in self.users.find_one({'_id': uid})['AUDIO DOWNLOADING NOW']:
            return True
        else:
            return False

    def is_video_downloading_now(self, yid, uid):
        if yid in self.users.find_one({'_id': uid})['VIDEO DOWNLOADING NOW']:
            return True
        else:
            return False

    def add_audio_downloading_now(self, yid, uid):
        self.users.update_one({'_id': uid}, {'$push': {'AUDIO DOWNLOADING NOW': yid}})

    def del_audio_downloading_now(self, yid, uid):
        self.users.update_one({'_id': uid}, {'$pull': {'AUDIO DOWNLOADING NOW': yid}})

    def add_video_downloading_now(self, yid, uid):
        self.users.update_one({'_id': uid}, {'$push': {'VIDEO DOWNLOADING NOW': yid}})

    def del_video_downloading_now(self, yid, uid):
        self.users.update_one({'_id': uid}, {'$pull': {'VIDEO DOWNLOADING NOW': yid}})

    def inc_audio_downloads(self, uid):
        self.users.update_one({'_id': uid}, {'$inc': {'AUDIO DOWNLOADS': 1}})

    def inc_video_downloads(self, uid):
        self.users.update_one({'_id': uid}, {'$pull': {'VIDEO DOWNLOADS': 1}})