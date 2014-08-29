# coding: utf-8
import copy
import random

from utg import relations as r
from utg import logic


RESTRICTIONS = { r.FORM.INFINITIVE: (r.TIME, r.PERSON, r.NUMBER, r.MOOD, r.GENDER),
                 r.NUMBER.PLURAL: (r.GENDER,),
                 r.TIME.PRESENT: (r.GENDER, r.MOOD),
                 r.TIME.FUTURE: (r.GENDER,),
                 r.ADJECTIVE_CATEGORY.RELATIVE: (r.GRADE,),
                 r.ADJECTIVE_CATEGORY.POSSESSIVE: (r.GRADE,),
                 r.PERSON.FIRST: (r.GENDER,),
                 r.PERSON.SECOND: (r.GENDER,),
                 r.PRONOUN_CATEGORY.REFLEXIVE: (r.NUMBER, r.GENDER, r.PERSON),
                 r.PRONOUN_CATEGORY.INTERROGATIVE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.RELATIVE: (r.NUMBER, r.GENDER, r.PERSON),
                 r.PRONOUN_CATEGORY.DEMONSTRATIVE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.ATTRIBUTIVE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.NEGATIVE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.VAGUE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.MUTUAL: (r.PERSON,) }

INVERTED_RESTRICTIONS = {}
for property, property_groups in RESTRICTIONS.iteritems():
    for property_group in property_groups:
        if property_group not in INVERTED_RESTRICTIONS:
            INVERTED_RESTRICTIONS[property_group] = set()
        INVERTED_RESTRICTIONS[property_group].add(property)

_DEFAULT_PROPERTIES = logic.get_default_properties()

WORDS_CACHES, INVERTED_WORDS_CACHES = logic.get_caches(restrictions=RESTRICTIONS)


class Properties(object):


    def __init__(self, *argv):
        self._data = {}
        self.update(*argv)

    def serialize(self):
        return {r.PROPERTY_TYPE.index_relation[property_type].value: property.value
                for property_type, property in self._data.iteritems()}

    @classmethod
    def deserialize(cls, data):
        return cls(*[r.PROPERTY_TYPE(int(property_type)).relation(property_value)
                     for property_type, property_value in data.iteritems()])

    def update(self, *argv):
        for property in argv:
            if property is None:
                continue

            if isinstance(property, self.__class__):
                self._data.update(property._data)
            else:
                self._data[property._relation] = property

    def get_key(self, key, schema=None):
        if schema is None:
            schema = key

        value = []
        for property_group in key:
            property = self.get(property_group)
            if property_group in INVERTED_RESTRICTIONS and any(self.get(p._relation) == p for p in INVERTED_RESTRICTIONS[property_group] if p._relation in schema):
                property = None
            value.append(property)

        return tuple(value)

    def get(self, property_group):
        if property_group in self._data:
            return self._data[property_group]
        return _DEFAULT_PROPERTIES[property_group]

    def is_specified(self, property_group):
        return property_group in self._data

    def clone(self):
        obj = self.__class__()
        obj._data = copy.copy(self._data)
        return obj

    def __unicode__(self):
        return u'(%s)' % (u','.join(property.verbose_id for property in self._data.itervalues()))

    def __eq__(self, other):
        return self._data == other._data


class Word(object):

    def __init__(self, type, forms, properties):
        self.type = type
        self.forms = forms
        self.properties = properties

    def serialize(self):
        return {'type': self.type.value,
                'forms': self.forms,
                'properties': self.properties.serialize()}

    @classmethod
    def deserialize(cls, data):
        return cls(type=r.WORD_TYPE(data['type']),
                   forms=data['forms'],
                   properties=Properties.deserialize(data['properties']))

    def form(self, properties):
        real_properties = properties.clone()
        real_properties.update(self.properties)
        return self.forms[WORDS_CACHES[self.type][real_properties.get_key(key=self.type.schema)]]

    def normal_form(self):
        return self.form(properties=self.properties)

    def __eq__(self, other):
        return (self.type == other.type and
                self.properties == other.properties and
                self.forms == other.forms)

    @classmethod
    def get_forms_number(cls, type):
        return len(WORDS_CACHES[type])

    @classmethod
    def create_test_word(cls, type, prefix=u'', only_required=False):
        cache = WORDS_CACHES[type]
        forms = [None] * len(cache)
        for key, index in cache.iteritems():
            forms[index] = prefix + u','.join(property.verbose_id for property in key if property is not None)

        properties = Properties()

        for relation, required in type.properties.iteritems():
            if not required and (only_required or random.random() > 0.5):
                continue
            properties.update(random.choice(relation.records))

        return cls(type=type, forms=forms, properties=properties)
