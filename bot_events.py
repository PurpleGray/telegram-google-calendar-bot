# -*- coding: utf-8 -*-

from app import bot, config, db, logger

from DB.models import  *

from telebot import *


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
            chat, created = Chat.get_or_create(chat_id=message.chat.id, google_calendar_id="test_g_id")
            if message.new_chat_member.id == bot.get_me().id:
                if chat != None and created == False:
                    # probably should delete old record about this chat and create new
                    raise (Exception('Not possible thing happened: bot added in new group which already exsists in bot DB :O'))
                elif chat != None and created == True:
                    logger.debug(msg='bot added in new chat group with id: ' + str(message.chat.id))
            else:
                user, created = User.get_or_create(user_id=message.new_chat_member.id, chat_membership=chat)
                if user != None and created == False:
                    logger.debug(msg='user (id: ' + str(user.user_id) + ' ) already exists in bot DB')
                elif user != None and created == True:
                    logger.debug(msg='new user (id: ' + str(user.user_id) + ' ) added in bot DB')
        else:
            pass
    except Exception as e:
        logger.debug(msg=e)


@bot.message_handler(func=lambda message: True, content_types=['left_chat_member'])
def user_removed(message):
    try:
        if message.chat.type == 'group':
            if message.left_chat_member.id == bot.get_me().id:
                try:
                    chat = Chat.get(Chat.chat_id == message.chat.id)
                    chat.delete_instance()
                    logger.debug("Bot removed from chat (id: " + str(message.chat.id) + ' )')
                except DoesNotExist as e:
                    logger.debug('Bot was removed from group (id: ' + str(message.chat.id) + ' ) that wasnt recorded in DB')
            else:
                try:
                    user = User.get(User.user_id == message.left_chat_member.id)
                    user.delete_instance()
                    logger.debug("user (id: " + str(message.left_chat_member.id) + " ) removed from chat (id: " + str(message.chat.id) + ' )')
                except DoesNotExist as e:
                    logger.debug('From group was removed user (id: ' + str(message.left_chat_member.id) + ' ) that wasnt recorded in bot DB')
        else:
            pass
    except Exception as e:
        logger.debug(e)


@bot.message_handler(func=lambda message: True, commands=['help'])
def help_command_handler(message):
    try:
        if message.chat.type == 'group':
            if message.text == "/help@" + bot.get_me().username:
                bot.send_message(message.chat.id, config.help_command_message)
            else:
                return
        elif message.chat.type == 'private':
            bot.send_message(message.chat.id, config.help_command_message)

    except Exception as e:
        logger.debug(e)

@bot.message_handler(func=lambda message: True, commands=['start'])
def start_command_handler(message):
    # TODO: implement start logic
    if message.chat.type == 'group' and message.text == "/start@" + bot.get_me().username:
        admins = bot.get_chat_administrators(message.chat.id)
        if any(chat_member.user.id == message.from_user.id for chat_member in admins):
            bot.send_message(message.chat.id, config.group_start_command_message)
        else:
            bot.send_message(message.chat.id, config.user_is_not_admin)

@bot.message_handler(func=lambda message: True, content_types=["text"])
def message_income_handler(message):
    if message.chat.type == 'group':
        print "kek"
    '''event_string = bot_event_handler.parse_event(message.text.encode('utf-8'))
    bot_msg = current_bot.reply_to(message, "Recognized event:\n" + event_string)'''
    pass

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
        logger.debug(e)
