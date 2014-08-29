# coding: utf-8

from utg import words
from utg import exceptions


class Dictionary(object):
    __slots__ = ('_data', )

    def __init__(self):
        self._data = {}


    def add_word(self, word):
        for i, form in enumerate(word.forms):
            if form not in self._data:
                self._data[form] = []

            if all(word is not test_word for test_word, j in self._data[form]):
                self._data[form].append((word, i))


    def get_words(self, text, type=None):
        if text not in self._data:
            return []

        choices = self._data[text]

        if type:
            choices = [word for word in choices if word[0].type == type]

        return choices


    def has_words(self, text, type=None):
        return bool(self.get_words(text, type=type))


    def get_word(self, text, type=None):

        choices = self.get_words(text, type=type)

        if not choices:
            raise exceptions.NoWordsFoundError(text=text, type=type)

        if len(choices) > 1:
            raise exceptions.MoreThenOneWordFoundError(text=text, type=type)

        word, cache_index = choices[0]

        return word, words.Properties(*words.INVERTED_WORDS_CACHES[word.type][cache_index])
