from app import app, config, db, bot

from flask import request, abort, g

import telebot


# @app.before_request
# def before_request():
#     db.connect()
#
# @app.after_request
# def after_request(response):
#     db.close()
#     return response

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


@app.route(config.WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if (request.headers.get('content-type') == 'application/json'):
        json_string = request.get_data().encode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)

