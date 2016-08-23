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

def print_all_chats_from_db(chat_id):
    out_str = ""
    for chat in Chat.select():
        out_str = "CHAT (ID: " + str(chat.chat_id) + " )\n"
        for user in chat.users:
            out_str += "USER (ID: " + str(user.user_id) + " )\n"
        bot.send_message(chat_id=chat_id, text=out_str)
        out_str = ""

def add_user_in_db(user_id, chat_id):
    try:
        # Is current chat in DB?
        chat = Chat.get(Chat.chat_id == chat_id)
    except DoesNotExist as e:
        logger.debug(msg=e.message)
        # Create one
        chat = Chat.insert(chat_id=chat_id, join_date=datetime.datetime.now())
        chat.execute()
        # chat = Chat.create(chat_id=chat_id, join_date=datetime.datetime.now())

    # If joined user is our bot do nothing
    if user_id == bot.get_me().id:
        logger.debug(msg='bot added in new chat group with id: ' + str(chat_id))
    else:
        try:
            # Is user already in db
            user = User.get(User.user_id == user_id)
            logger.debug(msg='user (id: ' + str(user.user_id) + ' ) already exists in bot DB')
            # Is connection already exist
            if(all(chat_user.user_id != user.user_id for chat_user in chat.users)):
                logger.debug(msg='user (id: ' + str(user.user_id) + ' already exist in DB, but connected with chat id: ' + str(chat.chat_id))
                chat.users.add(user)
            # If not, make one
                # chat.users.add(user)
        except DoesNotExist as e:
            # If not, create user
            user = User.create(user_id=user_id, join_date=datetime.datetime.now())
            logger.debug(msg='new user (id: ' + str(user.user_id) + ' ) added in bot DB')
            # And new connection
            chat.users.add(user)

def remove_user_from_chat_db(user_id, chat_id):
    try:
        chat = Chat.get(Chat.chat_id == chat_id)

        if user_id == bot.get_me().id:
            chat.delete_instance()
            logger.debug("Bot removed from chat (id: " + str(chat_id) + ' )')

        try:
            user = User.get(User.user_id == user_id)

            chat.users.remove(user)
            logger.debug("user (id: " + str(user_id) + " ) removed from chat (id: " + str(
                chat_id) + ' )')

        except DoesNotExist as e:
            logger.debug('From group was removed user (id: ' + str(user_id) + " ) that wasnt recorded in bot DB")

    except DoesNotExist as e:
        logger.debug('From group was removed user (id: ' + str(
            user_id) + ' ) that wasnt recorded in bot DB')


