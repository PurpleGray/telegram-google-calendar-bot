# -*- coding: utf-8 -*-
import telebot
import telebot.types as types
import cherrypy
import bot_event_handler
from config import Config
from webhook_server import WebhookServer
import yandex_speechkit
import DB.botdatabase
import logging

from peewee import *

# Instantiate our bot
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(Config.instance().telegram_api_token)
db = DB.botdatabase.DataBase.instance()
'''replied_messages = {}

@bot.edited_message_handler(func=lambda message: True, content_types=["text"])
def message_edited_handler(message):
    msgs = yandex_speechkit.recognize_date(message.text)
    if(message.message_id in replied_messages):
        bot.edit_message_text(chat_id=message.chat.id, text=u'Recognized dates:\n' + msgs,
                              message_id=replied_messages[message.message_id])
'''



@bot.message_handler(func=lambda message: True, commands=['help'])
def help_command_handler(message):
    help_message = Config.instance().help_command_message
    bot.send_message(message.chat.id, help_message)


@bot.message_handler(func=lambda message: True, content_types=["text"])
def message_income_handler(message):
     event_string = bot_event_handler.parse_event(message.text.encode('utf-8'))
     bot_msg = bot.reply_to(message, "Recognized event:\n" + event_string)

    # replied_messages[message.message_id] = bot_msg.message_id

@bot.inline_handler(lambda query: len(query.query) is 0)
def default_query(inline_query):
    hint_msg = "Введите событие, которое хотите добавить в календарь.\n*Примеры событий*:\n"
    hint_articles = [types.InlineQueryResultArticle(id='1', title='Ввод события', description=hint_msg, input_message_content=types.InputTextMessageContent('Пример: Праздничный обед в 12:00'))]
    for index, hint in enumerate(Config.instance().message_examples_hint):
        hint_articles.append(types.InlineQueryResultArticle(id=str(index), title="Событие " + str(index - 1), description=hint.encode('utf-8'),
                                                            input_message_content=types.InputTextMessageContent(hint.encode('utf-8'))))

    try:
        bot.answer_inline_query(inline_query.id, hint_articles)
    except Exception as e:
        print(e)



if __name__ == '__main__':
    # Removing webhook just for sure
    bot.remove_webhook()
    bot.set_webhook(url=Config.instance().WEBHOOK_URL_BASE + Config.instance().WEBHOOK_URL_PATH, certificate=open(Config.instance().WEBHOOK_SSL_CERT, 'r'))

    # Configuring our microserver
    cherrypy.config.update({
        'server.socket_host': str(Config.instance().WEBHOOK_LISTEN),
        'server.socket_port': int(Config.instance().WEBHOOK_PORT),
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': str(Config.instance().WEBHOOK_SSL_CERT),
        'server.ssl_private_key': str(Config.instance().WEBHOOK_SSL_PRIV)
    })

    # Server start
    cherrypy.quickstart(WebhookServer(bot_instance=bot), Config.instance().WEBHOOK_URL_PATH, {'/': {}})
