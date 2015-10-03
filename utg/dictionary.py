# coding: utf-8

from utg import exceptions


class Dictionary(object):
    __slots__ = ('_data',)

    def __init__(self, words=[]):
        self._data = {}

        for word in words:
            self.add_word(word)


    def add_word(self, word):
        for i, word_form in enumerate(word.all_forms()):

            if word_form.form not in self._data:
                self._data[word_form.form] = word_form
                continue

            registered_form = self._data[word_form.form]

            if word_form.word.type.value < registered_form.word.type.value:
                self._data[word_form.form] = word_form
                continue

            if word_form.word.type.value > registered_form.word.type.value:
                continue

            if word_form.word.forms < registered_form.word.forms:
                self._data[word_form.form] = word_form
                continue

            if word_form.word.forms > registered_form.word.forms:
                continue

            if word_form.properties.manhattan_distance() < registered_form.properties.manhattan_distance():
                self._data[word_form.form] = word_form
                continue

            if word_form.properties.manhattan_distance() > registered_form.properties.manhattan_distance():
                continue

            if word_form is registered_form:
                continue

            continue


    def has_word(self, text):
        return text in self._data

    def get_word(self, text):

        word = self._data.get(text)

        if word is None:
            raise exceptions.NoWordsFoundError(text=text)

        return word

    def get_words(self):
        return set(word_form.word for word_form in self._data.itervalues())
