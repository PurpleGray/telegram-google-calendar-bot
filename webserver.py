from app import app, config, db, bot

from flask import request, abort, g, url_for, redirect, session

from oauth2client import client

import apiclient

import httplib2

import telebot

__secret_file = 'google_calendar_secret.json'

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
    if 'credentials' not in session:
        return redirect(url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect(url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        calendar_service = apiclient.discovery.build("calendar", "v3", http_auth)
        events_list = calendar_service.calendarList().list(pageToken=None).execute(http=http_auth)
        print events_list
        return "XYU"

# Process bot requests
@app.route(config.WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if (request.headers.get('content-type') == 'application/json'):
        json_string = request.get_data().encode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)

@app.route('/oauth2callback')
def oauth2callback():

    flow = client.flow_from_clientsecrets(__secret_file,
                                          scope='https://www.googleapis.com/auth/calendar',
                                          redirect_uri=config.WEBHOOK_URL_BASE + '/oauth2callback')
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session['credentials'] = credentials.to_json()
        return redirect(url_for('index'))
