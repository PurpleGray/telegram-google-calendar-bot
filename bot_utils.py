from peewee import *

from app import bot, config, db, logger

from DB.models import  *

import random

import string


def is_command_for_bot(cmd_str, message_text):
    if message_text == "/" + cmd_str + "@" + bot.get_me().username:
        return True
    else:
        return False

def add_user_in_db(user_id, chat_id):
    try:
        # Is current chat in DB?
        chat = Chat.get(Chat.chat_id == chat_id)
    except DoesNotExist as e:
        logger.debug(msg=e.message)
        # Create one
        chat = Chat.create(chat_id=chat_id, google_calendar_id="".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(5)), join_date=datetime.datetime.now())

    # If joined user is our bot do nothing
    if user_id == bot.get_me().id:
        logger.debug(msg='bot added in new chat group with id: ' + str(chat_id))
    else:
        try:
            # Is user already in db
            user = User.get(User.user_id == user_id)
            logger.debug(msg='user (id: ' + str(user.user_id) + ' ) already exists in bot DB')
            # Is connection already exist
            try:
                userchat = UserChat.get(UserChat.chat.chat_id == chat_id & UserChat.user.user_id == user_id)
            except DoesNotExist as e:
                # If not, make one
                UserChat.create(chat=chat, user=user)
        except DoesNotExist as e:
            # If not, create user
            user = User.create(user_id=user_id, join_date=datetime.datetime.now())
            logger.debug(msg='new user (id: ' + str(user.user_id) + ' ) added in bot DB')
            # And new connection
            UserChat.create(user=user, chat=chat)


def remove_user_from_db(user_id, chat_id):
    if user_id== bot.get_me().id:
        try:
            chat = Chat.get(Chat.chat_id == chat_id)
            chat.delete_instance()
            logger.debug("Bot removed from chat (id: " + str(chat_id) + ' )')
        except DoesNotExist as e:
            logger.debug('Bot was removed from group (id: ' + str(chat_id) + ' ) that wasnt recorded in DB')
    else:
        try:
            user = User.get(User.user_id == user_id)
            user.delete_instance()
            logger.debug("user (id: " + str(user_id) + " ) removed from chat (id: " + str(
                chat_id) + ' )')
        except DoesNotExist as e:
            logger.debug('From group was removed user (id: ' + str(
                user_id) + ' ) that wasnt recorded in bot DB')

