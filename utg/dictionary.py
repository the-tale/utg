# coding: utf-8

from utg import exceptions


class Dictionary(object):
    __slots__ = ('_data', )

    def __init__(self):
        self._data = {}


    def add_word(self, word):
        for form in word.forms:
            if form not in self._data:
                self._data[form] = []

            if word not in self._data[form]:
                self._data[form].append(word)


    def get_words(self, text, type=None):
        if text not in self._data:
            return []

        words = self._data[text]

        if type:
            words = [word for word in words if word.type == type]

        return words


    def has_words(self, text, type=None):
        return bool(self.get_words(text, type=type))


    def get_word(self, text, type=None):

        words = self.get_words(text, type=type)

        if not words:
            raise exceptions.NoWordsFoundError(text=text, type=type)

        if len(words) > 1:
            raise exceptions.MoreThenOneWordFoundError(text=text, type=type)

        return words[0]
