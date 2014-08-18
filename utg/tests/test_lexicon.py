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

        self.assertEqual(self.lexicon._data, {1: ['template_1', 'template_3'],
                                              2: ['template_2']})


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


    def test_get_random_template__no_key(self):
        self.lexicon.add_template(1, 'template_1')
        self.lexicon.add_template(2, 'template_2')
        self.lexicon.add_template(1, 'template_3')

        self.assertRaises(exceptions.UnknownLexiconKeyError, self.lexicon.get_random_template, 3)
