'''
import json

class YandexSpeechResponse(object):

    def __init__(self, json_string):
        self.__dict__ = json.loads(json_string)
'''