# -*- coding: utf-8 -*-
import logging

import telebot
import telebot.types as types
from flask import Flask
from flask import abort
from flask import g
from flask import request
from peewee import *

from DB import botdatabase
from DB import models
from config import Config

# Create Flask microserver
app = Flask(__name__)

# Configure bot logger
logger = telebot.logger

telebot.logger.setLevel(logging.DEBUG)

# Instantiate bot
bot = telebot.TeleBot(Config.instance().telegram_api_token)

# Connect to bot DB
db = botdatabase.DataBase.instance().db

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
    try:
        help_message = Config.instance().help_command_message
        bot.send_message(message.chat.id, help_message)
    except Exception as e:
        logger.log(e)

@bot.message_handler(func=lambda message: True, commands=['start'])
def start_command_handler(message):
    # TODO: implement start logic
    pass

@bot.message_handler(func=lambda message: True, commands=['test_db'])
def db_test_handler(message):
    try:
        with db.transaction():
            chat = models.Chat(chat_id = "test_id",
                                  google_calendar_id = "g_test_id")

        bot.send_message(message.chat.id, chat.chat_id)
    except IntegrityError:
        print("Such chat id already exists in db")
        bot.send_message(message.chat.id, "This chat already exists in my DB")

@bot.message_handler(func=lambda message: True, content_types=["text"])
def message_income_handler(message):
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
    for index, hint in enumerate(Config.instance().message_examples_hint):
        hint_articles.append(types.InlineQueryResultArticle(id=str(index + 2), title="Событие " + str(index + 1),
                                                            description=hint.encode('utf-8'),
                                                            input_message_content=types.InputTextMessageContent(
                                                                hint.encode('utf-8'))))

    try:
        bot.answer_inline_query(inline_query.id, hint_articles)
    except Exception as e:
        logger.log(e)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


@app.route(Config.instance().WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if (request.headers.get('content-type') == 'application/json'):
        json_string = request.get_data().encode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)

@app.before_request
def before_request():
    g.db = db
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

if __name__ == '__main__':
    # Removing webhook just for sure
    bot.remove_webhook()
    bot.set_webhook(url=Config.instance().WEBHOOK_URL_BASE + Config.instance().WEBHOOK_URL_PATH,
                    certificate=open(Config.instance().WEBHOOK_SSL_CERT, 'r'))

    # Configuring and start our microserver
    app.run(host=Config.instance().WEBHOOK_LISTEN,
            port=Config.instance().WEBHOOK_PORT,
            ssl_context=(Config.instance().WEBHOOK_SSL_CERT, Config.instance().WEBHOOK_SSL_PRIV),
            debug=False)
