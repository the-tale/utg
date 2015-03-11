# coding: utf-8

from unittest import TestCase

from utg import exceptions
from utg.lexicon import Lexicon



class LexiconTests(TestCase):

    def setUp(self):
        super(LexiconTests, self).setUp()
        self.lexicon = Lexicon()


    def test_init(self):
        self.assertEqual(self.lexicon._data, {})


    def test_add_template(self):
        self.lexicon.add_template(1, 'template_1')
        self.lexicon.add_template(2, 'template_2')
        self.lexicon.add_template(1, 'template_3')

        self.assertEqual(self.lexicon._data, {1: [('template_1', frozenset()), ('template_3', frozenset())],
                                              2: [('template_2', frozenset())]})


    def test_add_template__restrictions(self):
        self.lexicon.add_template(1, 'template_1')
        self.lexicon.add_template(2, 'template_2')
        self.lexicon.add_template(1, 'template_3', restrictions=frozenset([1, 2]))

        self.assertEqual(self.lexicon._data, {1: [('template_1', frozenset()), ('template_3', frozenset([1, 2]))],
                                              2: [('template_2', frozenset())]})


    def test_get_random_template(self):
        self.lexicon.add_template(1, 'template_1')
        self.lexicon.add_template(2, 'template_2')
        self.lexicon.add_template(1, 'template_3')

        templates = set()

        for i in xrange(100):
            templates.add(self.lexicon.get_random_template(1))

        self.assertEqual(templates, set(['template_1', 'template_3']))

        templates = set()

        for i in xrange(100):
            templates.add(self.lexicon.get_random_template(2))

        self.assertEqual(templates, set(['template_2']))

    def check_get_random_template_restrictions(self, key, restrictions, expected):
        templates = set()

        for i in xrange(100):
            templates.add(self.lexicon.get_random_template(key, frozenset(restrictions)))

        self.assertEqual(templates, set(expected))


    def test_get_random_template__restrictions(self):
        self.lexicon.add_template(1, 'template_1')
        self.lexicon.add_template(1, 'template_2', restrictions=frozenset([1, 2]))
        self.lexicon.add_template(1, 'template_3', restrictions=frozenset([1, 3]))

        # key 1 no restrictions
        self.check_get_random_template_restrictions(1, [], ['template_1'])
        self.check_get_random_template_restrictions(1, [1], ['template_1'])
        self.check_get_random_template_restrictions(1, [2], ['template_1'])
        self.check_get_random_template_restrictions(1, [3], ['template_1'])
        self.check_get_random_template_restrictions(1, [1, 2], ['template_1', 'template_2'])
        self.check_get_random_template_restrictions(1, [1, 3], ['template_1', 'template_3'])
        self.check_get_random_template_restrictions(1, [2, 3], ['template_1'])
        self.check_get_random_template_restrictions(1, [1, 2, 3], ['template_1', 'template_2', 'template_3'])


    def test_get_random_template__no_key(self):
        self.lexicon.add_template(1, 'template_1')
        self.lexicon.add_template(2, 'template_2')
        self.lexicon.add_template(1, 'template_3')

        self.assertRaises(exceptions.UnknownLexiconKeyError, self.lexicon.get_random_template, 3)
