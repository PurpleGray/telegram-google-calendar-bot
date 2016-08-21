import datetime

from peewee import *

from app import db


class BaseModel(db.Model):
    class Meta:
        database = db


class CalendarEvent(BaseModel):

    event_date = DateTimeField()
    event_message = CharField()


class Chat(BaseModel):

    chat_id = CharField(unique=True)
    google_calendar_id = CharField(unique=True)
    join_date = DateTimeField(default=datetime.datetime.now)


class Person(BaseModel):

    chat_membership = ForeignKeyField(Chat, related_name='persons')



