import datetime

from peewee import *

from app import db


class Calendar(db.Model):

    calendar_id = CharField(unique=True)


class CalendarEvent(db.Model):
    event_date = DateTimeField()
    event_message = CharField()
    belongs_to = ForeignKeyField(Calendar, related_name='events', unique=True)


class Chat(db.Model):
    chat_id = BigIntegerField(unique=True)
    join_date = DateTimeField(default=datetime.datetime.now)
    calendar = ForeignKeyField(Calendar)

class User(db.Model):
    user_id = BigIntegerField(unique=True)
    join_date = DateTimeField(default=datetime.datetime.now)


# Many-to-Many table for User & Chat
class UserChat(db.Model):
    chat = ForeignKeyField(Chat)
    user = ForeignKeyField(User)


