from peewee import *


class BaseModel(Model):
    class Meta:
        from DB import botdatabase
        database = botdatabase.DataBase.instance().db


class Event(BaseModel):

    event_date = DateTimeField()
    event_message = CharField()


class Chat(BaseModel):

    chat_id = CharField(unique=True)
    google_calendar_id = CharField(unique=True)


class Person(BaseModel):

    chat_membership = ForeignKeyField(Chat, related_name='persons')



