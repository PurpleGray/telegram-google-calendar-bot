import requests
import config
import datetime
from config import Config
import json
import yandex_response

class YandexSpeechKit(object):

    def __init__(self, api_token, request_str):
        self.speech_api_token = api_token
        self.speech_request_str = request_str

    recognized_date = ""

    def parse(self, raw_string):
        request = "https://vins-markup.voicetech.yandex.net/markup/0.x/?text={0}&key={1}".format(raw_string, self.speech_api_token)
        response = requests.get(request).text
        self.__dict__ = json.loads(response)

    def get_string_without_date(self, raw_string):
        out_str = ""
        tokens = list()
        i = 0
        for token in self.Tokens:
            tokens.insert(i, token['Text'])
            i += 1
        for date_item in self.Date:
            begin = date_item['Tokens']['Begin']
            end = date_item['Tokens']['End']
            r = range(begin, end)
            for i in r:
                tokens[i] = ""
            print(unicode(u" ".join(tokens)).encode('utf-8'))
        return unicode(u" ".join(tokens)).encode('utf-8')

    def recognize_dates(self):
        recognized_dates = []

        for date_item in self.Date:
            format = ""
            date = ""
            current_date = datetime.datetime.now()

            # If month recognized add it to final format and date
            if ('Month' in date_item):
                format += "%m "
                date += str(date_item['Month']) + " "
            # If not - use current month
            else:
                format += "%m "
                date += str(current_date.month) + " "
            # Same for Day/Year/Hour/Min
            if ('Day' in date_item):
                format += "%d "
                # If RelativeDay = True count from current day
                if ('RelativeDay' in date_item):
                    if (date_item['RelativeDay'] is True):
                        date += str(datetime.datetime.now().day + date_item['Day']) + " "
                    else:
                        date += str(date_item['Day']) + " "
                else:
                    date += str(date_item['Day']) + " "
            else:
                format += "%d "
                date += str(current_date.day) + " "
            if ('Year' in date_item):
                format += "%Y "
                date += str(date_item['Year']) + " "
            else:
                format += "%Y "
                date += str(current_date.year) + " "
            if (('Hour' in date_item) and ('Min' in date_item)):
                format += "%H:%M "
                date += str(date_item['Hour']) + ":" + str(date_item['Min']) + " "

            formatted_date = datetime.datetime.strptime(date, format)
            recognized_dates.append(str(formatted_date))

        return recognized_dates



