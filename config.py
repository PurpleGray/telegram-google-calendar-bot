import json

config_name = "config.json"

class Config(object):

    __instance = None

    @staticmethod
    def instance():
        if(Config.__instance == None):
            Config.__instance = Config()
        return Config.__instance

    def __init__(self):
        with open(config_name) as file:
            self.__dict__ = json.load(file)
            self.WEBHOOK_URL_BASE = "https://{0}:{1}".format(self.__dict__["WEBHOOK_HOST"], self.__dict__["WEBHOOK_PORT"])
            self.WEBHOOK_URL_PATH =  "/{0}/".format(self.__dict__["telegram_api_token"])
            file.close()
