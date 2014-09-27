# coding: utf-8

import re

from utg import exceptions
from utg import words
from utg import relations as r
from utg import data

_VARIABLE_REGEX = re.compile(u'\[[^\]]+\]', re.UNICODE)




class Substitution(object):
    __slots__ = ('id', 'dependencies')

    def __init__(self):
        self.id = None
        self.dependencies = []

    def serialize(self):
        return {'id': self.id,
                'dependencies': [dep if isinstance(dep, basestring) else dep.serialize() for dep in self.dependencies]}

    @classmethod
    def deserialize(cls, data):
        obj = cls()
        obj.id = data['id']
        obj.dependencies = [dep if isinstance(dep, basestring) else words.Properties.deserialize(dep) for dep in data['dependencies']]

        return obj

    @classmethod
    def parse(cls, variable, externals):
        slugs = variable[1:-1].lower().split('|')

        if not slugs[0]:
            raise exceptions.WrongDependencyFormatError(dependency=variable)

        s = cls()

        s.id = slugs[0].strip()

        for slug in slugs[1:]:
            slug = slug.strip()
            if slug in externals:
                s.dependencies.append(slug)
            else:
                s.dependencies.append(cls.parse_properties(slug))

        return s


    @classmethod
    def parse_properties(cls, text):
        properties = words.Properties()
        for slug in text.split(','):
            slug.strip()

            if not slug:
                continue

            if slug not in data.VERBOSE_TO_PROPERTIES:
                raise exceptions.UnknownVerboseIdError(verbose_id=slug)

            properties.update(data.VERBOSE_TO_PROPERTIES[slug])

        return properties


    def _merge_properties(self, externals):
        properties = words.Properties()

        for dependency in self.dependencies:
            if isinstance(dependency, words.Properties):
                properties.update(dependency)
                continue

            if dependency not in externals:
                raise exceptions.ExternalDependecyNotFoundError(dependency=dependency)

            properties.update(externals[dependency].properties)

        return properties


    def get_word(self, externals, dictionary):
        properties = self._merge_properties(externals=externals)

        if self.id in externals:
            word = externals[self.id].word
            properties.update(externals[self.id].properties) # TODO: test that line
        else:
            word_form = dictionary.get_word(self.id, type=properties.get(r.WORD_TYPE))
            word_form.properties.update(properties)
            word = word_form.word
            properties = word_form.properties

        form = word.form(properties)

        if properties.get(r.WORD_CASE).is_UPPER:
            form = form[0].upper() + form[1:]

        return words.WordForm(word=word, form=form, properties=properties)

    def __eq__(self, other):
        return (self.id == other.id and
                self.dependencies == other.dependencies)


class Template(object):
    __slots__ = ('_substitutions', 'template')

    def __init__(self):
        self._substitutions = []
        self.template = None

    def serialize(self):
        return {'template': self.template,
                'substitutions': [substitution.serialize() for substitution in self._substitutions]}

    @classmethod
    def deserialize(cls, data):
        obj = cls()
        obj.template = data['template']
        obj._substitutions = [Substitution.deserialize(substitution_data) for substitution_data in data['substitutions']]

        return obj

    def get_undictionaried_words(self, externals, dictionary):
        words = []

        for substitution in self._substitutions:

            if substitution.id in externals:
                continue

            if dictionary.has_words(substitution.id):
                continue

            words.append(substitution.id)

        return words

    def parse(self, text, externals):

        variables = _VARIABLE_REGEX.findall(text)

        for i, variable in enumerate(variables):
            self._substitutions.append(Substitution.parse(variable, externals=externals))
            text = text.replace(variable, '%s', 1)

        self.template = text

    def substitute(self, externals, dictionary):
        substitutions = [substitution.get_word(externals=externals, dictionary=dictionary).form for substitution in self._substitutions]
        return self.template % tuple(substitutions)

    def __eq__(self, other):
        return (self._substitutions == other._substitutions and
                self.template == other.template)
