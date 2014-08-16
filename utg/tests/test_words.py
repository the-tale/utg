# coding: utf-8
import copy

from unittest import TestCase

from utg import relations as r
from utg import logic
from utg import words


class PropertiesTests(TestCase):

    def setUp(self):
        super(PropertiesTests, self).setUp()


    def test_construct__empty(self):
        properties = words.Properties()
        self.assertEqual(properties._data, words.Properties.DEFAULT_PROPERTIES)

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

    def test_get_key(self):
        properties = words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL, r.PERSON.SECOND)
        self.assertEqual(properties.get_key(), ())
        self.assertEqual(properties.get_key(r.TIME, r.CASE, r.PERSON), (r.TIME.PAST, r.CASE.DATIVE, r.PERSON.SECOND))
