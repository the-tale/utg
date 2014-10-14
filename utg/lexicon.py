# coding: utf-8

import random

from utg import exceptions


class Lexicon(object):
    __slots__ = ('_data',)

    def __init__(self):
        self._data = {}


    def add_template(self, key, template):
        if key not in self._data:
            self._data[key] = []

        self._data[key].append(template)

    def has_key(self, key):
        return key in self._data

    def get_random_template(self, key):
        if key not in self._data:
            raise exceptions.UnknownLexiconKeyError(key=key)

        return random.choice(self._data[key])
