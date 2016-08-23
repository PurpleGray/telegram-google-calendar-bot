import datetime

from peewee import *

from app import db


class Chat(db.Model):

    chat_id = BigIntegerField(unique=True)
    google_calendar_id = CharField(unique=True)
    join_date = DateTimeField(default=datetime.datetime.now)


class CalendarEvent(db.Model):

    event_date = DateTimeField()
    event_message = CharField()
    from_chat = ForeignKeyField(Chat, related_name='events', unique=True)


class User(db.Model):

    user_id = BigIntegerField(unique=True)
    join_date = DateTimeField(default=datetime.datetime.now)

# Many-to-Many table for User & Chat
class UserChat(db.Model):

    chat = ForeignKeyField(Chat)
    user = ForeignKeyField(User)





