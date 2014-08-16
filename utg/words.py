# coding: utf-8
import copy

from utg import relations as r
from utg import logic


_RESTRICTIONS = {r.FORM.INFINITIVE: (r.TIME, r.PERSON, r.NUMBER, r.MOOD),
                 r.NUMBER.PLURAL: (r.GENDER,),
                 r.TIME.PRESENT: (r.GENDER, r.MOOD),
                 r.TIME.FUTURE: (r.GENDER,),
                 r.ADJECTIVE_CATEGORY.RELATIVE: (r.GRADE,),
                 r.ADJECTIVE_CATEGORY.POSSESSIVE: (r.GRADE,),
                 r.PERSON.FIRSTH: (r.GENDER,),
                 r.PERSON.SECOND: (r.GENDER,),
                 r.PRONOUN_CATEGORY.REFLEXIVE: (r.NUMBER, r.GENDER, r.PERSON),
                 r.PRONOUN_CATEGORY.INTERROGATIVE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.RELATIVE: (r.NUMBER, r.GENDER, r.PERSON),
                 r.PRONOUN_CATEGORY.DEMONSTRATIVE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.ATTRIBUTIVE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.NEGATIVE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.VAGUE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.MUTUAL: (r.PERSON,) }



class Properties(object):
    DEFAULT_PROPERTIES = logic.get_default_properties()

    def __init__(self, *argv):
        self._data = copy.copy(self.DEFAULT_PROPERTIES)
        self.update(*argv)

    def update(self, *argv):
        for property in argv:
            self._data[property._relation] = property

    def get_key(self, *argv):
        return tuple(self._data[property_group] for property_group in argv)


class Word(object):
    CACHES = logic.get_caches(restrictions=_RESTRICTIONS)

    def __init__(self, type, forms, properties):
        self.type = type
        self.forms = forms
        self.properties = properties


    def get_form(self, properties):
        return self.forms[self.CACHES[self.type][properties.get_key(*self.type.schema)]]


class WordForm(object):

    def __init__(self, word, properties):
        self.word = word
        self.properties = properties
