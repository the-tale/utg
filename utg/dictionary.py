# coding: utf-8

from utg import words
from utg import exceptions
from utg import relations as r


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

        if isinstance(text, (int, long)):
            word = words.Word(type=r.WORD_TYPE.INTEGER, forms=[u'%s' % text], properties=words.Properties())
            return [words.WordForm(word=word, properties=word.properties, form=word.forms[0])]

        if text not in self._data:
            return []

        choices = [words.WordForm(word=word,
                                  properties=words.Properties(*words.INVERTED_WORDS_CACHES[word.type][index]),
                                  form=text)
                   for word, index in self._data[text]]

        if type:
            choices = [word for word in choices if word.word.type == type]

        return choices


    def has_words(self, text, type=None):
        return bool(self.get_words(text, type=type))


    def get_word(self, text, type=None):

        choices = self.get_words(text, type=type)

        if not choices:
            raise exceptions.NoWordsFoundError(text=text, type=type)

        if len(choices) > 1:
            raise exceptions.MoreThenOneWordFoundError(text=text, type=type)

        return choices[0]
