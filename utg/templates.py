# coding: utf-8

import re

from utg import exceptions
from utg import words
from utg import data
from utg import transformators

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
        properties = []
        for slug in text.split(','):
            slug.strip()

            if not slug:
                continue

            if slug not in data.VERBOSE_TO_PROPERTIES:
                raise exceptions.UnknownVerboseIdError(verbose_id=slug)

            properties.append(data.VERBOSE_TO_PROPERTIES[slug])

        return words.Properties(*properties)


    def _list_propeties(self, externals):
        properties = []
        external_words = []

        for dependency in self.dependencies:
            if isinstance(dependency, words.Properties):
                properties.append(dependency)
                continue

            if dependency not in externals:
                raise exceptions.ExternalDependecyNotFoundError(dependency=dependency)

            properties.append(externals[dependency].properties)
            external_words.append(externals[dependency])

        return properties, external_words


    def get_text(self, externals, dictionary):

        if self.id in externals:
            base_word = externals[self.id]
        else:
            # TODO: get_word must use type information if substitution has it
            base_word = dictionary.get_word(self.id)

        properties_list, externals = self._list_propeties(externals=externals)

        properties = base_word.properties.clone(*properties_list)

        form_properties = properties
        for external in externals:
            form_properties = transformators.transform(slave_type=base_word.word.type,
                                                       slave_propeties=form_properties,
                                                       master_type=external.word)

        word_form = words.WordForm(word=base_word.word, properties=properties, form_properties=form_properties)

        return word_form.form

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
        substitutions = [substitution.get_text(externals=externals, dictionary=dictionary) for substitution in self._substitutions]
        return self.template % tuple(substitutions)

    def __eq__(self, other):
        return (self._substitutions == other._substitutions and
                self.template == other.template)
