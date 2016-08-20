from peewee import *
import DB


class BaseModel(Model):
    class Meta:
        database = DB.botdatabase.DataBase.instance()


class Event(BaseModel):

    event_date = DateTimeField()
    event_message = CharField()


class Chat(BaseModel):

    chat_id = CharField(unique=True)
    google_calendar_id = CharField(unique=True)



class Person(BaseModel):

    chat_membership = ForeignKeyField(Chat, related_name='persons')



