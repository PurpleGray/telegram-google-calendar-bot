import telebot

from telebot import types

from config import Config

import logging

from flask import Flask

from flask_peewee.db import Database

# Create Flask microserver
app = Flask(__name__)
app.config.from_object('config.Configuration')

# Create DB
db = Database(app)

# Instantiate config
config = Config.instance()

# Configure bot logger
logger = telebot.logger

telebot.logger.setLevel(logging.DEBUG)

# Instantiate bot
bot = telebot.TeleBot(Config.instance().telegram_api_token)
