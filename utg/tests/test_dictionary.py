# coding: utf-8

from unittest import TestCase

from utg import words
from utg import exceptions
from utg import relations as r
from utg.dictionary import Dictionary



class DictionaryTests(TestCase):

    def setUp(self):
        super(DictionaryTests, self).setUp()
        self.dictionary = Dictionary()

    def test_init(self):
        self.assertEqual(self.dictionary._data, {})


    def test_add_word(self):
        word = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())
        self.dictionary.add_word(word)

        self.assertEqual(self.dictionary._data,
                         {'x1': [word],
                          'x2': [word],
                          'x3': [word]})


    def test_add_word__duplicates_in_one_word(self):
        word = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x1'], properties=words.Properties())
        self.dictionary.add_word(word)

        self.assertEqual(self.dictionary._data,
                         {'x1': [word],
                          'x2': [word]})


    def test_add_word__duplicates(self):
        word_1 = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())
        word_2 = words.Word(type=r.WORD_TYPE.VERB, forms=['y1', 'x2', 'y3'], properties=words.Properties())

        self.dictionary.add_word(word_1)
        self.dictionary.add_word(word_2)

        self.assertEqual(self.dictionary._data,
                         {'x1': [word_1],
                          'x2': [word_1, word_2],
                          'x3': [word_1],
                          'y1': [word_2],
                          'y3': [word_2]})


    def test_get_words(self):
        word_1 = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())
        word_2 = words.Word(type=r.WORD_TYPE.VERB, forms=['y1', 'x2', 'y3'], properties=words.Properties())

        self.dictionary.add_word(word_1)
        self.dictionary.add_word(word_2)

        self.assertEqual(self.dictionary.get_words('z'), [])
        self.assertEqual(self.dictionary.get_words('x1'), [word_1])
        self.assertEqual(self.dictionary.get_words('x2'), [word_1, word_2])
        self.assertEqual(self.dictionary.get_words('x3'), [word_1])
        self.assertEqual(self.dictionary.get_words('y1'), [word_2])
        self.assertEqual(self.dictionary.get_words('y3'), [word_2])


    def test_get_words__filter_by_type(self):
        word_1 = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())
        word_2 = words.Word(type=r.WORD_TYPE.VERB, forms=['y1', 'x2', 'y3'], properties=words.Properties())

        self.dictionary.add_word(word_1)
        self.dictionary.add_word(word_2)

        self.assertEqual(self.dictionary.get_words('z', type=r.WORD_TYPE.NOUN), [])
        self.assertEqual(self.dictionary.get_words('x1', type=r.WORD_TYPE.NOUN), [word_1])
        self.assertEqual(self.dictionary.get_words('x2', type=r.WORD_TYPE.NOUN), [word_1])
        self.assertEqual(self.dictionary.get_words('x3', type=r.WORD_TYPE.NOUN), [word_1])
        self.assertEqual(self.dictionary.get_words('y1', type=r.WORD_TYPE.NOUN), [])
        self.assertEqual(self.dictionary.get_words('y3', type=r.WORD_TYPE.NOUN), [])

        self.assertEqual(self.dictionary.get_words('z', type=r.WORD_TYPE.VERB), [])
        self.assertEqual(self.dictionary.get_words('x1', type=r.WORD_TYPE.VERB), [])
        self.assertEqual(self.dictionary.get_words('x2', type=r.WORD_TYPE.VERB), [word_2])
        self.assertEqual(self.dictionary.get_words('x3', type=r.WORD_TYPE.VERB), [])
        self.assertEqual(self.dictionary.get_words('y1', type=r.WORD_TYPE.VERB), [word_2])
        self.assertEqual(self.dictionary.get_words('y3', type=r.WORD_TYPE.VERB), [word_2])


    def test_has_words(self):
        word_1 = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())
        word_2 = words.Word(type=r.WORD_TYPE.VERB, forms=['y1', 'x2', 'y3'], properties=words.Properties())

        self.dictionary.add_word(word_1)
        self.dictionary.add_word(word_2)

        self.assertFalse(self.dictionary.has_words('z'))
        self.assertTrue(self.dictionary.has_words('x1'))
        self.assertTrue(self.dictionary.has_words('x2'))
        self.assertTrue(self.dictionary.has_words('x3'))
        self.assertTrue(self.dictionary.has_words('y1'))
        self.assertTrue(self.dictionary.has_words('y3'))


    def test_has_words__filter_by_type(self):
        word_1 = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())
        word_2 = words.Word(type=r.WORD_TYPE.VERB, forms=['y1', 'x2', 'y3'], properties=words.Properties())

        self.dictionary.add_word(word_1)
        self.dictionary.add_word(word_2)

        self.assertFalse(self.dictionary.has_words('z', type=r.WORD_TYPE.NOUN))
        self.assertTrue(self.dictionary.has_words('x1', type=r.WORD_TYPE.NOUN))
        self.assertTrue(self.dictionary.has_words('x2', type=r.WORD_TYPE.NOUN))
        self.assertTrue(self.dictionary.has_words('x3', type=r.WORD_TYPE.NOUN))
        self.assertFalse(self.dictionary.has_words('y1', type=r.WORD_TYPE.NOUN))
        self.assertFalse(self.dictionary.has_words('y3', type=r.WORD_TYPE.NOUN))

        self.assertFalse(self.dictionary.has_words('z', type=r.WORD_TYPE.VERB))
        self.assertFalse(self.dictionary.has_words('x1', type=r.WORD_TYPE.VERB))
        self.assertTrue(self.dictionary.has_words('x2', type=r.WORD_TYPE.VERB))
        self.assertFalse(self.dictionary.has_words('x3', type=r.WORD_TYPE.VERB))
        self.assertTrue(self.dictionary.has_words('y1', type=r.WORD_TYPE.VERB))
        self.assertTrue(self.dictionary.has_words('y3', type=r.WORD_TYPE.VERB))


    def test_get_word__no_words(self):
        word_1 = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())
        word_2 = words.Word(type=r.WORD_TYPE.VERB, forms=['y1', 'x2', 'y3'], properties=words.Properties())

        self.dictionary.add_word(word_1)
        self.dictionary.add_word(word_2)

        self.assertRaises(exceptions.NoWordsFoundError, self.dictionary.get_word, 'z')
        self.assertRaises(exceptions.NoWordsFoundError, self.dictionary.get_word, 'x1', type=r.WORD_TYPE.VERB)


    def test_get_word__more_then_one_words(self):
        word_1 = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())
        word_2 = words.Word(type=r.WORD_TYPE.NOUN, forms=['y1', 'x2', 'y3'], properties=words.Properties())

        self.dictionary.add_word(word_1)
        self.dictionary.add_word(word_2)

        self.assertRaises(exceptions.MoreThenOneWordFoundError, self.dictionary.get_word, 'x2')
        self.assertRaises(exceptions.MoreThenOneWordFoundError, self.dictionary.get_word, 'x2', type=r.WORD_TYPE.NOUN)


    def test_get_word(self):
        word_1 = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())
        word_2 = words.Word(type=r.WORD_TYPE.NOUN, forms=['y1', 'x2', 'y3'], properties=words.Properties())

        self.dictionary.add_word(word_1)
        self.dictionary.add_word(word_2)

        self.assertEqual(self.dictionary.get_word('x1'), word_1)
        self.assertEqual(self.dictionary.get_word('y1'), word_2)


    def test_get_word__filter_by_type(self):
        word_1 = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())
        word_2 = words.Word(type=r.WORD_TYPE.VERB, forms=['y1', 'x2', 'y3'], properties=words.Properties())

        self.dictionary.add_word(word_1)
        self.dictionary.add_word(word_2)

        self.assertEqual(self.dictionary.get_word('x2', type=r.WORD_TYPE.NOUN), word_1)
        self.assertEqual(self.dictionary.get_word('x2', type=r.WORD_TYPE.VERB), word_2)
