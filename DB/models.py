import datetime

from peewee import *

from playhouse.fields import ManyToManyField

from app import db


class Calendar(db.Model):
    calendar_id = CharField(unique=True, null=True)


class CalendarEvent(db.Model):
    event_date = DateTimeField(default=datetime.datetime.now)
    event_message = CharField(null=True)
    belongs_to = ForeignKeyField(Calendar, related_name='events')


class User(db.Model):
    user_id = BigIntegerField(unique=True)
    join_date = DateTimeField(default=datetime.datetime.now)


class Chat(db.Model):
    chat_id = BigIntegerField(unique=True)
    join_date = DateTimeField(default=datetime.datetime.now)
    calendar = ForeignKeyField(Calendar, null=True)
    users = ManyToManyField(User, related_name='in_chats')



# # Many-to-Many table for User & Chat
# class UserChat(db.Model):
#     chat = ForeignKeyField(Chat)
#     user = ForeignKeyField(User)


