import os
import DB
from peewee import *
from config import Config

class DataBase(object):
    __instance = None

    @staticmethod
    def instance():
        if (DataBase.__instance == None):
            DataBase.__instance = DataBase()
            DataBase.__instance.db = SqliteDatabase(Config.instance().db_path)
            if(not os.path.isfile(Config.instance().db_path)):
                DataBase.__instance.init_db()

        return DataBase.__instance

    def init_db(self):
        self.db.connect()
        self.db.create_tables([DB.models.Chat, DB.models.Person, DB.models.Event])