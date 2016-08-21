import os

from peewee import *
from config import Config

class DataBase(object):
    __instance = None

    def __init__(self):
        from DB import models

        self.db = SqliteDatabase(Config.instance().db_path)
        try:
            self.db.connect()
            self.db.create_tables([models.Chat, models.Person, models.Event])
        except Exception as e:
            print(e)
        finally:
            self.db.close()



    @staticmethod
    def instance():
        if (DataBase.__instance == None):
            DataBase.__instance = DataBase()
        return DataBase.__instance