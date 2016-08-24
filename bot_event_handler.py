from config import Config
from yandex_speechkit import YandexSpeechKit


def parse_event(raw_string):
    out_str = ""
    speechkit = YandexSpeechKit(api_token=Config.instance().yandex_api_token, request_str=Config.instance().yandex_speech_request)
    speechkit.parse(raw_string)
    out_str = "Event: " + speechkit.get_string_without_date(raw_string) + " " + " ".join(speechkit.recognize_dates())
    return out_str