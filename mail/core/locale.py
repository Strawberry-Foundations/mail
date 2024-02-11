from flask import request
from enum import Enum
from mail import server_dir
import yaml


class Languages(Enum):
    GERMAN = "de-de"
    ENGLISH = "en-de"


class Locale:
    def __init__(self):
        self.locale_de_DE = None
        self.locale_en_US = None

    def load_strings(self):
        with open(server_dir + "/locale/de_DE.yml", "r", encoding="utf-8") as _locales:
            self.locale_de_DE = yaml.load(_locales, Loader=yaml.SafeLoader)

        with open(server_dir + "/locale/en_US.yml", "r", encoding="utf-8") as _locales:
            self.locale_en_US = yaml.load(_locales, Loader=yaml.SafeLoader)


locales = Locale()
locales.load_strings()


class Strings:
    def __init__(self, lang: Languages):
        self.language = lang

    def load(self, string: str):
        lo_string = None

        match self.language:
            case "de-de": lo_string = locales.locale_de_DE
            case "en-us": lo_string = locales.locale_de_DE
            case _: lo_string = locales.locale_en_US

        string = lo_string[string]

        return string


def get_preferred_language():
    accept_language = request.headers.get('Accept-Language')

    if accept_language:
        languages = accept_language.replace(' ', '').split(',')

        preferred_language = languages[0].split(';')[0].lower()

        match preferred_language:
            case "de-de": return Languages.GERMAN.value
            case "en-us": return Languages.ENGLISH.value

    return None
