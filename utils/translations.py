# ======================================
# Translations module for shower-bot
# (taken from fujibot)
# ======================================

import os
import json


class Translations:

    def __init__(self, translations_path):
        self.translations_path = translations_path
        self.default_locale = "en_US"
        self.locales = []
        self.translations = {}  # used to store translations as cache

    def load_translations(self):
        path = self.translations_path
        self.locales = []
        for file in os.listdir(path):
            with open(path + file) as translations:
                self.locales.append(file[:-5])
                self.translations[file[:-5]] = json.load(translations)
                print(f"[Translations] Loaded translation file: {file}")

    def t(self, key, locale=None, **kwargs):
        if not locale:
            locale = self.default_locale
        try:
            return self.translations[locale][key].format(**kwargs)
        except KeyError:
            return self.translations[self.default_locale][key].format(**kwargs)


class Translate:

    def __init__(self, lang, translate_module):
        self.translations = translate_module.translations
        self.language = lang
        self.default_locale = "en_US"

    def t(self, key, locale=None, **kwargs):
        if not locale:
            locale = self.language
        try:
            if self.translations[locale][key]:
                return self.translations[locale][key].format(**kwargs)
            else:
                return key
        except KeyError:
            try:
                if self.translations[self.default_locale][key]:
                    return self.translations[self.default_locale][key].format(**kwargs)
                else:
                    return key
            except KeyError:
                return key