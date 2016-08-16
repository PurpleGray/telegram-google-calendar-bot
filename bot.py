# -*- coding: utf-8 -*-
import telebot
import cherrypy
from config import Config
from webhook_server import WebhookServer
import yandex_speechkit

# Instantiate our bot
bot = telebot.AsyncTeleBot(Config.instance().telegram_api_token)

# Message handler
@bot.message_handler(func=lambda message: True, content_types=["text"])
def repeat_all_messages(message):
    msgs = yandex_speechkit.recognize_date(message.text)
    bot.reply_to(message, u'Recognized dates:\n' + msgs)


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
