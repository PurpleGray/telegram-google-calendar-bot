import cherrypy
import telebot

class WebhookServer(object):

    def __init__(self, bot_instance):
        self.current_bot = bot_instance

    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            self.current_bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)
