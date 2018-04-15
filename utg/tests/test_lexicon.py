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

        for i in range(100):
            templates.add(self.lexicon.get_random_template(1))

        self.assertEqual(templates, set(['template_1', 'template_3']))

        templates = set()

        for i in range(100):
            templates.add(self.lexicon.get_random_template(2))

        self.assertEqual(templates, set(['template_2']))

    def check_get_random_template_restrictions(self, key, restrictions, expected):
        templates = set()

        for i in range(100):
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

    def test_get_nearest_templates(self):
        self.lexicon.add_template(1, 'template_1', restrictions={1})
        self.lexicon.add_template(2, 'template_2', restrictions={2})
        self.lexicon.add_template(1, 'template_3', restrictions={1, 3})

        self.lexicon.add_template(1, 'template_4', restrictions={1, 4})
        self.lexicon.add_template(1, 'template_5', restrictions={3, 4})
        self.lexicon.add_template(1, 'template_6', restrictions={2, 1, 3, 4})
        self.lexicon.add_template(1, 'template_7', restrictions={2})

        candidates = self.lexicon._get_nearest_templates(1, {5})
        self.assertEqual(len(candidates), 0)

        candidates = self.lexicon._get_nearest_templates(1, {1, 2, 3, 4, 5, 6})
        self.assertEqual(candidates, ['template_6'])

        candidates = self.lexicon._get_nearest_templates(1, {1, 3})
        self.assertEqual(candidates, ['template_3'])

        candidates = self.lexicon._get_nearest_templates(1, {1, 3, 4})
        self.assertEqual(candidates, ['template_3', 'template_4', 'template_5'])

        candidates = self.lexicon._get_nearest_templates(1, {1, 2})
        self.assertEqual(candidates, ['template_1', 'template_7'])

    def test_get_nearest_random_templates(self):
        self.lexicon.add_template(1, 'template_1', restrictions={1})
        self.lexicon.add_template(2, 'template_2', restrictions={2})
        self.lexicon.add_template(1, 'template_3', restrictions={1, 3})

        self.lexicon.add_template(1, 'template_4', restrictions={1, 4})
        self.lexicon.add_template(1, 'template_5', restrictions={3, 4})
        self.lexicon.add_template(1, 'template_6', restrictions={2, 1, 3, 4})
        self.lexicon.add_template(1, 'template_7', restrictions={2})

        for i in range(10):
            template = self.lexicon.get_random_nearest_template(1, {1, 2, 3, 4, 5, 6})
            self.assertIn(template, ['template_6'])

            template = self.lexicon.get_random_nearest_template(1, {1, 3})
            self.assertIn(template, ['template_3'])

            template = self.lexicon.get_random_nearest_template(1, {1, 3, 4})
            self.assertIn(template, ['template_3', 'template_4', 'template_5'])

            template = self.lexicon.get_random_nearest_template(1, {1, 2})
            self.assertIn(template, ['template_1', 'template_7'])

    def test_get_random_nearest_template__no_key(self):
        self.lexicon.add_template(1, 'template_1')
        self.lexicon.add_template(2, 'template_2')
        self.lexicon.add_template(1, 'template_3')

        self.assertRaises(exceptions.UnknownLexiconKeyError, self.lexicon.get_random_nearest_template, 3)


    def test_get_random_nearest_template__no_templates(self):
        self.lexicon.add_template(1, 'template_1', {1})
        self.lexicon.add_template(2, 'template_2', {2})
        self.lexicon.add_template(1, 'template_3', {3})

        self.assertRaises(exceptions.NoTemplatesWithSpecifiedRestrictions, self.lexicon.get_random_nearest_template, 2, {4})
