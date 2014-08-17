# coding: utf-8
import copy

from unittest import TestCase

from utg import words
from utg import logic
from utg import relations as r
from utg.tests import helpers


class PropertiesTests(TestCase):

    def setUp(self):
        super(PropertiesTests, self).setUp()

    def test_construct__empty(self):
        properties = words.Properties()
        self.assertEqual(properties._data, {})

    def test_construct(self):
        properties = words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL, r.PERSON.SECOND)

        self.assertTrue(properties._data[r.CASE].is_DATIVE)
        self.assertTrue(properties._data[r.NUMBER].is_PLURAL)
        self.assertTrue(properties._data[r.PERSON].is_SECOND)

    def test_update__empty(self):
        properties = words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL, r.PERSON.SECOND)

        old_data = copy.copy(properties._data)

        properties.update()

        self.assertEqual(old_data, properties._data)

    def test_update(self):
        properties = words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL, r.PERSON.SECOND)
        properties.update(r.NUMBER.SINGULAR, r.TIME.FUTURE)

        self.assertTrue(properties._data[r.CASE].is_DATIVE)
        self.assertTrue(properties._data[r.NUMBER].is_SINGULAR)
        self.assertTrue(properties._data[r.PERSON].is_SECOND)
        self.assertTrue(properties._data[r.TIME].is_FUTURE)

    def test_get(self):
        properties = words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL, r.PERSON.SECOND)

        for relation in logic.get_property_relations():
            if relation == r.WORD_TYPE:
                self.assertEqual(properties.get(relation), None)
            elif relation in properties._data:
                self.assertEqual(properties.get(relation), properties._data[relation])
            else:
                self.assertEqual(properties.get(relation), relation.records[0])

    def test_get_key(self):
        properties = words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL, r.PERSON.SECOND)
        self.assertEqual(properties.get_key(), ())
        self.assertEqual(properties.get_key(r.TIME, r.CASE, r.PERSON), (r.TIME.PAST, r.CASE.DATIVE, r.PERSON.SECOND))

    def test_eq(self):
        properties_1 = words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL, r.PERSON.SECOND)

        properties_2 = words.Properties()
        properties_2.update(r.CASE.DATIVE, r.NUMBER.PLURAL, r.PERSON.SECOND)

        self.assertEqual(properties_1, properties_2)

        properties_2.update(r.NUMBER.SINGULAR)

        self.assertNotEqual(properties_1, properties_2)



class WordTests(TestCase):

    def setUp(self):
        super(WordTests, self).setUp()

    def test_init(self):
        word = words.Word(type=r.WORD_TYPE.VERB, forms=['x1', 'x2', 'x3'], properties=words.Properties(r.CASE.DATIVE, r.TIME.FUTURE))
        self.assertTrue(word.type.is_VERB)
        self.assertEqual(word.forms, ['x1', 'x2', 'x3'])
        self.assertEqual(word.properties, words.Properties(r.CASE.DATIVE, r.TIME.FUTURE))

    def test_form(self):
        word = helpers.create_noun(properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE))

        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE)), u'ед3')
        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL)), u'мн3')
        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE, r.TIME.FUTURE)), u'ед3')


    def test_form__optional_property(self):
        word = helpers.create_noun(properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE, r.NUMBER.PLURAL))

        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE)), u'мн3')
        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL)), u'мн3')
        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE, r.TIME.FUTURE)), u'мн3')

        word = helpers.create_noun(properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE, r.NUMBER.SINGULAR))

        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE)), u'ед3')
        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL)), u'ед3')
        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE, r.TIME.FUTURE)), u'ед3')
