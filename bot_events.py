# -*- coding: utf-8 -*-

from app import bot, config, db, logger

from DB.models import  *

from telebot import *

import bot_utils

import random

import string

'''replied_messages = {}

@bot.edited_message_handler(func=lambda message: True, content_types=["text"])
def message_edited_handler(message):
    msgs = yandex_speechkit.recognize_date(message.text)
    if(message.message_id in replied_messages):
        bot.edit_message_text(chat_id=message.chat.id, text=u'Recognized dates:\n' + msgs,
                              message_id=replied_messages[message.message_id])
'''

@bot.message_handler(func=lambda message: True, content_types=["new_chat_member"])
def new_user_added(message):
    try:
        if message.chat.type == 'group':
            bot_utils.add_user_in_db(user_id=message.new_chat_member.id, chat_id=message.chat.id)
            if message.new_chat_member.id == bot.get_me().id:
                bot.send_message(message.chat.id, config.bot_added_to_group_message)
        else:
            pass
    except Exception as e:
        logger.debug(msg=e.message)


@bot.message_handler(func=lambda message: True, content_types=['left_chat_member'])
def user_removed(message):
    try:
        if message.chat.type == 'group':
            bot_utils.remove_user_from_chat_db(message.left_chat_member.id, message.chat.id)
        else:
            pass
    except Exception as e:
        logger.debug(e.message)


# @bot.message_handler(func=lambda message: True, commands=['show_users'])
# def show_users(message):
#     try:
#         for user in User.select():
#            bot.send_message(message.chat.id, "USER: (id: " + str(user.user_id) + " , join_date: " + str(user.join_date))
#     except Exception as e:
#         logger.debug(e.message)
#
# @bot.message_handler(func=lambda message: True, commands=['show_chats'])
# def show_users(message):
#     try:
#         for chat in Chat.select():
#            bot.send_message(message.chat.id, "CHAT: (id: " + str(chat.chat_id) + " , join_date: " + str(chat.join_date) + " , G Calendar id: x" + str(chat.google_calendar_id))
#     except Exception as e:
#         logger.debug(e.message)
#
# @bot.message_handler(func=lambda message: True, commands=['in_chat'])
# def show_in_chat(message):
#     try:
#         users = (User.select().join(UserChat).join(Chat).where(Chat.chat_id == message.chat.id))
#         for user in users:
#             bot.send_message(message.chat.id, 'USER ID:' + str(user.user_id))
#
#     except Exception as e:
#         logger.debug(e.message)

@bot.message_handler(func=lambda message: True, commands=['show_all'])
def print_all_command_handler(message):
    try:
        bot_utils.print_all_chats_from_db(message.chat.id)
    except Exception as e:
        logger.debug(e.message)

@bot.message_handler(func=lambda message: True, commands=['help'])
def help_command_handler(message):
    try:
        if message.chat.type == 'group':
            if bot_utils.is_command_for_bot(cmd_str='help', message_text=message.text):
                bot.send_message(message.chat.id, config.help_command_message)
            else:
                return
        elif message.chat.type == 'private':
            bot.send_message(message.chat.id, config.help_command_message)

    except Exception as e:
        logger.debug(e.message)

@bot.message_handler(func=lambda message: True, commands=['start'])
def start_command_handler(message):
    # TODO: implement start logic
    if message.chat.type == 'group' and bot_utils.is_command_for_bot(cmd_str='start', message_text=message.text):
        admins = bot.get_chat_administrators(message.chat.id)
        if any(chat_member.user.id == message.from_user.id for chat_member in admins):
            bot.send_message(message.chat.id, config.group_start_command_message)
        else:
            bot.send_message(message.chat.id, config.user_is_not_admin)

@bot.message_handler(func=lambda message: True, content_types=["text"])
def message_income_handler(message):
    try:
        if message.chat.type == 'group':
            pass
        else:
            # Смотрим, есть ли юзер в одном из чатов, добавленных в БД
            user_in_chats = []
            for chat in Chat.select():
                user_status = bot.get_chat_member(chat_id=chat.chat_id, user_id=message.from_user.id).status
                if user_status != 'left' and user_status != 'kicked':
                    user_in_chats.append(chat)
            if len(user_in_chats) != 0:
                bot.send_message(message.chat.id, 'Youre in one of the chats!')
            else:
                bot.send_message(message.chat.id, 'Youre not in chats')
            # Если есть, то пытаемся распознать событие
                # Если удалось распознать эвент
                    # То отправляем распознанное событие и спрашиваем, все ли так
                        # Если все ок, то добавляем эвент в календарь и завершаем разговор
                        # Если не ок, то просим ввести заново
                # Если не удалось, то пишем, что не удалось и говорим если что обратиться к /help
                # Если все так, то добавляем эвент
            # Если нет, то отвечаем, что не удалось его найти ни в одной из групп, где есть бот
            pass
        '''event_string = bot_event_handler.parse_event(message.text.encode('utf-8'))
        bot_msg = current_bot.reply_to(message, "Recognized event:\n" + event_string)'''
        pass
    except Exception as e:
        logger.debug(e.message)
    # replied_messages[message.message_id] = bot_msg.message_id


@bot.inline_handler(lambda query: len(query.query) is 0)
def default_query(inline_query):
    hint_msg = "Введите событие, которое хотите добавить в календарь.\n*Примеры событий*:\n"
    hint_articles = [types.InlineQueryResultArticle(id='1', title='Ввод события', description=hint_msg,
                                                    input_message_content=types.InputTextMessageContent(
                                                        'Пример: Праздничный обед в 12:00'))]
    for index, hint in enumerate(config.message_examples_hint):
        hint_articles.append(types.InlineQueryResultArticle(id=str(index + 2), title="Событие " + str(index + 1),
                                                            description=hint.encode('utf-8'),
                                                            input_message_content=types.InputTextMessageContent(
                                                                hint.encode('utf-8'))))

    try:
        bot.answer_inline_query(inline_query.id, hint_articles)
    except Exception as e:
        logger.debug(e.message)
